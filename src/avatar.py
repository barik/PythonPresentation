import pygame
import numpy as np

class Avatar():
    """
    Represents an Avatar in the game world.
    """

    def __init__(self, world, image, position, max_speed,
                 is_npc = False):

        self.reference = (50, 138)
        self.world = world
        self.image = image
        self.position = position

        self.velocity = np.array([0., 0.])
        self.prev_velocity = np.array([0., 0.])
        self.max_velocity_magnitude = max_speed

        self.lastAcceleration = np.array([0., 0.])
        self.isNonPlayerCharacter = is_npc


    def blitOn(self, worldTiles):
        # Since the position always refers to the midpoint from the top left
        # we do this computation to obtain where the actual top left of the
        # image is so that we can blit it.

        avatarLocation = (self.position[0] - self.reference[0],
                          self.position[1] - self.reference[1])

        worldTiles.blit(self.image, avatarLocation)

    def move(self, acceleration, time_passed):
        self.updateVelocity(acceleration, time_passed)
        self.updatePosition(time_passed)


    def updatePosition(self, time_passed):
        position_update = self.position + (self.velocity * time_passed)

        if self.canMove(position_update):
            self.position = position_update

        else:
            # If we can't move, we hit a boundary.
            # Since we hit a boundary, null the
            # velocity/lastAcceleration for instant stop.
            self.velocity[0] = 0.
            self.velocity[1] = 0.
            self.lastAcceleration[0] = 0.
            self.lastAcceleration[1] = 0.


    def updateVelocity(self, acceleration, time_passed):
        print acceleration
        print self.velocity

        # no external force applied - player is not controlling avatar
        if acceleration[0] == 0. and acceleration[1] == 0.:
            if self.isNonPlayerCharacter:
                self.velocity = (self.velocity + (
                    self.lastAcceleration * time_passed * -1 * self.max_velocity_magnitude))

                # if the velocity changes sign to match that of the lastAcceleration, stop
            if cmp(self.velocity[0], 0) == cmp(self.lastAcceleration[0], 0):
                self.velocity[0] = 0.
                self.lastAcceleration[0] = 0

            if cmp(self.velocity[1], 0) == cmp(self.lastAcceleration[1], 0):
                self.velocity[1] = 0.
                self.lastAcceleration[1] = 0

            else:
                self.velocity = np.array([0, 0])

        else:
            self.velocity = (acceleration * time_passed *
                             self.max_velocity_magnitude * 100)

            self.lastAcceleration = acceleration


    def canSpeedUp(self, velocity):
        # Check for velocity in both x and y directions
        if (velocity[0] > self.max_velocity_magnitude or
            velocity[0] < -self.max_velocity_magnitude):

            return False

        if (velocity[1] > self.max_velocity_magnitude or
            velocity[1] < -self.max_velocity_magnitude):
            return False

        return True


    def canMove(self, pos):
        # Calculate based on avatar midpoint.
        print "actual position", self.position

        # Construct a bounding box around the position. These are actually
        # somewhat arbitrary. This assumes all avatar's will have a
        # similar figure, which they do.

        tryBoundary = pygame.Rect(0, 0, 20, 20)
        tryBoundary.midbottom = self.position

        print tryBoundary.midbottom

        print "tryBoundary", tryBoundary

        if self.world.collideWall(tryBoundary):
            return True # Todo
        else:
            return True

