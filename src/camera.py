import cv2

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

def generateFrames():
    while True:
        success, frame = cam.read()
        if success:
            frame = frame.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
