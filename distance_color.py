import json

import pyrealsense2 as rs
import numpy as np
import cv2
import math
import time
# Start streaming

# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)
# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
# if depth_sensor.supports(rs.option.depth_units):
#     depth_sensor.set_option(rs.option.depth_units,0.01)
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)
print(depth_sensor.get_option.__dict__)

# align_to = rs.stream.color
#
# align = rs.align(align_to)
# #
# try:
#     while True:
#
#         # Get frameset of color and depth
#         frames = pipeline.wait_for_frames()
#         # frames.get_depth_frame() is a 640x360 depth image
#
#         # Align the depth frame to color frame
#         aligned_frames = align.process(frames)
#
#         # Get aligned frames
#         aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
#         color_frame = aligned_frames.get_color_frame()
#
#         # Validate that both frames are valid
#         if not aligned_depth_frame or not color_frame:
#             continue
#
#         depth_image = np.asanyarray(aligned_depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#
#         depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
#         # cv2.imshow(title, color_frame)
#         cv2.imshow(title,color_image)
#
#         # def onMouse(event, x, y, flags, params):
#         #     if event == cv2.EVENT_RBUTTONDOWN:
#         #         depth = depth_image[y, x].astype(float)
#         #         print(np.shape(depth_image))
#         #         distance = depth * depth_scale
#         #         print("Distance (m): ", distance)
#         #         print(x,y)
#
#
#         # cv2.setMouseCallback(title, onMouse)
#         def distance(x,y,w,h):
#             print(x,y,w,h)
#             return round(math.sqrt(w**2+h**2),3)
#         key = cv2.waitKey(10)
#         if key == 27:
#             break
#         if key == 97:
#             color_image_copy = color_image
#             x,y,w,h = cv2.selectROI('select',img=color_image_copy)
#             height = h
#             a =16/h # centimeters
#             x, y, w, h = cv2.selectROI('select', img=color_image_copy)
#             if w and h:
#                 d =distance(x,y,w,h)
#                 print(a*d)
#
#
#
#
#
#
#
# finally:
#     cv2.destroyAllWindows()
