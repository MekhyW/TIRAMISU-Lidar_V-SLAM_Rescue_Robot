#TIRAMISU Robot - MASTER
import math
import serial
import Poser
import Topographer
import MotionPlanner
import Signalizer
SERIAL = serial.Serial('/dev/ttyS0', 115200)
COMMAND = None
LAST_COMMAND = None

def exit_bonus():
    for _ in range(10):
        SERIAL.write(0)
    Signalizer.signalize_exit_bonus()

def victim(victim_type):
    if not victim_type in (4, 11, 7, 14):
        while MotionPlanner.get_angle_error(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) > 30:
            SERIAL.write(-200)
            SERIAL.write(455)
        while MotionPlanner.get_angle_error(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) < -30:
            SERIAL.write(200)
            SERIAL.write(-455)
    for _ in range(10):
        SERIAL.write(0)
    if victim_type in (2, 9, 5, 12):
        for _ in range(10):
            SERIAL.write("DEPLOYTWOKITS")
    else:
        for _ in range(10):
            SERIAL.write("DEPLOYKIT")
    Signalizer.signalize_victim(victim_type)
    


while True:
    Signalizer.graphics_refresh()
    Poser.get_robot_pose()
    Topographer.plot_presence()
    Topographer.plot_walls()
    MotionPlanner.plan_path()
    pwm_l, pwm_r = MotionPlanner.set_velocity()
    SERIAL.write(pwm_l)
    SERIAL.write(pwm_r)
    if SERIAL.in_waiting:
        while SERIAL.in_waiting:
            COMMAND = SERIAL.readline()
        if COMMAND != LAST_COMMAND:
            if COMMAND == "BLACKTILE":
                Topographer.plot_black_tile(Poser.CURRENT_FLOOR)
            elif 0 < int(COMMAND) <= 14:
                if Topographer.plot_victim(int(COMMAND)):
                    victim(int(COMMAND))
            elif COMMAND == "STANDBY" and Topographer.SWEEPER_IS_ON:
                Topographer.sweeper_on(False)
            elif COMMAND == "RUNNING" and not Topographer.SWEEPER_IS_ON:
                Topographer.sweeper_on(True)
        LAST_COMMAND = COMMAND
    if MotionPlanner.MAZE_FINISHED and math.sqrt(math.pow((500 - Poser.ROBOT_POSITION_X), 2) + math.pow((500 - Poser.ROBOT_POSITION_Y), 2)) < 5:
        exit_bonus()
