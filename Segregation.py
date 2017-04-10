import random as rnd
import GridBasic as grd
import GridPrice as prc
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.stats.mstats as stats
from scipy.optimize import curve_fit
from fractions import gcd

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

def experiment(n, happyThreshold=1./3., randomHouse=False, w=8,h=8, order = 1):
    nSteps = []
    totalHappiness = []
    
    for i in range(n):
        grid = grd.GridBasic(w,h, typeNums=[20,20], 
                        happyThreshold=happyThreshold, 
                        randomHouse=randomHouse, order = order)
        
        step = 0
        maxSteps = 100  
        while grid.step() and step < maxSteps:
            step=step+1
        
        nSteps.append(step)
        totalHappiness.append(grid.getTotalHappiness()/len(grid.personList))
    return nSteps, totalHappiness

def avg(ls):
    return float(sum(ls))/len(ls)

def atThreshold(iterations, order=1, notifyEvery=5, randomHouse=False):
    thresholds = getFracs((2*order+1)**2-1)
    thresholds.sort()
    happinessList = []
    avgSteps = []
    n=0
    print '%d points to check'%(len(thresholds))
    for h in thresholds: 
        n+=1
        nSteps, happiness = experiment(iterations, happyThreshold=h,
                                       randomHouse=randomHouse, order=order)
        happinessList.append(avg(happiness))
        avgSteps.append(avg(nSteps))
        if n%notifyEvery==0 :
            print '%d of %d experiments done'%(n, len(thresholds))
    return thresholds, happinessList, avgSteps

#plot total happiness against happyThreshold
def thresholdPlot(nDatapoints, iterations, randomHouse):
    notifyEvery=5
    totalHappy = []
    happyThreshold = []
    avgSteps = []
    
    for n in range(nDatapoints):
        t = float(n)/nDatapoints
        happyThreshold.append(t)
        
        nSteps, totalHappiness = experiment(iterations, randomHouse=randomHouse,
                                            happyThreshold=t)
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

def logisticregr(ax, x, y, epsilon=0.00001):
    y=np.array(y)
    x=np.array(x)
    mmin = min(y)-epsilon
    mmax = max(y)+epsilon
    y=y-mmin
    y=y/(mmax-mmin)
    invy=loginv(y)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,invy)
    ax.set_title('f(x)=1/(2+2exp( %.2fx %s %.2f ))+(1/2)'%(-slope, ['+','-'][intercept>0],
    abs(intercept)))
    ax.plot(x, regression(x, intercept, slope)*(mmax-mmin)+mmin, label='approximation')

def getThresholds(n):
    s = {(0,1)}
    for i in range(1,n+1):
        for j in range(1,i+1):
            d = gcd(j,i)
            s.add((j/d, i/d))
    s=list(s)
    s.sort()
    return s

def getFracs(n):
    return [float(s[0])/s[1] for s in getThresholds(n)]

def drawLines(ax,n, ymin, ymax):
    s = getThresholds(n)
    print s
    for line in s:
        x = float(line[0])/line[1]
        ax.text(x,0.5, r'$\frac{%d}{%d}$'%(line[0],line[1]), fontsize=12)
#       plt.plot((x, x), (ymin,ymax), 'r-')
        
def drawFlatGraph(ax, x, y, label='data'):
    xx = []
    yy = []
    for i in range(0,len(x)-1):
        xx.append(x[i])
        yy.append(y[i])
        xx.append(x[i+1])
        yy.append(y[i])
    ax.plot(xx, yy, label=label)

def func(x, a, M, b1, b2):
    return a+M/(1+np.exp(-(b1*x+b2)))

def fitcurve(ax, x, y, f):
    popt, pcov = curve_fit(f, np.array(x), np.array(y))
    drawFlatGraph(ax, x, f(x, *popt), label='fit')
    print 'a=%f, M=%f, b1=%f, b2=%f'%(popt[0],popt[1],popt[2],popt[3])
    return popt

def thplot():
    plt.figure(1)
    happyThreshold, happy, avgSteps = thresholdPlot(40, 20)
    
def fit():
    happyThreshold, happy, avgSteps = atThreshold(5, order=1)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_xlabel('threshold')
    ax.set_ylabel('average happiness')
    drawFlatGraph(ax, happyThreshold, happy, label='happiness')
    popt = fitcurve(ax, np.array(happyThreshold), np.array(happy), func)
    plt.title(r'$f(x)=%.2f+\frac{%.2f}{1+\exp(-(%.2fx %s %.2f))}$'%(popt[0],popt[1],
              popt[2],['+','-'][popt[3] >= 0],popt[3]))
    plt.legend()
    plt.show()

def regr():
    fig =  plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('threshold')
    ax.set_ylabel('average happiness')
    happyThreshold, happy, avgSteps = atThreshold(50, notifyEvery)
    logisticregr(ax, happyThreshold, avgSteps)
    drawFlatGraph(ax, happyThreshold, avgSteps, label='data')
    plt.legend()
    plt.show()

def phaseTrans():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('threshold')
    ax.set_ylabel('average happiness')
    happyThreshold, happy, avgSteps = atThreshold(50, randomHouse=True)
    drawFlatGraph(ax, happyThreshold, happy, label='random moving')
    drawLines(ax,8,0,1)
    plt.legend()
    plt.show()

#Experiment for graphs
phaseTrans()

#
#grid = prc.GridPrice(8,8, typeNums=[20,20])
#consoleTest(grid, True, 2)


#nSteps1, happiness1 = experiment(1000, happyThreshold=1.0/3)
#nSteps2, happiness2 = experiment(1000, happyThreshold=1.0/3, w=10, h=10)
#results = stats.ttest_ind(happiness1, happiness2)
#print results

