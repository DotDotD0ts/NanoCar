import jetson_inference
import jetson_utils
import cv2
import globalVar
from command import execCommand

# --- CONFIGURATION CAMERA ---
cam = cv2.VideoCapture(
    "nvarguscamerasrc sensor-mode=4 ! "
    "nvvidconv ! "
    "video/x-raw, width=1280, height=720, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! appsink",
    cv2.CAP_GSTREAMER
)

# --- CONFIGURATION GPU ---
# On charge le réseau de neurones sur le GPU (SSD MobileNet V2)
# threshold=0.5 signifie qu'on veut être sûr à 50% que c'est bien une personne
net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# --- CONFIGURATION ROBOT ---
FRAME_WIDTH = 1280
CENTER_X = FRAME_WIDTH // 2
DEAD_ZONE_X = 250
TARGET_AREA = 400000
AREA_TOLERANCE = 40000
OBSTACLE_MIN_AREA = 80000

def generateFrames():
    while True:
        success, frame = cam.read()
        if success:
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
    obstacle = None

    for d in detections:
        # ClassID 1 = Personne (dans le dataset COCO utilisé par mobilenet)
        if d.ClassID == globalVar.target_class_id:
            if target is None or d.Area > target.Area:
                target = d
        else:
            if d.Area > OBSTACLE_MIN_AREA:
                if obstacle is None or d.Area > obstacle.Area:
                    obstacle = d

    if obstacle is not None:
        obs_x = obstacle.Center[0]
        
        # Si l'obstacle est au milieu de l'écran (+/- 300px)
        if (CENTER_X - 300) < obs_x < (CENTER_X + 300):
            # Récupération du nom de l'obstacle pour affichage
            obs_name = net.GetClassDesc(obstacle.ClassID)
            status_text = f"DODGE: {obs_name}"
            
            # Dessin Obstacle (Rouge)
            l, t, r, b = int(obstacle.Left), int(obstacle.Top), int(obstacle.Right), int(obstacle.Bottom)
            cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 3)
            
            # Esquive
            if obs_x > CENTER_X:
                command = "LEFT"
            else:
                command = "RIGHT"
                
            execCommand(command)
            cv2.putText(frame, f"{status_text} -> {command}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return frame # On quitte ici, sécurité maximale

    # Si pas de personne trouvée
    if target is None:
        cv2.putText(frame, "RECHERCHE CIBLE...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
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
