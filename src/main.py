import pygame
import random
import astar, levels
import numpy as np
import kinematics as ai

from agent import Agent
from world import World
from pygame.locals import *

# Set these constants before starting the game.
FPS = 20
LEVEL = levels.EASY
MAX_PLAYER_SPEED = 100
MAX_ENEMY_SPEED = 20

# Audio TRACKS; easy to implement. Get TRACKS at:
# http://www.nosoapradio.us/
TRACKS = [
    "DST-Greensky.mp3", "DST-Travel.mp3"
]


def main():
    global screen, images
    global enemy, player
    global tiles, world

    global draw_vectors
    global behavior

    global LEVEL

    showDialog = False

    # Startup code
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    pygame.display.set_caption("Carolina Games Summit")
    images = loadImages()

    # The game world.
    world = World(images, LEVEL['level'])

    # Internal clock - used for computing velocities 
    # We use time-based calculations rather than frame-based
    clock = pygame.time.Clock()

    player_pos = np.array(LEVEL['player'])
    player = Agent(world, images["boy"], player_pos, MAX_PLAYER_SPEED)

    enemy_pos = np.array(LEVEL['enemy'])
    enemy = Agent(world, images["girl"], enemy_pos, MAX_ENEMY_SPEED,
                  is_npc=True)

    # Initially, background music is playing.
    backgroundMusic()

    # Default behavior.
    behavior = 'seek'
    draw_vectors = False

    level_change = False

    # The main game event loop.
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_m:
                    backgroundMusic()
                elif event.key == K_d:
                    draw_vectors = not draw_vectors
                    print "Toggled:", draw_vectors
                    # Magic keys to change in-game behavior.
                elif event.key == K_w:
                    behavior = 'wander'
                # Special case to close off left-most ramp
                # in hard map.
                elif event.key == K_x:
                    if LEVEL['level'][1][3] == 'ramp block':
                        LEVEL['level'][1][3] = 'water block'
                    else:
                        LEVEL['level'][1][3] = 'ramp block'

                elif event.key == K_s:
                    behavior = 'seek'
                elif event.key == K_a:
                    behavior = 'a*'
                elif event.key == K_f:
                    behavior = 'flee'
                elif event.key == K_v:
                    behavior = 'avoid'
                elif event.key == K_r:
                    behavior = 'arrive'
                elif event.key == K_1:
                    LEVEL = levels.EASY
                    level_change = True
                elif event.key == K_2:
                    LEVEL = levels.MEDIUM
                    level_change = True
                elif event.key == K_3:
                    LEVEL = levels.HARD
                    level_change = True

        # If level change was indicated.
        if level_change:
            world = World(images, LEVEL['level'])

            player_pos = np.array(LEVEL['player'])
            player = Agent(world, images["boy"], player_pos, MAX_PLAYER_SPEED)

            enemy_pos = np.array(LEVEL['enemy'])
            enemy = Agent(world, images["girl"], enemy_pos, MAX_ENEMY_SPEED,
                          is_npc=True)

            level_change = False
            pass

        # Handle movement.
        pressed_keys = pygame.key.get_pressed()

        # Compute the vector indicating the acceleration that the
        # player will experience.
        acceleration = np.array([0, 0])

        if pressed_keys[K_LEFT]:
            acceleration += [-1, 0]
        elif pressed_keys[K_RIGHT]:
            acceleration += [1, 0]

        if pressed_keys[K_UP]:
            acceleration += [0, -1]
        elif pressed_keys[K_DOWN]:
            acceleration += [0, 1]

        if not np.array_equal(acceleration, [0, 0]):
            # Using /= here breaks. NumPy issue?
            acceleration = acceleration / np.sqrt(
                np.dot(acceleration, acceleration))

        time_passed = clock.tick(FPS)
        time_passed_seconds = time_passed / 1000.0

        player.update(acceleration, time_passed_seconds)

        # This is where the magic happens.
        executeAIBehavior(behavior, enemy, player, time_passed_seconds)

        # Render to intermediate memory buffer.
        refreshBlit()

        if draw_vectors is True:
            if behavior == "a*":
                drawLineTile(apath.path, tiles)
            else:
                line = [(enemy.position[0], enemy.position[1]),
                    (player.position[0], player.position[1])]
                drawLinePixel(line, tiles)

        # Intermediate buffer to screen.
        screen.blit(tiles, (0, 0))

        # Update the display, and loop again!
        pygame.display.update()


def executeAIBehavior(behavior, enemy, player, time_passed_seconds):
    global apath # For drawing overlays.

    if behavior == 'wander':
        ai.wander(enemy, time_passed_seconds)

    elif behavior == 'seek':
        ai.seek(enemy, player.position, time_passed_seconds)

    elif behavior == 'a*':
        apath = astar.go(enemy.position, player.position, world)
        waypoint = astar.goNext(apath, world)

        if waypoint is not None:
            ai.seek(enemy, waypoint, time_passed_seconds)

    elif behavior == 'flee':
        ai.flee(enemy, player.position, time_passed_seconds)

    elif behavior == 'avoid':
        ai.avoid(enemy, player.position, time_passed_seconds)

    elif behavior == 'arrive':
        ai.arrive(enemy, player.position, time_passed_seconds)


def loadImages():
    images = {
        "boy": pygame.image.load("../res/Character Boy.png"),
        "girl": pygame.image.load("../res/Character Pink Girl.png"),
        "enemy": pygame.image.load("../res/Enemy Bug.png"),
        "heart": pygame.image.load("../res/Heart.png"),
        "chest closed": pygame.image.load("../res/Chest Closed.png"),
        "gem": pygame.image.load("../res/Gem Blue.png"),
        "key": pygame.image.load("../res/Gem Blue.png"),
        "dirt block": pygame.image.load("../res/Dirt Block.png"),
        "stone block": pygame.image.load("../res/Stone Block.png"),
        "plain block": pygame.image.load("../res/Plain Block.png"),
        "grass block": pygame.image.load("../res/Grass Block.png"),
        "ramp block": pygame.image.load("../res/Ramp South.png"),
        "water block": pygame.image.load("../res/Water Block.png"),
        "wall block": pygame.image.load("../res/Wall Block.png"),
        "wall block tall": pygame.image.load("../res/Wall Block Tall.png"),
        "ramp west": pygame.image.load("../res/Ramp West.png"),
        "tree short": pygame.image.load("../res/Tree Short.png"),
        "speech bubble": pygame.image.load("../res/SpeechBubble.png")
    }

    # Key
    images["key"] = pygame.transform.scale(images["key"],
        (images["key"].get_width() / 2, images["key"].get_height() / 2))

    # Heart
    images["heart"] = pygame.transform.scale(images["heart"],
        (images["heart"].get_width() / 2, images["heart"].get_height() / 2))

    # Gem
    images["gem"] = pygame.transform.scale(images["gem"],
        (images["gem"].get_width() / 2, images["gem"].get_height() / 2))

    return images

# Useful for didactic purposes.
def drawLineTile(path, tiles):
    global world

    to_draw = []

    for p in path:
        to_draw.append(world.getCenterForTile(p))

    if len(path) >= 2:
        pygame.draw.lines(tiles, (255, 0, 0), False, to_draw, 5)


def drawLinePixel(path, tiles):
    global world

    if len(path) >= 2:
        pygame.draw.lines(tiles, (255, 0, 0), False, path, 5)


def dialogBox(image, text):
    global screen, tiles, images

    print "Dialog box."

    # The mask is used to dim the screen.
    maskSurface = pygame.Surface(tiles.get_size())
    maskSurface.set_alpha(192)
    maskSurface.fill((0, 0, 0))

    tiles.blit(maskSurface, (0, 0))

    # Now display the dialog box.
    box = pygame.Surface((500, 150))
    box.fill((255, 255, 255))
    pygame.draw.rect(box, (0, 0, 0), (0, 0, 500, 10))
    # pygame.draw.rect(box, (0,0,0), (0,140,500,10))

    box.blit(image, (10, -30))

    font = pygame.font.Font("../res/Jet Set.ttf", 36)
    text = font.render(text, True, (0, 0, 0))
    box.blit(text, (150, 50))

    tiles.blit(box, (100, 200))

    screen.blit(tiles, (0, 0))

    pygame.display.update()

    while pygame.event.wait().type != KEYDOWN: pass

    print "Dialog acknowledged."


def backgroundMusic():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)
    else:
        pygame.mixer.music.load("../res/" + random.choice(TRACKS))
        pygame.mixer.music.play(-1)


def refreshBlit():
    global screen, enemy, player, tiles, world

    tiles = world.renderWorld()
    screen.fill((0, 0, 0))

    # Display level, and display behavior.
    font = pygame.font.Font("../res/Jet Set.ttf", 36)
    text = font.render(LEVEL['name'], True, (255, 255, 255))
    tiles.blit(text, (0, 0))

    text = font.render(behavior.upper(), True, (255, 255, 255))
    tiles.blit(text, (400, 0))

    enemy.blitOn(tiles)
    player.blitOn(tiles)


if __name__ == '__main__':
    main()