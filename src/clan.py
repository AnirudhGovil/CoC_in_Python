from math import *

from numpy import append

def distance(self, x, y):
        return ((self.location[0] - x)**2 + (self.location[1] - y)**2)** 0.5

class Troop:
    def __init__(self, maxHP, attack, speed, ID, aerial):
        self.ID = ID # symbol to be printed on screen
        self.location = [0,0] # X,Y
        self.attack = attack    # damage dealt per hit
        self.speed = speed    # measured in blocks per second
        self.alive = True     #flag to check if alive
        self.maxHP = maxHP
        self.HP = maxHP # current HP
        self.aerial = aerial

    def distanceTo(self, x, y):
        return ((self.location[0] - x)**2 + (self.location[1] - y)**2)** 0.5
    
    
    def takeDamage(self, dmg):
        if self.HP > 0:
            self.HP -= dmg
        else:
            self.alive = False
    
class King(Troop):
    def __init__(self, m, n):
        super().__init__(1000, 50, 1, 'K',False)
        self.lastMove = 'w'


    # checks if move is in range
    def validMove(self, x, y, Map):
        if x >= Map.n or y >= Map.m or x <=-1 or y<=-1:
            return 2

        for building in Map.buildings:
            if building.alive:
                if x >= building.location[0] and x < building.location[0] + building.sizeX and y >= building.location[1] and y < building.location[1] + building.sizeY:
                    return 3
        
        for wall in Map.walls:
            if wall.alive:
                if x == wall.location[0] and y == wall.location[1]:
                    return 3

        return 1

    # checks if move is colliding
    def collidingMove(self,x,y,Map):

        for building in Map.buildings:
            if building.alive:
                if x >= building.location[0] and x < building.location[0] + building.sizeX and y >= building.location[1] and y < building.location[1] + building.sizeY:
                    return 0
        
        for wall in Map.walls:
            if wall.alive:
                if x == wall.location[0] and y == wall.location[1]:
                    return 0
        
        return 1

    
    
    def move(self, command, Map):

        temp = 0

        # valid non-movement input
        if command == '1' or command == '2' or command == '3' or command == 'h' or command == 'j' or command == 'k' or command == 'q':
            return True

        if self.alive == True:

        # movement
            if command == 'w' and self.location[1] > 0:
                self.lastMove = 'w'
                self.ID = '^'
                temp = self.validMove(self.location[0], self.location[1] - self.speed, Map) * self.collidingMove(self.location[0], self.location[1] - 1, Map)
                if temp == 1:
                    self.location[1] -= self.speed
                elif temp == 2:
                    self.location[1] = 0
                elif temp == 3:
                    self.location[1] -= 1


            elif command == 'a' and self.location[0] > 0:
                self.lastMove = 'a'
                self.ID = '<'
                temp = self.validMove(self.location[0] - self.speed, self.location[1], Map) * self.collidingMove(self.location[0] - 1, self.location[1], Map)
                if temp == 1:
                    self.location[0] -= self.speed
                elif temp == 2:
                    self.location[0] = 0
                elif temp == 3:
                    self.location[0] -= 1


            elif command == 's' and self.location[1] < Map.m - 1:
                self.lastMove = 's'
                self.ID = 'v'
                temp = self.validMove(self.location[0], self.location[1] + self.speed, Map) * self.collidingMove(self.location[0], self.location[1] + 1, Map)
                if temp == 1:
                    self.location[1] += self.speed
                elif temp == 2:
                    self.location[1] = Map.m - 1
                elif temp == 3:
                    self.location[1] += 1



            elif command == 'd' and self.location[0] < Map.n - 1:
                self.lastMove = 'd'
                self.ID = '>'
                temp = self.validMove(self.location[0] + self.speed, self.location[1], Map) * self.collidingMove(self.location[0] + 1, self.location[1], Map)
                if temp == 1:
                    self.location[0] += self.speed
                elif temp == 2:
                    self.location[0] = Map.n - 1
                elif temp == 3:
                    self.location[0] += 1

            # attacking
            elif command == ' ':            
                if self.lastMove == 'w':
                    Map.registerHit(self.location[0], self.location[1] - 1, self.attack)
                elif self.lastMove == 'a':
                    Map.registerHit(self.location[0] - 1, self.location[1], self.attack)
                elif self.lastMove == 's':
                    Map.registerHit(self.location[0], self.location[1] + 1, self.attack)
                elif self.lastMove == 'd':
                    Map.registerHit(self.location[0] + 1, self.location[1], self.attack)

            elif command == 'x':            
                    Map.registerHit(self.location[0], self.location[1], self.attack/2)
                    Map.registerHit(self.location[0]+1, self.location[1], self.attack/2)
                    Map.registerHit(self.location[0]-1, self.location[1], self.attack/2)
                    Map.registerHit(self.location[0], self.location[1]+1, self.attack/2)
                    Map.registerHit(self.location[0], self.location[1]-1, self.attack/2)
                    Map.registerHit(self.location[0]+1, self.location[1]-1, self.attack/2)
                    Map.registerHit(self.location[0]-1, self.location[1]+1, self.attack/2)
                    Map.registerHit(self.location[0]+1, self.location[1]+1, self.attack/2)
                    Map.registerHit(self.location[0]-1, self.location[1]-1, self.attack/2)

                    Map.registerHit(self.location[0]+2, self.location[1], self.attack/2)
                    Map.registerHit(self.location[0]-2, self.location[1], self.attack/2)
                    Map.registerHit(self.location[0], self.location[1]+2, self.attack/2)
                    Map.registerHit(self.location[0], self.location[1]-2, self.attack/2)

                    Map.registerHit(self.location[0]+2, self.location[1]-2, self.attack/2)
                    Map.registerHit(self.location[0]-2, self.location[1]+2, self.attack/2)
                    Map.registerHit(self.location[0]+2, self.location[1]+2, self.attack/2)
                    Map.registerHit(self.location[0]-2, self.location[1]-2, self.attack/2)

                    Map.registerHit(self.location[0]+2, self.location[1]-1, self.attack/2)
                    Map.registerHit(self.location[0]-2, self.location[1]+1, self.attack/2)
                    Map.registerHit(self.location[0]+2, self.location[1]+1, self.attack/2)
                    Map.registerHit(self.location[0]-2, self.location[1]-1, self.attack/2)

                    Map.registerHit(self.location[0]+1, self.location[1]-2, self.attack/2)
                    Map.registerHit(self.location[0]-1, self.location[1]+2, self.attack/2)
                    Map.registerHit(self.location[0]+1, self.location[1]+2, self.attack/2)
                    Map.registerHit(self.location[0]-1, self.location[1]-2, self.attack/2)

            # no move occured
            else:
                return False
            
            # move occured
            return True
        
        # no move occured
        else:
            return False

class Queen(Troop):
    def __init__(self, m, n):
        super().__init__(1000, 10, 1, 'Q',False)
        self.lastMove = 'w'

    # checks if move is in range
    def validMove(self, x, y, Map):
        if x >= Map.n or y >= Map.m or x <=-1 or y<=-1:
            return 2

        for building in Map.buildings:
            if building.alive:
                if x >= building.location[0] and x < building.location[0] + building.sizeX and y >= building.location[1] and y < building.location[1] + building.sizeY:
                    return 3
        
        for wall in Map.walls:
            if wall.alive:
                if x == wall.location[0] and y == wall.location[1]:
                    return 3

        return 1

    # checks if move is colliding
    def collidingMove(self,x,y,Map):

        for building in Map.buildings:
            if building.alive:
                if x >= building.location[0] and x < building.location[0] + building.sizeX and y >= building.location[1] and y < building.location[1] + building.sizeY:
                    return 0
        
        for wall in Map.walls:
            if wall.alive:
                if x == wall.location[0] and y == wall.location[1]:
                    return 0
        
        return 1

    
    
    def move(self, command, Map):

        temp = 0

        # valid non-movement input
        if command == '1' or command == '2' or command == '3' or command == 'h' or command == 'j' or command == 'k' or command == 'q':
            return True

        if self.alive == True:

        # movement
            if command == 'w' and self.location[1] > 0:
                self.lastMove = 'w'
                self.ID = '^'
                temp = self.validMove(self.location[0], self.location[1] - self.speed, Map) * self.collidingMove(self.location[0], self.location[1] - 1, Map)
                if temp == 1:
                    self.location[1] -= self.speed
                elif temp == 2:
                    self.location[1] = 0
                elif temp == 3:
                    self.location[1] -= 1


            elif command == 'a' and self.location[0] > 0:
                self.lastMove = 'a'
                self.ID = '<'
                temp = self.validMove(self.location[0] - self.speed, self.location[1], Map) * self.collidingMove(self.location[0] - 1, self.location[1], Map)
                if temp == 1:
                    self.location[0] -= self.speed
                elif temp == 2:
                    self.location[0] = 0
                elif temp == 3:
                    self.location[0] -= 1


            elif command == 's' and self.location[1] < Map.m - 1:
                self.lastMove = 's'
                self.ID = 'v'
                temp = self.validMove(self.location[0], self.location[1] + self.speed, Map) * self.collidingMove(self.location[0], self.location[1] + 1, Map)
                if temp == 1:
                    self.location[1] += self.speed
                elif temp == 2:
                    self.location[1] = Map.m - 1
                elif temp == 3:
                    self.location[1] += 1



            elif command == 'd' and self.location[0] < Map.n - 1:
                self.lastMove = 'd'
                self.ID = '>'
                temp = self.validMove(self.location[0] + self.speed, self.location[1], Map) * self.collidingMove(self.location[0] + 1, self.location[1], Map)
                if temp == 1:
                    self.location[0] += self.speed
                elif temp == 2:
                    self.location[0] = Map.n - 1
                elif temp == 3:
                    self.location[0] += 1

            # attacking
            elif command == ' ':  
                centre=[]          
                if self.lastMove == 'w':
                    centre.append(self.location[0])
                    centre.append(self.location[1] - 8)
                elif self.lastMove == 'a':
                    centre.append(self.location[0] - 8)
                    centre.append(self.location[1])
                elif self.lastMove == 's':
                    centre.append(self.location[0])
                    centre.append(self.location[1] + 8)
                elif self.lastMove == 'd':
                    centre.append(self.location[0] + 8)
                    centre.append(self.location[1])
                for i in range(centre[0]-2,centre[0]+3):
                    for j in range(centre[1]-2,centre[1]+3):
                        Map.registerHit(i,j, self.attack)
            

            # no move occured
            else:
                return False
            
            # move occured
            return True
        
        # no move occured
        else:
            return False

#helps find closest buidling            
def closest_helper(self,Map):

    flag=0 
    closest=0
    for building in Map.buildings:
        if building.alive == True:
            if(flag==0):
                closest = building
                minDist = Map.buildings[0].distanceTo(self.location[0], self.location[1])
                flag=1
            dist = building.distanceTo(self.location[0], self.location[1])
            if dist <= minDist:
                closest = building
                minDist = dist
    return closest

# checks if a position is adjacent to the structure     
def adjacency_helper(self, x, y):           
    if ((x == self.location[0] + self.sizeX or x == self.location[0] -1)
        and
        (y <= self.location[1] + self.sizeY and y >= self.location[1] - 1)
        ):
        return True
    
    elif ((x <= self.location[0] + self.sizeX and x >= self.location[0] - 1)
        and
        (y == self.location[1] + self.sizeY or y == self.location[1] - 1)
        ):
        return True
    
    return False  

class Barbarian(Troop):
    
    def __init__(self, X, Y):
        super().__init__(300, 50, 1, 'B',False)
        self.location[0] = X
        self.location[1] = Y
           
    
    
    def move(self, Map):
       
        if self.alive == True:
            
            # find closest structure
            closest = closest_helper(self,Map)

            if(closest):
                
                # attack it
                if adjacency_helper(closest,self.location[0], self.location[1]) and closest.alive:
                    closest.takeDamage(self.attack)

                # move otherwise
                else:
                    xMove = 0
                    yMove = 0
                    if closest.location[0] + closest.sizeX/2 > self.location[0]: 
                        if closest.isStruct(self.location[0] + self.speed, self.location[1]):
                            xMove += ceil(self.speed/2)
                        else:
                            xMove += self.speed
                    elif closest.location[0] + closest.sizeX/2 < self.location[0]:
                        if closest.isStruct(self.location[0] - self.speed, self.location[1]):
                            xMove -= ceil(self.speed/2)
                        else:
                            xMove -= self.speed

                    if closest.location[1] + closest.sizeY/2 > self.location[1]:
                        if closest.isStruct(self.location[0], self.location[1]+self.speed):
                            yMove += ceil(self.speed/2)
                        else:
                            yMove += self.speed
                    elif closest.location[1] + closest.sizeY/2 < self.location[1]:
                        if closest.isStruct(self.location[0], self.location[1]- self.speed):
                            yMove -= ceil(self.speed/2)
                        else:
                            yMove -= self.speed
                    
                    # check if wall is blocking, and attack it 
                    for wall in Map.walls:
                        if (wall.alive == True):
                            if wall.isStruct(self.location[0] + xMove, self.location[1] + yMove) or wall.isStruct(self.location[0] + ceil(xMove/2), self.location[1] + ceil(yMove/2)):
                                wall.takeDamage(self.attack)
                                return

                    self.location[0] += xMove
                    self.location[1] += yMove            

        return

# checks if a position is adjacent to the structure     
def range_helper_archer(self, x, y):           
    
    if distance(self,x,y) <= 7 or distance(self,x-self.sizeX,y) <=7 or distance(self,x,y-self.sizeY) <=7 or distance(self,x-self.sizeX,y-self.sizeY) <=7 :
        return True

    return False  

class Archer(Troop):
    
    def __init__(self, X, Y):
        super().__init__(150, 25, 2, 'A',False)
        self.location[0] = X
        self.location[1] = Y
    
    
    def move(self, Map):
       
        if self.alive == True:
            
            # find closest structure
            closest = closest_helper(self,Map)

            if(closest):

                must_destroy_wall=True
                
                # attack it
                if range_helper_archer(closest,self.location[0], self.location[1]) and closest.alive:
                    must_destroy_wall=False
                    closest.takeDamage(self.attack)

                # move otherwise
                else:
                    xMove = 0
                    yMove = 0
                    if closest.location[0] + closest.sizeX/2 > self.location[0]: 
                        if closest.isStruct(self.location[0] + self.speed, self.location[1]) or closest.isStruct(self.location[0] + self.speed-1, self.location[1]):
                            xMove += ceil(self.speed/2)
                        else:
                            xMove += self.speed
                    elif closest.location[0] + closest.sizeX/2 < self.location[0]:
                        if closest.isStruct(self.location[0] - self.speed, self.location[1]) or closest.isStruct(self.location[0] - self.speed+1, self.location[1]):
                            xMove -= ceil(self.speed/2)
                        else:
                            xMove -= self.speed
                    if closest.location[1] + closest.sizeY/2 > self.location[1]:
                        if closest.isStruct(self.location[0], self.location[1]+self.speed) or closest.isStruct(self.location[0], self.location[1]+self.speed-1):
                            yMove += ceil(self.speed/2)
                        else:
                            yMove += self.speed
                    elif closest.location[1] + closest.sizeY/2 < self.location[1]:
                        if closest.isStruct(self.location[0], self.location[1]- self.speed) or closest.isStruct(self.location[0], self.location[1]- self.speed +1):
                            yMove -= ceil(self.speed/2)
                        else:
                            yMove -= self.speed

                    # check if wall is blocking, and attack it 
                    for wall in Map.walls:
                        if (wall.alive == True):
                            if wall.isStruct(self.location[0] + xMove, self.location[1] + yMove) or wall.isStruct(self.location[0] + ceil(xMove/2), self.location[1] + ceil(yMove/2)) or wall.isStruct(self.location[0] + ceil(xMove/2) + ceil(xMove/4), self.location[1] + ceil(yMove/2) + ceil(yMove/4)):
                                wall.takeDamage(self.attack)
                                return
                    self.location[0] += xMove
                    self.location[1] += yMove             

        return

#helps find closest buidling            
def closest_helper_balloon(self,Map):

    flag=0 
    closest=0
    for building in Map.buildings:
        if building.ID=='C' or building.ID=='Z':
            if building.alive == True:
                if(flag==0):
                    closest = building
                    minDist = Map.buildings[0].distanceTo(self.location[0], self.location[1])
                    flag=1
                dist = building.distanceTo(self.location[0], self.location[1])
                if dist <= minDist:
                    closest = building
                    minDist = dist
    if closest == 0:
        for building in Map.buildings:
            if building.alive == True:
                if(flag==0):
                    closest = building
                    minDist = Map.buildings[0].distanceTo(self.location[0], self.location[1])
                    flag=1
                dist = building.distanceTo(self.location[0], self.location[1])
                if dist <= minDist:
                    closest = building
                    minDist = dist
    return closest

# checks if a position is adjacent to the structure     
def range_helper_balloon(self, x, y):           
    
    if distance(self,x,y) <= 2 or distance(self,-self.sizeX,y) <=2 or distance(self,x,y-self.sizeY) <=2 or distance(self,x-self.sizeX,y-self.sizeY) <=2 :
        return True

    return False  

class Balloon(Troop):
    
    def __init__(self, X, Y):
        super().__init__(300, 100, 2, 'L',True)
        self.location[0] = X
        self.location[1] = Y
           
    
    
    def move(self, Map):
       
        if self.alive == True:
            
            # find closest structure
            closest = closest_helper_balloon(self,Map)

            if(closest):
                
                # attack it
                if range_helper_balloon(closest,self.location[0], self.location[1]) and closest.alive:
                    closest.takeDamage(self.attack)
                    
                # move otherwise
                else:
                    xMove = 0
                    yMove = 0
                    if closest.location[0] + closest.sizeX >= self.location[0] + self.speed:  
                            xMove += self.speed
                    elif closest.location[0] + closest.sizeX <= self.location[0] - self.speed:
                            xMove -= self.speed
                    if closest.location[1] + closest.sizeY >= self.location[1] + self.speed:
                            yMove += self.speed
                    elif closest.location[1] + closest.sizeY <= self.location[1] - self.speed:
                            yMove -= self.speed
                    

                    self.location[0] += xMove
                    self.location[1] += yMove    
            else:
                return        

        return
                
class Clan:
    def __init__(self, m, n, b,a,l, h_uses, j_uses,leader):
        if leader==1:
            self.king = King(m, n)
        if leader==2:
            self.king = Queen(m,n)
        self.troops = []
        self.barbarianSpawnsLeft = b
        self.archerSpawnsLeft = a
        self.balloonSpawnsLeft = l
        self.healSpell = h_uses
        self.rageSpell = j_uses
        
    def spawn(self, location, Map):
        # location can be either 1 2 or 3
        if self.barbarianSpawnsLeft > 0:
            if(location=='1'):
                self.troops.append(Barbarian(0,Map.m-1))
                self.barbarianSpawnsLeft -= 1
                return 1
            elif(location=='2'):
                self.troops.append(Barbarian(Map.n-1,Map.m-1))
                self.barbarianSpawnsLeft -= 1
                return 1
            elif(location=='3'):
                self.troops.append(Barbarian(Map.n-1,0))
                self.barbarianSpawnsLeft -= 1
                return 1
            

        if self.archerSpawnsLeft > 0:
            if(location=='4'):
                self.troops.append(Archer(0,Map.m-1))
                self.archerSpawnsLeft -= 1
                return 1
            elif(location=='5'):
                self.troops.append(Archer(Map.n-1,Map.m-1))
                self.archerSpawnsLeft -= 1
                return 1
            elif(location=='6'):
                self.troops.append(Archer(Map.n-1,0))
                self.archerSpawnsLeft -= 1
                return 1
            
                
        if self.balloonSpawnsLeft > 0:
            if(location=='7'):
                self.troops.append(Balloon(0,Map.m-1))
                self.balloonSpawnsLeft -= 1
                return 1
            elif(location=='8'):
                self.troops.append(Balloon(Map.n-1,Map.m-1))
                self.balloonSpawnsLeft -= 1
                return 1
            elif(location=='9'):
                self.troops.append(Balloon(Map.n-1,0))
                self.balloonSpawnsLeft -= 1
                return 1

        else:
            return 0
    
    def useHealSpell(self):
        if self.healSpell > 0:
            self.healSpell -= 1
            for troop in self.troops:
                if troop.alive == True:
                    troop.HP = min(troop.maxHP, int(troop.HP * 1.5))
            if self.king.alive == True:
                self.king.HP = min(self.king.maxHP, int(self.king.HP * 1.5))
            return 1

        else:
            return 0
            

    def useRageSpell(self):
        if self.rageSpell > 0:
            self.rageSpell -= 1
            for troop in self.troops:
                if troop.alive == True:
                    troop.attack = troop.attack * 2
                    troop.speed = troop.speed * 2
            if self.king.alive == True:
                self.king.attack = self.king.attack * 2
                self.king.speed = self.king.speed * 2
            
            return 1

        else:
            return 0
            
    
    def moveTroops(self, Map):
        for troop in self.troops:
            troop.move(Map)