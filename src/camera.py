import cv2

cam = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1024, height=576, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

def generateFrames():
    while True:
        success, frame = cam.read()
        if success:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
