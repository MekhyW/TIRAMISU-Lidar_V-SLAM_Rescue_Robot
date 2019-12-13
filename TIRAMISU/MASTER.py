#TIRAMISU Robot - MASTER
import math
import serial
import Poser
import Topographer
import MotionPlanner
import Signalizer
Serial = serial.Serial('/dev/ttyS0', 115200)

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
            elif(Command == "STANDBY" and Topographer.SweeperIsOn==True):
                Topographer.SweeperOn(False)
            elif(Command == "RUNNING" and Topographer.SweeperIsOn==False):
                Topographer.SweeperOn(True)
        LastCommand = Command
