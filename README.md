# CoC_in_Python

Terminal based Clash of Clans - esque game in Python

Objective: Destroy all buildings i.e. TownHall (labelled with a T), Huts (labelled with a H) and Canons (Labelled with C). Walls (Labelled with W) restrict your movement but need not be destroyed to win.

Canons will fire at you and your troops from a distance and kill you so be careful.

The colour of the label tells you how much health the troop/structure has left:
Green more than 2/3rds health
Yellow more than 1/3rd, less than 2/3rds health
Red less than 1/3rd health

Watch your own health bar at the bottom of the map to see how much health you have remaining

Controls: 

WASD to move, X for axe attack, dealing 50% of your attack rating to everything in a 2 block radius, useful for opening large gaps in walls, Spacebar for sword attacks, dealing 100% of your attack rating to the structure you are facing, useful for destroying buildings.

J activates Rage Spell, Doubling the attack rating and speed of all troops who are currently alive and spawned.
H activates Healing Spell, Increasing your and all alive troops health to 150% of your current health (maxes at full health)

1,2,3 spawn troops at the 3 corners of the map.

to play, simply type: python3 game.py

to watch the replay of your match, type: python3 reply.py


