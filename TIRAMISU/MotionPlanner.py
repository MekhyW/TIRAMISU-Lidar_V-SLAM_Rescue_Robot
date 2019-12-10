import Poser
import Topographer
import math
import operator
UnvisitedNodeList = []
VisitedNodeList = []
ExistentNodeMap = [[0]*1000]*1000
SearchDone = False

class Node:
    def __init__(self, PositionX, PositionY):
        ExistentNodeMap[PositionX][PositionY] = 1
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.PreviousNode = None
        self.UpdateGraphDist()
    def UpdateGraphDist(self):
        if(Topographer.WallMap[Poser.CurrentFloor][self.PositionX][self.PositionY]==1 or Topographer.WallSplashMap[Poser.CurrentFloor][self.PositionX][self.PositionY]>0 or Topographer.LandmarkMap[Poser.CurrentFloor][self.PositionX][self.PositionY]==99):
            self.GraphDistance = math.inf
        else:
            self.EuclideanDistance = math.sqrt(math.pow((self.PositionX - Poser.RobotPositionX), 2) + math.pow((self.PositionY - Poser.RobotPositionY), 2))
            self.GraphDistance = self.EuclideanDistance + Topographer.EdgeWeightMap[Poser.CurrentFloor][self.PositionX][self.PositionY]
    def Visit(self):
        UnvisitedNodeList.remove(self)
        VisitedNodeList.append(self)
        if(Topographer.PresenceMap[Poser.CurrentFloor][self.PositionX][self.PositionY]==0 and 0 < Topographer.EdgeWeightMap[Poser.CurrentFloor][self.PositionX][self.PositionY] < 3):
            SearchDone = True
        for c in range(-1, 2):
            for r in range(-1, 2):
                if(ExistentNodeMap[self.PositionX+c][self.PositionY+r]==0 and Topographer.WallMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]==0 and Topographer.WallSplashMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]<=0 and Topographer.LandmarkMap[Poser.CurrentFloor][self.PositionX+c][self.PositionY+r]!=99):
                    node = Node(self.PositionX+c, self.PositionY+r)
                    UnvisitedNodeList.append(node)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
                    

#still doesn´t output anything useful, just performs the iterations
def PlanPath():
    SearchDone = False
    if not UnvisitedNodeList:
        startnode = Node(Poser.RobotPositionX, Poser.RobotPositionY)
        UnvisitedNodeList.append(startnode)
        startnode.Visit()
    for x in UnvisitedNodeList:
        x.UpdateGraphDist()
        x.PreviousNode = None
    PreviousNode = None
    while(SearchDone == False and UnvisitedNodeList == True):
        UnvisitedNodeList.sort(key=operator.attrgetter('GraphDistance'))
        UnvisitedNodeList[0].PreviousNode = PreviousNode
        UnvisitedNodeList[0].Visit()
        PreviousNode = UnvisitedNodeList[0]
    for x in VisitedNodeList:
        UnvisitedNodeList.append(x)
    VisitedNodeList.clear()
