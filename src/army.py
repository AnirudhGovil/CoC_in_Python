class Army:
    def __init__(self, m, n):
        self.king = King(m, n)
        self.units = []
        self.spawnsLeft = 10
        self.healSpell = HealSpell()
        self.rageSpell = RageSpell()
        
        self.raging = False
        self.rageTimer = 0
        
    def spawnBarbarian(self, inputChar, Map):
        # either 1 2 or 3
        idx = int(inputChar) - 1
        if self.spawnsLeft > 0:
            self.units.append(Barbarian(Map.spawnpoints[idx]["posX"], Map.spawnpoints[idx]["posY"]))
            self.spawnsLeft -= 1
            return 0
    
        return 1
    
    def useSpell(self, command):
        if command == 'j':
            return self.healSpell.use(self)
        elif command == 'k':
            return self.rageSpell.use(self)
    
    def moveUnits(self, Map):
        for unit in self.units:
            unit.move(Map)

class Unit:
    def __init__(self, maxHP, AD, MS, symbol):
        self.alive = True
        self.maxHP = maxHP
        self.HP = maxHP
        self.AD = AD    # dmg per hit
        self.MS = MS    # measured in blocks per second
        self.symbol = symbol
        
        self.posX = 0
        self.posY = 0
    
    # checks collisions with all buildings
    def isColliding(self, x, y, Map):
        for building in Map.buildings:
            if x >= building.posX and x < building.posX + building.sizeX and y >= building.posY and y < building.posY + building.sizeY and building.alive:
                return True
        
        for wall in Map.walls:
            if x == wall.posX and y == wall.posY and wall.alive:
                return True
        
        return False
    
    def distanceTo(self, x, y):
        distance = (self.posX - x)**2 + (self.posY - y)**2
        distance = distance ** 0.5
        
        return distance
    
    def takeDamage(self, dmg):
        self.HP -= dmg
        
        if self.HP <= 0:
            self.alive = False
    
    def move(self):
        pass
    
class King(Unit):
    def __init__(self, m, n):
        super().__init__(1000, 200, 10, 'K')
        self.lastMove = 'w'
        # self.HP = 700
    
    def move(self, command, Map):
        # movement
        if command == 'w' and self.posY > 0 and self.alive == True:
            if self.isColliding(self.posX, self.posY - 1, Map) is False:
                self.posY -= 1
            self.lastMove = 'w'
            self.symbol = '^'
        elif command == 'a' and self.posX > 0 and self.alive == True:
            if self.isColliding(self.posX - 1, self.posY, Map) is False:
                self.posX -= 1
            self.lastMove = 'a'
            self.symbol = '<'
        elif command == 's' and self.posY < Map.m - 1 and self.alive == True:
            if self.isColliding(self.posX, self.posY + 1, Map) is False:
                self.posY += 1
            self.lastMove = 's'
            self.symbol = 'v'
        elif command == 'd' and self.posX < Map.n - 1 and self.alive == True:
            if self.isColliding(self.posX + 1, self.posY, Map) is False:
                self.posX += 1
            self.lastMove = 'd'
            self.symbol = '>'
            
        # attacking
        elif command == ' ' and self.alive == True:            
            if self.lastMove == 'w':
                Map.registerHit(self.posX, self.posY - 1, self.AD)
            elif self.lastMove == 'a':
                Map.registerHit(self.posX - 1, self.posY, self.AD)
            elif self.lastMove == 's':
                Map.registerHit(self.posX, self.posY + 1, self.AD)
            elif self.lastMove == 'd':
                Map.registerHit(self.posX + 1, self.posY, self.AD)

        # spawning, spells handled by army class
        elif command == '1' or command == '2' or command == '3':
            pass
        
        elif command == 'j' or command == 'k':
            pass

        elif command == 'z' or command == 'q':
            pass
        
        # move occured
        else:
            return False
        
        return True
            

class Barbarian(Unit):
    def __init__(self, posX, posY):
        super().__init__(200, 50, 1, 'B')
        self.posX = posX
        self.posY = posY
           
    
    def move(self, Map):
        # find closest structure
        if self.alive == False:
            return
        
        closest = Map.buildings[0]
        for building in Map.buildings:
            if building.alive:
                closest = building
                minDist = Map.buildings[0].distanceTo(self.posX, self.posY)
                break
            
        for building in Map.buildings:
            if building.alive == True:
                dist = building.distanceTo(self.posX, self.posY)
                if dist <= minDist:
                    closest = building
                    minDist = dist
                
        # move towards it
        if closest.isAdjacent(self.posX, self.posY) and closest.alive:
            closest.takeDamage(self.AD)
        # attack otherwise
        else:
            xMove = 0
            yMove = 0
            if closest.posX + closest.sizeX/2 > self.posX:
                xMove += self.MS
            elif closest.posX + closest.sizeX/2 < self.posX:
                xMove -= self.MS
            
            if closest.posY + closest.sizeY/2 > self.posY:
                yMove += self.MS
            elif closest.posY + closest.sizeY/2 < self.posY:
                yMove -= self.MS
                
            # check if it would move into a wall, and attack it if so
            for wall in Map.walls:
                if wall.isOverlapping(self.posX + xMove, self.posY + yMove) and wall.alive == True:
                    wall.takeDamage(self.AD)
                    return
            
            self.posX += xMove
            self.posY += yMove            
            
            return
                

class Spell:
    def __init__(self, code, num):
        self.code = code
        self.startingNum = num
        self.numLeft = num
    
    def use():
        pass
    
class HealSpell(Spell):
    def __init__(self):
        super().__init__('H', 1)
        
    def use(self, army):
        if self.numLeft == 0:
            return 1
        else:
            self.numLeft -= 1
            for unit in army.units:
                if unit.alive == True:
                    unit.HP = min(unit.maxHP, int(unit.HP * 1.5))
            if army.king.alive == True:
                # army.king.HP = min(army.king.maxHP, int(army.king.HP * 1.5))
                army.king.HP = army.king.maxHP
            
            return 0
        
class RageSpell(Spell):
    def __init__(self):
        super().__init__('R', 1)
        self.timer = 5
        
    def use(self, army):
        if self.numLeft == 0:
            return 1
        else:
            self.numLeft -= 1
            army.raging = True
            army.rageTimer = self.timer
                
            return 0
        