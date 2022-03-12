# parent class for all buildings
from random import seed
import colorama
import numpy as np
from sympy import false

class Structure:
    def __init__(self, X, Y, sizeX, sizeY, maxHP, ID):
        self.ID = ID # symbol to be printed on screen
        self.sizeX=sizeX #length
        self.sizeY=sizeY #breadth
        self.location = [X,Y] # X,Y
        self.alive = True     #flag to check if alive
        self.maxHP = maxHP
        self.HP = maxHP # current HP
    
    # checks if a position is inside a structure
    def isStruct(self, x, y):
        if self.alive:
            return self.location[0] <= x < self.location[0] + self.sizeX and self.location[1] <= y < self.location[1] + self.sizeY
        else:
            return False
    
    # returns the distance to a position as a float
    def distanceTo(self, x, y):
        return ((self.location[0] - x)**2 + (self.location[1] - y)**2)** 0.5
   
    # takes damage from a hit
    def takeDamage(self, dmg):
        if self.HP > 0:
            self.HP -= dmg
        else:
            self.alive = False
        
class Townhall(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 4, 3, maxHP, 'T')
        
class Hut(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 2, 2, maxHP, 'H')

def closest_helper(self,Clan):

    # no troops on map
    if(len(Clan.troops) == 0):
        if Clan.king.alive == True:
            closest = Clan.king
            minDist = Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
        else:
            closest=0
            minDist = 10000 # hold fire
    else:
        allELiminated=True # flag for checking if there are any troops
        flag=0 
        closest=0
        for troop in Clan.troops:
            if troop.alive == True:
                allELiminated=False
                if(flag==0):
                    closest = troop
                    minDist = Clan.troops[0].distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                    flag=1
                dist = troop.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
                if dist <= minDist:
                    closest = troop
                    minDist = dist

        if(allELiminated):
            if Clan.king.alive == True:
                closest = Clan.king
                minDist = Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
            else:
                closest=0
                minDist = 10000 # hold fire

        if Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2) < minDist:
            closest = Clan.king
            minDist = Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)

    return closest,minDist
      
class Cannon(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 2, 2, maxHP, 'C')
        self.range = 8
        self.attack = 150
        self.fired=False
        
    def fire(self, clan):
        # wait for the shot to cooldown
        self.fired=False

        #anyAlive = False
        #for troop in clan.troops:
        #    if troop.alive == True:
        #        anyAlive = True
        #        break
        #
        ## no troops on map
        #if (len(clan.troops) == 0 or anyAlive == False):
        #    if clan.king.alive == True:
        #        closest = clan.king
        #        minDist = clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
        #    else:
        #        minDist = 10000 # hold fire
#
        ## troops present
        #else:
        #    for troop in clan.troops:
        #        if troop.alive == True:
        #            closest = troop
        #            minDist = troop.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
        #    
        #    for troop in clan.troops:
        #        if troop.alive == True:
        #            dist = troop.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
        #            if dist <= minDist:
        #                closest = troop
        #                minDist = dist
        #                
        #    if clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2) < minDist:
        #        closest = clan.king
        #        minDist = clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)
        #    

        closest,minDist=closest_helper(self,clan)
        # fire in range        
        if minDist <= self.range:
            closest.takeDamage(self.attack)
            self.fired=True
        
        return
    
class Wall(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 1, 1, maxHP, 'W')
    
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
    def draw(self, clan):
        colorama.init()
        
        # first fill a m*n matrix, then draw over the empty tiles
        plan = np.full([self.m, self.n, 2], fill_value='E')
                
        for building in self.buildings:
            if building.alive == True:
                for i in range(building.sizeX):
                    for j in range(building.sizeY):
                        plan[building.location[1] + j][building.location[0] + i][0] = building.ID
                        
                        if(isinstance(building, Cannon) and building.fired == True):
                            plan[building.location[1] + j][building.location[0] + i][0] = 'f' # + building.type # building has fired
                        
                        fraction = building.HP/building.maxHP
                        if fraction > 0.8:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'g'
                        elif fraction > 0.4:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'y'
                        else:
                            plan[building.location[1] + j][building.location[0] + i][1] = 'r'
                    
        for wall in self.walls:
            if wall.alive == True:
                plan[wall.location[1]][wall.location[0]][0] = 'W'
                fraction = wall.HP/wall.maxHP
                if fraction > 0.5:
                    plan[wall.location[1]][wall.location[0]][1] = 'g'
                elif fraction > 0.2:
                    plan[wall.location[1]][wall.location[0]][1] = 'y'
                else:
                    plan[wall.location[1]][wall.location[0]][1] = 'r'
            
        for idx in range(self.numSpawnpoints):
            plan[self.spawnpoints[idx]["Y"]][self.spawnpoints[idx]["X"]][0] = 'S'
        
        
        for troop in clan.troops:
            if troop.alive == True:
                plan[troop.location[1]][troop.location[0]][0] = troop.ID
                fraction = troop.HP/troop.maxHP
                if fraction > 0.5:
                    plan[troop.location[1]][troop.location[0]][1] = 'g'
                elif fraction > 0.2:
                    plan[troop.location[1]][troop.location[0]][1] = 'y'
                else:
                    plan[troop.location[1]][troop.location[0]][1] = 'r'
        
        plan[clan.king.location[1]][clan.king.location[0]][0] = 'K'
        if clan.king.alive == True:
            plan[clan.king.location[1]][clan.king.location[0]][1] = 'w'
        else:
            plan[clan.king.location[1]][clan.king.location[0]][1] = 'bl'
                
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
                    framebuffer += '\033[48;2;177;0;186m' + clan.king.ID
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
        
        # print the HP bar
        print('\033[38;2;177;0;186m', end='')
        for i in range(int(clan.king.HP/clan.king.maxHP * self.n)):
            print('██', end='')
        print('\033[40m\033[0m')
        

    
    # x and y define the top left of the structure
    def addTownhall(self, x, y, maxHP):
        t = Townhall(x,y,maxHP)
        self.buildings.append(t)
        
    def addHut(self, x, y,maxHP):
        h = Hut(x,y,maxHP)
        self.buildings.append(h)
        
    def addCannon(self, x, y,maxHP):
        c = Cannon(x,y,maxHP)
        self.buildings.append(c)
    
    def addWall(self, x, y,maxHP):
        w = Wall(x,y,maxHP)
        self.walls.append(w)
    
    
    def fireDefenses(self, clan):
        for building in self.buildings:
            if building.alive == True and isinstance(building, Cannon):
                building.fire(clan)
    
    
    def registerHit(self, x, y, dmg):
        for building in self.buildings:
            if building.isStruct(x, y):
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
        self.addTownhall(10,10,800)

        self.addCannon(7,12,300)
        self.addCannon(13,7,300)
        self.addCannon(13,14,300)

        self.addHut(7, 9,400)
        self.addHut(10,7,400)
        self.addHut(10,14,400)
        self.addHut(15,9,400)
        self.addHut(15,12,400)


        self.addWall(9,9,400)
        self.addWall(10,9,400)
        self.addWall(11,9,400)
        self.addWall(12,9,400)
        self.addWall(13,9,400)
        self.addWall(14,9,400)

        self.addWall(9,7,400)
        self.addWall(9,8,400)
        self.addWall(9,10,400)
        self.addWall(9,11,400)
        self.addWall(9,12,400)
        self.addWall(9,14,400)
        self.addWall(9,15,400)

        self.addWall(14,10,400)
        self.addWall(14,11,400)
        self.addWall(14,12,400)

        self.addWall(9,13,400)
        self.addWall(10,13,400)
        self.addWall(11,13,400)
        self.addWall(12,13,400)
        self.addWall(13,13,400)
        self.addWall(14,13,400)
        
        self.addWall(9,6,400)
        self.addWall(10,6,400)
        self.addWall(11,6,400)
        self.addWall(12,6,400)
        self.addWall(13,6,400)
        self.addWall(14,6,400)
        self.addWall(15,6,400)
        self.addWall(16,6,400)
        
        self.addWall(9,16,400)
        self.addWall(10,16,400)
        self.addWall(11,16,400)
        self.addWall(12,16,400)
        self.addWall(13,16,400)
        self.addWall(14,16,400)
        self.addWall(15,16,400)
        self.addWall(16,16,400)
        
        self.addWall(17,6,400)
        self.addWall(17,7,400)
        self.addWall(17,8,400)
        self.addWall(17,9,400)
        self.addWall(17,10,400)
        self.addWall(17,11,400)
        self.addWall(17,12,400)
        self.addWall(17,13,400)
        self.addWall(17,14,400)
        self.addWall(17,15,400)
        self.addWall(17,16,400)
        
        self.addWall(6,8,400)
        self.addWall(6,9,400)
        self.addWall(6,10,400)
        self.addWall(6,11,400)
        self.addWall(6,12,400)
        self.addWall(6,13,400)
        self.addWall(6,14,400)
        
        self.addWall(7,8,400)
        self.addWall(8,8,400)
        
        self.addWall(7,14,400)
        self.addWall(8,14,400)
        
