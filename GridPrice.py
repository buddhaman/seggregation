from Grid import *
import numpy as np
import random as rnd

class GridPrice(Grid):
    
    def __init__(self, width, height, typeNums):
        Grid.__init__(self, width, height, typeNums=typeNums)
        
        #houses cost (pricefactor) * more than income
        self.priceFactor = 10
        
        for n in range(self.nTypes):
            for i in range(typeNums[n]):
                self.personList.append(per.Person(n+1))
        
        self.shufflePersonList()
        self.populateGrid()
        self.initHouseCoordinates()
        self.initHousePrices()
    
    def initHousePrices(self):
         for house in self.grid:
            price = self.getAvgIncome(house.x, house.y)*self.priceFactor
            house.price = self.getAvgIncome(house.x, house.y)*self.priceFactor
    
    def getHousePrices(self):
        return [h.price for h in self.grid]
    
    def step(self):
        #call supermethod
        Grid.step(self)
        
        #for every house: check average income in neighbourhood. (floor)
        #If more than house price: housePrice+=1
        #If less than house price: housePrice-=1
        #If exactly average: do nothing
        
        for house in self.grid:
            expectedPrice = np.round(self.getAvgIncome(house.x, house.y)*self.priceFactor)
            if expectedPrice > house.price:
                house.price+=1
            elif expectedPrice < house.price:
                house.price+=1
                
        #check person income against house price
        #if less : House price=person income * factor
        #else : move to more expensive house
        for person in self.personList:
            worth = person.kind*self.priceFactor
            house = person.house
            if(house.price > worth):
                house.price = worth
            roundedHousePrice = self.priceFactor*np.round(int(house.price)/int(self.priceFactor))
            if roundedHousePrice < worth:
                x, y = person.getX(), person.getY()
                #move
                self.removePersonFromHouse(person)
                newHouse = self.findNewHouse(x, y, person.kind)
                if newHouse==None:
                    newHouse = house
                self.addPersonToHouse(person, newHouse)
        
        return True
                    
            
    #call after removing person from own house. Own house shouldn't count
    #new house should be better than threshold (person current happiness). If no house found. return house
    #at (x,y)
    def findNewHouse(self, x, y, kind):
        candidates = []
        for house in self.emptyHouseList:
            if(house.x==x and house.y==y):
                continue
            price = house.price
            if price > kind*self.priceFactor and price < (kind+1)*self.priceFactor:
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
        
    def getAvgIncome(self, x, y):
        neighbourhood = self.getNeigbourhood(x, y)
        
        n=0         #number of people
        income=0
        
        for house in neighbourhood:
            if house.person == None:
                continue
            else:
                n+=1
                income+=house.person.kind
        if n==0:
            return 0
        else:
            return float(income)/n
        
        
    def __str__(self):
        string = ""
        for x in range(self.width):
            for y in range(self.height):
                string+=([' ', '1', '2', '3', '4','5','6'][self.getKindAt(x, y)]+' ')
            string+="\n"
        return string
    
