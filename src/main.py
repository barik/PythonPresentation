#@PydevCodeAnalysisIgnore
import pygame
import random
import math  

from avatar import Avatar
from world import World
from pygame.locals import *
import numpy as np
import kinematics as ai

def main():

    global screen, clock, images
    global player_pos, enemy_pos
    global tiles

    # Startup code
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Carolina Games Summit")
    images = loadImages()

    # The game world.
    world = World(images)
    

    print 'PyGame version ' + pygame.ver

    clock = pygame.time.Clock()

    player_pos  = np.array([80,100])
    player      = Avatar(world, images["boy"], player_pos, 100)

    enemy_pos   = np.array([300,100])
    enemy       = Avatar(world, images["girl"], enemy_pos, 100, True)

    # The main game event loop.
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # Handle movement.
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_SPACE]:

            print pygame.key.name(K_SPACE)
            pass

        # Compute the vector indicating the acceleration that the
        # player will experience.
        acceleration = np.array([0,0])

        if pressed_keys[K_LEFT]:
            acceleration += [-1, 0]

        elif pressed_keys[K_RIGHT]:
            acceleration += [1, 0]

        if pressed_keys[K_UP]:
            acceleration += [0, -1]

        elif pressed_keys[K_DOWN]:
            acceleration += [0, 1]

        if not np.array_equal(acceleration, [0,0]):
            acceleration = acceleration / np.sqrt(np.dot(acceleration, acceleration))

        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0
        player.move(acceleration, time_passed_seconds)
        tiles = world.renderWorld()

        lmb, mmb, rmb = pygame.mouse.get_pressed()
        if lmb:
            print "Mouse Position: ", pygame.mouse.get_pos()
            exit()


        # Perform our AI work!
        
        # Seek behavior
        # ai.seek(enemy, player.position, time_passed_seconds)
        # ai.flee(enemy, player.position, time_passed_seconds)
        
        pass


        screen.fill((0, 0, 0))

        enemy.blitOn(tiles)
        player.blitOn(tiles)
        screen.blit(tiles, (0, 0))

        pygame.display.update()

def loadImages():

    images = {
        "boy": pygame.image.load("../res/Character Boy.png"),
        "girl": pygame.image.load("../res/Character Pink Girl.png"),
        "enemy": pygame.image.load("../res/Enemy Bug.png"),
        "dirt block": pygame.image.load("../res/Dirt Block.png"),
        "stone block": pygame.image.load("../res/Stone Block.png"),
        "plain block": pygame.image.load("../res/Plain Block.png"),
        "grass block": pygame.image.load("../res/Grass Block.png"),
        "water block": pygame.image.load("../res/Water Block.png"),
        "wall block": pygame.image.load("../res/Wall Block.png"),
        "wall block tall": pygame.image.load("../res/Wall Block Tall.png"),
        "ramp west": pygame.image.load("../res/Ramp West.png"),
        "tree short": pygame.image.load("../res/Tree Short.png")
    }

    return images


if __name__ == '__main__':
    main()