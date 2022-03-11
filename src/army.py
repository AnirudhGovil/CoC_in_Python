class Clan:
    def __init__(self, m, n, size):
        self.king = King(m, n)
        self.troops = []
        self.spawnsLeft = size
        self.healSpell = HealSpell()
        
    def spawn(self, location, Map):
        # location can be either 1 2 or 3
        if self.spawnsLeft > 0:
            self.troops.append(Barbarian(Map.spawnpoints[int(location) - 1]["X"], Map.spawnpoints[int(location) - 1]["Y"]))
            self.spawnsLeft -= 1
            return 1
        else:
            return 0
    
    def useHealSpell(self):
        return self.healSpell.use(self)
    
    def moveTroops(self, Map):
        for troop in self.troops:
            troop.move(Map)

class Troop:
    def __init__(self, maxHP, attack, speed, ID):
        self.alive = True
        self.maxHP = maxHP
        self.HP = maxHP
        self.attack = attack    # dmg per hit
        self.speed = speed    # measured in blocks per second
        self.ID = ID
        
        self.X = 0
        self.Y = 0
    
    def distanceTo(self, x, y):
        distance = (self.X - x)**2 + (self.Y - y)**2
        distance = distance ** 0.5
        
        return distance
    
    def takeDamage(self, dmg):
        self.HP -= dmg
        
        if self.HP <= 0:
            self.alive = False
    
class King(Troop):
    def __init__(self, m, n):
        super().__init__(1000, 200, 10, 'K')


    # checks if move is valid
    def validMove(self, x, y, Map):
        for building in Map.buildings:
            if x >= building.X and x < building.X + building.sizeX and y >= building.Y and y < building.Y + building.sizeY and building.alive:
                return False
        
        for wall in Map.walls:
            if x == wall.X and y == wall.Y and wall.alive:
                return False
        
        return True
    
    def move(self, command, Map):

        # valid non-movement input
        if command == '1' or command == '2' or command == '3' or command == 'h' or command == 'z' or command == 'q':
            return True

        if self.alive == True:

        # movement
            if command == 'w' and self.Y > 0:
                self.lastMove = 'w'
                self.ID = '^'
                if self.validMove(self.X, self.Y - 1, Map) is True:
                    self.Y -= 1

            elif command == 'a' and self.X > 0:
                self.lastMove = 'a'
                self.ID = '<'
                if self.validMove(self.X - 1, self.Y, Map) is True:
                    self.X -= 1

            elif command == 's' and self.Y < Map.m - 1:
                self.lastMove = 's'
                self.ID = 'v'
                if self.validMove(self.X, self.Y + 1, Map) is True:
                    self.Y += 1

            elif command == 'd' and self.X < Map.n - 1:
                self.lastMove = 'd'
                self.ID = '>'
                if self.validMove(self.X + 1, self.Y, Map) is True:
                    self.X += 1


            # attacking
            elif command == ' ':            
                if self.lastMove == 'w':
                    Map.registerHit(self.X, self.Y - 1, self.attack)
                elif self.lastMove == 'a':
                    Map.registerHit(self.X - 1, self.Y, self.attack)
                elif self.lastMove == 's':
                    Map.registerHit(self.X, self.Y + 1, self.attack)
                elif self.lastMove == 'd':
                    Map.registerHit(self.X + 1, self.Y, self.attack)

            # no move occured
            else:
                return False
            
            # move occured
            return True
        
        # no move occured
        else:
            return False
            
def closest_helper(self,Map):

    flag=0 
    for building in Map.buildings:
        if building.alive == True:
            if(flag==0):
                closest = building
                minDist = Map.buildings[0].distanceTo(self.X, self.Y)
            dist = building.distanceTo(self.X, self.Y)
            if dist <= minDist:
                closest = building
                minDist = dist

    return closest
    

class Barbarian(Troop):
    
    def __init__(self, X, Y):
        super().__init__(200, 50, 1, 'B')
        self.X = X
        self.Y = Y
           
    
    def move(self, Map):
       
        if self.alive == True:
            
            # find closest structure
            closest = closest_helper(self,Map)

            # attack it
            if closest.isAdjacent(self.X, self.Y) and closest.alive:
                closest.takeDamage(self.attack)

            # move otherwise
            else:
                xMove = 0
                yMove = 0
                if closest.X + closest.sizeX/2 > self.X:
                    xMove += self.speed
                elif closest.X + closest.sizeX/2 < self.X:
                    xMove -= self.speed

                if closest.Y + closest.sizeY/2 > self.Y:
                    yMove += self.speed
                elif closest.Y + closest.sizeY/2 < self.Y:
                    yMove -= self.speed

                # check if wall is blocking, and attack it 
                for wall in Map.walls:
                    if (wall.alive == True):
                        if wall.isOverlapping(self.X + xMove, self.Y + yMove):
                            wall.takeDamage(self.attack)
                            return

                self.X += xMove
                self.Y += yMove            

        return
                
    
class HealSpell:

    def __init__(self):
        self.code = 'H'
        self.startingNum = 1
        self.numLeft = 1
        
    def use(self, army):
        if self.numLeft == 0:
            return 1
        else:
            self.numLeft -= 1
            for troop in army.troops:
                if troop.alive == True:
                    troop.HP = min(troop.maxHP, int(troop.HP * 1.5))
            if army.king.alive == True:
                # army.king.HP = min(army.king.maxHP, int(army.king.HP * 1.5))
                army.king.HP = army.king.maxHP
            
            return 0
        