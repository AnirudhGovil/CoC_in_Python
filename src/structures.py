# parent class for all buildings
from random import seed
import colorama
import numpy as np

class Structure:
    def __init__(self, X, Y, sizeX, sizeY, health):
        self.alive = True
        self.location=[X,Y]
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.health = health
        self.maxHealth = health
    
    # returns the distance to a position as a float
    def distanceTo(self, x, y):
        distance = (self.location[0] + self.sizeX/2 - x)**2 + (self.location[1] + self.sizeY/2  - y)**2
        distance = distance ** 0.5
        
        return distance
    
    # checks if a position is adjacent to the structure                
    def isAdjacent(self, x, y):
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
    
    # checks if a position is inside a structure
    def isOverlapping(self, x, y):
        return x >= self.location[0] and x < self.location[0] + self.sizeX and y >= self.location[1] and y < self.location[1] + self.sizeY and self.alive
    
    # takes damage from a hit
    def takeDamage(self, damage):
        self.health -= damage
        
        if self.health <= 0:
            self.alive = False
        
class Townhall(Structure):
    def __init__(self, x, y):
        Structure.__init__(self, x, y, 4, 3, 800)
        self.type = 'T'
        
class Hut(Structure):
    def __init__(self, x, y):
        Structure.__init__(self, x, y, 2, 2, 400)
        self.type = 'H'
        
class Cannon(Structure):
    def __init__(self, x, y):
        Structure.__init__(self, x, y, 2, 2, 300)
        self.type = 'C'
        self.fired = False
        
        self.charge = 0
        self.shotCooldown = 3
        self.range = 8
        self.attack = 150
        
    def fire(self, army):
        # wait for the shot to cooldown
        if self.charge < self.shotCooldown:
            self.fired = False
            self.charge += 1
        else:
            # target the closest troop
            anyAlive = False
            for troop in army.troops:
                if troop.alive == True:
                    anyAlive = True
                    break
            
            # no troops on map
            if (len(army.troops) == 0 or anyAlive == False):
                if army.king.alive == True:
                    closest = army.king
                    minDist = army.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                else:
                    minDist = 10000 # hold fire
            # troops present
            else:
                for troop in army.troops:
                    if troop.alive == True:
                        closest = troop
                        minDist = troop.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                
                for troop in army.troops:
                    if troop.alive == True:
                        dist = troop.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                        if dist <= minDist:
                            closest = troop
                            minDist = dist
                            
                if army.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2) < minDist:
                    closest = army.king
                    minDist = army.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                
            # fire in range        
            if minDist <= self.range:
                self.fired = True
                closest.takeDamage(self.attack)
                self.charge = 0
            else:
                self.fired = False
            
        return
    
class Wall(Structure):
    def __init__(self, x, y):
        Structure.__init__(self, x, y, 1, 1, 400)
        self.type = 'W'
        
    def isOverlapping(self, x, y):
        return self.location[0] == x and self.location[1] == y
        
    
# class to store the state of the map
class Map:
    def __init__(self, x, y):
        # row first
        self.m = y
        self.n = x
        self.buildings = []
        self.walls = []
        
        self.numSpawnpoints = 3
        self.spawnpoints = []
        self.spawnpoints.append({"X": self.n-1, "Y": self.m-1})
        self.spawnpoints.append({"X": 0, "Y": self.m-1})
        self.spawnpoints.append({"X": self.n-1, "Y": 0})
    
    # draws the map onto the terminal    
    def draw(self, army):
        colorama.init()
        
        # first fill a m*n matrix, then draw over the empty tiles
        plan = np.full([self.m, self.n, 2], fill_value='E')
                
        for building in self.buildings:
            if building.alive == True:
                for i in range(building.sizeX):
                    for j in range(building.sizeY):
                        plan[building.location[1] + j][building.location[0] + i][0] = building.type
                        
                        if(isinstance(building, Cannon) and building.fired == True):
                            plan[building.location[1] + j][building.location[0] + i][0] = 'f' # + building.type # building has fired
                        
                        fraction = building.health/building.maxHealth
                        if fraction > 0.8:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'g'
                        elif fraction > 0.4:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'y'
                        else:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'r'
                    
        for wall in self.walls:
            if wall.alive == True:
                plan[wall.location[1]][wall.location[0]][0] = 'W'
                fraction = wall.health/wall.maxHealth
                if fraction > 0.5:
                    plan[wall.location[1]][wall.location[0]][1] = 'g'
                elif fraction > 0.2:
                    plan[wall.location[1]][wall.location[0]][1] = 'y'
                else:
                    plan[wall.location[1]][wall.location[0]][1] = 'r'
            
        for idx in range(self.numSpawnpoints):
            plan[self.spawnpoints[idx]["Y"]][self.spawnpoints[idx]["X"]][0] = 'S'
        
        
        for troop in army.troops:
            if troop.alive == True:
                plan[troop.location[1]][troop.location[0]][0] = troop.ID
                fraction = troop.HP/troop.maxHP
                if fraction > 0.5:
                    plan[troop.location[1]][troop.location[0]][1] = 'g'
                elif fraction > 0.2:
                    plan[troop.location[1]][troop.location[0]][1] = 'y'
                else:
                    plan[troop.location[1]][troop.location[0]][1] = 'r'
        
        plan[army.king.location[1]][army.king.location[0]][0] = 'K'
        if army.king.alive == True:
            plan[army.king.location[1]][army.king.location[0]][1] = 'w'
        else:
            plan[army.king.location[1]][army.king.location[0]][1] = 'bl'
                
        # scan plan for each building tile
        print("\033c")  # clear screen
        framebuffer = ''
        for i in range(self.m):
            for j in range(self.n):
                if plan[i][j][1] == 'E' or plan[i][j][1] == 'g':
                    framebuffer += '\033[32m'
                elif plan[i][j][1] == 'y':
                    framebuffer += '\033[33m'
                elif plan[i][j][1] == 'r':
                    framebuffer += '\033[31m'
                elif plan[i][j][1] == 'w':
                    framebuffer += '\033[38;5;15m'
                elif plan[i][j][1] == 'bl':
                    framebuffer += '\033[30m'
                
                if(plan[i][j][0] == 'E'):
                    framebuffer += '\033[38;2;0;35;84m' + '█'
                elif(plan[i][j][0] == 'T'):
                    framebuffer += '\033[48;5;178m' + 'T'
                elif(plan[i][j][0] == 'C'):
                    framebuffer += '\033[48;5;52m' + 'C'
                elif(plan[i][j][0] == 'H'):
                    framebuffer += '\033[48;5;136m' + 'H'
                elif(plan[i][j][0] == 'W'):
                    framebuffer += '\033[48;5;241m' + 'W'
                
                elif(plan[i][j][0] == 'f'):
                    framebuffer += '\033[48;5;230m' + 'C'
                
                elif(plan[i][j][0] == 'K'):
                    framebuffer += '\033[48;2;177;0;186m' + army.king.ID
                elif(plan[i][j][0] == 'S'):
                    framebuffer += '\033[48;2;100;100;100;31m' + 'S'
                elif(plan[i][j][0] == 'B'):
                    framebuffer += '\033[48;2;200;200;0m' + 'B'
                
                if(plan[i][j][0] == 'E'):
                    framebuffer += '█' + '\033[40m'
                else:
                    framebuffer += ' ' + '\033[40m'
            framebuffer += '\n'
        print(framebuffer, end='')
        
        # print the health bar
        print('\033[38;2;177;0;186m', end='')
        for i in range(int(army.king.HP/army.king.maxHP * self.n)):
            print('██', end='')
        print('\033[40m\033[0m')
        

    
    # x and y define the top left of the structure
    def addTownhall(self, x, y):
        t = Townhall(x,y)
        self.buildings.append(t)
        
    def addHut(self, x, y):
        h = Hut(x,y)
        self.buildings.append(h)
        
    def addCannon(self, x, y):
        c = Cannon(x,y)
        self.buildings.append(c)
    
    def addWall(self, x, y):
        w = Wall(x,y)
        self.walls.append(w)
    
    
    def fireDefenses(self, army):
        for building in self.buildings:
            if building.alive == True and isinstance(building, Cannon):
                building.fire(army)
    
    
    def registerHit(self, x, y, dmg):
        for building in self.buildings:
            if building.isOverlapping(x, y):
                building.takeDamage(dmg)
        
        for wall in self.walls:
            if wall.location[0] == x and wall.location[1] == y:
                wall.takeDamage(dmg)
                
    def checkWinLoss(self, Army):
        structureAlive = False
        troopAlive = False
        
        for building in self.buildings:
            if building.alive:
                structureAlive = True
        
        for troop in Army.troops:
            if troop.alive:
                troopAlive = True
                
        if structureAlive == False:
            return 1
        elif troopAlive == False and Army.king.alive == False and Army.spawnsLeft == 0:
            return -1
        else:
            return 0
    
    def setupMap(self):
        self.addTownhall(10,10)

        self.addCannon(7,12)
        self.addCannon(13,7)
        self.addCannon(13,14)

        self.addHut(7, 9)
        self.addHut(10,7)
        self.addHut(10,14)
        self.addHut(15,9)
        self.addHut(15,12)


        self.addWall(9,9)
        self.addWall(10,9)
        self.addWall(11,9)
        self.addWall(12,9)
        self.addWall(13,9)
        self.addWall(14,9)

        self.addWall(9,7)
        self.addWall(9,8)
        self.addWall(9,10)
        self.addWall(9,11)
        self.addWall(9,12)
        self.addWall(9,14)
        self.addWall(9,15)

        self.addWall(14,10)
        self.addWall(14,11)
        self.addWall(14,12)

        self.addWall(9,13)
        self.addWall(10,13)
        self.addWall(11,13)
        self.addWall(12,13)
        self.addWall(13,13)
        self.addWall(14,13)
        
        self.addWall(9,6)
        self.addWall(10,6)
        self.addWall(11,6)
        self.addWall(12,6)
        self.addWall(13,6)
        self.addWall(14,6)
        self.addWall(15,6)
        self.addWall(16,6)
        
        self.addWall(9,16)
        self.addWall(10,16)
        self.addWall(11,16)
        self.addWall(12,16)
        self.addWall(13,16)
        self.addWall(14,16)
        self.addWall(15,16)
        self.addWall(16,16)
        
        self.addWall(17,6)
        self.addWall(17,7)
        self.addWall(17,8)
        self.addWall(17,9)
        self.addWall(17,10)
        self.addWall(17,11)
        self.addWall(17,12)
        self.addWall(17,13)
        self.addWall(17,14)
        self.addWall(17,15)
        self.addWall(17,16)
        
        self.addWall(6,8)
        self.addWall(6,9)
        self.addWall(6,10)
        self.addWall(6,11)
        self.addWall(6,12)
        self.addWall(6,13)
        self.addWall(6,14)
        
        self.addWall(7,8)
        self.addWall(8,8)
        
        self.addWall(7,14)
        self.addWall(8,14)
        
