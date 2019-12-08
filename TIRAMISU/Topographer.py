import PyLidar3
import Poser
import Navigator
import math
Sweeper = PyLidar3.YdLidarX4('COM13', 6000)
Sweeper.Connect()
SweeperIsOn = False
LandmarkMap = [[[0]*3]*1000]*1000
PresenceMap = [[[0]*3]*1000]*1000
WallMap = [[[-1]*3]*1000]*1000
WallSplashMap = [[[0]*3]*1000]*1000
EdgeWeightMap = [[[1]*3]*1000]*1000
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
            AngCos = math.cos(math.radians(angle+Poser.RobotCompass))
            AngSin = math.sin(math.radians(angle+Poser.RobotCompass))
            for i in range(0, round(lidardata[angle]*0.1)):
                if(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos))][round(Poser.RobotPositionY+(i*AngSin))] == (-1)):
                    WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos))][round(Poser.RobotPositionY+(i*AngSin))] = 0
                elif(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos))][round(Poser.RobotPositionY+(i*AngSin))] == 1):
                    WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos))][round(Poser.RobotPositionY+(i*AngSin))] = 0
                    for c in range(-15, 15):
                        for r in range(-15, 15):
                            if(math.sqrt((c*c)+(r*r)) <= 9):
                                WallSplashMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos)) + c][round(Poser.RobotPositionY+(i*AngSin)) + r] -= 1
                            elif(math.sqrt((c*c)+(r*r)) <= 15 and EdgeWeightMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos)) + c][round(Poser.RobotPositionY+(i*AngSin)) + r] >= 15-math.sqrt((c*c)+(r*r))):
                                EdgeWeightMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(i*AngCos)) + c][round(Poser.RobotPositionY+(i*AngSin)) + r] -= 15-math.sqrt((c*c)+(r*r))
            if(WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle]*0.1*AngCos))][round(Poser.RobotPositionY+(lidardata[angle]*0.1*AngSin))] == (-1) or WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle]*0.1*AngCos))][round(Poser.RobotPositionY+(lidardata[angle]*0.1*AngSin))] == 0):
                WallMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle]*0.1*AngCos))][round(Poser.RobotPositionY+(lidardata[angle]*0.1*AngSin))] = 1
                for c in range(-15, 15):
                    for r in range(-15, 15):
                        if(math.sqrt((c*c)+(r*r)) <= 9):
                            WallSplashMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle]*0.1*AngCos)) + c][round(Poser.RobotPositionY+(lidardata[angle]*0.1*AngSin)) + r] += 1
                        elif(math.sqrt((c*c)+(r*r)) <= 15):
                            EdgeWeightMap[Poser.CurrentFloor][round(Poser.RobotPositionX+(lidardata[angle]*0.1*AngCos)) + c][round(Poser.RobotPositionY+(lidardata[angle]*0.1*AngSin)) + r] += 15-math.sqrt((c*c)+(r*r))

def PlotPresence():
    for c in range(-15, 15):
        for r in range(-10, 10):
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