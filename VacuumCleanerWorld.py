CLEAN = 0
DIRTY = 1
WALL = 3

CCW = 0
CW = 1

NORTH = (0,1)
NORTHEAST = (1,1)
EAST = (1,0)
SOUTHEAST = (1,-1)
SOUTH = (0,-1)
SOUTHWEST = (-1,-1)
WEST = (-1,0)
NORTHWEST = (-1,1)

UP = NORTH
DOWN = SOUTH
LEFT = WEST
RIGHT = EAST

def RotateDirVec45Deg(dirVec,rotation):
    if rotation == CW:
        if dirVec == NORTH:
            return NORTHEAST
        elif dirVec == NORTHEAST:
            return EAST
        elif dirVec == EAST:
            return SOUTHEAST
        elif dirVec == SOUTHEAST:
            return SOUTH
        elif dirVec == SOUTH:
            return SOUTHWEST
        elif dirVec == SOUTHWEST:
            return WEST
        elif dirVec == WEST:
            return NORTHWEST
        elif dirVec == NORTHWEST:
            return NORTH

    elif rotation == CCW:
        if dirVec == NORTH:
            return NORTHWEST
        elif dirVec == NORTHWEST:
            return WEST
        elif dirVec == WEST:
            return SOUTHWEST
        elif dirVec == SOUTHWEST:
            return SOUTH
        elif dirVec == SOUTH:
            return SOUTHEAST
        elif dirVec == SOUTHEAST:
            return EAST
        elif dirVec == EAST:
            return NORTHEAST
        elif dirVec == NORTHEAST:
            return NORTH

def RotateDirVec90Deg(dirVec,rotation):
    return RotateDirVec45Deg(RotateDirVec45Deg(dirVec,rotation),rotation)

def RotateDirVec180Deg(dirVec,rotation):
    return RotateDirVec90Deg(RotateDirVec90Deg(dirVec,rotation),rotation)


class Environment:
    Grid = []
    Width = 0
    Height = 0
    NumCollisions = 0
    NumTurns = 0

    def __init__(self,width,height):
        self.Grid = []
        for x in range(width):
            newCol = []
            for y in range(height):
                newCol.append(CLEAN)
            self.Grid.append(newCol)

    def GetTile(self,x,y):
        return self.Grid[x][y]
    
    def SetTile(self,x,y,val):
        self.grid[x][y] = val

    def Collide(self,pos):
        self.NumTurns += 1
        if pos[0] >= self.Width or pos[1] >= self.Height:
            self.NumCollisions += 1
            return True
        elif self.GetTile(self,pos[0],pos[1]) == WALL:
            self.NumCollisions += 1
            return True
        else:
            return False

class Agent:
    Status = CLEAN
    FacingTile = CLEAN
    
    Position = (0,0)
    DirFacingVec = NORTH

    def __init__(self, startingPos, startingDir, environ):
        self.Position = startingPos 
        self.DirFacingVec = startingDir

    def GetPercept(self,environ):
        self.Status = environ.GetTile(self.Position[0],self.Position[1])
        self.FacingTile = environ.GetTile(self.Position[0] + self.DirFacingVec[0],self.Position[1] + self.DirFacingVec[1])

    def Rotate(self, dir):
        self.DirFacingVec = RotateDirVec45Deg(self.DirFacingVec,dir)

    def MoveForward(self,environ):
        if not environ.Collide(self.Position[0] + self.DirFacingVec[0],self.Position[1] + self.DirFacingVec[1]):
            self.Position = (self.Position[0] + self.DirFacingVec[0],self.Position[1] + self.DirFacingVec[1])


class SimpleReflexAgent(Agent):
    def __init__(self, startingPos, startingDir, environ):
        super().__init__(startingPos, startingDir, environ)


