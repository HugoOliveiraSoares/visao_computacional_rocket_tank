import cv2
from flask import Response
from flask import Flask
from flask import render_template
from line_tracking import LineTracking

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def edge_detection():
    while True:
        _, outframe = camera.read()
        outframe = cv2.flip(outframe, -1)
        test = LineTracking(outframe) 
        test.processing() 
        (flag, encodedImage) = cv2.imencode(".jpg", test.img_final)

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


def generate_video():
    while True:
        _, outputFrame = camera.read()
        outputFrame = cv2.flip(outputFrame, -1)
        
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_video(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video_edge")
def video_edge():
    return Response(edge_detection(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
    camera.release()
