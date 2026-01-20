import jetson_inference
import jetson_utils
import cv2
import globalVar
import threading
from command import execCommand

class CameraStream:
    def __init__(self):
        self.stream = cv2.VideoCapture(
            "nvarguscamerasrc sensor-mode=4 ! "
            "nvvidconv ! "
            "video/x-raw, width=1280, height=720, format=BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=BGR ! appsink max-buffers=1 drop=true",
            cv2.CAP_GSTREAMER
        )
        self.grabbed, self.frame = self.stream.read()

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            (grabbed, frame) = self.stream.read()
            if grabbed:
                self.frame = frame

    def read(self):
        return self.frame

cam = CameraStream().start()

# --- CONFIGURATION GPU ---
# On charge le réseau de neurones sur le GPU (SSD MobileNet V2)
# threshold=0.5 signifie qu'on veut être sûr à 50% que c'est bien une personne
net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.60)

# --- CONFIGURATION ROBOT ---
FRAME_WIDTH = 1280
CENTER_X = FRAME_WIDTH // 2
DEAD_ZONE_X = 250
TARGET_AREA = 400000
AREA_TOLERANCE = 40000

def generateFrames():
    while True:
        frame = cam.read()
        if frame is not None:
            if globalVar.automode:
                frame = followTarget(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def followTarget(frame):
    # 1. Conversion OpenCV (Numpy) -> CUDA (GPU)
    # OpenCV utilise BGR, Jetson Inference préfère RGBA
    img_cuda = jetson_utils.cudaFromNumpy(frame)

    # 2. DÉTECTION GPU (C'est ici que la magie opère)
    detections = net.Detect(img_cuda)

    target = None
    obstacle = []

    for d in detections:
        if d.ClassID == globalVar.target_class_id:
            if target is None or d.Area > target.Area:
                target = d
        else:
            obstacle.append(d)
            obs_x = d.Center[0]
            
            # Si l'obstacle est au milieu de l'écran (+/- 300px)
            if (CENTER_X - 300) < obs_x < (CENTER_X + 300):
                # Récupération du nom de l'obstacle pour affichage
                obs_name = net.GetClassDesc(d.ClassID)
                status_text = f"DODGE: {obs_name}"
                
                # Dessin Obstacle (Rouge)
                l, t, r, b = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
                cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 3)
                cv2.putText(frame, f"{obs_name}", (l, t), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
                ## Esquive
                #if obs_x > CENTER_X:
                #    command = "LEFT"
                #else:
                #    command = "RIGHT"
                #    
                #execCommand(command)
                #cv2.putText(frame, f"{status_text} -> {command}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Si pas de personne trouvée
    if target is None:
        cv2.putText(frame, "RECHERCHE CIBLE...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        if globalVar.search:
            execCommand("RIGHT")
        else:
            execCommand("STOP")
        return frame

    # --- SI PERSONNE TROUVÉE ---
    
    # Récupération des coordonnées
    # L'objet 'd' contient directement le Centre et l'Aire !
    x, y = int(target.Center[0]), int(target.Center[1])
    w, h = int(target.Width), int(target.Height)
    area = w * h
    
    # Dessin sur l'image (Retour visuel)
    # On dessine le rectangle autour de la personne
    left, top = int(target.Left), int(target.Top)
    right, bottom = int(target.Right), int(target.Bottom)
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.putText(frame, f"{net.GetClassDesc(target.ClassID)}", (left, top), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    
    # --- LOGIQUE DE PILOTAGE ---
    # Gestion Direction
    command = "STOP"
    if x < (CENTER_X - DEAD_ZONE_X):
        command = "LEFT"
    elif x > (CENTER_X + DEAD_ZONE_X):
        command = "RIGHT"
    else:
        # Gestion Distance
        if area < (TARGET_AREA - AREA_TOLERANCE):
            command = "FORWARD"
        elif area > (TARGET_AREA + AREA_TOLERANCE):
            command = "BACKWARD"
    execCommand(command)

    # Affichage Infos
    cv2.putText(frame, f"{command} (Conf: {int(target.Confidence*100)}%)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame
