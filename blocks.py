import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, group, lefttop, rightbottom, block_type):
        pygame.sprite.Sprite.__init__(self, group)
        size = rightbottom - lefttop 
        self.image = pygame.Surface(size)

        if block_type == BLOCK_TYPE_GROUND:
            self.image.fill((0, 0, 200))
        elif block_type == BLOCK_TYPE_SOLID:
            self.image.fill((0, 200, 0))
        elif block_type == BLOCK_TYPE_LAVA:
            self.image.fill((200, 0, 0))
        elif block_type == BLOCK_TYPE_FINISH:
            self.image.fill((100, 100, 0))
        else:
            self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect(topleft=lefttop, bottomright=rightbottom)
