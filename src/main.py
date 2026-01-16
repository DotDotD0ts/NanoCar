from flask import Flask, request, Response
from command import execCommand
from camera import generateFrames

app = Flask(__name__)

automode = False

@app.route("/")
def home():
    content = "Page not found"
    with open('./page/home.html') as file:
        content = file.read()
    return content

@app.route('/videoFeed')
def videoFeed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/command", methods=["POST"])
def command():
    action: str = request.get_json()['action']
    print(action)
    execCommand(action)
    return "";

@app.route("/hello")
def helloWorld():
    return "<p>Hello World!</p>"

if __name__ == "__main__":
    app.run(host="10.42.0.2", port=3000, threaded=True)

