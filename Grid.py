import Person as per
import random as rnd
import House as hs
import itertools as itr

def distance(x1, y1, x2, y2):
    return abs(x2-x1)+abs(y2-y1)

class Grid(object):
    
    def __init__(self, width, height, typeNums=[20,20]):
        self.width = width
        self.height = height
        #number of types (each {index+1} in list is type, list stores amount of each type)
        self.typeNums = typeNums
         #grid is single array to make shuffling easier
        self.grid = []
        self.personList = []
        self.emptyHouseList = []
       
        for n in range(len(typeNums)):
            for i in range(typeNums[n]):
                self.personList.append(per.Person(n+1))
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

    def step(self):
        for person in self.personList:
            x, y = person.getX(), person.getY()
            happy = self.getHappy(x, y, person.kind)
            #if satisfied, do nothing
            if happy >= 1./3.:
                continue
            #remove from house and find new one. If none found move back
            self.removePersonFromHouse(person)
            newHouse = self.findNewHouse(x, y, person.kind, happy)
            if(newHouse==None):
                newHouse = self.getHouseAt(x, y)
            self.addPersonToHouse(person, newHouse)
            
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

    #get happyness at (x,y). Excludes (x,y)
    def getHappy(self, x, y, kind):
        #order 2 neighbourhoord
        (x1, y1) = max(0, x-1), max(0, y-1)
        (x2, y2) = min(x+1, self.width-1), min(y+1, self.height-1)
        #number of gridpoints
        n = (x2-x1+1)*(y2-y1+1) - 1
        happy = 0
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                if(i==x and j==y):
                    continue
                if(self.getKindAt(i, j)==kind):
                    happy+=1
        return float(happy)/n

    def __str__(self):
        string = ""
        for x in range(self.width):
            for y in range(self.height):
                string+=(str(self.getKindAt(x, y))+' ')
            string+="\n"
        return string
       
