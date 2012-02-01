import pygame
from pygame.constants import BLEND_SUB, BLEND_ADD

class Cutscene(object):

    def __init__(self, dialog):
        self.images = images
        pass

    def dim(self, surface, darken_factor=64, color_filter=(0,0,0)):

        maskSurface = pygame.Surface(surface.get_size(), masks = 0)
        maskSurface.set_alpha(192)
        maskSurface.fill((0,0,0))

        surface.blit(maskSurface, (0,0))

    def renderNext(self, tiles, image = "", text = ""):

        self.dim(tiles)

        conversationBox = pygame.Surface((500, 150))
        conversationBox.fill((255,255,255))
        pygame.draw.rect(conversationBox, (0,0,0), (0,0,500,10))
        pygame.draw.rect(conversationBox, (0,0,0), (0,140,500,10))

        girl = self.images["girl"]
        conversationBox.blit(girl, (10,-30))


        font = pygame.font.Font(None, 36)
        text = font.render("Hah! I finally caught you!", True, (0,0,0))
        conversationBox.blit(text, (150,50))

        tiles.blit(conversationBox, (100,200))
        pygame.display.update()

        pass

    pass