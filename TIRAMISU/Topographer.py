import math
import PyLidar3
import Poser
Sweeper = PyLidar3.YdLidarX4('COM13', 6000)
Sweeper.Connect()
SweeperIsOn = False
SweeperGenerator = None
LANDMARK_MAP = [[[0]*3]*1000]*1000
PRESENCE_MAP = [[[0]*3]*1000]*1000
WALL_MAP = [[[-1]*3]*1000]*1000
WALL_SPLASH_MAP = [[[0]*3]*1000]*1000
EDGE_WEIGHT_MAP = [[[0]*3]*1000]*1000
VICTIM_X = 0
VICTIM_Y = 0

def SweeperOn(state):
    global SweeperIsOn
    global SweeperGenerator
    if state:
        SweeperGenerator = Sweeper.StartScanning()
        SweeperIsOn = True
    elif not state:
        Sweeper.StopScanning()
        SweeperIsOn = False


def PlotWalls():
    lidardata = next(SweeperGenerator)
    for angle in range(0, 360):
        if lidardata[angle] > 0:
            AngCos = math.cos(math.radians(angle+Poser.ROBOT_COMPASS))
            AngSin = math.sin(math.radians(angle+Poser.ROBOT_COMPASS))
            for i in range(0, round(lidardata[angle]*0.1)):
                if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos))][round(Poser.ROBOT_POSITION_Y+(i*AngSin))] == (-1):
                    WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos))][round(Poser.ROBOT_POSITION_Y+(i*AngSin))] = 0
                elif WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos))][round(Poser.ROBOT_POSITION_Y+(i*AngSin))] == 1:
                    WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos))][round(Poser.ROBOT_POSITION_Y+(i*AngSin))] = 0
                    for c in range(-15, 16):
                        for r in range(-15, 16):
                            if math.sqrt((c*c)+(r*r)) <= 9:
                                WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos)) + c][round(Poser.ROBOT_POSITION_Y+(i*AngSin)) + r] -= 1
                            elif math.sqrt((c*c)+(r*r)) <= 15 and EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos)) + c][round(Poser.ROBOT_POSITION_Y+(i*AngSin)) + r] >= 15-math.sqrt((c*c)+(r*r)):
                                EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*AngCos)) + c][round(Poser.ROBOT_POSITION_Y+(i*AngSin)) + r] -= 15-math.sqrt((c*c)+(r*r))
            if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(lidardata[angle]*0.1*AngCos))][round(Poser.ROBOT_POSITION_Y+(lidardata[angle]*0.1*AngSin))] in (-1, 0):
                WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(lidardata[angle]*0.1*AngCos))][round(Poser.ROBOT_POSITION_Y+(lidardata[angle]*0.1*AngSin))] = 1
                for c in range(-15, 16):
                    for r in range(-15, 16):
                        if math.sqrt((c*c)+(r*r)) <= 9:
                            WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(lidardata[angle]*0.1*AngCos)) + c][round(Poser.ROBOT_POSITION_Y+(lidardata[angle]*0.1*AngSin)) + r] += 1
                        elif math.sqrt((c*c)+(r*r)) <= 15:
                            EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(lidardata[angle]*0.1*AngCos)) + c][round(Poser.ROBOT_POSITION_Y+(lidardata[angle]*0.1*AngSin)) + r] += 15-math.sqrt((c*c)+(r*r))


def PlotPresence():
    for c in range(-15, 16):
        for r in range(-10, 11):
            PRESENCE_MAP[Poser.CURRENT_FLOOR][Poser.ROBOT_POSITION_X + c*math.cos(math.radians(Poser.ROBOT_COMPASS))][Poser.ROBOT_POSITION_Y + r*math.sin(math.radians(Poser.ROBOT_COMPASS))] = 1


def PlotBlackTile(floor):
    for c in range(30):
        for r in range(30):
            angle = math.radians(Poser.ROBOT_COMPASS) + math.atan((c-15)/(r+15))
            hipotenuse = math.sqrt(((c-15)*(c-15))+((r+15)*(r+15)))
            LANDMARK_MAP[floor][round(Poser.ROBOT_POSITION_X + hipotenuse*math.cos(angle))][round(Poser.ROBOT_POSITION_Y + hipotenuse*math.sin(angle))] = 99


def PlotVictim(VictimType):
    VictimFoundInRadius = False
    WallFoundInRaytrace = False
    WallDist = 15
    if VictimType > 0 and VictimType <= 7:
        AngCos = math.cos(math.radians(Poser.ROBOT_COMPASS+270))
        AngSin = math.sin(math.radians(Poser.ROBOT_COMPASS+270))
        for i in range(20):
            if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + (i * AngCos))][round(Poser.ROBOT_POSITION_Y + (i * AngSin))] == 1:
                WallFoundInRaytrace = True
                WallDist = i
                break
        for c in range(-15, 16):
            for r in range(-15, 16):
                if math.sqrt((c*c)+(r*r)) <= 15 and 0 < LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(WallDist * AngCos)+c)][round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin)+r)] <= 14:
                    VictimFoundInRadius = True
        if not VictimFoundInRadius and WallFoundInRaytrace:
            LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(WallDist * AngCos))][round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin))] = VictimType
            global VICTIM_X
            global VICTIM_Y
            VICTIM_X = round(Poser.ROBOT_POSITION_X+(WallDist * AngCos))
            VICTIM_Y = round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin))
            return True
        else:
            return False
    elif VictimType > 7:
        AngCos = math.cos(math.radians(Poser.ROBOT_COMPASS+90))
        AngSin = math.sin(math.radians(Poser.ROBOT_COMPASS+90))
        for i in range(20):
            if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + (i * AngCos))][round(Poser.ROBOT_POSITION_Y + (i * AngSin))] == 1:
                WallFoundInRaytrace = True
                WallDist = i
                break
        for c in range(-15, 16):
            for r in range(-15, 16):
                if math.sqrt((c*c)+(r*r)) <= 15 and 0 < LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(WallDist * AngCos)+c)][round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin)+r)] <= 14:
                    VictimFoundInRadius = True
        if not VictimFoundInRadius and WallFoundInRaytrace:
            LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(WallDist * AngCos))][round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin))] = VictimType
            global VICTIM_X
            global VICTIM_Y
            VICTIM_X = round(Poser.ROBOT_POSITION_X+(WallDist * AngCos))
            VICTIM_Y = round(Poser.ROBOT_POSITION_Y+(WallDist * AngSin))
            return True
        else:
            return False
