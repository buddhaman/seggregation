
class House(object):

    def __init__(self, person, x=0, y=0, price=-1):
        self.person = person
        if(person!=None):
           person.house = self
        self.x = x
        self.y = y
        if price >= 0:
            self.price=price

    def __str__(self):
        return str((self.x, self.y))



