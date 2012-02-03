import pygame

class World():

    # The total width and height of each tile in pixels.
    TILE_WIDTH = 101
    TILE_HEIGHT = 171
    TILE_OFFSET = 90

    # The amount of pixels shifted before the actual tile begins.
    TILE_VISIBLE_SHIFT = 50
    TILE_VISIBLE_HEIGHT = 130
    TILE_VISIBLE_WIDTH = 101

    # A giant list representing the world model.
    # We want it such that in level[x][y], the x will select the column and
    # the y will select the row.

    # In doing so, each sub-list in the level list is column-wise, not
    # row-wise.

    level = [

        # Column 1
        ['dirt block',
         'dirt block',
         'wall block',
         'grass block',
         'grass block',
         'grass block',
         'grass block',
         ],

        # Column 2
        ['dirt block',
         'dirt block',
         'wall block',
         'stone block',
         'stone block',
         'wall block',
         'wall block',
        ],

        # Column 3
        ['water block',
         'dirt block',
         'wall block',
         'stone block',
         'stone block',
         'grass block',
         'grass block',
        ],

        # Column 4
        ['water block',
         'ramp block',
         'water block',
         'stone block',
         'stone block',
         'grass block',
         'grass block',
        ],

        # Column 5
        ['water block',
         'ramp block',
         'water block',
         'stone block',
         'stone block',
         'grass block',
         'grass block',
        ],

        # Column 6
        ['water block',
         'ramp block',
         'ramp block',
         'stone block',
         'stone block',
         'stone block',
         'stone block',
        ],

        # Column 7
        ['water block',
         'water block',
         'water block',
         'stone block',
         'stone block',
         'stone block',
         'stone block',
        ]
    ]

    def __init__(self, images):

        self.images = images
        pass

    def renderWorld(self):

        # Reminder: left (x), top (y)
        # such that len(self.level) is top/height (y)
        # and len(self.level[0]) is left/width (x)

        width = len(self.level) * self.TILE_WIDTH
        height = len(self.level[0]) * self.TILE_HEIGHT

        tiles = pygame.Surface((width, height))
        # tiles.fill((70,70,70))

        for x in range(len(self.level)):
            for y in range(len(self.level[0])):

                # Rectangle is: left, top, width, height
                where = (x * self.TILE_WIDTH, y *
                        (self.TILE_HEIGHT - self.TILE_OFFSET),
                         self.TILE_WIDTH, self.TILE_HEIGHT)

                tiles.blit(self.images[self.level[x][y]], where)

        return tiles

    # Returns the length of the world in pixels.
    def getLength(self):
        return len(self.level) * self.TILE_WIDTH

    # Returns the height of the world in pixels.
    def getHeight(self):
        return len(self.level[0]) * self.TILE_HEIGHT

    def getRectangleForTile(self, position):

        x, y = position

        return pygame.Rect(
            x * self.TILE_WIDTH,
            self.TILE_VISIBLE_SHIFT + y * self.TILE_VISIBLE_HEIGHT,
            self.TILE_WIDTH,
            self.TILE_VISIBLE_HEIGHT
        )

    def getTileForPoint(self, pos):

        return (pos[0] // self.TILE_WIDTH,
               (pos[1] - self.TILE_VISIBLE_SHIFT) //
               (self.TILE_VISIBLE_HEIGHT - self.TILE_VISIBLE_SHIFT))

    # Go to the center of a tile. Used by A*. Maybe.
    def getCenterForTile(self, pos):

        print "Center", pos
        x, y = pos

        print "now going to", self.TILE_VISIBLE_SHIFT + y * self.TILE_VISIBLE_HEIGHT

        return (x * self.TILE_WIDTH + self.TILE_WIDTH / 2,
                self.TILE_VISIBLE_SHIFT + y * self.TILE_VISIBLE_HEIGHT)

    # Refactor this with collideWall.
    def isWallAtTile(self, pos):

        x, y = pos

        tileType = self.level[x][y]

        # Block checking.
        if tileType == "wall block" or tileType == "water block":
            return True

    # Get the underlying tile that occurs at that position.
    # Check the four corners for now, and then check the diagonals later
    # if it's needed.
    def collideWall(self, rect):

        tileLocation = self.getTileForPoint(rect.midbottom)
        x, y = tileLocation

        if x >= len(self.level)  or y >= len(self.level[0]):
            print "[collideWall] Tile is out of bounds:", x, y
            return True

        tileType = self.level[x][y]

        # Block checking.
        if tileType == "wall block" or tileType == "water block":
            return True

        # If you end up here, you must not have collided.
        return False

