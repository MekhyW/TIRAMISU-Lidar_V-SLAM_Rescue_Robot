import PyLidar3
import Poser
import math
Sweeper = PyLidar3.YdLidarX4('COM13', 6000)
Sweeper.Connect()
SweeperIsOn = False
LandmarkMap = [[[0]*3]*1000]*1000
PresenceMap = [[[0]*3]*1000]*1000
WallMap = [[[-1]*3]*1000]*1000
WallSplashMap = [[[0]*3]*1000]*1000
SweeperGenerator = None

def SweeperOn(state):
    if state==True:
        SweeperGenerator = Sweeper.StartScanning()
        SweeperIsOn = True
    elif state==False:
        Sweeper.StopScanning()
        SweeperIsOn = False

def PlotWalls():
    lidardata = next(SweeperGenerator)
    for angle in range(0, 360):
        if(lidardata[angle]>0):
            for i in lidardata[angle]*0.1:
                if(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(i * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] == (-1)):
                    WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(i * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] = 0
                elif(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(i * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] == 1):
                    WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(i * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] = 0
                    for c in range(-9, 9):
                        for r in range(-9, 9):
                            if(math.sqrt((c*c)+(r*r)) <= 9):
                                WallSplashMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass)))) + c][round(Poser.RobotPositionY+(i * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass)))) + r] -= 1
            if(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle] * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(lidardata[angle] * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] == (-1) or WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle] * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(lidardata[angle] * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] == 0):
                WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle] * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass))))][round(Poser.RobotPositionY+(lidardata[angle] * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass))))] = 1
                for c in range(-9, 9):
                    for r in range(-9, 9):
                        if(math.sqrt((c*c)+(r*r)) <= 9):
                            WallSplashMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle] * 0.1 * math.cos(math.radians(angle+180+Poser.RobotCompass)))) + c][round(Poser.RobotPositionY+(lidardata[angle] * 0.1 * math.sin(math.radians(angle+180+Poser.RobotCompass)))) + r] += 1

def PlotPresence():
    for c in range(-15, 15):
        for r in range(-15, 15):
            PresenceMap[Poser.CurrentFloor][Poser.RobotPositionX + c*math.cos(math.radians(Poser.RobotCompass))][Poser.RobotPositionY + r*math.sin(math.radians(Poser.RobotCompass))] = 1

def PlotBlackTile():
    for c in range(0, 30):
        for r in range(0, 30):
            angle = math.radians(Poser.RobotCompass) + math.atan((c-15)/(r+15))
            hipotenuse = math.sqrt(((c-15)*(c-15))+((r+15)*(r+15)))
            LandmarkMap[Poser.CurrentFloor][round(Poser.RobotPositionX + hipotenuse*math.cos(angle))][round(Poser.RobotPositionY + hipotenuse*math.sin(angle))] = 99

def PlotVictim(VictimType):
    if(VictimType>0 and VictimType<=7):
        LandmarkMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(15 * math.cos(math.radians(Poser.RobotCompass+270))))][round(Poser.RobotPositionY+(15 * math.sin(math.radians(Poser.RobotCompass+270))))] = VictimType
    elif(VictimType>7):
        LandmarkMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(15 * math.cos(math.radians(Poser.RobotCompass+90))))][round(Poser.RobotPositionY+(15 * math.sin(math.radians(Poser.RobotCompass+90))))] = VictimType