from pygame import Vector2
from enum import Enum
import math

class Transform:
    def __init__(self,pos,angle):
        self.posx = pos.x
        self.posy = pos.y
        self.sin = math.sin(angle)
        self.cos = math.cos(angle)

    def makeTransform(self,vert):
        x = self.cos * vert.x - self.sin * vert.y + self.posx
        y = self.sin * vert.x + self.cos * vert.y + self.posy
        return Vector2(x,y)
    
class Physic(Enum):
    STATIC = 1
    DYNAMIC = 2

class Shape(Enum):
    CIRCLE = 1
    BOX = 2

class Interval:
        def __init__(self,body,isx):
            if body.shapetype == Shape.CIRCLE:
                self.minval = body.position.x - body.radius
                self.maxval = body.position.x + body.radius
            elif body.shapetype == Shape.BOX:
                self.minval = float('inf')
                self.maxval = float('-inf')
                for vertex in body.transvertices:
                    if vertex.x < self.minval:
                        self.minval = vertex.x
                    if vertex.x > self.maxval:
                        self.maxval = vertex.x
            self.bodyref = body

class Pair:
    def __init__(self,bodyA,bodyB):
        self.bodyA = bodyA
        self.bodyB = bodyB

class Math:
    def iscloseFloat(a,b):
        return abs(a-b) < 0.0005
    
    def iscloseVec(a,b):
        return Vector2.distance_squared_to(a,b) < 0.0005 * 0.0005
