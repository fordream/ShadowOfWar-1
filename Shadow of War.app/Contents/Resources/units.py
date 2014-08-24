from framework import Unit

class Swordsman(Unit):
    def __init__(self,pos,team):
        self.pos = pos
        self.team = team
        self.number = 0
        self.rect = [pos[0],pos[1],64,64]
        self.fl = 'images/swordsman.png'
        self.hp = 100

        Unit.__init__(self,self.number,self.rect,self.fl,self.team,self.hp)


class Archer(Unit):
    def __init__(self,pos,team):
        self.pos = pos
        self.team = team
        self.number = 1
        self.rect = [pos[0],pos[1],64,64]
        self.fl = 'images/archer.png'
        self.hp = 75

        Unit.__init__(self,self.number,self.rect,self.fl,self.team,self.hp)
        

