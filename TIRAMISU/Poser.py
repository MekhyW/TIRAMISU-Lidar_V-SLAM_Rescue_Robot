import math
import pyrealsense2 as rs
import Topographer
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe.start(cfg)
ROBOT_POSITION_X = 500
ROBOT_POSITION_Y = 500
ROBOT_POSITION_CONFIDENCE = 2
ROBOT_COMPASS = 0
ROBOT_TILT_DEVIATION = 0


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


def get_robot_pose():
    global ROBOT_COMPASS, ROBOT_POSITION_X, ROBOT_POSITION_Y, ROBOT_POSITION_CONFIDENCE, ROBOT_TILT_DEVIATION
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
        ROBOT_COMPASS += 90
        if ROBOT_COMPASS > 360:
            ROBOT_COMPASS -= 360
        ROBOT_POSITION_X = (((-1) * data.translation.x) * 100) - (9.5 * math.cos(math.radians(ROBOT_COMPASS))) + 500
        ROBOT_POSITION_Y = (((-1) * data.translation.z) * 100) - (9.5 * math.sin(math.radians(ROBOT_COMPASS))) + 500
        ROBOT_POSITION_CONFIDENCE = data.tracker_confidence
        if (Alpha >= 0 and Gamma <= 0) or (Alpha <= 0 and Gamma >= 0):
            ROBOT_TILT_DEVIATION = Alpha + Gamma
        else:
            ROBOT_TILT_DEVIATION = abs(Alpha - Gamma)
        ROBOT_TILT_DEVIATION = abs(ROBOT_TILT_DEVIATION)
        