import pygame
vec = pygame.math.Vector2

BLOCK_TYPE_GROUND = 1
BLOCK_TYPE_SOLID = 2
BLOCK_TYPE_ELEVATOR = 3

BLOCKS = [
    [vec(0,15), vec(50,16), BLOCK_TYPE_GROUND],

    [vec(10,14), vec(11,15), BLOCK_TYPE_SOLID],
    [vec(13,13), vec(14,14), BLOCK_TYPE_ELEVATOR],
    [vec(16,12), vec(20,13), BLOCK_TYPE_SOLID],
    [vec(16,13), vec(17,15), BLOCK_TYPE_SOLID],
    [vec(23,11), vec(26,12), BLOCK_TYPE_SOLID],
    [vec(28,10), vec(34,11), BLOCK_TYPE_SOLID],
]

FINISH = vec (33,9)
# START = vec(0,14)
START = vec(15,5)
