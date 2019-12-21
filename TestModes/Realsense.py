import math
import time
import pyrealsense2 as rs
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe.start(cfg)

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

while True:
    frames = pipe.wait_for_frames()
    pose = frames.get_pose_frame()
    if pose:
        data = pose.get_pose_data()
        Alpha, Beta, Gamma = quaternion_to_euler(data.rotation.x, data.rotation.y, data.rotation.z, data.rotation.w)
        ROBOT_COMPASS = int(Beta*(-1))
        if not 0 < abs(Alpha) < 90:
            if ROBOT_COMPASS > 0:
                ROBOT_COMPASS = 180 - ROBOT_COMPASS
            else:
                ROBOT_COMPASS = (-180) - ROBOT_COMPASS
        if ROBOT_COMPASS < 0:
            ROBOT_COMPASS += 360
        print(int(Alpha), ROBOT_COMPASS, int(data.translation.x*100), int(data.translation.z*(-100)), int(data.translation.y*100))
    #time.sleep(0.3)