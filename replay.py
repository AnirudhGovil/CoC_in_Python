from pickle import load
from time import sleep

from matplotlib.pyplot import draw
from src.structures import *
from src.clan import *

with open("replays/maps", 'rb') as f:
    maps = list(load(f))

with open("replays/clans", 'rb') as f:
    clans = list(load(f))

for i,j in zip(maps,clans):
    i.draw(j)
    sleep(0.5)


    

