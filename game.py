from src.structures import *
from src.clan import *
from src.input import *
from pickle import dump
import copy

m = 25
n = 25
myClan = Clan(m, n, 10, 2 , 1)

#replay file
replay_list2 = [myClan,]
myMap = Map(m, n)
myMap.setupMap()
myMap.draw(myClan)

replay_list1 = [myMap,]
# render loop
# the user can input 'k' to skip a time frame

status = ''
flag=0

replay_list1.append(myMap)
replay_list2.append(myClan)

while(True):
    # check for win/loss 
    command = ''
    flag=myMap.checkWinLoss(myClan)
    if flag == 1:
        print("You won!")
        break
    elif flag == -1:
        print("You lost.")
        break
    elif flag == 0:
        pass
    
    # move troops
    myClan.moveTroops(myMap)
    myMap.draw(myClan)

    # print status texts
    print("\n"+status)
    
    #get input
    
    timestep=0
    while(True):
        command = input_to(Get())
        if(myClan.king.move(command, myMap)):
            break 

    


    if command == 'q':
        break

    elif command == ' ':
        if myClan.king.alive:
            status = "King attacks with sword!"
    
    elif command == 'x':
        if myClan.king.alive:
            status = "King attacks with axe!"
    
    elif command == 'h':
        if myClan.useHealSpell() :
            status = ('Heal spell used')
        else:
            status = "No more heal spells"

    elif command == 'j':
       if myClan.useRageSpell():
           status = "Rage spell used"
       else:
           status = "No more rage spells"

    elif command == '1' or command == '2' or command == '3':
        if myClan.spawn(command, myMap):
            status = "Troop spawned at spawnpoint " + command
        else:
            status = "No more spawns available"

    myMap.fireCanons(myClan)

    replay_list1.append(copy.deepcopy(myMap))
    replay_list2.append(copy.deepcopy(myClan))
    
  
    
myMap.draw(myClan)
if(flag==1): 
    print("You won!")  
if(flag==-1):
    print("You lost.") 
print("Game Over")

with open("replays/maps", 'wb') as f:
    dump(replay_list1, f)
with open("replays/clans", 'wb') as f:
    dump(replay_list2, f)