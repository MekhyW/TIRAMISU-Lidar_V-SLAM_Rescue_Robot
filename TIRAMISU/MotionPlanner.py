import math
import operator
import Poser
import Topographer
UNVISITED_NODE_LIST = []
VISITED_NODE_LIST = []
EXISTENT_NODE_MAP = [[0]*1000]*1000
SEARCH_DONE = False
MAZE_FINISHED = False
ROBOT_ANGLE_ERROR = 0


def GetAngleError(currentAngle, currentX, currentY, targetX, targetY):
    if currentAngle > 180:
        result = math.degrees(math.atan2(targetY-currentY, targetX-currentX) - (currentAngle-360))
    else:
        result = math.degrees(math.atan2(targetY-currentY, targetX-currentX) - currentAngle)
    if result >= 360:
        result -= 360
    elif result <= -360:
        result += 360
    return result


class Node:
    def __init__(self, PositionX, PositionY, PreviousNode):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.PreviousNode = PreviousNode
        self.EuclideanDistance = math.sqrt(math.pow((self.PositionX - Poser.ROBOT_POSITION_X), 2) + math.pow((self.PositionY - Poser.ROBOT_POSITION_Y), 2))
        self.GraphDistance = self.EuclideanDistance + Topographer.EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][self.PositionX][self.PositionY]
        EXISTENT_NODE_MAP[self.PositionX][self.PositionY] = 1
    def Visit(self):
        UNVISITED_NODE_LIST.remove(self)
        VISITED_NODE_LIST.append(self)
        if(Topographer.PRESENCE_MAP[Poser.CURRENT_FLOOR][self.PositionX][self.PositionY] == 0 and 0 < Topographer.EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][self.PositionX][self.PositionY] < 3):
            global SEARCH_DONE
            SEARCH_DONE = True
            self.BacktracePath()
        elif(self.PositionX==500 and self.PositionY==500):
            self.BacktracePath()
        for c in range(-1, 2):
            for r in range(-1, 2):
                if(EXISTENT_NODE_MAP[self.PositionX+c][self.PositionY+r] == 0 and Topographer.WALL_MAP[Poser.CURRENT_FLOOR][self.PositionX+c][self.PositionY+r]==0 and Topographer.WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][self.PositionX+c][self.PositionY+r]<=0 and Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][self.PositionX+c][self.PositionY+r] != 99):
                    node = Node(self.PositionX+c, self.PositionY+r, self)
                    UNVISITED_NODE_LIST.append(node)
    def BacktracePath(self):
        if round(self.EuclideanDistance) <= 10:
            global ROBOT_ANGLE_ERROR
            ROBOT_ANGLE_ERROR = GetAngleError(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, self.PositionX, self.PositionY)
        else:
            self.PreviousNode.BacktracePath()
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
                    

def PlanPath():
    global SEARCH_DONE
    SEARCH_DONE = False
    startnode = Node(Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, None)
    UNVISITED_NODE_LIST.append(startnode)
    startnode.Visit()
    while (not SEARCH_DONE) and (UNVISITED_NODE_LIST):
        UNVISITED_NODE_LIST.sort(key=operator.attrgetter('GraphDistance'))
        UNVISITED_NODE_LIST[0].Visit()
    if not UNVISITED_NODE_LIST:
        global MAZE_FINISHED
        MAZE_FINISHED = True
    else:
        global MAZE_FINISHED
        MAZE_FINISHED = False
    for x in VISITED_NODE_LIST:
        EXISTENT_NODE_MAP[x.PositionX][x.PositionY] = 0
        VISITED_NODE_LIST.remove(x)
        del x
    for x in UNVISITED_NODE_LIST:
        EXISTENT_NODE_MAP[x.PositionX][x.PositionY] = 0
        UNVISITED_NODE_LIST.remove(x)
        del x


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def SetVelocity():
    kp = 3
    if ROBOT_ANGLE_ERROR > 30:
        return -200, 455
    elif ROBOT_ANGLE_ERROR < -30:
        return 200, -455
    else:
        pwmL = constrain(round(200-(ROBOT_ANGLE_ERROR*kp)), 1, 250)
        pwmR = constrain(round(455+(ROBOT_ANGLE_ERROR*kp)), 256, 505)
        return pwmL, pwmR
