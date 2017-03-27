
class Person(object):
    
    def __init__(self, kind, changeProb=0):
        self.kind = kind
        self.house = None
        self.changeProb = changeProb
    
    def getX(self):
        return self.house.x

    def getY(self):
        return self.house.y
