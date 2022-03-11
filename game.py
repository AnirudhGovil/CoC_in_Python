from distutils.spawn import spawn
from src.structures import *
from src.army import *
from src.input import *

import time

m = 26
n = 26
myMap = Map(m, n)
myArmy = Army(m, n)
myMap.setupMap()

heals = HealSpell()
rages = RageSpell()

# render loop

# wait for user input
# the user can input 'z' to skip a time frame
g = Get()
statusText = ''
longMayHeReign = True
myMap.draw(myArmy)
while(True):
        
    # check for win/loss states
    check = myMap.checkWinLoss(myArmy)
    if check == 1:
        print("You won! All buildings destroyed")
        break
    elif check == -1:
        print("You lost. All troops are dead. You got gapped")
        break
    
    # move units
    myMap.draw(myArmy)
    myArmy.moveUnits(myMap)
    
    # print status texts for last turn
    if statusText != '':
        print(statusText)
    statusText = ''
    
    #get input
    command = ''
    spawned = ''
    timestep=0
    while(True):
        command = input_to(g)
        result = myArmy.king.move(command, myMap)
        if(result is True):
            break
 
    

    # set flags    
    if command == 'q':
        break
    elif command == '1' or command == '2' or command == '3':
        result = myArmy.spawnBarbarian(command, myMap)
        if result == 0:
            statusText = ("Troop spawned at spawnpoint " + command)
        else:
            statusText = ("No more spawns available")
            
    elif command == ' ':
        statusText = ("King attacks!")
    
    elif command == 'j':
        result = myArmy.useSpell(command)
        if result == 0:
            statusText = ('Heal spell used')
        else:
            statusText = ('No more heal spells')
    elif command == 'k':
        result = rages.use(myArmy)
        if result == 0:
            statusText = ('Rage spell used')
        else:
            statusText = ('No more rage spells')
    
    if myArmy.king.alive == False and longMayHeReign == True:
        statusText = ("The king has died!")
        longMayHeReign = False
        
    
    myMap.fireDefenses(myArmy)

    
myMap.draw(myArmy)
if check == 1:
    print("You won! All buildings destroyed")
elif check == -1:
    print("You lost. All troops are dead. You got gapped")