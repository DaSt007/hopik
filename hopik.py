import pygame
from settings import *
from level01 import *
from blocks import Block
from player import Player

# Initialize pygame
pygame.init()

# Set screen size
s = pygame.display.set_mode((640, 480))

# Set screen caption
pygame.display.set_caption("Hopííík")

vec = pygame.math.Vector2 

player = Player()
playersprite = pygame.sprite.RenderPlain(player)

all_blocksprites = pygame.sprite.Group()
for block in BLOCKS:
    Block(all_blocksprites, lefttop=block[0], rightbottom=block[1], block_type=block[2])

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Arial', 12)

finish_image = pygame.image.load('img/finish7.png')

# Game loop
r = True
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

    player.move(td, keys, all_blocksprites)
    # Draw player
    s.blit(player.image, player.draw_position())
    s.blit(player.image2, player.draw_position())
    
    s.blit(finish_image, FINISH)
    
    for entity in all_blocksprites:
        s.blit(entity.image, entity.rect)

    for bound in player.bounds:        
        pygame.draw.rect(s, (250,150,0), bound)
    
    lines = player.debug_text.splitlines()
    for i, l in enumerate(lines):
        text_surface = my_font.render(l, False, (200, 200, 200))
        s.blit(text_surface, (5,5 + 13 * i))

    # Update screen
    pygame.display.update()

# Quit pygame
pygame.quit()
