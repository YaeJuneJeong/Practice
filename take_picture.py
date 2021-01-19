import os;
import pyrealsense2 as rs
import numpy as np
import cv2


original_data_dir = 'C:/Users/jyj98/Desktop/Realsense/Mashroom'




## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Show images
        color_image = np.asanyarray(color_frame.get_data())
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)
        key = cv2.waitKey(1) & 0xff
        if key == 13:  # Esc
            fnames = ['non_mash{}.jpg'.format(i) for i in range(4)]
            for fname in fnames:
                cv2.imwrite(os.path.join(original_data_dir,fname),color_image)
        if key == 27: # Enter
            break

finally:

    # Stop streaming
    pipeline.stop()