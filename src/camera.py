import cv2
import main.py
from command import driveMotor

WIDTH = 1280
HEIGHT = 720
CENTER_X = FRAME_WIDTH // 2
DEAD_ZONE = 160
TARGET_AREA = 120000 
AREA_TOLERANCE = 20000
TRACKING_SPEED = 40 
TURN_SPEED = 50

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

def generateFrames():
    while True:
        success, frame = cam.read()
        if success:
            if main.automode:
                frame = followTarget(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def followTarget(frame):
    """
    Détecte un visage et envoie les commandes aux moteurs.
    Retourne l'image avec le rectangle dessiné.
    """
    # 1. Conversion en niveaux de gris (plus rapide pour la détection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Détection des visages
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Si aucun visage n'est détecté -> On s'arrête
    if len(faces) == 0:
        drive_motor(1, 0)
        drive_motor(2, 0)
        return frame

    # On prend le premier visage trouvé (le plus proche généralement)
    (x, y, w, h) = faces[0]
    
    # Calcul du centre du visage
    face_center_x = x + (w // 2)
    face_area = w * h

    # Dessin du rectangle et du centre sur l'image (Retour visuel)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.circle(frame, (face_center_x, y + h//2), 5, (0, 0, 255), -1)

    # --- LOGIQUE D'ASSERVISSEMENT ---
    
    command = "STOP"
    left_motor = 0
    right_motor = 0

    # 3. GESTION DE LA DIRECTION (Gauche / Droite)
    if face_center_x < (CENTER_X - DEAD_ZONE_X):
        # Visage à GAUCHE -> Tourner à GAUCHE
        command = "LEFT"
        left_motor = -TURN_SPEED
        right_motor = TURN_SPEED
        cv2.putText(frame, "Tourne GAUCHE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    elif face_center_x > (CENTER_X + DEAD_ZONE_X):
        # Visage à DROITE -> Tourner à DROITE
        command = "RIGHT"
        left_motor = TURN_SPEED
        right_motor = -TURN_SPEED
        cv2.putText(frame, "Tourne DROITE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    else:
        # Visage au CENTRE -> Gérer l'AVANCE / RECUL
        
        if face_area < (TARGET_AREA - AREA_TOLERANCE):
            # Visage trop petit = Trop loin -> AVANCER
            command = "FORWARD"
            left_motor = TRACKING_SPEED
            right_motor = TRACKING_SPEED
            cv2.putText(frame, "AVANCE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        elif face_area > (TARGET_AREA + AREA_TOLERANCE):
            # Visage trop gros = Trop près -> RECULER (ou STOP)
            command = "BACK"
            left_motor = -TRACKING_SPEED
            right_motor = -TRACKING_SPEED
            cv2.putText(frame, "RECULE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
        else:
            # Visage à la bonne distance -> STOP
            command = "STOP"
            left_motor = 0
            right_motor = 0
            cv2.putText(frame, "CIBLE VERROUILLEE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 4. Envoi aux moteurs
    drive_motor(1, left_motor)
    drive_motor(2, right_motor)

    return frame
