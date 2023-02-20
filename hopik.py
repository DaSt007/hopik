import pygame
from level01 import BLOCKS, START, FINISH, GROUND

# Initialize pygame
pygame.init()

# Set screen size
s = pygame.display.set_mode((640, 480))

pygame.display.set_caption("Hopííík")
vec = pygame.math.Vector2 

# Set gravity strength
GRAVITY = 50

SCALE = 16

BLOCKS_SCALED = []
for block in BLOCKS:
    BLOCKS_SCALED.append([vec(block[0][0] * SCALE, block[0][1] * SCALE), vec(block[1][0] * SCALE, block[1][1] * SCALE)])
BLOCKS = BLOCKS_SCALED

GROUND_SCALED = ([vec(GROUND[0][0] * SCALE, GROUND[0][1] * SCALE), vec(GROUND[1][0] * SCALE, GROUND[1][1] * SCALE)])
GROUND = GROUND_SCALED

START_SCALED = vec(START[0] * SCALE, START[1] * SCALE)
START = START_SCALED

# Set jumping strength
jump_strength = -80

max_run_vel = 100

run_acc = 400
run_dec = 400


# Set ground level
GROUND_LEVEL = 480

FPS = 60

class Block(pygame.sprite.Sprite):

    def __init__(self, group, lefttop, rightbottom):
        pygame.sprite.Sprite.__init__(self, group)
        size = rightbottom - lefttop 
        self.image = pygame.Surface(size)
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(topleft=lefttop, bottomright=rightbottom)

class Ground(pygame.sprite.Sprite):

    def __init__(self, group, lefttop, rightbottom):
        pygame.sprite.Sprite.__init__(self, group)
        size = rightbottom - lefttop 
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 200))
        self.rect = self.image.get_rect(topleft=lefttop, bottomright=rightbottom)

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
        'img/TiM1.png',
        'img/TiM2.png',
        'img/TiM3.png',
        'img/TiM4.png',
        'img/TiM5.png',
        'img/TiM6.png',
        'img/TiM7.png',
    ]

    images2 = [
        'img/TiM1LEFT.png',
        'img/TiM2LEFT.png',
        'img/TiM3LEFT.png',
        'img/TiM4LEFT.png',
        'img/TiM5LEFT.png',
        'img/TiM6LEFT.png',
        'img/TiM7LEFT.png',
    ]

    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('img/TiM.png')

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center = (self.image.get_width()/2, self.image.get_height()))
        self.position = [START.x, START.y]
        self.velocity = [0, 0]

    def draw_position(self):
        x = self.position[0] + self.image.get_width()/2
        y = self.position[1] - self.image.get_height()
        return [x, y]
        
        

    def move(self, td, keys, all_sprites):
            
        # Apply gravity to player's velocity
        self.velocity[1] += GRAVITY * td
       
        # Update player's position based on velocity
        self.position[0] += self.velocity[0] * td
        self.position[1] += self.velocity[1] * td
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
        hits = pygame.sprite.spritecollide(self, all_sprites, False)
        print(hits, self.rect)
        
        if self.velocity[1] > 0:        
            if hits:
                # Check if player is colliding with ground
                self.velocity[1] = 0
                self.position[1] -= 1
            if self.position[1] > GROUND_LEVEL:
                self.position[1] = GROUND_LEVEL
                self.velocity[1] = 0
                
        if self.velocity[0] > 0 and not keys[pygame.K_RIGHT]:
            self.velocity[0] -= run_dec * td
            if self.velocity[0] < 0:
                self.velocity[0] = 0
                
        if self.velocity[0] < 0 and not keys[pygame.K_LEFT]:
            self.velocity[0] += run_dec * td
            if self.velocity[0] > 0:
                self.velocity[0] = 0

        # Check if player is jumping

        if keys[pygame.K_UP] and self.position[1] == GROUND_LEVEL:
            self.velocity[1] = jump_strength
        # Check if player is going right
        elif keys[pygame.K_RIGHT]:
            self.image = pygame.image.load(self.images[self.counter])
            self.counter = (self.counter + 1) % len(self.images)
    
            if self.velocity[0] < 0:
                self.velocity[0] = 0
            self.velocity[0] += run_acc * td
            if self.velocity[0] > max_run_vel:
                self.velocity[0] = max_run_vel
        # Check if player is going left
        elif keys[pygame.K_LEFT]:
            self.image = pygame.image.load(self.images2[self.counter])
            self.counter = (self.counter + 1) % len(self.images2)
            
            if self.velocity[0] > 0:
                self.velocity[0] = 0
            self.velocity[0] -= run_acc * td
            if self.velocity[0] < -max_run_vel:
                self.velocity[0] = -max_run_vel
        
        # elif self.position[1] != hits:
        #     self.image = pygame.image.load('img/TiM.png')
                
        else:
            self.image = pygame.image.load('img/TiM.png')




player = Player()
# layer = Layer()
playersprite = pygame.sprite.RenderPlain(player)
# layersprite = pygame.sprite.RenderPlain(layer)

all_blocksprites = pygame.sprite.Group()
for block in BLOCKS:
    Block(all_blocksprites, lefttop=block[0], rightbottom=block[1])

Ground(all_blocksprites, lefttop=GROUND[0], rightbottom=GROUND[1])
    
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
       
    player.move(td, keys, all_blocksprites)
    # Draw player
    # s.blit(player.image, player.position)
    s.blit(player.image, player.draw_position())
    
    for entity in all_blocksprites:
        s.blit(entity.image, entity.rect)
    # Update screen
    pygame.display.update()

# Quit pygame
pygame.quit()
