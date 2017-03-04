import Person as per
import random as rnd
import House as hs
import itertools as itr

class Grid(object):
    
    def __init__(self, width, height, typeNums=[20,20], nBack=1, happyThreshold=.3333):
        self.width = width
        self.height = height
        #number of types (each {index+1} in list is type, list stores amount of each type)
        self.typeNums = typeNums
         #grid is single array to make shuffling easier
        self.grid = []
        self.personList = []
        self.emptyHouseList = []
        self.lastGrids = []
        self.nBack = nBack
        self.atStep = 0
        self.happyThreshold = happyThreshold
       
        for n in range(len(typeNums)):
            for i in range(typeNums[n]):
                self.personList.append(per.Person(n+1))
                
        #shuffle personlist for total randomness
        rnd.shuffle(self.personList)
        
        for person in self.personList:
            self.grid.append(hs.House(person))

        #add remaining empty houses
        n = sum(typeNums)
        for i in range(n, self.width*self.height):
            house = hs.House(None)
            self.grid.append(house)
            self.emptyHouseList.append(house)

        rnd.shuffle(self.grid)
        self.initHouseCoordinates()
        
    #set x,y coordinates of all houses 
    def initHouseCoordinates(self):
        for i in range(self.width*self.height):
            h = self.grid[i]
            h.x, h.y = i%self.width, i/self.width

    def getKindGrid(self, grid):
        return [h.person.kind if h.person!=None else 0 for h in grid]
    
    def getTotalHappiness(self):
        happySum = 0
        for person in self.personList:
            x=person.getX()
            y=person.getY()
            
            happySum+=self.getHappy(x, y, person.kind)
        return happySum
    
    def step(self):
         #add to list of previous grid states
        self.lastGrids.insert(0, list(self.getKindGrid(self.grid)))
        if(len(self.lastGrids) > self.nBack):
            del self.lastGrids[-1]
        
        stateChanged = False;
        
        self.atStep+=1
        for person in self.personList:
            x, y = person.getX(), person.getY()
            happy = self.getHappy(x, y, person.kind)
            
            #if satisfied, do nothing
            if happy >= self.happyThreshold:
                continue
            
            #remove from house and find new one. If none found, move back
            self.removePersonFromHouse(person)
            newHouse = self.findNewHouse(x, y, person.kind, happy)
            if(newHouse==None):
                newHouse = self.getHouseAt(x, y)
            else:
                stateChanged = True
            self.addPersonToHouse(person, newHouse)
        return stateChanged
            
    def getHouseAt(self, x, y):
        return self.grid[x+y*self.width]
            
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
        mindst = self.width+self.height+self.width*self.height
        bestHouse = None
        for house in candidates:
            dst = distance(x, y, house.x, house.y)
            if(dst < mindst):
                bestHouse = house
                mindst = dst
        return bestHouse
    
    #also sets person.house=None
    def removePersonFromHouse(self, person):
        house = person.house
        person.house = None
        house.person = None
        self.emptyHouseList.append(house)
        
    #house should be empty                       
    def addPersonToHouse(self, person, house):
        self.emptyHouseList.remove(house)
        house.person = person
        person.house = house
    
    def getKindAt(self, x, y):
        person = self.grid[x+y*self.width].person
        if(person==None):
            return 0
        else:
            return person.kind

    def isStable(self):
        if(len(self.lastGrids)<self.nBack):
            return False
        grid = self.getKindGrid(self.grid)
        for g in self.lastGrids:
            if g!=grid:
                return False
        return True
        
    #get happyness at (x,y). Excludes (x,y)
    def getHappy(self, x, y, kind):
        #order 2 neighbourhoord
        (x1, y1) = max(0, x-1), max(0, y-1)
        (x2, y2) = min(x+1, self.width-1), min(y+1, self.height-1)
        #number of gridpoints
        n = 0
        happy = 0
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                if(i==x and j==y):
                    continue
                otherKind = self.getKindAt(i,j)
                if(otherKind!=0):
                    n+=1
                if(otherKind==kind):
                    happy+=1
        if n==0:
            return 1
        else:
            return float(happy)/n
    
    def __str__(self):
        string = ""
        for x in range(self.width):
            for y in range(self.height):
                string+=([' ', 'O', '#', 'X', 'I'][self.getKindAt(x, y)]+' ')
            string+="\n"
        return string

def distance(x1, y1, x2, y2):
    return (x2-x1)**2+(y2-y1)**2
