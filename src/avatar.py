import pygame

'''
Represents an Avatar in the game world.
Has three properties: an image, the image size and a position in the world.
'''
class Avatar(pygame.sprite.Sprite):

    def __init__(self, image, width, height, pos, sprite_speed):
        self.image        = image
        self.width        = width
        self.height       = height
        self.pos          = pos
        self.sprite_speed = sprite_speed


    def blitOn(self, worldTiles):
        avatarRect = (self.pos[0], self.pos[1], self.width, self.height)
        worldTiles.blit(self.image,avatarRect)


    def move(self, direction, time_passed_seconds):
        destination = self.pos + ( direction *
                                   self.sprite_speed *
                                   time_passed_seconds )

        if self.canMove(destination):
            self.pos = destination

        else:
            pass #do nothing


    def canMove(self, destination):
        if destination[0] < 0 or destination[1] < 0:
            return False

        return True
