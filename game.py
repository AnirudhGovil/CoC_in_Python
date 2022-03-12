from distutils.spawn import spawn
from src.structures import *
from src.clan import *
from src.input import *

m = 26
n = 26
myMap = Map(m, n)
myClan = Clan(m, n, 10, 2 , 1)
myMap.setupMap()

# render loop

# wait for user input
# the user can input 'k' to skip a time frame
g = Get()
statusText = ''
myMap.draw(myClan)
flag=0
while(True):
        
    # check for win/loss states
    flag=myMap.checkWinLoss(myClan)
    if flag == 1:
        print("You won! All buildings destroyed")
        break
    elif flag == -1:
        print("You lost. All troops are dead.")
        break
    elif flag == 0:
        pass
    
    # move troops
    myMap.draw(myClan)
    myClan.moveTroops(myMap)
    
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
        if(myClan.king.move(command, myMap)):
            break 

    if command == 'q':
        break

    elif command == ' ':
        if myClan.king.alive:
            statusText = ("King attacks!")

    elif command == '1' or command == '2' or command == '3':
        if myClan.spawn(command, myMap):
            statusText = ("Troop spawned at spawnpoint " + command)
        else:
            statusText = ("No more spawns available")
    
    elif command == 'h':
        if myClan.useHealSpell() :
            statusText = ('Heal spell used')
        else:
            statusText = ('No more heal spells')

    elif command == 'j':
       if myClan.useRageSpell():
           statusText = ('Rage spell used')
       else:
           statusText = ('No more rage spells')
    
    
        
    myMap.fireDefenses(myClan)

    
myMap.draw(myClan)
if(flag==1): 
    print("You won! All buildings destroyed")  
if(flag==-1):
    print("You lost. All troops are dead.") 
print("Game Over")