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

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def get_angle_error(current_angle, current_x, current_y, target_x, target_y):
    if current_angle > 180:
        result = math.degrees(math.atan2(target_y-current_y, target_x-current_x) - (current_angle-360))
    else:
        result = math.degrees(math.atan2(target_y-current_y, target_x-current_x) - current_angle)
    if result >= 360:
        result -= 360
    elif result <= -360:
        result += 360
    return result


class Node:
    def __init__(self, position_x, position_y, previous_node):
        self.position_x = position_x
        self.position_y = position_y
        self.previous_node = previous_node
        self.euclidean_distance = math.sqrt(math.pow((self.position_x - Poser.ROBOT_POSITION_X), 2) + math.pow((self.position_y - Poser.ROBOT_POSITION_Y), 2))
        self.graph_distance = self.euclidean_distance + Topographer.EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][self.position_x][self.position_y]
        EXISTENT_NODE_MAP[self.position_x][self.position_y] = 1
    def visit(self):
        UNVISITED_NODE_LIST.remove(self)
        VISITED_NODE_LIST.append(self)
        if(Topographer.PRESENCE_MAP[Poser.CURRENT_FLOOR][self.position_x][self.position_y] == 0 and 0 < Topographer.EDGE_WEIGHT_MAP[Poser.CURRENT_FLOOR][self.position_x][self.position_y] < 3):
            global SEARCH_DONE
            SEARCH_DONE = True
            self.backtrace_path()
        elif(self.position_x == 500 and self.position_y == 500):
            self.backtrace_path()
        for c in range(-1, 2):
            for r in range(-1, 2):
                if(EXISTENT_NODE_MAP[self.position_x+c][self.position_y+r] == 0 and Topographer.WALL_MAP[Poser.CURRENT_FLOOR][self.position_x+c][self.position_y+r] == 0 and Topographer.WALL_SPLASH_MAP[Poser.CURRENT_FLOOR][self.position_x+c][self.position_y+r] <= 0 and Topographer.LANDMARK_MAP[Poser.CURRENT_FLOOR][self.position_x+c][self.position_y+r] != 99):
                    node = Node(self.position_x+c, self.position_y+r, self)
                    UNVISITED_NODE_LIST.append(node)
    def backtrace_path(self):
        if round(self.euclidean_distance) <= 10:
            global ROBOT_ANGLE_ERROR
            ROBOT_ANGLE_ERROR = constrain(get_angle_error(Poser.ROBOT_COMPASS, Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, self.position_x, self.position_y), -90, 90)
        else:
            self.previous_node.backtrace_path()
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
                    

def plan_path():
    for x in VISITED_NODE_LIST:
        EXISTENT_NODE_MAP[x.position_x][x.position_y] = 0
        VISITED_NODE_LIST.remove(x)
        del x
    for x in UNVISITED_NODE_LIST:
        EXISTENT_NODE_MAP[x.position_x][x.position_y] = 0
        UNVISITED_NODE_LIST.remove(x)
        del x
    global SEARCH_DONE
    SEARCH_DONE = False
    startnode = Node(Poser.ROBOT_POSITION_X, Poser.ROBOT_POSITION_Y, None)
    UNVISITED_NODE_LIST.append(startnode)
    startnode.visit()
    while (not SEARCH_DONE) and (UNVISITED_NODE_LIST):
        UNVISITED_NODE_LIST.sort(key=operator.attrgetter('graph_distance'))
        UNVISITED_NODE_LIST[0].visit()
    if not UNVISITED_NODE_LIST:
        global MAZE_FINISHED
        MAZE_FINISHED = True
    else:
        global MAZE_FINISHED
        MAZE_FINISHED = False
