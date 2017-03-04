import random as rnd
import Grid as grd
import numpy as np
import matplotlib.pyplot as plt


#run 500 simulations


def consoleTest(grid, printGrid, maxIterations):
    if printGrid:
        print grid
    
    stp = 0
    stateChanged = True    

    while(stateChanged and stp<maxIterations):
        stateChanged = grid.step()
        if stateChanged:
            stp+=1
        if printGrid and stateChanged:
            print grid
    
    print "stepsBeforeStable", stp

def experiment(n, happyThreshold=1./3.):
    nSteps = []
    totalHappiness = []
    
    for i in range(n):
        grid = grd.Grid(10,10, typeNums=[30,30], happyThreshold=happyThreshold)
        step = 0
        
        while grid.step():
            step=step+1
        
        nSteps.append(step)
        totalHappiness.append(grid.getTotalHappiness())
    return nSteps, totalHappiness

def avg(ls):
    return float(sum(ls))/len(ls)

#plot total happiness against happyThreshold
def happyThresholdPlot(nDatapoints, iterations, notifyEvery=10):
    
    totalHappy = []
    happyThreshold = []
    
    for n in range(nDatapoints):
        t = float(n)/nDatapoints
        happyThreshold.append(t)
                         
        nSteps, totalHappiness = experiment(iterations, happyThreshold=t)
        totalHappy.append(avg(totalHappiness))
        if n%notifyEvery==0:
            print '%d of %d experiments done'%(n, nDatapoints)
            
    
    plt.plot(happyThreshold, totalHappy)
    plt.show()
        
happyThresholdPlot(50, 200)

