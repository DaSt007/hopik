import pygame
from time import sleep
from settings import *
from blocks import Block
from player import Player
from importlib import import_module
# Initialize pygame
pygame.init()

# Set screen size
s = pygame.display.set_mode((1400, 480))

# Set screen caption
pygame.display.set_caption("Hopííík")

vec = pygame.math.Vector2 


debug_visible = False
debug_pressed = False
level = 0
level_list = [
    "padaaaas",
    "levelsrovinou",
    "leveldostansekedverim",
    "levelpozornahlavu",
    "levelsorlojem",
    "levelkonec"
]

pygame.font.init() # you have to call this at the start, 
                # if you want to use this module.
my_font = pygame.font.SysFont('Arial', 12)
big_font = pygame.font.SysFont('Arial', 24)


# show welcome screen
s.fill((0,0,0))
lines = WELCOME_TEXT.splitlines()
for i, l in enumerate(lines):
    text_surface = big_font.render(l, False, (200, 200, 200))
    s.blit(text_surface, (50, 50 + 25 * i))
pygame.display.update()
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        break

# Game loop
r = True
while r:

    level_loader = import_module(level_list[level])
    BLOCKS = []
    FINISH = vec(10,10)
    START = vec(15,10)
    INTRO_TEXT = ""
    if hasattr(level_loader, "INTRO_TEXT"):
        INTRO_TEXT = level_loader.INTRO_TEXT

    cnt_y = 0
    for row in level_loader.RAW_BLOCKS:
        cnt_x = 0
        for block in row:
            if block == "S":
                START = vec(cnt_x, cnt_y)
            elif block == "F":
                FINISH = vec(cnt_x, cnt_y)
            elif block == "1":
                BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_SOLID])
            elif block == "2":
                BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_LAVA])
            elif block == "3":
                BLOCKS.append([vec(cnt_x, cnt_y), vec(cnt_x + 1, cnt_y + 1), BLOCK_TYPE_GROUND])
            cnt_x += 1
        cnt_y += 1
            


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
    
    player = Player(START)
    playersprite = pygame.sprite.RenderPlain(player)

    
    all_blocksprites = pygame.sprite.Group()
    for block in BLOCKS:
        Block(all_blocksprites, lefttop=block[0], rightbottom=block[1], block_type=block[2])

    finish_blocks = pygame.sprite.Group()
    Block(finish_blocks, lefttop=FINISH, rightbottom=vec(FINISH.x + 1,FINISH.y + 2), block_type=BLOCK_TYPE_FINISH)

    finish_image = pygame.image.load('img/finish7.png')

    # Initialise clock
    clock = pygame.time.Clock()
    
    # Event loop
    while r:
        # Make sure game doesn't run at more than 60 frames per second
        td = clock.tick(FPS) / 1000
        player.debug_text = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False

        s.fill((0,0,0))
        pygame.display.set_caption(f'{clock.get_fps() :.1f}')
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if not debug_pressed:
                debug_visible = not debug_visible
            debug_pressed = True
        else:
            debug_pressed = False
        
        
        level_finished = player.move(td, keys, all_blocksprites, finish_blocks)
        if level_finished:
            level += 1
            break
        
        # Draw player
        s.blit(player.image, player.draw_position())
        s.blit(player.image2, player.draw_position())
        
        s.blit(finish_image, FINISH)
        
        for entity in all_blocksprites:
            s.blit(entity.image, entity.rect)

        for bound in player.bounds:        
            pygame.draw.rect(s, (250,150,0), bound)
        
        if debug_visible:
            lines = player.debug_text.splitlines()
            for i, l in enumerate(lines):
                text_surface = my_font.render(l, False, (200, 200, 200))
                s.blit(text_surface, (5,5 + 13 * i))

        # Update screen
        pygame.display.update()
        
# Quit pygame
pygame.quit()
