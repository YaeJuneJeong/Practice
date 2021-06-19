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
import threading

import pyrealsense2 as rs
import numpy as np
import cv2

pipeline_check = False
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# socket 서버 연결
sio = socketio.Client()
sio.connect('http://localhost:3001')

stream_end_value = False

@sio.on("req_cosdata")
def socket_data(temp = 0, hum = 0):
    sio.emit("res_cosdata", {"temperature": temp, "humidity": hum})

@sio.on("req_video")
def socket_stream(req) :
    global stream_end_value
    print("web socket req_video connect")
    if req == 'disconnect' :
        print("web socket req_video disconnect")
        stream_end_value = True
        return 
    t = threading.Thread(target=stream_thread)
    t.start() ;

def stream_thread() :

    global pipeline_check
    global pipeline
    global config
    global stream_end_value

    if pipeline_check == False :
        pipeline_check = True
        profile = pipeline.start(config)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        print("Web socket on")

        while True:
            time.sleep(0.2)
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            result, frame = cv2.imencode('.jpg', color_image, encode_param)
            data = base64.b64encode(frame).decode('utf-8')
            sio.emit('res_video', data)
            if stream_end_value:
                pipeline.stop()
                print("Web socket disconnet")
                stream_end_value = False
                break
        pipeline_check = False
        return
    else :
        return



SERVER_URL = 'http://184.73.45.24/api'  # 서버 url
PIN = '107512'  # 기기 고유 핀번호

R = "R"  # 환경 데이터 프로토콜
C = "C"  # 온도 프로토콜
S = "S"  # 습도 프로토콜
WATER_ORDER = 'W'  # 물주기 프로토콜
MOTER_ORDER = 'M'  # 3D 촬영 프로토콜

DAY = 86400
HOUR = 3600  # 온도 데이터 전송 시간 기준값
WATER_TIME = 0  # 물주는 시간 기준값
MOTER_TIME = HOUR * 3  # 모터 시간 기준값
D2_TIME = 1000

water_num = 0


data = None  # 환경 데이터 전역
title = 'title'
file_path = 'D:/example1.jpg'

prg_id = 0

def take_3Dpicture(name, pipeline, decimate, pc):
    try:

        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        depth_frame = decimate.process(depth_frame)
        color_image = np.asanyarray(color_frame.get_data())

        mapped_frame, color_source = color_frame, color_image
        points = pc.calculate(depth_frame)
        pc.map_to(mapped_frame)

        points.export_to_ply(name, mapped_frame)

    except Exception as e:
        print(e)


# 시작전 polling 코드
def start_before():
    global data
    global water_num
    global prg_id
    global pipeline

    machien = { 'id' : 1, 'ip' : 'http://192.168.0.10' }
    response_machien = requests.put(SERVER_URL + "/myfarm/register/ip", data=machien)

    print(f" machien ip set server : {response_machien.status_code}")

    # GUI 코드
    while True :
        response_user = requests.get(SERVER_URL + "/user/info/3")

        print(f" user data : {response_user.status_code}")

        if response_user.status_code == 200 :
            break
        time.sleep(5)

    #while True :
        #time.sleep(1)
        #print("exist check ...")
        #pipeline.start()
        #frames = pipeline.wait_for_frames()
        #color_frame = frames.get_color_frame()
        #color_image = np.asarray(color_frame.get_data())
     
        ## take the only location of mushroom pot -> 1/3 * width,1/2*height
        #recent_image = color_image[100:350, 290:550]
        #check_image = cv2.imread('./check.jpg')[100:350, 290:550]
        #cv2.imwrite('./rec.jpg',check_image)
        #cv2.imwrite('./recent.jpg',recent_image)
        #hist_recent = cv2.calcHist(recent_image, [0,1], None, [180,256], [0,180,0,256])
        #hist_check = cv2.calcHist(check_image, [0,1], None, [180,256], [0,180,0,256])
        #number = cv2.compareHist(hist_recent, hist_check, cv2.HISTCMP_CORREL)
     
        #print(number)
        #pipeline.stop()
        #if number > 0.4:
            #print('Not exist')   
           
        #else:
                #            배지입력 확인
            #print("Exist !!")    
            #break 

        
    
    while True:
        params = {'pin': PIN}
        response = requests.get(
            SERVER_URL + '/farm/exist',
            params=params
        )

        if response.status_code == 200:
            prg_id = response.text
            break
        else : 
            print("Not prg")
        time.sleep(5)  # 429 에러 방지

    params = {'id': prg_id, 'type': 'custom'}
    response = requests.get(SERVER_URL + '/farm/data', params=params)
    result = json.loads(response.text)
    water_num = result['water']
    temp_array = result['temperature']
    hum_array = result['humidity']

    params_status = { 'id' : "1", "status" : "true" } 
    response_status = requests.put(SERVER_URL + '/myfarm/status', params=params_status)

    print(f"machien status : {response_status.status_code}")

    data_len = len(temp_array)

    data = [None] * data_len

    for i in range(0, data_len):
        temp_array[i] = str(temp_array[i]['setting_value'])
        hum_array[i] = str(hum_array[i]['setting_value'])
        data[i] = R + C + temp_array[i] + S + hum_array[i]

    print(f"water_num : {water_num}")
    print(f"temp_array : {temp_array}")
    print(f"hum_array : {hum_array}")
    print(f"total_data : {data}")

    return True if data else False


def encode_serial_data(str):
    return str.encode('utf-8')


# 기기 가동 코드
def start_after():
    global water_num
    global data
    global D2_TIME
    global pipeline
    global config
    global pipeline_check
    global prg_id
    global DAY

    # HOUR * 24 / water_num
    WATER_TIME = HOUR * 24 / water_num

    serial_send_len = 0
    hour = 0  # 시간 초로 변환
    # WATER_TIME
    water_time = 10000  # 값 받아 오면 연산할 물주기 시간
    # MOTER_TIME
    moter_time = MOTER_TIME
    picTime = 100000

    now = datetime.datetime.now()
    Arduino = serial.Serial(port='COM5', baudrate=9600)
    print(f"data success : {data}")
    
    seconds = 0
    dt2 = None
    loadTime = 0
    hum = 0
    temp = 0

    while True:
        dt1 = datetime.datetime.now()
        result = dt1 - now
        seconds =  int(result.total_seconds()) - loadTime

        print(f"Python hour : {hour}, water_time : {water_time} moter_time : {moter_time} image : {picTime}")
        print(f"Python seconds : {seconds}")
        
        if Arduino.readable():
            LINE = Arduino.readline()
            code = str(LINE.decode().replace('\n', ''))
            print(code)
            hum = code[18: 20]
            temp = code[38: 40]
            socket_data(temp, hum)

        if seconds - 2 <= hour and hour <= seconds + 2 :

            if len(data) - 1 < serial_send_len :
                response_status_prg = requests.put(SERVER_URL + f'/farm/end?id={prg_id}')
                print(f"prg status : {response_status_prg.status_code}")
                
                params_status = { 'id' : "1", "status" : "false" } 
                response_status = requests.put(SERVER_URL + '/myfarm/status', params=params_status)
                print(f"machien status : {response_status.status_code}")
                break
            
            Arduino.write(data[serial_send_len].encode('utf-8'))
            req_data_humi_temp = { 'prgId' : prg_id, 'tempValue' : temp, 'humiValue' : hum }
            humi_temp_res = requests.post(SERVER_URL + "/data/add", data=req_data_humi_temp) ;
            print(f"Python res_temp : {humi_temp_res.status_code}")
            serial_send_len += 1
            hour += DAY

        if seconds - 2 <= water_time and  water_time <= seconds + 2:
            Arduino.write(WATER_ORDER.encode('utf-8'))
            dt2 = datetime.datetime.now()

            while Arduino.readable() :
                LINE = Arduino.readline()
                code = str(LINE.decode().replace('\n', ''))
                print(code)
                if code[0: 3] == 'end' :
                    loadTime += int((datetime.datetime.now() - dt2).total_seconds())
                    break
                
            water_time += WATER_TIME

        if seconds - 2 <= moter_time - HOUR / 3 and moter_time - HOUR / 3 <= seconds + 2 :

            if pipeline_check == False :
                pipeline_check = True
                Arduino.write(MOTER_ORDER.encode('utf-8'))
                dt2 = datetime.datetime.now()

                # 3d config
                device = rs.context().query_devices()[0]
                advnc_mode = rs.rs400_advanced_mode(device)
                depth_table_control_group = advnc_mode.get_depth_table()
                depth_table_control_group.disparityShift = 60
                depth_table_control_group.depthClampMax = 4000
                depth_table_control_group.depthClampMin = 0
                advnc_mode.set_depth_table(depth_table_control_group)

                pipeline1 = rs.pipeline()
                config1 = rs.config()
                
                config1.enable_stream(rs.stream.depth, rs.format.z16, 30)
                config1.enable_stream(rs.stream.color, rs.format.bgr8, 30)

                # Start streaming
                profile1=pipeline1.start(config)
                # Get stream profile and camera intrinsics
                profile = pipeline1.get_active_profile()
                depth_profile = rs.video_stream_profile(profile1.get_stream(rs.stream.depth))
                pc = rs.pointcloud()
                decimate = rs.decimation_filter()
                decimate.set_option(rs.option.filter_magnitude, 1)

                file_name_3d = [0,90,180,270]
                file_names_3d = ['./3dScan{}.ply'.format(i) for i in file_name_3d]

                i = 0
                
                while Arduino.readable() :
                    LINE = Arduino.readline()
                    code = str(LINE.decode().replace('\n', ''))
                    print(code)
                    print(f"i : {i}")
                    if code[0: 3] == 'end' :
                        loadTime += int((datetime.datetime.now() - dt2).total_seconds())
                        break
                    take_3Dpicture(file_names_3d[i], pipeline1, decimate, pc)
                    i += 0 if i >= 3 else 1
                    
                files = { 'ply' : open(file_names_3d[0], 'rb')}
                req_data_3d = [ ("machineid" , 1) ]
                res_3d = requests.post(SERVER_URL + "/upload/ply", files=files, data=req_data_3d) ;
                print(f"Python res_3d : {res_3d.status_code}")
                    
                pipeline1.stop()
                moter_time += MOTER_TIME
                pipeline_check = False
            else :
                moter_time += 50

        if seconds - 2 <= picTime + 30 and picTime + 30 <= seconds + 2 :


            if pipeline_check == False :
                pipeline_check = True
                profile = pipeline.start(config)

                depth_sensor = profile.get_device().first_depth_sensor()
                
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()

                # Convert images to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())
                cv2.imwrite('./color_sensor.jpg', color_image)

                files = {'compost': ('compost.jpg', open('./color_sensor.jpg', 'rb'))}
                data1 = [('machineid', 1)]
                response_image = requests.post(SERVER_URL + "/upload/compost", files=files, data=data1)
                print(f"Python res_image : {response_image.status_code}")
                pipeline.stop()
                picTime += D2_TIME
                pipeline_check = False
            else :
                picTime += 50
                

        # 끝내기 데이터 오면 break 후 리턴


while True:

    if start_before():
        start_after()
