import time
import numpy as np
import pyrealsense2 as rs
import open3d as o3d

# setting max, min range
device = rs.context().query_devices()[0]
advnc_mode = rs.rs400_advanced_mode(device)
depth_table_control_group = advnc_mode.get_depth_table()
depth_table_control_group.disparityShift = 60
depth_table_control_group.depthClampMax = 4000
depth_table_control_group.depthClampMin = 0
advnc_mode.set_depth_table(depth_table_control_group)



# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, rs.format.z16, 30)
config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

# Start streaming
profile=pipeline.start(config)
# Get stream profile and camera intrinsics
profile = pipeline.get_active_profile()
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 1)

def take_3Dpicture(name):
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
        time.sleep(1)

    except Exception as e:
        print(e)
file_name = [0,90,180,270]
file_names = ['3dScan.{}.ply'.format(i) for i in file_name]

for name in file_names:
    take_3Dpicture(name)
    #  check option
    # pcd = o3d.io.read_point_cloud("./out1.ply")
    # o3d.visualization.draw_geometries([pcd])
pipeline.stop()