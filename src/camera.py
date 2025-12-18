import cv2

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height}, framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
    )

print("Initialisation GStreamer...")
cam = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

if not cam.isOpened():
    print("ERREUR: Impossible d'ouvrir la caméra avec GStreamer")
else:
    print("Caméra ouverte avec succès !")

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def generateFrames():
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            frame = buffer.tobytes()
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
