import math
import mypylidar3
import Poser
Sweeper = mypylidar3.YdLidarX4('COM6', 5000)
Sweeper.Connect()
SWEEPER_IS_ON = True
SWEEPER_GENERATOR = Sweeper.StartScanning()
AVOID = 0
LANDMARK_MAP = [[[0 for x in range(1000)] for y in range(1000)] for z in range(3)]
PRESENCE_MAP = [[[0 for x in range(1000)] for y in range(1000)] for z in range(3)]
WALL_MAP = [[[-1 for x in range(1000)] for y in range(1000)] for z in range(3)]
WALL_SPLASH_MAP = [[[0 for x in range(1000)] for y in range(1000)] for z in range(3)]
EDGE_WEIGHT_MAP = [[[0 for x in range(1000)] for y in range(1000)] for z in range(3)]
VICTIM_X = 0
VICTIM_Y = 0

def sweeper_on(state):
    global SWEEPER_IS_ON
    global SWEEPER_GENERATOR
    if state:
        SWEEPER_GENERATOR = Sweeper.StartScanning()
        SWEEPER_IS_ON = True
    elif not state:
        Sweeper.StopScanning()
        SWEEPER_IS_ON = False


def plot_walls():
    lidardata = next(SWEEPER_GENERATOR)
    global AVOID
    AVOID = 0
    for angle in [x for x in range(0, 360) if x not in range(91, 270)]:
        angcos = math.cos(math.radians(angle+Poser.ROBOT_COMPASS))
        angsin = math.sin(math.radians(angle+Poser.ROBOT_COMPASS))
        distance = (lidardata[angle] * 0.1) + 3.3
        if distance > 3.3 and 9 <= Poser.ROBOT_POSITION_X+(distance*angcos) < 991 and 9 <= Poser.ROBOT_POSITION_Y+(distance*angsin) < 991:
            if 15 < angle < 45 and distance < 14:
                AVOID = 1
            elif 315 < angle < 345 and distance < 14:
                AVOID = -1
            for i in range(0, round(distance)):
                if i > 30:
                    break
                if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos))][round(Poser.ROBOT_POSITION_Y+(i*angsin))] == (-1):
                    WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos))][round(Poser.ROBOT_POSITION_Y+(i*angsin))] = 0
                elif WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos))][round(Poser.ROBOT_POSITION_Y+(i*angsin))] == 1:
                    WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos))][round(Poser.ROBOT_POSITION_Y+(i*angsin))] = 0
                    for c in range(-10, 11):
                        for r in range(-10, 11):
                            if math.sqrt((c*c)+(r*r)) <= 6:
                                WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos)) + c][round(Poser.ROBOT_POSITION_Y+(i*angsin)) + r] -= 1
                            elif math.sqrt((c*c)+(r*r)) <= 15 and EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos)) + c][round(Poser.ROBOT_POSITION_Y+(i*angsin)) + r] >= 15-math.sqrt((c*c)+(r*r)):
                                EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(i*angcos)) + c][round(Poser.ROBOT_POSITION_Y+(i*angsin)) + r] -= 15-math.sqrt((c*c)+(r*r))
                if i == round(distance)-1 and WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(distance*angcos))][round(Poser.ROBOT_POSITION_Y+(distance*angsin))] in (-1, 0):
                    WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(distance*angcos))][round(Poser.ROBOT_POSITION_Y+(distance*angsin))] = 1
                    for c in range(-10, 11):
                        for r in range(-10, 11):
                            if math.sqrt((c*c)+(r*r)) <= 6:
                                WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(distance*angcos)) + c][round(Poser.ROBOT_POSITION_Y+(distance*angsin)) + r] += 1
                            elif math.sqrt((c*c)+(r*r)) <= 15:
                                EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(distance*angcos)) + c][round(Poser.ROBOT_POSITION_Y+(distance*angsin)) + r] += 15-math.sqrt((c*c)+(r*r))


def plot_presence():
    for c in range(-15, 15):
        for r in range(-15, 15):
            if math.sqrt((c*c)+(r*r)) <= 15:
                PRESENCE_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+c)][round(Poser.ROBOT_POSITION_Y+r)] = 1


def plot_black_tile(floor):
    for c in range(30):
        for r in range(30):
            angle = math.radians(Poser.ROBOT_COMPASS) + math.atan((c-15)/(r+15))
            hipotenuse = math.sqrt(((c-15)*(c-15))+((r+15)*(r+15)))
            LANDMARK_MAP[floor][round(Poser.ROBOT_POSITION_X + hipotenuse*math.cos(angle))][round(Poser.ROBOT_POSITION_Y + hipotenuse*math.sin(angle))] = 99


def plot_victim(victim_type):
    global VICTIM_X
    global VICTIM_Y
    victim_found_in_radius = False
    wall_found_in_raytrace = False
    wall_dist = 15
    if victim_type > 0 and victim_type <= 7:
        angcos = math.cos(math.radians(Poser.ROBOT_COMPASS+270))
        angsin = math.sin(math.radians(Poser.ROBOT_COMPASS+270))
        for i in range(20):
            if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + (i * angcos))][round(Poser.ROBOT_POSITION_Y + (i * angsin))] == 1:
                wall_found_in_raytrace = True
                wall_dist = i
                break
        for c in range(-15, 16):
            for r in range(-15, 16):
                if math.sqrt((c*c)+(r*r)) <= 15 and 0 < LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(wall_dist * angcos)+c)][round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin)+r)] <= 14:
                    victim_found_in_radius = True
        if not victim_found_in_radius and wall_found_in_raytrace:
            LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(wall_dist * angcos))][round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin))] = victim_type
            VICTIM_X = round(Poser.ROBOT_POSITION_X+(wall_dist * angcos))
            VICTIM_Y = round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin))
            return True
        else:
            return False
    elif victim_type > 7:
        angcos = math.cos(math.radians(Poser.ROBOT_COMPASS+90))
        angsin = math.sin(math.radians(Poser.ROBOT_COMPASS+90))
        for i in range(20):
            if WALL_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X + (i * angcos))][round(Poser.ROBOT_POSITION_Y + (i * angsin))] == 1:
                wall_found_in_raytrace = True
                wall_dist = i
                break
        for c in range(-15, 16):
            for r in range(-15, 16):
                if math.sqrt((c*c)+(r*r)) <= 15 and 0 < LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(wall_dist * angcos)+c)][round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin)+r)] <= 14:
                    victim_found_in_radius = True
        if not victim_found_in_radius and wall_found_in_raytrace:
            LANDMARK_MAP[Poser.CURRENT_FLOOR][round(Poser.ROBOT_POSITION_X+(wall_dist * angcos))][round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin))] = victim_type
            VICTIM_X = round(Poser.ROBOT_POSITION_X+(wall_dist * angcos))
            VICTIM_Y = round(Poser.ROBOT_POSITION_Y+(wall_dist * angsin))
            return True
        else:
            return False
