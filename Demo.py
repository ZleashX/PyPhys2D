import pygame
import sys , math
from Body import Circle, Box
from World import World
from Utils import Physic
import random

def main():
    pygame.init()
    WIN_HEIGHT =900
    WIN_WIDTH = 1200
    window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    world = World()
    clock = pygame.time.Clock()

    barrierA = Box((5,WIN_HEIGHT/2),10,WIN_HEIGHT,0,Physic.STATIC)
    barrierB = Box((WIN_WIDTH/2,5),WIN_WIDTH,10,0,Physic.STATIC)
    barrierC = Box((WIN_WIDTH-5,WIN_HEIGHT/2),10,WIN_HEIGHT,0,Physic.STATIC)
    barrierD = Box((WIN_WIDTH/2,WIN_HEIGHT-5),WIN_WIDTH,10,0,Physic.STATIC)

    rotatedbarrierA = Box((800,200),400,10,20,Physic.STATIC)
    rotatedbarrierA.angle = math.radians(-20)
    rotatedbarrierB = Box((400,400),400,10,20,Physic.STATIC)
    rotatedbarrierB.angle = math.radians(20)
    rotatedbarrierC = Box((800,600),400,10,20,Physic.STATIC)
    rotatedbarrierC.angle = math.radians(-20)

    world.addbody(barrierA)
    world.addbody(barrierB)
    world.addbody(barrierC)
    world.addbody(barrierD)
    world.addbody(rotatedbarrierA)
    world.addbody(rotatedbarrierB)
    world.addbody(rotatedbarrierC)

    force = 200
    world.setgravity(9.8)
    dt = 0
    prev_time = pygame.time.get_ticks()

    while True:
        dt = pygame.time.get_ticks() - prev_time
        prev_time = pygame.time.get_ticks()

        mx,my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            body = Circle((mx,my),30,50)
            r = random.randint(0,255)
            b = random.randint(0,255)
            g = random.randint(0,255)
            body.color = (r,g,b)
            world.addbody(body)
            body.addforce(-force,force)
            
        if pygame.mouse.get_pressed()[2]:
            body = Box((mx,my),60,60,50)
            r = random.randint(0,255)
            b = random.randint(0,255)
            g = random.randint(0,255)
            body.color = (r,g,b)
            world.addbody(body)
            body.addforce(-force,force)

        window.fill("black")
        world.step(5,dt)

        world.debugdraw(window)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()