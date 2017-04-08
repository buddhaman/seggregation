from Grid import *
import Person as per
import random as rnd
import House as hs
import itertools as itr

class GridBasic(Grid):
    
    def __init__(self, width, height, typeNums=[20,20], 
                 happyThreshold=.3333, randomHouse = False,
                 changeProb=0,
                 order=1):
        Grid.__init__(self, width, height, typeNums, order=order)
        self.happyThreshold = happyThreshold
        self.randomHouse = randomHouse
       
        for n in range(self.nTypes):
            for i in range(typeNums[n]):
                self.personList.append(per.Person(n+1, changeProb=changeProb))
        
        self.shufflePersonList()
        self.populateGrid()
        self.initHouseCoordinates()
    
    def getTotalHappiness(self):
        happySum = 0
        for person in self.personList:
            x=person.getX()
            y=person.getY()
            
            happySum+=self.getHappy(x, y, person.kind)
        return happySum
    
    def step(self):
        Grid.step(self)
        stateChanged = False
        for person in self.personList:
            x, y = person.getX(), person.getY()
            happy = self.getHappy(x, y, person.kind)
            
            if rnd.uniform(0,1) < person.changeProb*(1-happy):
                person.kind = rnd.randint(1, self.nTypes)
                stateChanged = True
            
            #if satisfied, do nothing
            if happy >= self.happyThreshold:
                continue
            
            #remove from house and find new one. If none found, move back
            self.removePersonFromHouse(person)
            
            newHouse = None
            if(self.randomHouse):
                newHouse = self.findRandomHouse(x, y)
            else:
                newHouse = self.findNewHouse(x, y, person.kind, happy)
            if(newHouse==None):
                newHouse = self.getHouseAt(x, y)
            else:
                stateChanged = True
            self.addPersonToHouse(person, newHouse)
        return stateChanged
            
    #call after removing person from own house. Own house shouldn't count
    #new house should be better than threshold (person current happieness). If no house found. return house
    #at (x,y)
    def findNewHouse(self, x, y, kind, threshold):
        candidates = []
        for house in self.emptyHouseList:
            if(house.x==x and house.y==y):
                continue
            happy = self.getHappy(house.x, house.y, kind)
            if happy > threshold:
                candidates.append(house)
        #choose house with minimal distance
        mindst = self.width*self.width+self.height*self.height
        bestHouse = None
        for house in candidates:
            dst = distance(x, y, house.x, house.y)
            if(dst < mindst):
                bestHouse = house
                mindst = dst
        return bestHouse
    
    #get happyness at (x,y). Excludes (x,y)
    def getHappy(self, x, y, kind):
        neighbourhood = self.getNeigbourhood(x, y)
        n = 0
        happy = 0
        for house in neighbourhood:
            if house.person==None:
                continue
            else:
                otherKind = house.person.kind
                if(otherKind!=0):
                    n+=1
                if(otherKind==kind):
                    happy+=1
        if n==0:
            return 1
        else:
            h=float(happy)/n
            return h