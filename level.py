import pygame
from settings import *
from levelpozornahlavu import RAW_BLOCKS
vec = pygame.math.Vector2


BLOCKS = []
FINISH = vec(33,8)
START = vec(2,12)

cnt_y = 0
for row in RAW_BLOCKS:
    cnt_x = 0
    for block in row:
        if block == "S":
            START = vec(cnt_x, cnt_y)
        if block == "F":
            FINISH = vec(cnt_x, cnt_y)
        elif block == "1":
            BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_SOLID])
        elif block == "2":
            BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_ELEVATOR])
        elif block == "3":
            BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_GROUND])
        cnt_x += 1
    cnt_y += 1
        

# BLOCKS = [
#     [vec(0,15), vec(41,16), BLOCK_TYPE_GROUND],
#     [vec(0,0), vec(1,15), BLOCK_TYPE_GROUND],
#     [vec(38,10), vec(40,15), BLOCK_TYPE_GROUND],
#     [vec(10,14), vec(11,15), BLOCK_TYPE_SOLID],
#     [vec(13,13), vec(14,14), BLOCK_TYPE_ELEVATOR],
#     [vec(16,12), vec(20,13), BLOCK_TYPE_SOLID],
#     # [vec(16,13), vec(17,15), BLOCK_TYPE_SOLID],
#     [vec(23,11), vec(26,12), BLOCK_TYPE_SOLID],
#     [vec(28,10), vec(34,11), BLOCK_TYPE_SOLID],
# ]


# START = vec(15,5)


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

FINISH_SCALED = vec(FINISH[0] * SCALE, FINISH[1] * SCALE)
FINISH = FINISH_SCALED