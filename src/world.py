import pygame

class World():

    # The total width and height of each tile in pixels.
    TILE_WIDTH = 101
    TILE_HEIGHT = 171
    TILE_OFFSET = 90

    # A giant list representing the world model.
    # level[x] is the row.
    # level[x][y] gives you the column in the row.

    level = [
        ['dirt block',
         'dirt block',
         'dirt block',
         'dirt block',
         'dirt block',
         'wall block',
         'water block'],

        ['plain block',
         'stone block',
         'stone block',
         'ramp west',
         'grass block',
         'wall block',
         'water block'],

        ['stone block',
         'stone block',
         'stone block',
         'grass block',
         'grass block',
         'wall block',
         'water block'],

        ['stone block',
         'stone block',
         'stone block',
         'grass block',
         'grass block',
         'wall block',
         'water block'],

        ['stone block',
         'wall block',
         'stone block',
         'grass block',
         'grass block',
         'wall block',
         'water block'],

        ['wall block',
         'wall block',
         'wall block',
         'wall block',
         'wall block',
         'wall block',
         'water block']
    ]

    def __init__(self, images):

        self.images = images
        pass

    def renderWorld(self):

        width = len(self.level[0]) * self.TILE_WIDTH
        height = len(self.level) * self.TILE_HEIGHT + self.TILE_HEIGHT

        tiles = pygame.Surface((width, height))

        for x in range(len(self.level)):
            for y in range(len(self.level[0])):

                # Rectangle is: left, top, width, height
                where = (y * self.TILE_WIDTH, x *
                        (self.TILE_HEIGHT - self.TILE_OFFSET),
                         self.TILE_WIDTH, self.TILE_HEIGHT)

                tiles.blit(self.images[self.level[x][y]], where)

        return tiles