#TIRAMISU Robot - MASTER
import math
import serial
import Poser
import Topographer
import MotionPlanner
import Signalizer
Serial = serial.Serial('/dev/ttyS0', 115200)

def Exit():
    for _ in range(10):
        Serial.write(0)
    Signalizer.SignalizeExit()

def Victim(VictimType):
    if not (VictimType in (4, 11, 7, 14)):
        while(MotionPlanner.GetAngleError(Poser.RobotCompass, Poser.RobotPositionX, Poser.RobotPositionY, Topographer.VictimX, Topographer.VictimY) > 30):
            Serial.write(-200)
            Serial.write(455)
        while(MotionPlanner.GetAngleError(Poser.RobotCompass, Poser.RobotPositionX, Poser.RobotPositionY, Topographer.VictimX, Topographer.VictimY) < -30):
            Serial.write(200)
            Serial.write(-455)
    for _ in range(10):
        Serial.write(0)
    if(VictimType in (2, 9, 5, 12)):
        for _ in range(10):
            Serial.write("DEPLOYTWOKITS")
    else:
        for _ in range(10):
            Serial.write("DEPLOYKIT")
    Signalizer.SignalizeVictim(VictimType)
    


while True:
    Signalizer.GraphicsRefresh()
    Poser.GetRobotPose()
    Topographer.PlotPresence()
    Topographer.PlotWalls()
    MotionPlanner.PlanPath()
    pwmL, pwmR = MotionPlanner.SetVelocity()
    Serial.write(pwmL)
    Serial.write(pwmR)
    if(Serial.in_waiting):
        while(Serial.in_waiting):
            Command = Serial.readline()
        if(Command != LastCommand):
            if(Command == "BLACKTILE"):
                Topographer.PlotBlackTile()
            elif(0 < int(Command) <= 14):
                if(Topographer.PlotVictim(int(Command))):
                    Victim(int(Command))
            elif(Command == "STANDBY" and Topographer.SweeperIsOn==True):
                Topographer.SweeperOn(False)
            elif(Command == "RUNNING" and Topographer.SweeperIsOn==False):
                Topographer.SweeperOn(True)
        LastCommand = Command
    if(MotionPlanner.MazeFinished == True and math.sqrt(math.pow((500 - Poser.RobotPositionX), 2) + math.pow((500 - Poser.RobotPositionY), 2)) < 5):
        Exit()
