CLEAN = 0
DIRTY = 1

CCW = 0
CW = 1

class Environment:
    Grid = []
    Width = 0
    Height = 0
    NumCollisions = 0

    def __init__(self,width,height):
        self.Grid = []
        for x in range(width):
            newCol = []
            for y in range(height):
                newCol.append(CLEAN)
            self.Grid.append(newCol)

    def GetDirty(self,x,y):
        return self.Grid[x][y] == DIRTY
    
    def SetDirty(self,x,y,isDirty):
        self.grid[x][y] = isDirty

class Agent:
    Status = CLEAN
    FacingDirty = CLEAN
    Position = (0,0)
    DirFacingVec = (1,0)

    def __init__(self, startingPos, startingDir, environ):
        self.Position = startingPos 
        self.DirFacingVec = startingDir

    def GetPercept(self,environ):
        if environ.GetDirty(Position[0] + DirFacingVec[0],Position[1] + Position[1]):
            FacingDirty = DIRTY


class SimpleReflexAgent(Agent):
    def __init__(self, startingPos, startingDir, environ):
        super().__init__(startingPos, startingDir, environ)


