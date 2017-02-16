
class House(object):

    def __init__(self, person, x=0, y=0):
        self.person = person
        if(person!=None):
           person.house = self
        self.x = x
        self.y = y
        
