import pygame
from settings import *
vec = pygame.math.Vector2


BLOCKS = [
    [vec(0,15), vec(41,16), BLOCK_TYPE_GROUND],
    [vec(0,0), vec(1,15), BLOCK_TYPE_GROUND],
    [vec(38,10), vec(40,15), BLOCK_TYPE_GROUND],
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


# Resize blocks
BLOCKS_SCALED = []
for block in BLOCKS:
    BLOCKS_SCALED.append(
        [
            vec(block[0][0] * SCALE, block[0][1] * SCALE),
            vec(block[1][0] * SCALE, block[1][1] * SCALE),
            block[2]
        ]
    )
BLOCKS = BLOCKS_SCALED

# Resize start
START_SCALED = vec(START[0] * SCALE, START[1] * SCALE)
START = START_SCALED
