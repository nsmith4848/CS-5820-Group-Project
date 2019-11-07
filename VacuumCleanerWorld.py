import random

CLEAN = 0
DIRTY = 1
WALL = 2

CCW = 0
CW = 1

NORTH = (0,-1)
NORTHEAST = (1,-1)
EAST = (1,0)
SOUTHEAST = (1,1)
SOUTH = (0,1)
SOUTHWEST = (-1,1)
WEST = (-1,0)
NORTHWEST = (-1,-1)

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

print_rotations = False

class Environment:
    Grid = []
    Width = 0
    Height = 0
    NumCollisions = 0
    NumTurns = 0
    InitialDirtyAmount = 0

    def __init__(self,width,height):
        self.Width = width
        self.Height = height
        self.Grid = []
        for x in range(width):
            newCol = []
            for y in range(height):
                newCol.append(CLEAN)
            self.Grid.append(newCol)

    def GetTile(self,x,y):
        if x >= self.Width or y >= self.Height or x < 0 or y < 0:
            return WALL
        else:
            return self.Grid[x][y]
    
    def SetTile(self,x,y,val):
        self.Grid[x][y] = val

    def Collide(self,pos):
        self.NumTurns += 1
        if pos[0] >= self.Width or pos[1] >= self.Height:
            self.NumCollisions += 1
            return True
        elif self.GetTile(pos[0],pos[1]) == WALL:
            self.NumCollisions += 1
            return True
        else:
            return False

    def CountDirty(self):
        numDirty = 0
        for x in range(self.Width):
            for y in range(self.Height):
                if self.GetTile(x,y) == DIRTY:
                    numDirty += 1
        return numDirty

    def GetPercentClean(self):
        return (1-(self.CountDirty()/self.InitialDirtyAmount)) * 100

    def RandomizeWithoutWalls(self):
        for x in range(self.Width):
            for y in range(self.Height):
                self.SetTile(x,y,random.randint(CLEAN,DIRTY))
        self.InitialDirtyAmount = self.CountDirty()

    def RandomizeWithWalls(self):
        for x in range(self.Width):
            for y in range(self.Height):
                self.SetTile(x,y,random.randint(CLEAN,WALL))
        self.InitialDirtyAmount = self.CountDirty()
    
    

    def Visualize(self):
        print("visualizing w:{}, h:{}".format(self.Width,self.Height))
        for y in range (self.Height):
            for x in range (self.Width):
                print("[{}] ".format(self.GetTile(x,y)),end="")
            print("")
        print("Collisions: {}, Steps: {}, Percent Cleaned: {}%".format(self.NumCollisions, self.NumTurns,self.GetPercentClean()))
        return

class Agent:
    Status = CLEAN
    FacingTile = CLEAN
    
    Position = (0,0)
    DirFacingVec = NORTH
    Environ = Environment(2,1)

    def __init__(self, startingPos, startingDir, environ):
        self.Position = startingPos 
        self.DirFacingVec = startingDir
        self.Environ = environ

    def GetPercept(self):
        self.Status = self.Environ.GetTile(x=self.Position[0],y=self.Position[1])
        self.FacingTile = self.Environ.GetTile(self.Position[0] + self.DirFacingVec[0],self.Position[1] + self.DirFacingVec[1])

    def Rotate(self, dir):
        self.DirFacingVec = RotateDirVec45Deg(self.DirFacingVec,dir)

        if print_rotations:
            if dir == CW:
                print("agent rotated 45 degrees clockwise")
            elif dir == CCW:
                print("agent rotated 45 degrees counterclockwise")
            print("agent direction: x:{} y:{}".format(self.DirFacingVec[0],self.DirFacingVec[1]))

    def MoveForward(self):
        newX = self.Position[0] + self.DirFacingVec[0]
        newY = self.Position[1] + self.DirFacingVec[1]
        if not self.Environ.Collide((newX,newY)):
            self.Position = (self.Position[0] + self.DirFacingVec[0],self.Position[1] + self.DirFacingVec[1])
            print("agent position: x:{} y:{}".format(self.Position[0],self.Position[1]))
            return True
        else:
            print("agent collided")
            return False
    
    def CleanTile(self):
        self.Environ.SetTile(self.Position[0],self.Position[1],CLEAN)
        return

    def Run(self):
        return


class SimpleReflexAgent(Agent):
    def __init__(self, startingPos, startingDir, environ):
        super().__init__(startingPos, startingDir, environ)

    def Run(self):
        running = True
        print("agent starting position: x:{} y:{}".format(self.Position[0],self.Position[1]))
        print("agent starting direction: x:{} y:{}".format(self.DirFacingVec[0],self.DirFacingVec[1]))
        while running:
            
            self.GetPercept()

            if self.Status == DIRTY:
                self.CleanTile()

            if self.FacingTile == DIRTY:
                self.MoveForward()
            else:
                self.Rotate(CW) #45 deg
                
                self.GetPercept()
                if self.FacingTile == DIRTY:
                    self.MoveForward()
                else:
                    self.Rotate(CW) #90 deg
                    self.GetPercept()
                    if self.FacingTile == DIRTY:
                        self.MoveForward()
                    else:
                        self.Rotate(CW) #135 deg
                        self.GetPercept()
                        if self.FacingTile == DIRTY:
                            self.MoveForward()
                        else:
                            self.Rotate(CW) #180 deg
                            self.GetPercept()
                            if self.FacingTile == DIRTY:
                                self.MoveForward()
                            else:
                                self.Rotate(CW) #225 deg
                                self.GetPercept()
                                if self.FacingTile == DIRTY:
                                    self.MoveForward()
                                else:
                                    self.Rotate(CW) #270 deg
                                    self.GetPercept()
                                    if self.FacingTile == DIRTY:
                                        self.MoveForward()
                                    else:
                                        self.Rotate(CW) #315 deg
                                        self.GetPercept()
                                        if self.FacingTile == DIRTY:
                                            self.MoveForward()
                                        else:
                                            running = False
        
        return

class ZigZagVacuum(Agent):
    def __init__(self, startingPos, startingDir, environ):
        super().__init__(startingPos, startingDir, environ)

    def Run(self):
        steps = 0
        running = True
        print("agent starting position: x:{} y:{}".format(self.Position[0],self.Position[1]))
        print("agent starting direction: x:{} y:{}".format(self.DirFacingVec[0],self.DirFacingVec[1]))
        while running and steps < 100:
            steps += 1
            self.GetPercept() # >
            if self.Status == DIRTY:
                self.CleanTile()
            if self.FacingTile == WALL: # >
                rotationDir = CW
                if self.DirFacingVec == WEST: 
                    rotationDir = CCW
               
                self.Rotate(rotationDir)
                self.Rotate(rotationDir) # V
                
                self.GetPercept()

                if self.FacingTile == WALL:
                    running = False
                    
                else:
                    self.MoveForward()
                    self.Rotate(rotationDir) 
                    self.Rotate(rotationDir) # <
            else:
                self.MoveForward()





def main():
    vacuumWorld = Environment(10,10)
    vacuumWorld.RandomizeWithoutWalls()
    
    vacuumWorld.Visualize()
    print("")
    reflexAgent = SimpleReflexAgent((0,0),EAST,vacuumWorld)
    reflexAgent.Run()

    print("")
    vacuumWorld.Visualize()

    print("done")

if __name__ == "__main__":
    main()

