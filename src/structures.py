# parent class for all buildings
from random import seed
from unittest import case
from colorama import Fore, Back, Style
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
            minDist = 999999 # hold fire
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
                minDist = 999999 # hold fire

        if Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2) < minDist:
            closest = Clan.king
            minDist = Clan.king.distanceTo(self.location[0] + self.sizeX/2, self.location[1] + self.sizeY/2)

    return closest,minDist
      
class Cannon(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 2, 2, maxHP, 'C')
        self.range = 8
        self.attack = 50
        self.fired=False
        
    def fire(self, clan):
        # reset canon colour
        self.fired=False
        closest,minDist=closest_helper(self,clan)
        # fire in range        
        if minDist <= self.range:
            closest.takeDamage(self.attack)
            self.fired=True
        
        return
    
class Wall(Structure):
    def __init__(self, x, y, maxHP):
        Structure.__init__(self, x, y, 1, 1, maxHP, 'W')

# class to store the map
class Map:
    def __init__(self, x, y):
        self.buildings = []
        self.walls = []
        # row first
        self.m = y
        self.n = x
        
    # draws the map on the terminal    
    def draw(self, clan):
        
        # first fill a m*n matrix, then draw over the empty tiles
        plan = np.full([self.m, self.n, 2], fill_value='0')

        plan[0][self.n-1][0]='S'
        plan[self.m-1][self.n-1][0]='S'
        plan[self.m-1][0][0]='S'
                
        for building in self.buildings:
            if building.alive: 
                for j in range(building.sizeY):
                    for i in range(building.sizeX):
                        plan[building.location[1] + i][building.location[0] + j][0] = building.ID
                        
                        if(isinstance(building, Cannon)):
                            if(building.fired == True):
                                plan[building.location[1] + i][building.location[0] + j][0] = 'f' # + building.type # building has fired

                        if building.HP/building.maxHP > 0.66:
                            plan[building.location[1] + i][building.location[0] + j][1] = 'g'
                        elif building.HP/building.maxHP > 0.33:
                            plan[building.location[1] + i][building.location[0] + j][1] = 'y'
                        else:
                            plan[building.location[1] + i][building.location[0] + j][1] = 'r'
                    
        for wall in self.walls:
            if wall.alive:
                plan[wall.location[1]][wall.location[0]][0] = 'W'
                if wall.HP/wall.maxHP > 0.66:
                    plan[wall.location[1]][wall.location[0]][1] = 'g'
                elif wall.HP/wall.maxHP > 0.33:
                    plan[wall.location[1]][wall.location[0]][1] = 'y'
                else:
                    plan[wall.location[1]][wall.location[0]][1] = 'r'
        
        
        for troop in clan.troops:
            if troop.alive:
                plan[troop.location[1]][troop.location[0]][0] = troop.ID
                if troop.HP/troop.maxHP > 0.66:
                    plan[troop.location[1]][troop.location[0]][1] = 'g'
                elif troop.HP/troop.maxHP > 0.33:
                    plan[troop.location[1]][troop.location[0]][1] = 'y'
                else:
                    plan[troop.location[1]][troop.location[0]][1] = 'r'
        

        plan[clan.king.location[1]][clan.king.location[0]][0] = 'K'
        if clan.king.alive:
            plan[clan.king.location[1]][clan.king.location[0]][1] = 'w'
        else:
            plan[clan.king.location[1]][clan.king.location[0]][1] = 'bl'
                
        print("\033c")  # clear screen
        fb = ''
        for i in range(self.m):
            for j in range(self.n):
                if  plan[i][j][1] == '0':
                    fb += Fore.BLACK + Style.DIM

                elif  plan[i][j][1] == 'g':
                    fb += Fore.GREEN + Style.BRIGHT

                elif plan[i][j][1] == 'y':
                    fb += Fore.YELLOW + Style.BRIGHT

                elif plan[i][j][1] == 'r':
                    fb += Fore.RED + Style.BRIGHT

                elif plan[i][j][1] == 'w':
                    fb += Fore.WHITE + Style.BRIGHT

                elif plan[i][j][1] == 'bl':
                    fb += Fore.BLACK + Style.DIM   

                if(plan[i][j][0] == '0'):
                    fb += Back.BLACK + '██' + Style.NORMAL

                elif(plan[i][j][0] == 'T'):
                    fb += Back.LIGHTRED_EX + 'T ' + Style.NORMAL

                elif(plan[i][j][0] == 'C'):
                    fb += Back.BLUE + 'C ' + Style.NORMAL

                elif(plan[i][j][0] == 'H'):
                    fb += Back.MAGENTA + 'H ' + Style.NORMAL

                elif(plan[i][j][0] == 'W'):
                    fb += Back.LIGHTBLACK_EX + 'W ' + Style.NORMAL
                
                elif(plan[i][j][0] == 'f'):
                    fb += Back.CYAN + 'C ' + Style.NORMAL
                
                elif(plan[i][j][0] == 'K' and clan.king.alive):
                    fb += Back.WHITE + Fore.BLACK + clan.king.ID + " " + Style.NORMAL

                elif(plan[i][j][0] == 'K' and clan.king.alive==False):
                    fb += Back.BLACK + '██' + Style.NORMAL

                elif(plan[i][j][0] == 'S'):
                    fb += Back.WHITE + 'S ' + Style.NORMAL

                elif(plan[i][j][0] == 'B'):
                    fb += Back.LIGHTWHITE_EX + 'B ' + Style.NORMAL

            fb += '\n'
        print(fb, end='')
        
        # print the HP bar
        print('\033[38;2;177;0;186m', end='')
        if (clan.king.HP <= 0):
            print("The king has died!", end= '')
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
            if isinstance(building, Cannon):
                if building.alive: 
                    building.fire(clan)
    
    
    def registerHit(self, x, y, dmg):
        for building in self.buildings:
            if building.isStruct(x, y):
                building.takeDamage(dmg)
        
        for wall in self.walls:
            if wall.isStruct(x,y):
                wall.takeDamage(dmg)
                
    def checkWinLoss(self, Clan):
        structureAlive = False
        troopAlive = False
        
        for building in self.buildings:
            if building.alive:
                structureAlive = True
        if structureAlive == False:
            return 1
        
        for troop in Clan.troops:
            if troop.alive:
                troopAlive = True
        if troopAlive == False and Clan.king.alive == False and Clan.spawnsLeft == 0:
            return -1
        else:
            return 0
    
    def setupMap(self):
        self.addTownhall(12,11,600)

        self.addHut(8,17,200)
        self.addHut(17,12,400)
        self.addHut(12,7,400)
        self.addHut(8,12,400)
        self.addHut(17,17,400)

        self.addCannon(8,7,200)
        self.addCannon(17,7,200)
        self.addCannon(12,17,400)

        self.addWall(6,5,300)
        self.addWall(7,5,300)
        self.addWall(8,5,300)
        self.addWall(9,5,300)
        self.addWall(10,5,300)
        self.addWall(11,5,300)
        self.addWall(12,5,300)
        self.addWall(13,5,300)
        self.addWall(14,5,300)
        self.addWall(15,5,300)
        self.addWall(16,5,300)
        self.addWall(17,5,300)
        self.addWall(18,5,300)
        self.addWall(19,5,300)
        self.addWall(20,5,300)

        self.addWall(20,6,300)
        self.addWall(20,7,300)
        self.addWall(20,8,300)
        self.addWall(20,9,300)
        self.addWall(20,10,300)
        self.addWall(20,11,300)
        self.addWall(20,12,300)
        self.addWall(20,13,300)
        self.addWall(20,14,300)
        self.addWall(20,15,300)
        self.addWall(20,16,300)
        self.addWall(20,17,300)
        self.addWall(20,18,300)
        self.addWall(20,19,300)

        self.addWall(6,20,300)
        self.addWall(7,20,300)
        self.addWall(8,20,300)
        self.addWall(9,20,300)
        self.addWall(10,20,300)
        self.addWall(11,20,300)
        self.addWall(12,20,300)
        self.addWall(13,20,300)
        self.addWall(14,20,300)
        self.addWall(15,20,300)
        self.addWall(16,20,300)
        self.addWall(17,20,300)
        self.addWall(18,20,300)
        self.addWall(19,20,300)
        self.addWall(20,20,300)
        
        self.addWall(6,6,300)
        self.addWall(6,7,300)
        self.addWall(6,8,300)
        self.addWall(6,9,300)
        self.addWall(6,10,300)
        self.addWall(6,11,300)
        self.addWall(6,12,300)
        self.addWall(6,13,300)
        self.addWall(6,14,300)
        self.addWall(6,15,300)
        self.addWall(6,16,300)
        self.addWall(6,17,300)
        self.addWall(6,18,300)
        self.addWall(6,19,300)
        self.addWall(6,20,300)

        self.addWall(11,10,200)
        self.addWall(12,10,200)
        self.addWall(13,10,200)
        self.addWall(14,10,200)
        self.addWall(15,10,200)

        self.addWall(15,11,200)
        self.addWall(15,12,200)
        self.addWall(15,13,200)
        self.addWall(15,14,200)
        self.addWall(15,15,200)

        self.addWall(11,15,200)
        self.addWall(12,15,200)
        self.addWall(13,15,200)
        self.addWall(14,15,200)
        self.addWall(15,15,200)

        self.addWall(11,11,200)
        self.addWall(11,12,200)
        self.addWall(11,13,200)
        self.addWall(11,14,200)
        self.addWall(11,15,200)
