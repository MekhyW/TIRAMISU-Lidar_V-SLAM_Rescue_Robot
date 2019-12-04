import pyrealsense2 as rs
import math
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe.start(cfg)
CurrentFloor = 1
RobotPositionX = 500
RobotPositionY = 500
RobotInclination = 0
RobotCompass = 0
RobotTilt = 0


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


def GetRobotPose():
    pipe.start(cfg)
    try:
        frames = pipe.wait_for_frames()
        pose = frames.get_pose_frame()
        if pose:
            data = pose.get_pose_data()
            RobotPoseFrame = pose.frame_number
            RobotInclination, RobotCompass, RobotTilt = quaternion_to_euler(data.rotation.x, data.rotation.y, data.rotation.z, data.rotation.w)
            RobotPositionX = (data.translation.x * 100) - (9.5 * math.cos(math.radians(RobotCompass))) + 500
            RobotPositionY = (((-1) * data.translation.z) * 100) - (9.5 * math.sin(math.radians(RobotCompass))) + 500
            if data.translation.y * 100 > 30:
                CurrentFloor = 2
            elif data.translation.y * 100 < (-30):
                CurrentFloor = 0
            else:
                CurrentFloor = 1
    finally:
        pipe.stop()