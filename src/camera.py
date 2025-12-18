import cv2

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cam.isOpened():
    print("ERREUR: Impossible d'ouvrir la caméra avec GStreamer")
else:
    print("Caméra ouverte avec succès !")

def generateFrames():
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            frame = buffer.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
