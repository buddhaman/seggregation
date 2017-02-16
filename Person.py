
class Person(object):

    def __init__(self, kind):
        self.kind = kind
        self.house = None
    
    def getX(self):
        return self.house.x

    def getY(self):
        return self.house.y
