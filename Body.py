from pygame import Vector2
from Utils import *

class Body:
    def __init__(self, mass ,physictype = Physic.DYNAMIC):
        self.physictype = physictype
        self.mass = mass
        self.invmass = 0.1
        self.elasticity = 0.5
        self.staticfriction = 0.6
        self.dynamicfriction = 0.4
        self.inertia = 0
        self.velocity = Vector2(0,0)
        self.force = Vector2(0,0)
        self.position = Vector2(0,0)
        self.angle = 0
        self.angularvel = 0
        self.color = (255,0,0)

        if physictype == Physic.DYNAMIC:
            self.invmass = 1/self.mass
        else:
            self.invmass = 0

    def move(self, xamount, yamount):
        self.position += Vector2(xamount,yamount)

    def _move(self, amount):
        self.position += amount

    def _applyTrans(self):
        return

    def addforce(self, xforce, yforce):
        self.force += Vector2(xforce,yforce)

    def _update(self,gravity,dt):
        if self.physictype != Physic.DYNAMIC:
            return

        acceleration = self.force * self.invmass
        self.velocity += self.invmass * acceleration * dt
        self.velocity += gravity * dt
        self.position += self.velocity * dt
        self.angle += self.angularvel * dt
        self.force = Vector2(0,0)

class Circle(Body):
    def __init__(self, pos, radius, mass, physictype = Physic.DYNAMIC):
        super().__init__(mass, physictype)
        self.position = Vector2(pos[0],pos[1])
        self.shapetype = Shape.CIRCLE
        self.radius = radius
        self.inertia = 1 / 2 * mass * radius * radius

        if physictype == Physic.DYNAMIC:
            self.invinertia = 1/self.inertia
        else:
            self.invinertia = 0
    
    def _projCircle(self, axis):
        direction = Vector2.normalize(axis)
        dirCircle = direction * self.radius

        p1 = self.position + dirCircle
        p2 = self.position - dirCircle

        v1 = Vector2.dot(p1,axis)
        v2 = Vector2.dot(p2,axis)

        return min(v1,v2), max(v1,v2)
    
    def _findClosestPoint(self, boxvertices):
        minDis = float('inf')

        for vertex in boxvertices:
            distance = Vector2.distance_to(vertex,self.position)

            if distance < minDis:
                minDis = distance
                result = vertex

        return result
    
class Box(Body):
    def __init__(self, pos, width, height, mass, physictype = Physic.DYNAMIC):
        super().__init__(mass,physictype)
        self.position = Vector2(pos[0],pos[1])
        self.shapetype = Shape.BOX
        self.width = width
        self.height = height
        self.inertia = (1 / 12) * mass * (width * width + height * height)
        self.updatetrans = False

        if physictype == Physic.DYNAMIC:
            self.invinertia = 1/self.inertia
        else:
            self.invinertia = 0

        #make vertices
        left = -self.width / 2
        right = left + self.width
        bottom = -self.height / 2
        top = bottom + self.height
        self.vertices = [Vector2(left,top),Vector2(right,top),Vector2(right,bottom),Vector2(left,bottom)]
        self.transvertices = self.vertices.copy()

    def _applyTrans(self):
        if self.physictype == Physic.STATIC and self.updatetrans:
            return
        transform = Transform(self.position,self.angle)
        for i, vertex in enumerate(self.vertices):
            self.transvertices[i] = transform.makeTransform(vertex)
        self.updatetrans = True

    def _projVertices(self,vertices,axis):
        dot_products = [Vector2.dot(vertex,axis) for vertex in vertices]
        return min(dot_products), max(dot_products)
