from __future__ import division
import pygame, Queue, math

class Unit(pygame.sprite.Sprite):
    "Unit class, subclasses are different kinds of units"
    movespeed=0 
    orders=Queue.Queue()
    attacking=False
    target=None
    current_order=None
    def __init__(self, number, rect, imgname, team,hp):
        "Initalizes. team is a Team object to add the unit to."

        super(Unit, self).__init__(team)
        self.image=pygame.image.load(imgname)
        self.rect=rect 
        self.number=number
        self.hp = hp
        

        
        
    def update(self):
        "Updates the unit"
        if self.current_order==None:
            try:self.current_order=self.orders.get()
            except Queue.Empty:
                if self.team.defender:
                    self.current_order=OrderStandGround()
                else:
                    self.current_order=OrderSeek(self.team.opponent.base.pos)
        self.rect.left, self.rect.right=self.current_order.get_new_pos(self)
        if self.hp==0:self.kill() #Makes the unit get removed from all teams it is in
        if self.current_order.completed:self.current_order=None
    def queue_order(order):
        self.orders.put(order)
class OrderSleep(object):
    "Base order that makes the unit not move and not do anything"
    def __init__(self):self.completed=False
    def get_new_pos(self, obj):return obj.rect.left, obj.rect.right
class OrderSeek(OrderSleep):
    "For now, this order makes a unit follow the target with no pathfinding. TODO:Add pathfinding. TODO:Make the unit attack units in its way."
    def __init__(self, target):
        self.target=target
        super(OrderSeek, self).__init__()
    def get_new_pos(self, obj):
        #WARNING: Trigonometry follows
        pos=[obj.rect.left, obj.rect.right]
        speed=obj.movespeed
        diff=[self.target[0]-pos[0], self.target[1]-pos[1]]
        direction=math.atan(diff[1]/diff[0])
        x=math.cos(direction)*speed+pos[0]
        y=math.sin(direction)*speed+pos[1]
        return [x, y]
class OrderStandGround(OrderSleep):
    "Makes nothing happen right now. TODO:Make unit attack threats"
    pass

class Team:
    def __init__(self,color,units,territory):
        self.color = color
        self.units = units
        self.territory = territory

class Map: # Note: Map.land is the list of territories 
    def __init__(self,land):
        self.land = land

class Territory:
    def __init__(self,troops,buildings):
        self.troops = troops
        self.buildings = buildings
class Building:
    def __init__(self,number,rect,fl,life):
        self.number = number
        self.rect = rect
        self.fl = pygame.image.load(fl)

        
    
