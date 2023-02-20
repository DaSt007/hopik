import pygame
from level01 import BLOCKS, START, FINISH, GROUND

# Initialize pygame
pygame.init()

# Set screen size
s = pygame.display.set_mode((640, 480))

pygame.display.set_caption("Hopííík")

# Set gravity strength
GRAVITY = 50

# Set jumping strength
jump_strength = -80

max_run_vel = 100

run_acc = 400
run_dec = 400

vec = pygame.math.Vector2 

# Set ground level
GROUND_LEVEL = 480

FPS = 60

class Block(pygame.sprite.Sprite):

    def __init__(self, group, lefttop, rightbottom):
        pygame.sprite.Sprite.__init__(self, group)
        size = rightbottom - lefttop 
        self.image = pygame.Surface(size * 32)
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(topleft=lefttop * 32, bottomright=rightbottom * 32)


# class Layer(pygame.sprite.Sprite):
#     def __init__(self):
#         # Call the parent class (Sprite) constructor
#         pygame.sprite.Sprite.__init__(self)

#         # Create an image of the block, and fill it with a color.
#         # This could also be an image loaded from the disk.
#         self.image = pygame.image.load('l2mask.png')

#         # Fetch the rectangle object that has the dimensions of the image
#         # Update the position of this object by setting the values of rect.x and rect.y
#         self.rect = self.image.get_rect()
#         self.mask = pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    counter = 1

    images = [
        'img/TIM1.png',
        'img/TIM2.png',
        'img/TIM3.png',
        'img/TIM4.png',
        'img/TIM5.png',
        'img/TIM6.png',
        'img/TIM7.png',
    ]

    images2 = [
        'img/TIM1LEFT.png',
        'img/TIM2LEFT.png',
        'img/TIM3LEFT.png',
        'img/TIM4LEFT.png',
        'img/TIM5LEFT.png',
        'img/TIM6LEFT.png',
        'img/TIM7LEFT.png',
    ]

    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('img/TIM.png')

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center = (self.image.get_width()/2, self.image.get_height()))
        self.position = [320, 240]
        self.velocity = [0, 0]

    def draw_position(self):
        x = self.position[0] + self.image.get_width()/2
        y = self.position[1] - self.image.get_height()
        return [x, y]
        
        

    def move(self, td, keys, all_sprites):
            
        # Apply gravity to player's velocity
        player.velocity[1] += GRAVITY * td
       
        # Update player's position based on velocity
        player.position[0] += player.velocity[0] * td
        player.position[1] += player.velocity[1] * td

        # hits = pygame.sprite.spritecollide(self, all_sprites, False)
        
        if self.velocity[1] > 0:        
            # if hits:
            #     # Check if player is colliding with ground
            #     player.velocity[1] = 0
            if player.position[1] > GROUND_LEVEL:
                player.position[1] = GROUND_LEVEL
                player.velocity[1] = 0
                
        if player.velocity[0] > 0 and not keys[pygame.K_RIGHT]:
            player.velocity[0] -= run_dec * td
            if player.velocity[0] < 0:
                player.velocity[0] = 0
                
        if player.velocity[0] < 0 and not keys[pygame.K_LEFT]:
            player.velocity[0] += run_dec * td
            if player.velocity[0] > 0:
                player.velocity[0] = 0

        # Check if player is jumping

        if keys[pygame.K_UP] and player.position[1] == GROUND_LEVEL:
            player.velocity[1] = jump_strength
        # Check if player is going right
        elif keys[pygame.K_RIGHT]:
            self.image = pygame.image.load(self.images[self.counter])
            self.counter = (self.counter + 1) % len(self.images)
    
            if player.velocity[0] < 0:
                player.velocity[0] = 0
            player.velocity[0] += run_acc * td
            if player.velocity[0] > max_run_vel:
                player.velocity[0] = max_run_vel
        # Check if player is going left
        elif keys[pygame.K_LEFT]:
            self.image = pygame.image.load(self.images2[self.counter])
            self.counter = (self.counter + 1) % len(self.images2)
            
            if player.velocity[0] > 0:
                player.velocity[0] = 0
            player.velocity[0] -= run_acc * td
            if player.velocity[0] < -max_run_vel:
                player.velocity[0] = -max_run_vel
        
        # elif player.position[1] != hits:
        #     self.image = pygame.image.load('img/TIM.png')
                
        else:
            self.image = pygame.image.load('img/TIM.png')




player = Player()
# layer = Layer()
playersprite = pygame.sprite.RenderPlain(player)
# layersprite = pygame.sprite.RenderPlain(layer)

all_blocksprites = pygame.sprite.Group()
for block in BLOCKS:
    Block(all_blocksprites, lefttop=block[0], rightbottom=block[1])
    
# all_sprites = pygame.sprite.Group()
# all_sprites.add(layer)


# Game loop
r = True
# Initialise clock
clock = pygame.time.Clock()
# Event loop
while r:
    # Make sure game doesn't run at more than 60 frames per second
    td = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False

    # playersprite.draw(s)
    # layersprite.draw(s)

    s.fill((0,0,0))

    keys = pygame.key.get_pressed()
    
    print(player.velocity[1])
    
    # player.move(td, keys, all_sprites)
    # Draw player
    # s.blit(player.image, player.position)
    s.blit(player.image, player.draw_position())
    
    for entity in all_blocksprites:
        s.blit(entity.image, entity.rect)
    # Update screen
    pygame.display.update()

# Quit pygame
pygame.quit()
