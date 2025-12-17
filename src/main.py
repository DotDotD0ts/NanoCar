from flask import Flask, request
from command import execCommand
import cv2

app = Flask(__name__)

@app.route("/")
def home():
    content = "Page not found"
    with open('./page/home.html') as file:
        content = file.read()
    return content

@app.route("/command", methods=["POST"])
def command():
    action = request.get_json()['action']
    print(action)
    execCommand(action)
    return "";

@app.route("/hello")
def hello_world():
    return "<p>Hello World!</p>"

if __name__ == "__main__":
    app.run(port=3000)
