import cv2
from flask import Response
from flask import Flask
from flask import render_template
from line_tracking import LineTracking
import threading
import serial_con

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

motors = serial_con.Motors('/dev/ttyS0', 115200)

frame = None

def cam():
    global frame
    while True:
        _, cam = camera.read()
        frame = cv2.flip(cam, -1)

def edge_detection():
    global frame
    while True:
        if frame is None:
            continue
        outframe = frame.copy()
        line = LineTracking(outframe) 
        img_line, M = line.processing() 
        cv2.line(outframe,pt1=(0,60),pt2=(160,60),color=(255, 255, 255),thickness=3)
        cv2.line(outframe,pt1=(80,0),pt2=(80,120),color=(255, 255, 255),thickness=3)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Left")
                motors.turn_left() 
            if cx < 120 and cx > 40 :
                print("On Track!")
                motors.forward()
            if cx <=40 :
                print("Turn Right")
                motors.turn_rigth()

        (flag, encodedImage) = cv2.imencode(".jpg", img_line)

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


def generate_video():
    while True:
        if frame is None:
            continue
        outputFrame = frame.copy()
        # cv2.line(outputFrame,pt1=(0,240),pt2=(640,240),color=(255, 255, 255),thickness=1)
        # cv2.line(outputFrame,pt1=(320,0),pt2=(320,480),color=(255, 255, 255),thickness=1)
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

    t = threading.Thread(target=cam)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=5000, threaded=True)
    camera.release()
