import jetson_inference
import jetson_utils
import cv2
import globalVar
from command import driveMotor

# --- CONFIGURATION CAMERA ---
cam = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

# --- CONFIGURATION GPU ---
# On charge le réseau de neurones sur le GPU (SSD MobileNet V2)
# threshold=0.5 signifie qu'on veut être sûr à 50% que c'est bien une personne
net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# --- CONFIGURATION ROBOT ---
FRAME_WIDTH = 640
CENTER_X = FRAME_WIDTH // 2
DEAD_ZONE_X = 80
TARGET_AREA = 30000
AREA_TOLERANCE = 10000

TRACKING_SPEED = 40
TURN_SPEED = 50

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

    # 3. Recherche de "PERSONNE" (ClassID 1 pour MobileNet)
    target = None
    
    for d in detections:
        # ClassID 1 = Personne (dans le dataset COCO utilisé par mobilenet)
        if d.ClassID == 1:
            target = d
            break # On prend la première personne trouvée

    # Si pas de personne trouvée
    if target is None:
        driveMotor(1, 0)
        driveMotor(2, 0)
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
    command = "STOP"
    left_motor = 0
    right_motor = 0

    # Gestion Direction
    if x < (CENTER_X - DEAD_ZONE_X):
        command = "GAUCHE"
        left_motor = -TURN_SPEED
        right_motor = TURN_SPEED
    elif x > (CENTER_X + DEAD_ZONE_X):
        command = "DROITE"
        left_motor = TURN_SPEED
        right_motor = -TURN_SPEED
    else:
        # Gestion Distance
        if area < (TARGET_AREA - AREA_TOLERANCE):
            command = "AVANCE"
            left_motor = TRACKING_SPEED
            right_motor = TRACKING_SPEED
        elif area > (TARGET_AREA + AREA_TOLERANCE):
            command = "RECULE"
            left_motor = -TRACKING_SPEED
            right_motor = -TRACKING_SPEED
        else:
            command = "STOP (Verrouille)"
            left_motor = 0
            right_motor = 0

    # Affichage Infos
    cv2.putText(frame, f"{command} (Conf: {int(target.Confidence*100)}%)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Envoi Moteurs
    driveMotor(1, left_motor)
    driveMotor(2, right_motor)

    return frame
