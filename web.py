import cv2
from flask import Response
from flask import Flask
from flask import render_template

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def generate(is_gray):
    while True:
        _, outputFrame = camera.read()
        outputFrame = cv2.flip(outputFrame, -1)
        if is_gray:
            outputFrame = cv2.cvtColor(outputFrame, cv2.COLOR_BGR2GRAY)
            outputFrame = cv2.Canny(image=outputFrame, threshold1=127, threshold2=127)
        
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/video")
def video():
	return Response(generate(False),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video_gray")
def video_gray():
	return Response(generate(True),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

camera.release()
