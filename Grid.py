import Person as per
import random as rnd
import House as hs
import itertools as itr

class Grid(object):
    
    def __init__(self, width, height, typeNums=[20,20], order=1):
        self.width = width
        self.height = height
        
        #number of types (each {index+1} in list is type, list stores amount of each type)
        self.typeNums = typeNums
        
        #grid is single array to make shuffling easier
        self.grid = []
        self.personList = []
        self.emptyHouseList = []
        self.atStep = 0
        self.order = order
        self.nTypes = len(typeNums)

    def populateGrid(self):
        for person in self.personList:
            self.grid.append(hs.House(person))
        #add remaining empty houses
        n = sum(self.typeNums)
        for i in range(n, self.width*self.height):
            house = hs.House(None)
            self.grid.append(house)
            self.emptyHouseList.append(house)
        rnd.shuffle(self.grid)

    def shufflePersonList(self):
        #shuffle personlist for total randomness
        rnd.shuffle(self.personList)

    #set x,y coordinates of all houses 
    def initHouseCoordinates(self):
        for i in range(self.width*self.height):
            h = self.grid[i]
            h.x, h.y = i%self.width, i/self.width

    def getKindGrid(self):
        return [h.person.kind if h.person!=None else 0 for h in self.grid]
    
    def getTotalHappiness(self):
        happySum = 0
        for person in self.personList:
            x=person.getX()
            y=person.getY()
            
            happySum+=self.getHappy(x, y, person.kind)
        return happySum
    
    def step(self):
        self.atStep+=1
            
    def getHouseAt(self, x, y):
        return self.grid[x+y*self.width]
    
    #return random house, including own house
    def findRandomHouse(self, x, y):
        return self.emptyHouseList[rnd.randint(0,len(self.emptyHouseList)-1)]
    
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
    
    #get all houses in neighbourhood around (x, y).
    #Excludes house at (x, y)
    def getNeigbourhood(self, x, y):
        order = self.order
        (x1, y1) = max(0, x-order), max(0, y-order)
        (x2, y2) = min(x+order, self.width-1), min(y+order, self.height-1)
        neighbourhood = []
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                if((i,j)==(x,y)):
                    continue
                else:
                    neighbourhood.append(self.getHouseAt(i, j))
        return neighbourhood
    
    def getKindAt(self, x, y):
        person = self.grid[x+y*self.width].person
        if(person==None):
            return 0
        else:
            return person.kind
    
    def __str__(self):
        string = ""
        for x in range(self.width):
            for y in range(self.height):
                string+=([' ', 'O', '#', 'X', 'I'][self.getKindAt(x, y)]+' ')
            string+="\n"
        return string
    

def distance(x1, y1, x2, y2):
    return (x2-x1)**2+(y2-y1)**2
