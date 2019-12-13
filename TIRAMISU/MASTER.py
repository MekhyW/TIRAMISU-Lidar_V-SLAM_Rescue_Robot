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

def Exit():
    for _ in range(10):
        SERIAL.write(0)
    Signalizer.SignalizeExit()

def Victim(VictimType):
    if not VictimType in (4, 11, 7, 14):
        while MotionPlanner.GetAngleError(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) > 30:
            SERIAL.write(-200)
            SERIAL.write(455)
        while MotionPlanner.GetAngleError(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, Topographer.VICTIM_X, Topographer.VICTIM_Y) < -30:
            SERIAL.write(200)
            SERIAL.write(-455)
    for _ in range(10):
        SERIAL.write(0)
    if VictimType in (2, 9, 5, 12):
        for _ in range(10):
            SERIAL.write("DEPLOYTWOKITS")
    else:
        for _ in range(10):
            SERIAL.write("DEPLOYKIT")
    Signalizer.SignalizeVictim(VictimType)
    


while True:
    Signalizer.GraphicsRefresh()
    Poser.GetRobotPose()
    Topographer.PlotPresence()
    Topographer.PlotWalls()
    MotionPlanner.PlanPath()
    pwmL, pwmR = MotionPlanner.SetVelocity()
    SERIAL.write(pwmL)
    SERIAL.write(pwmR)
    if SERIAL.in_waiting:
        while SERIAL.in_waiting:
            COMMAND = SERIAL.readline()
        if COMMAND != LAST_COMMAND:
            if COMMAND == "BLACKTILE":
                Topographer.PlotBlackTile(Poser.CURRENT_FLOOR)
            elif 0 < int(COMMAND) <= 14:
                if Topographer.PlotVictim(int(COMMAND)):
                    Victim(int(COMMAND))
            elif COMMAND == "STANDBY" and Topographer.SweeperIsOn:
                Topographer.SweeperOn(False)
            elif COMMAND == "RUNNING" and not Topographer.SweeperIsOn:
                Topographer.SweeperOn(True)
        LAST_COMMAND = COMMAND
    if MotionPlanner.MAZE_FINISHED and math.sqrt(math.pow((500 - Poser.ROBOT_POSITION_X), 2) + math.pow((500 - Poser.ROBOT_POSITION_Y), 2)) < 5:
        Exit()
