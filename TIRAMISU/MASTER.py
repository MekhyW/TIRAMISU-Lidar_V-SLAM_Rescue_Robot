#TIRAMISU Robot - MASTER
import math
import serial
import time
import Poser
import Topographer
import MotionPlanner
import Signalizer
SERIAL = serial.Serial('COM26', 115200)
COMMAND = None
LAST_COMMAND = None

def exit_bonus():
    for _ in range(10):
        SERIAL.write(200)
    Signalizer.signalize_exit_bonus()

def victim(victim_type):
    if not victim_type in (4, 11, 7, 14):
        while MotionPlanner.get_angle_error(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) > 15:
            Poser.get_robot_pose()
            SERIAL.write(180)
        while MotionPlanner.get_angle_error(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) < -15:
            Poser.get_robot_pose()
            SERIAL.write(0)
    if victim_type in (2, 9, 5, 12):
        for _ in range(10):
            SERIAL.write(252)
    else:
        for _ in range(10):
            SERIAL.write(251)
    Signalizer.signalize_victim(victim_type)
    


while True:
    t = time.time()
    Signalizer.graphics_refresh()
    Poser.get_robot_pose()
    if Topographer.SWEEPER_IS_ON:
        Topographer.plot_presence()
        Topographer.plot_walls()
        if Topographer.AVOID == 0:
            MotionPlanner.plan_path()
            SERIAL.write(int(MotionPlanner.ROBOT_ANGLE_ERROR+90))
        elif Topographer.AVOID == -1:
            SERIAL.write(201)
        elif Topographer.AVOID == 1:
            SERIAL.write(202)
    if SERIAL.in_waiting:
        while SERIAL.in_waiting:
            COMMAND = SERIAL.read()
        if COMMAND != LAST_COMMAND:
            if COMMAND == 99:
                Topographer.plot_black_tile()
            elif 0 < int(COMMAND) <= 14:
                if Topographer.plot_victim(int(COMMAND)):
                    victim(int(COMMAND))
            elif COMMAND == 20 and Topographer.SWEEPER_IS_ON:
                Topographer.sweeper_on(False)
            elif COMMAND == 21 and not Topographer.SWEEPER_IS_ON:
                Topographer.sweeper_on(True)
        LAST_COMMAND = COMMAND
    if MotionPlanner.MAZE_FINISHED and math.sqrt(math.pow((500 - Poser.ROBOT_POSITION_X), 2) + math.pow((500 - Poser.ROBOT_POSITION_Y), 2)) < 5 and Topographer.SWEEPER_IS_ON:
        exit_bonus()
    print(time.time() - t, MotionPlanner.ROBOT_ANGLE_ERROR)
