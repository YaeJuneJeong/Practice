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

# import pyrealsense2 as rs
# import numpy as np
# import cv2

# # Start streaming

# # Create a pipeline
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# profile = pipeline.start(config)

# depth_sensor = profile.get_device().first_depth_sensor()
# depth_sensor.set_option(rs.option.depth_units, 0.001)

# socket 서버 연결
sio = socketio.Client()
sio.connect('http://172.26.3.62:3001')


@sio.on("req_cosdata")
def socket_data(temp, hum):
    sio.emit("res_cosdata", {"temperature": temp, "humidity": hum})


SERVER_URL = 'http://54.210.105.132/api'  # 서버 url
PIN = '107512'  # 기기 고유 핀번호

R = "R"  # 환경 데이터 프로토콜
C = "C"  # 온도 프로토콜
S = "S"  # 습도 프로토콜
WATER_ORDER = 'W'  # 물주기 프로토콜
MOTER_ORDER = 'M'  # 3D 촬영 프로토콜

HOUR = 100  # 온도 데이터 전송 시간 기준값
WATER_TIME = 0  # 물주는 시간 기준값
MOTER_TIME = HOUR * 6  # 모터 시간 기준값
D2_TIME = 0

water_num = 0

data = None  # 환경 데이터 전역

url = "http://54.210.105.132/api/image/upload"
title = 'title'
file_path = 'D:/example1.jpg'


# 시작전 polling 코드
def start_before():
    global data
    global water_num

    id_value = ''

    while True:
        time.sleep(1)  # 429 에러 방지
        params = {'pin': PIN}
        response = requests.get(
            SERVER_URL + '/farm/exist',
            params=params
        )

        if response.status_code == 200:
            id_value = response.text
            break

    params = {'id': id_value, 'type': 'custom'}
    response = requests.get(SERVER_URL + '/farm/data', params=params)
    result = json.loads(response.text)
    water_num = result['water']
    temp_array = result['temperature']
    hum_array = result['humidity']

    data_len = len(temp_array)

    data = [None] * data_len

    for i in range(0, data_len):
        temp_array[i] = str(temp_array[i]['setting_value'])
        hum_array[i] = str(hum_array[i]['setting_value'])
        data[i] = R + C + temp_array[i] + S + hum_array[i]

    print(f"물 횟수 : {water_num}")
    print(f"온도 : {temp_array}")
    print(f"습도 : {hum_array}")
    print(f"데이터 : {data}")

    return True if data else False


def encode_serial_data(str):
    return str.encode('utf-8')


# 기기 가동 코드
def start_after():
    global water_num
    global data
    global pipeline
    global D2_TIME

    WATER_TIME = HOUR * 24 / water_num

    serial_send_len = 0
    hour = 0  # 시간 초로 변환
    water_time = WATER_TIME  # 값 받아 오면 연산할 물주기 시간
    moter_time = MOTER_TIME

    now = datetime.datetime.now()
    Arduino = serial.Serial(port='COM7', baudrate=9600)
    print(f"데이터 받기 성공  기기 가동중 데이터 : {data}")

    while True:
        dt1 = datetime.datetime.now()
        result = dt1 - now
        seconds = int(result.total_seconds())

        if Arduino.readable():
            LINE = Arduino.readline()
            code = str(LINE.decode().replace('\n', ''))
            print(code)
            hum = code[10: 12]
            temp = code[30: 32]
            socket_data(hum, temp)

        if seconds == hour:
            Arduino.write(encode_serial_data(data[serial_send_len]))

            serial_send_len += 1
            hour += HOUR

        if seconds == water_time:
            Arduino.write(encode_serial_data(WATER_ORDER))
            water_time += WATER_TIME

        if seconds == moter_time:
            Arduino.write(encode_serial_data(MOTER_ORDER))
            moter_time += MOTER_TIME

        # if seconds == D2_TIME:
        # Wait for a coherent pair of frames: depth and color
        # frames = pipeline.wait_for_frames()
        # color_frame = frames.get_color_frame()

        # # Convert images to numpy arrays
        # color_image = np.asanyarray(color_frame.get_data())
        # cv2.imwrite('./color_sensor.jpg', color_image)

        # files = {'mushroom': ('mushroom12.jpg', open(file_path, 'rb'))}
        # data = [('mushroomId', 17)]
        # response =requests.post(url, files=files, data=data)
        # print(response.status_code)
        # D2_TIME += 1000

        # 끝내기 데이터 오면 break 후 리턴


while True:

    if start_before():
        start_after()