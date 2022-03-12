class Troop:
    def __init__(self, maxHP, attack, speed, ID):
        self.alive = True
        self.maxHP = maxHP
        self.HP = maxHP
        self.attack = attack    # dmg per hit
        self.speed = speed    # measured in blocks per second
        self.ID = ID
        self.location = [0,0] # X,Y
    
    def distanceTo(self, x, y):
        distance = (self.location[0] - x)**2 + (self.location[1] - y)**2
        distance = distance ** 0.5
        
        return distance
    
    def takeDamage(self, dmg):
        self.HP -= dmg
        
        if self.HP <= 0:
            self.alive = False
    
class King(Troop):
    def __init__(self, m, n):
        super().__init__(1000, 200, 1, 'K')


    # checks if move is valid
    def validMove(self, x, y, Map):

        if x >= Map.n or y >= Map.m or x <=-1 or y<=-1:
            return 2

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
                temp = self.validMove(self.location[0], self.location[1] - self.speed, Map)
                if temp == 1:
                    self.location[1] -= self.speed
                elif temp == 2:
                    self.location[1] = 0


            elif command == 'a' and self.location[0] > 0:
                self.lastMove = 'a'
                self.ID = '<'
                temp = self.validMove(self.location[0] - self.speed, self.location[1], Map)
                if temp == 1:
                    self.location[0] -= self.speed
                elif temp == 2:
                    self.location[0] = 0


            elif command == 's' and self.location[1] < Map.m - 1:
                self.lastMove = 's'
                self.ID = 'v'
                temp = self.validMove(self.location[0], self.location[1] + self.speed, Map)
                if temp == 1:
                    self.location[1] += self.speed
                elif temp == 2:
                    self.location[1] = Map.m - 1


            elif command == 'd' and self.location[0] < Map.n - 1:
                self.lastMove = 'd'
                self.ID = '>'
                temp = self.validMove(self.location[0] + self.speed, self.location[1], Map)
                if temp == 1:
                    self.location[0] += self.speed
                elif temp == 2:
                    self.location[0] = Map.n - 1


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
    closest=0
    for building in Map.buildings:
        if building.alive == True:
            if(flag==0):
                closest = building
                minDist = Map.buildings[0].distanceTo(self.location[0], self.location[1])
            dist = building.distanceTo(self.location[0], self.location[1])
            if dist <= minDist:
                closest = building
                minDist = dist
    return closest
    

class Barbarian(Troop):
    
    def __init__(self, X, Y):
        super().__init__(200, 50, 1, 'B')
        self.location[0] = X
        self.location[1] = Y
           
    
    def move(self, Map):
       
        if self.alive == True:
            
            # find closest structure
            closest = closest_helper(self,Map)

            if(closest):
                # attack it
                if closest.isAdjacent(self.location[0], self.location[1]) and closest.alive:
                    closest.takeDamage(self.attack)

                # move otherwise
                else:
                    xMove = 0
                    yMove = 0
                    if closest.location[0] + closest.sizeX/2 > self.location[0]:
                        xMove += self.speed
                    elif closest.location[0] + closest.sizeX/2 < self.location[0]:
                        xMove -= self.speed

                    if closest.location[1] + closest.sizeY/2 > self.location[1]:
                        yMove += self.speed
                    elif closest.location[1] + closest.sizeY/2 < self.location[1]:
                        yMove -= self.speed

                    # check if wall is blocking, and attack it 
                    for wall in Map.walls:
                        if (wall.alive == True):
                            if wall.isOverlapping(self.location[0] + xMove, self.location[1] + yMove):
                                wall.takeDamage(self.attack)
                                return

                    self.location[0] += xMove
                    self.location[1] += yMove            

        return
                
class Clan:
    def __init__(self, m, n, size, h_uses, j_uses):
        self.king = King(m, n)
        self.troops = []
        self.spawnsLeft = size
        self.healSpell = h_uses
        self.rageSpell = j_uses
        
    def spawn(self, location, Map):
        # location can be either 1 2 or 3
        if self.spawnsLeft > 0:
            self.troops.append(Barbarian(Map.spawnpoints[int(location) - 1]["X"], Map.spawnpoints[int(location) - 1]["Y"]))
            self.spawnsLeft -= 1
            return 1
        else:
            return 0
    
    def useHealSpell(self):
        if self.healSpell == 0:
            return 0
        else:
            self.healSpell -= 1
            for troop in self.troops:
                if troop.alive == True:
                    troop.HP = min(troop.maxHP, int(troop.HP * 1.5))
            if self.king.alive == True:
                self.king.HP = min(self.king.maxHP, int(self.king.HP * 1.5))
            
            return 1

    def useRageSpell(self):
        if self.rageSpell == 0:
            return 0

        else:
            self.rageSpell -= 1
            for troop in self.troops:
                if troop.alive == True:
                    troop.attack = troop.attack * 2
                    troop.speed = troop.speed * 2
            if self.king.alive == True:
                self.king.attack = self.king.attack * 2
                self.king.speed = self.king.speed * 2
            
            return 1
    
    def moveTroops(self, Map):
        for troop in self.troops:
            troop.move(Map)