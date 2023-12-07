from pygame import Vector2
from Utils import Shape, Math

class Collision:
    def __init__(self):
        self.penetrate = Vector2(0,0)
        self.normal = Vector2(0,0)
        self.contact = []

    def collideCircles(self,circleA,circleB):
        self.normal = Vector2(0,0)
        self.penetrate = float('inf')
        distance = circleA.position.distance_to(circleB.position)
        radii = circleA.radius + circleB.radius
        if (distance > radii):
            return False
        
        if (distance != 0):
            self.normal = Vector2.normalize(circleB.position - circleA.position)
            self.penetrate = radii - distance
        else:
            self.normal = Vector2(1,0)
            self.penetrate = circleA.radius
        return True
    
    def collidePolys(self,polyA,polyB):
        self.normal = Vector2(0,0)
        self.penetrate = float('inf')

        for i in range(len(polyA.transvertices)):
            vertA = polyA.transvertices[i]
            vertB = polyA.transvertices[(i + 1) % len(polyA.transvertices)]

            edge = vertB - vertA
            axis = Vector2(-edge.y,edge.x).normalize()

            minA, maxA = polyA._projVertices(polyA.transvertices,axis)
            minB, maxB = polyA._projVertices(polyB.transvertices,axis)

            if minA >= maxB or minB >= maxA:
                return False
            
            axisDepth = min(maxB - minA, maxA - minB)

            if axisDepth < self.penetrate:
                self.penetrate = axisDepth
                self.normal = axis

        for i in range(len(polyB.transvertices)):
            vertA = polyB.transvertices[i]
            vertB = polyB.transvertices[(i + 1) % len(polyB.transvertices)]

            edge = vertB - vertA
            axis = Vector2(-edge.y,edge.x).normalize()

            minA, maxA = polyA._projVertices(polyA.transvertices,axis)
            minB, maxB = polyA._projVertices(polyB.transvertices,axis)

            if minA >= maxB or minB >= maxA:
                return False
            
            axisDepth = min(maxB - minA, maxA - minB)

            if axisDepth < self.penetrate:
                self.penetrate = axisDepth
                self.normal = axis

        direction = polyB.position - polyA.position

        if Vector2.dot(direction, self.normal) < 0:
            self.normal = -self.normal

        return True
    
    def collideCirclePoly(self,circle,poly):
        self.normal = Vector2(0,0)
        self.penetrate = float('inf')

        for i in range(len(poly.transvertices)):
            vertA = poly.transvertices[i]
            vertB = poly.transvertices[(i + 1) % len(poly.transvertices)]

            edge = vertB - vertA
            axis = Vector2(-edge.y,edge.x).normalize()

            minBox, maxBox = poly._projVertices(poly.transvertices,axis)
            minCircle, maxCircle = circle._projCircle(axis)

            if minBox >= maxCircle or minCircle >= maxBox:
                return False
            
            axisDepth = min(maxCircle - minBox, maxBox - minCircle)

            if axisDepth < self.penetrate:
                self.penetrate = axisDepth
                self.normal = axis

        closestpoint = circle._findClosestPoint(poly.transvertices)
        axis = Vector2(closestpoint - circle.position).normalize()
        
        minBox, maxBox = poly._projVertices(poly.transvertices,axis)
        minCircle, maxCircle = circle._projCircle(axis)

        if minBox >= maxCircle or minCircle >= maxBox:
            return False
        
        axisDepth = min(maxCircle - minBox, maxBox - minCircle)

        if axisDepth < self.penetrate:
            self.penetrate = axisDepth
            self.normal = axis

        direction = poly.position - circle.position

        if Vector2.dot(direction, self.normal) < 0:
            self.normal = -self.normal

        return True
    
    def checkCollide(self,bodyA,bodyB):
        bodyA._applyTrans()
        bodyB._applyTrans()
        if bodyA.shapetype is Shape.CIRCLE:
            if bodyB.shapetype is Shape.CIRCLE:
                return self.collideCircles(bodyA,bodyB)
            elif bodyB.shapetype is Shape.BOX:
                return self.collideCirclePoly(bodyA,bodyB)
        elif bodyA.shapetype is Shape.BOX:
            if bodyB.shapetype is Shape.CIRCLE:
                result = self.collideCirclePoly(bodyB,bodyA)
                if result:
                    self.normal = -self.normal
                return result
            elif bodyB.shapetype is Shape.BOX:
                return self.collidePolys(bodyA,bodyB)
            
    def cpCircles(self,circleA,circleB):
        direction = Vector2.normalize(circleB.position - circleA.position)
        contact = circleA.position + direction * circleA.radius
        self.contact.append(contact)

    def cpPolys(self,polyA,polyB):
        contact1 = Vector2(0,0)
        contact2 = Vector2(0,0)
        contactnum = 0

        minDistSq = float('inf')

        for vertex in polyA.transvertices:
            for j in range(len(polyB.transvertices)):
                vertA = polyB.transvertices[j]
                vertB = polyB.transvertices[(j + 1) % len(polyB.transvertices)]

                distSq , cp = self.distPointLine(vertex, vertA, vertB)

                if Math.iscloseFloat(distSq,minDistSq):
                    if contact1 != cp and contact2 != cp:
                        contact2 = cp
                        contactnum = 2
                elif distSq < minDistSq:
                    minDistSq = distSq
                    contact1 = cp

        for vertex in polyB.transvertices:
            for j in range(len(polyA.transvertices)):
                vertA = polyA.transvertices[j]
                vertB = polyA.transvertices[(j + 1) % len(polyA.transvertices)]

                distSq , cp = self.distPointLine(vertex, vertA, vertB)

                if distSq == minDistSq:
                    if contact1 != cp and contact2 != cp:
                        contact2 = cp
                        contactnum = 2
                elif distSq < minDistSq:
                    minDistSq = distSq
                    contact1 = cp

        self.contact.append(contact1)
        if contactnum == 2:
            self.contact.append(contact2)

    def cpCirclePoly(self,circle,poly):
        contact = Vector2(0,0)
        cp = Vector2(0,0)
        minDistSq = float('inf')

        for i in range(len(poly.transvertices)):
            vertA = poly.transvertices[i]
            vertB = poly.transvertices[(i + 1) % len(poly.transvertices)]

            distSq , cp = self.distPointLine(circle.position, vertA, vertB)

            if distSq < minDistSq:
                minDistSq = distSq
                contact = cp

        self.contact.append(contact)

    def getCp(self,bodyA,bodyB):
        bodyA._applyTrans()
        bodyB._applyTrans()
        self.contact.clear()
        if bodyA.shapetype is Shape.CIRCLE:
            if bodyB.shapetype is Shape.CIRCLE:
                return self.cpCircles(bodyA,bodyB)
            elif bodyB.shapetype is Shape.BOX:
                return self.cpCirclePoly(bodyA,bodyB)
        elif bodyA.shapetype is Shape.BOX:
            if bodyB.shapetype is Shape.CIRCLE:
                return self.cpCirclePoly(bodyB,bodyA)
            elif bodyB.shapetype is Shape.BOX:
                return self.cpPolys(bodyA,bodyB)

    def distPointLine(self,point,p1,p2):
        line1 = p2 - p1
        line2 = point - p1

        proj = Vector2.dot(line2,line1)
        lenSq = Vector2.length_squared(line1)
        d = proj / lenSq

        if d <= 0:
            cp = p1
        elif d >= 1:
            cp = p2
        else:
            cp = p1 + line1 * d

        return Vector2.distance_squared_to(point,cp) , cp

    def resolve(self,bodyA,bodyB):
        e = min(bodyA.elasticity,bodyB.elasticity)
        statifFriction = (bodyA.staticfriction + bodyB.staticfriction) * 0.5
        dynamicFriction = (bodyA.dynamicfriction + bodyB.dynamicfriction) * 0.5
        if len(self.contact) > 1:
            contact = (self.contact[0] + self.contact[1]) * 0.5
        else:
            contact = self.contact[0]

        ra = contact - bodyA.position
        rb = contact - bodyB.position

        raPerp = Vector2(-ra.y,ra.x)
        rbPerp = Vector2(-rb.y,rb.x)

        angularLinearVelA = raPerp * bodyA.angularvel
        angularLinearVelB = rbPerp * bodyB.angularvel

        relativeVel = (bodyB.velocity + angularLinearVelB) - (bodyA.velocity + angularLinearVelA)

        contactVelNorm = Vector2.dot(relativeVel,self.normal)

        if contactVelNorm > 0:
            return

        raPerpDotN = Vector2.dot(raPerp,self.normal)
        rbPerpDotN = Vector2.dot(rbPerp,self.normal)
        j = -(1 + e) * contactVelNorm
        j /= bodyA.invmass + bodyB.invmass + (raPerpDotN * raPerpDotN) * bodyA.invinertia + (rbPerpDotN * rbPerpDotN) * bodyB.invinertia

        impulse = j * self.normal
        bodyA.velocity += -impulse * bodyA.invmass
        bodyA.angularvel += -Vector2.cross(ra,impulse) * bodyA.invinertia
        bodyB.velocity += impulse * bodyB.invmass
        bodyB.angularvel += Vector2.cross(rb,impulse) * bodyB.invinertia

        #calculate friction
        tangent = relativeVel - Vector2.dot(relativeVel,self.normal) * self.normal

        if Math.iscloseVec(tangent,Vector2(0,0)):
            return
        else:
            tangent = Vector2.normalize(tangent)

        raPerpDotT = Vector2.dot(raPerp,tangent)
        rbPerpDotT = Vector2.dot(rbPerp,tangent)

        jt = -Vector2.dot(relativeVel,tangent)
        jt /= bodyA.invmass + bodyB.invmass + (raPerpDotT * raPerpDotT) * bodyA.invinertia + (rbPerpDotT * rbPerpDotT) * bodyB.invinertia

        if abs(jt) < j * statifFriction:
            impulsefriction = jt * tangent
        else:
            impulsefriction = -j * tangent * dynamicFriction

        bodyA.velocity += -impulsefriction * bodyA.invmass
        bodyA.angularvel += -Vector2.cross(ra,impulsefriction) * bodyA.invinertia
        bodyB.velocity += impulsefriction * bodyB.invmass
        bodyB.angularvel += Vector2.cross(rb,impulsefriction) * bodyB.invinertia
