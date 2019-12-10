import Poser
import Topographer
import math
import operator
UnvisitedNodeList = []
VisitedNodeList = []
ExistentNodeMap = [[0]*1000]*1000
SearchDone = False

class Node:
    def __init__(self, PositionX, PositionY, PreviousNode):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.PreviousNode = PreviousNode
        self.EuclideanDistance = math.sqrt(math.pow((self.PositionX - Poser.RobotPositionX), 2) + math.pow((self.PositionY - Poser.RobotPositionY), 2))
        self.GraphDistance = self.EuclideanDistance + Topographer.EdgeWeightMap[Poser.CurrentFloor][self.PositionX][self.PositionY]
        ExistentNodeMap[self.PositionX][self.PositionY] = 1
    def Visit(self):
        UnvisitedNodeList.remove(self)
        VisitedNodeList.append(self)
        if(Topographer.PresenceMap[Poser.CurrentFloor][self.PositionX][self.PositionY]==0 and 0 < Topographer.EdgeWeightMap[Poser.CurrentFloor][self.PositionX][self.PositionY] < 3):
            SearchDone = True
        for c in range(-1, 2):
            for r in range(-1, 2):
                if(ExistentNodeMap[self.PositionX+c][self.PositionY+r]==0 and Topographer.WallMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]==0 and Topographer.WallSplashMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]<=0 and Topographer.LandmarkMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]!=99):
                    node = Node(self.PositionX+c, self.PositionY+r, self)
                    UnvisitedNodeList.append(node)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
                    

def PlanPath():
    SearchDone = False
    startnode = Node(Poser.RobotPositionX, Poser.RobotPositionY, None)
    UnvisitedNodeList.append(startnode)
    startnode.Visit()
    while(SearchDone == False and UnvisitedNodeList == True):
        UnvisitedNodeList.sort(key=operator.attrgetter('GraphDistance'))
        UnvisitedNodeList[0].Visit()
    #backtrace path to obtain target angle
    for x in VisitedNodeList:
        ExistentNodeMap[x.PositionX][x.PositionY] = 0
        VisitedNodeList.remove(x)
        del x
    for x in UnvisitedNodeList:
        ExistentNodeMap[x.PositionX][x.PositionY] = 0
        UnvisitedNodeList.remove(x)
        del x