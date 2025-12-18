from flask import Flask, request
from command import execCommand
import cv2

app = Flask(__name__)
cam = cv2.VideoCapture(0)

@app.route("/")
def home():
    content = "Page not found"
    with open('./page/home.html') as file:
        content = file.read()
        ret, frame = cam.read()
        cv2.imshow('Camera', frame)
    return content

@app.route("/command", methods=["POST"])
def command():
    action: str = request.get_json()['action']
    print(action)
    execCommand(action)
    return "";

@app.route("/hello")
def hello_world():
    return "<p>Hello World!</p>"

if __name__ == "__main__":
    app.run(host="10.42.0.2",port=3000)
