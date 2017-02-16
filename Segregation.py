import random as rnd
import Grid as grd

grid = grd.Grid(8,8, typeNums=[20,20])
print grid
for i in range(20):
    grid.step()
    print grid
