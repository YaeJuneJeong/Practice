import cv2
import socketio
import base64
import time
# setting Yju-guest
sio = socketio.Client()
sio.connect('http://172.26.3.62:3001')

cap = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
ret , fname = cap.read()
result , frame = cv2.imencode('.jpg',fname,encode_param)
data = base64.b64encode(frame)


@sio.on
def connect():
    print('connect')

    cap.release()
    # sio.disconnect()
@sio.event
def connect():
    while True:
        ret, fname = cap.read()
        result, frame = cv2.imencode('.jpg', fname, encode_param)
        data = base64.b64encode(frame)
        sio.emit('req_image',data)
        
@sio.on("msg")
def msg():
    print("msg")

sio.connect('http://172.26.3.62:3001')
# sio.wait()