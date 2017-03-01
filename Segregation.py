import random as rnd
import Grid as grd
import numpy as np
import matplotlib.pyplot as plt

grid = grd.Grid(30,30, typeNums=[200,300,100, 200], nBack=1)
#run 500 simulations

stp = 0
stopAt = 100
while(not grid.isStable() and stp<stopAt):
    print grid
    grid.step()
    stp+=1
print "stepsBeforeStable", stp-1

