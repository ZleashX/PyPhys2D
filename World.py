import pygame
from pygame import Vector2
from Collision import Collision
from Utils import *

class World:
    def __init__(self):
        self.gravity = Vector2(0,0)
        self.bodylist = []
        self._collision = Collision()
        self._pairlist = []

    def step(self,substep,dt):
        dt /= substep
        for i in range(substep):
            for body in self.bodylist:
                body._update(self.gravity,dt)

            self._broadPhase()
            self._narrowPhase()

    #Use Sweep and prune for the broader phase
    #body get sort based on its mininum value of x 
    #possible collision is put into pairlist
    def _broadPhase(self):
        axisX = []
        for body in self.bodylist:
            body._applyTrans()
            axisX.append(Interval(body,True))
        axisX.sort(key= lambda x: x.minval)

        self._pairlist = []
        for i in range(len(axisX)):
            for j in range(i+1,len(axisX)):
                if axisX[i].bodyref.physictype != Physic.DYNAMIC and axisX[j].bodyref.physictype != Physic.DYNAMIC:
                    continue
                if axisX[i].maxval < axisX[j].minval:
                    break
                self._pairlist.append(Pair(axisX[i].bodyref,axisX[j].bodyref))

    def _narrowPhase(self):
        for pair in self._pairlist:
            if self._collision.checkCollide(pair.bodyA,pair.bodyB):

                if pair.bodyA.physictype != Physic.DYNAMIC:
                    pair.bodyB._move(self._collision.normal * self._collision.penetrate)
                elif pair.bodyB.physictype != Physic.DYNAMIC:
                    pair.bodyA._move(-self._collision.normal * self._collision.penetrate)
                else:
                    pair.bodyA._move(-self._collision.normal * (self._collision.penetrate/2))
                    pair.bodyB._move(self._collision.normal * (self._collision.penetrate/2))

                self._collision.getCp(pair.bodyA,pair.bodyB)
                self._collision.resolve(pair.bodyA,pair.bodyB)

    def debugdraw(self,window):
        for body in self.bodylist:
            if body.shapetype == Shape.CIRCLE:
                va = Vector2(0,0)
                vb = Vector2(body.radius,0)
                transform = Transform(body.position,body.angle)
                va = transform.makeTransform(va)
                vb = transform.makeTransform(vb)
                pygame.draw.circle(window,body.color,body.position,body.radius)
                pygame.draw.line(window,"white",va,vb)
            else:
                pygame.draw.lines(window,body.color,True,body.transvertices,5)

    def setgravity(self,value):
        self.gravity = Vector2(0,value * 0.0001)

    def addbody(self,body):
        self.bodylist.append(body)

    def removebody(self,body):
        self.bodylist.remove(body)


    

