import math
#import pyrealsense2 as rs
#import Topographer
#pipe = rs.pipeline()
#cfg = rs.config()
#cfg.enable_stream(rs.stream.pose)
#pipe.start(cfg)
CURRENT_FLOOR = 1
CURRENT_FLOOR_LAST = 1
ROBOT_POSITION_X = 500
ROBOT_POSITION_Y = 500
ROBOT_INCLINATION = 0
ROBOT_COMPASS = 0
ROBOT_TILT = 0


def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))
    return X, Y, Z


#def get_robot_pose():
#    pipe.start(cfg)
#    try:
#        frames = pipe.wait_for_frames()
#        pose = frames.get_pose_frame()
#        if pose:
#            data = pose.get_pose_data()
#            global ROBOT_INCLINATION, ROBOT_COMPASS, ROBOT_TILT, CURRENT_FLOOR, CURRENT_FLOOR_LAST, ROBOT_POSITION_X, ROBOT_POSITION_Y
#            ROBOT_INCLINATION, ROBOT_COMPASS, ROBOT_TILT = quaternion_to_euler(data.rotation.x, data.rotation.y, data.rotation.z, data.rotation.w)
#            ROBOT_POSITION_X = (data.translation.x * 100) - (9.5 * math.cos(math.radians(ROBOT_COMPASS))) + 500
#            ROBOT_POSITION_Y = (((-1) * data.translation.z) * 100) - (9.5 * math.sin(math.radians(ROBOT_COMPASS))) + 500
#            CURRENT_FLOOR_LAST = CURRENT_FLOOR
#            if data.translation.y * 100 > 30:
#                CURRENT_FLOOR = 2
#            elif data.translation.y * 100 < (-30):
#                CURRENT_FLOOR = 0
#            else:
#                CURRENT_FLOOR = 1
#            if CURRENT_FLOOR_LAST != CURRENT_FLOOR:
#                Topographer.plot_black_tile(CURRENT_FLOOR_LAST)
#    finally:
#        pipe.stop()
        