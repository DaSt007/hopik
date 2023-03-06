import pygame
from level01 import BLOCKS, START, FINISH, BLOCK_TYPE_SOLID, BLOCK_TYPE_GROUND, BLOCK_TYPE_ELEVATOR

# Initialize pygame
pygame.init()

# Set screen size
s = pygame.display.set_mode((640, 480))

# Set screen caption
pygame.display.set_caption("Hopííík")

vec = pygame.math.Vector2 

# Set gravity strength
GRAVITY = 100

# Set player and block scale
SCALE = 16

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

# Set jumping strength(negative number)
jump_strength = -80

# Set max speed
max_run_vel = 100

# Set aceleracion
run_acc = 400

# Set deceleration
run_dec = 400

# Set FPS of game
FPS = 60


class Block(pygame.sprite.Sprite):
    def __init__(self, group, lefttop, rightbottom, block_type):
        pygame.sprite.Sprite.__init__(self, group)
        size = rightbottom - lefttop 
        self.image = pygame.Surface(size)

        if block_type == BLOCK_TYPE_GROUND:
            self.image.fill((0, 0, 200))
        elif block_type == BLOCK_TYPE_SOLID:
            self.image.fill((0, 200, 0))
        elif block_type == BLOCK_TYPE_ELEVATOR:
            self.image.fill((200, 0, 0))
        else:
            self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect(topleft=lefttop, bottomright=rightbottom)


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

        # Create an image of the player, this could also be an image loaded from the disk
        self.image = pygame.image.load('img/TiM.png')
        self.image2 = pygame.image.load('img/Outline.png')
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center = (self.image.get_width()/2, self.image.get_height()))
        
        # self.rect.left = self.rect.left + 10
        # self.rect.right = self.rect.right - 10
        self.position = [START.x, START.y]
        self.velocity = [0, 0]

    def draw_position(self):
        x = self.position[0]
        y = self.position[1]
        return [x, y]
        
        

    def move(self, td, keys, all_sprites):
        self.image = pygame.image.load('img/TiM.png')

        # Apply gravity to player's velocity
        self.velocity[1] += GRAVITY * td    
              
        # Check if player is colliding with block
        hits = pygame.sprite.spritecollide(self, all_sprites, False)
        print(hits, self.rect)
        
        move_ignore_up = False
        move_ignore_down = False
        move_ignore_left = False
        move_ignore_right = False
        
        
        if hits:
            for h in hits:
                tl = h.rect.collidepoint(self.rect.topleft)
                tr = h.rect.collidepoint(self.rect.topright)
                bl = h.rect.collidepoint(self.rect.bottomleft)
                br = h.rect.collidepoint(self.rect.bottomright)
                
                col_t = h.rect.colliderect(pygame.Rect(self.rect.top+1, self.rect.left+1, self.rect.width-2, 0))
                col_r = h.rect.colliderect(pygame.Rect(self.rect.top+1, self.rect.left+1+self.rect.width, 0, self.rect.height-2))
                col_b = h.rect.colliderect(pygame.Rect(self.rect.top+1+self.rect.height, self.rect.left+1, self.rect.width-2, 0))
                col_l = h.rect.colliderect(pygame.Rect(self.rect.top+1, self.rect.left+1, 0, self.rect.height-2))
                
                
                print(tl, tr, bl, br)
                if tl and tr and bl and br:
                    # Player is inside block
                    print("Player is inside a block")
                    pass
                
                elif col_t or (tl and tr):
                    # Player is hitting block from bottom
                    move_ignore_up = True
                    
                elif col_r or (tr and br):
                    # Player is hitting block from left
                    move_ignore_right = True
                
                elif col_b or (br and bl):
                    # Player is hitting block from top
                    move_ignore_down = True
                    
                elif col_l or (tl and bl):
                    # Player is hitting block from right
                    move_ignore_left = True
                
                elif tl:
                    # Player is hitting block from bottom right
                    move_ignore_left = True
                    move_ignore_up = True
                
                elif tr:
                    # Player is hitting block from bottom left
                    move_ignore_up = True
                    move_ignore_right = True
                    
                elif br:
                    # Player is hitting block from top left
                    move_ignore_down = True
                    move_ignore_right = True
                
                elif bl:
                    # Player is hitting block from top right
                    move_ignore_left = True
                    move_ignore_down = True
                
                else:
                    # Block is in player
                    print("Block is inside a player")
                    exit
                # This is elevator 
            # if self.velocity[1] > 0:        

            #     self.velocity[1] = 0
            #     self.position[1] -= 1
            
            

        # Update player's position based on velocity
        dx = self.velocity[0] * td
        dy = self.velocity[1] * td
        
        if dx > 0:
            # Moving right
            if move_ignore_right:
                dx = 0  
                          
        if dx < 0:
            # Moving left
            if move_ignore_left:
                dx = 0  
                          
        if dy > 0:
            # Moving down
            if move_ignore_down:
                dy = 0     
                       
        if dy < 0:
            # Moving up
            if move_ignore_up:
                dy = 0            
        
        
        
        self.position[0] += dx
        self.position[1] += dy

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
        
        
        
        
        # Check if player is decelerating    
        if self.velocity[0] > 0 and not keys[pygame.K_RIGHT]:
            self.velocity[0] -= run_dec * td
            if self.velocity[0] < 0:
                self.velocity[0] = 0
                
        # Check if player is decelerating
        if self.velocity[0] < 0 and not keys[pygame.K_LEFT]:
            self.velocity[0] += run_dec * td
            if self.velocity[0] > 0:
                self.velocity[0] = 0

        # Check if player is jumping
        if keys[pygame.K_UP]:
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
                




player = Player()
playersprite = pygame.sprite.RenderPlain(player)

all_blocksprites = pygame.sprite.Group()
for block in BLOCKS:
    Block(all_blocksprites, lefttop=block[0], rightbottom=block[1], block_type=block[2])


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

    s.fill((0,0,0))

    keys = pygame.key.get_pressed()
       
    player.move(td, keys, all_blocksprites)
    # Draw player
    s.blit(player.image, player.draw_position())
    s.blit(player.image2, player.draw_position())
    
    for entity in all_blocksprites:
        s.blit(entity.image, entity.rect)
    # Update screen
    pygame.display.update()

# Quit pygame
pygame.quit()
