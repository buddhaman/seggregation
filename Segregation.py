import random as rnd
import Grid as grd
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.stats.mstats as stats
from scipy.optimize import curve_fit
from fractions import gcd

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

def experiment(n, happyThreshold=1./3., randomHouse=False, w=8,h=8):
    nSteps = []
    totalHappiness = []
    
    for i in range(n):
        grid = grd.Grid(w,h, typeNums=[20,20], 
                        happyThreshold=happyThreshold, randomHouse=randomHouse)
        
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

def writeCSV():
    Threshold, happy, Nsteps = thresholdPlot(50, 200, notifyEvery = 5)
    with open('Nstepsrulemodel', 'wb') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(Nsteps)
    
def loginv(y):
    return np.log(y/(1-y))

def regression(x, b0, b1):
    return 1/(1+np.exp(-(x*b1+b0)))

def logisticregr(x, y, epsilon=0.00001):
    y=np.array(y)
    x=np.array(x)
    mmin = min(y)-epsilon
    mmax = max(y)+epsilon
    y=y-mmin
    y=y/(mmax-mmin)
    invy=loginv(y)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,invy)
    plt.title('f(x)=1/(2+2exp( %.2fx %s %.2f ))+(1/2)'%(-slope, ['+','-'][intercept>0],
    abs(intercept)))
    plt.plot(x, regression(x, intercept, slope)*(mmax-mmin)+mmin)
   
def drawLines(n, ymin, ymax):
    s = {(0,8)}
    for i in range(1,n+1):
        for j in range(1,i+1):
            d = gcd(j,i)
            s.add((j/d, i/d))
    for line in s:
        x = float(line[0])/line[1]
        plt.text(x,0.1, r'$\frac{%d}{%d}$'%(line[0],line[1]), fontsize=15)
        plt.plot((x, x), (ymin,ymax), 'r-')

#Experiment for graphs
happyThreshold, happy, avgSteps = thresholdPlot(30,10, notifyEvery=5)
plt.plot(happyThreshold, avgSteps)
logisticregr(happyThreshold, avgSteps)
drawLines(12,0,5)
plt.show()

#nSteps1, happiness1 = experiment(1000, happyThreshold=1.0/3)
#nSteps2, happiness2 = experiment(1000, happyThreshold=1.0/3, w=10, h=10)
#results = stats.ttest_ind(happiness1, happiness2)
#print results

