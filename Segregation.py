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
        grid = grd.Grid(8,8, typeNums=[20,20], 
                        happyThreshold=happyThreshold, randomHouse=False)
        
        step = 0
        maxSteps = 100
        while grid.step() and step < maxSteps:
            step=step+1
        
        nSteps.append(step)
        totalHappiness.append(grid.getTotalHappiness()/len(grid.personList))
    return nSteps, totalHappiness

def avg(ls):
    return float(sum(ls))/len(ls)

#plot total happiness against happyThreshold
def thresholdPlot(nDatapoints, iterations, notifyEvery=5):
    
    totalHappy = []
    happyThreshold = []
    avgSteps = []
    
    for n in range(nDatapoints):
        t = float(n)/nDatapoints
        happyThreshold.append(t)
                         
        nSteps, totalHappiness = experiment(iterations, happyThreshold=t)
        totalHappy.append(avg(totalHappiness))
        avgSteps.append(avg(nSteps))
        
        if n%notifyEvery==0:
            print '%d of %d experiments done'%(n, nDatapoints)
    
    return happyThreshold, totalHappy, avgSteps

happyThreshold, happy, avgSteps = thresholdPlot(150, 1000, notifyEvery=1)

plt.plot(happyThreshold, happy)
plt.show()

