# pip install pyserial
# pip install requests
# pip install "python-socketio[client]"

import requests;
import serial;
import datetime;
import time;
import math;
import json;
import socketio;
import base64
import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


# socket 서버 연결
sio = socketio.Client()
sio.connect('http://localhost:3001')

@sio.on("req_cosdata")
def socket_data(temp, hum):
    sio.emit("res_cosdata", {"temperature": temp, "humidity": hum})


@sio.on("req_video")
def socket_stream(req):
    if req:
        stream_end_value = True
    t= threading.Thread(target=stream_thread)
def stream_thread(req):

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        result, frame = cv2.imencode('.jpg', color_image, encode_param)
        data = base64.b64encode(frame)

        sio.emit('req_image', data)
        if stream_end_value:
            print("영상 촬영")
            break
