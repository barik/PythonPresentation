'''
Represents an Avatar in the game world.
Has three properties: an image, the image size and a position in the world.
'''
class Avatar():

    def __init__(self, image, width, height, pos):
        self.image     = image
        self.width     = width
        self.height    = height
        self.pos       = pos

    def blitOn(self, worldTiles):
        avatarRect = (self.pos[0], self.pos[1], self.width, self.height)
        worldTiles.blit(self.image,avatarRect)

    def move(self, destination):
        if self.canMove(destination):
            self.pos = destination

        else:
            pass #do nothing


    def canMove(self, destination):
        if destination[0] < 0 or destination[1] < 0:
            return False

        return True


