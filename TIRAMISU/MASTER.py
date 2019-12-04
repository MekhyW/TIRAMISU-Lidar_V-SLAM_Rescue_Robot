#TIRAMISU Robot - MASTER.py
#Version: 1.0
import numpy
import math
import serial
import Poser
import Topographer
import PathPlanner
import Navigator
import Signalizer
Serial = serial.Serial('/dev/ttyS0', 115200)

while True:
    Signalizer.GraphicsRefresh()
    Poser.GetRobotPose()
    Topographer.PlotPresence()
    Topographer.PlotWalls()
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
