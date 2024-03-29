import pygame
from settings import *
from collections import deque

right_animation = [
    'img/TiM3.png',
    'img/TiM2.png',
    'img/TiM1.png',
    'img/TiM2.png',
    'img/TiM3.png',
    'img/TiM4.png',
    'img/TiM5.png',
    'img/TiM6.png',
]

left_animation = [
    'img/TiM3LEFT.png',
    'img/TiM2LEFT.png',
    'img/TiM1LEFT.png',
    'img/TiM2LEFT.png',
    'img/TiM3LEFT.png',
    'img/TiM4LEFT.png',
    'img/TiM5LEFT.png',
    'img/TiM6LEFT.png',
]

idle_animation = [

    'img/TiM7LEFT.png',
    'img/TiM7LEFT.png',
    'img/TiM7LEFT.png',
    'img/TiM7LEFT.png',
    'img/TiM7LEFT.png',

    'img/TiM7.png',
    'img/TiM7.png',
    'img/TiM7.png',
    'img/TiM7.png',    
    'img/TiM7.png',
]

class Player(pygame.sprite.Sprite):
    


    def __init__(self, start):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.start = start

        # Create an image of the player, this could also be an image loaded from the disk
        self.image = pygame.image.load('img/TiM.png')
        self.image2 = pygame.image.load('img/Outline.png')
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center = (self.image.get_width()/2, self.image.get_height()))
        self.images_left = self.get_images(left_animation)
        self.images_right = self.get_images(right_animation)
        self.images_idle = self.get_images(idle_animation)

        # self.rect.left = self.rect.left + 10
        # self.rect.right = self.rect.right - 10
        self.position = [start.x, start.y]
        self.velocity = [0, 0]
        self.bounds = []
        self.debug_text = ""

        self.last_update = pygame.time.get_ticks()


    def draw_position(self):
        x = self.position[0]
        y = self.position[1]
        return [x, y]
        

    def get_images(self, path_list):
        images = deque()
        for file_name in path_list:
            img = pygame.image.load(file_name).convert_alpha()
            images.append(img)
        return images        

    def move(self, td, keys, all_sprites, finish_blocks):
        self.bounds = []

        # Apply gravity to player's velocity
        self.velocity[1] += GRAVITY * td    

        finish_hits = pygame.sprite.spritecollide(self, finish_blocks, False)
        if finish_hits:
            return True  
               
        # Check if player is colliding with block
        hits = pygame.sprite.spritecollide(self, all_sprites, False)
        self.debug_text += f"hits: {hits}\n"
        self.debug_text += f"rect: {self.rect}\n"
        
        move_ignore_up = False
        move_ignore_down = False
        move_ignore_left = False
        move_ignore_right = False
        
        
        
        if hits:
            for h in hits:
                # tl = h.rect.collidepoint(self.rect.topleft)
                # tr = h.rect.collidepoint(self.rect.topright)
                # bl = h.rect.collidepoint(self.rect.bottomleft)
                # br = h.rect.collidepoint(self.rect.bottomright)
                
                _t = pygame.Rect(self.rect.left+1, self.rect.top, self.rect.width-2, 1)
                _r = pygame.Rect(self.rect.left+self.rect.width-1, self.rect.top+1, 1, self.rect.height-2)
                _b = pygame.Rect(self.rect.left+1, self.rect.top+self.rect.height-1, self.rect.width-2, 1)
                _l = pygame.Rect(self.rect.left, self.rect.top+1, 1, self.rect.height-2)
                
                self.bounds.append(_t)
                self.bounds.append(_r)
                self.bounds.append(_b)
                self.bounds.append(_l)

                col_t = h.rect.colliderect(_t)
                col_r = h.rect.colliderect(_r)
                col_b = h.rect.colliderect(_b)
                col_l = h.rect.colliderect(_l)
                
                # self.debug_text += f"tl: {tl}\n"
                # self.debug_text += f"tr: {tr}\n"
                # self.debug_text += f"bl: {bl}\n"
                # self.debug_text += f"br: {br}\n"
                
                self.debug_text += f"col_t: {col_t}\n"
                self.debug_text += f"col_r: {col_r}\n"
                self.debug_text += f"col_b: {col_b}\n"
                self.debug_text += f"col_l: {col_l}\n"
                
                if col_t and col_r and col_b and col_l:
                    # Player is inside block
                    self.debug_text += "Player is inside a block\n"

                if not col_t and not col_r and not col_b and not col_l:
                    # Block is in player
                    self.debug_text += "Block is inside a player\n"

                if col_t:
                    # Player is hitting block from bottom
                    move_ignore_up = True
                    
                if col_r:
                    # Player is hitting block from left
                    move_ignore_right = True
                
                if col_b:
                    # Player is hitting block from top
                    move_ignore_down = True
                    
                if col_l:
                    # Player is hitting block from right
                    move_ignore_left = True

                
                # if tl and not tr:
                #     # Player is hitting block from bottom right
                #     move_ignore_left = True
                #     move_ignore_up = True
                
                # if tr:
                #     # Player is hitting block from bottom left
                #     move_ignore_up = True
                #     move_ignore_right = True
                    
                # if br:
                #     # Player is hitting block from top left
                #     move_ignore_down = True
                #     move_ignore_right = True

                # if bl:
                #     # Player is hitting block from top right
                #     move_ignore_left = True
                #     move_ignore_down = True


                # This is elevator 
            # if self.velocity[1] > 0:        

            #     self.velocity[1] = 0
            #     self.position[1] -= 1
            
        self.debug_text += f"move_ignore_up: {move_ignore_up}\n"            
        self.debug_text += f"move_ignore_right: {move_ignore_right}\n"            
        self.debug_text += f"move_ignore_down: {move_ignore_down}\n"            
        self.debug_text += f"move_ignore_left: {move_ignore_left}\n"
            
        if move_ignore_up and self.velocity[1] < 0:
            self.velocity[1] = 0
        if move_ignore_right and self.velocity[0] > 0:
            self.velocity[0] = 0
        if move_ignore_down and self.velocity[1] > 0:
            self.velocity[1] = 0
        if move_ignore_left and self.velocity[0] < 0:
            self.velocity[0] = 0

        # Update player's position based on velocity
        self.position[0] += self.velocity[0] * td
        self.position[1] += self.velocity[1] * td

        cor_t = False
        cor_l = False
        cor_b = False
        cor_r = False

        if move_ignore_left and move_ignore_up:
            cor_r = True
            cor_b = True

        if move_ignore_up and move_ignore_right:
            cor_l = True
            cor_b = True

        if move_ignore_down and move_ignore_right:
            cor_l = True
            cor_t = True

        if move_ignore_down and move_ignore_left:
            cor_r = True
            cor_t = True

        if move_ignore_left and move_ignore_up and move_ignore_right and move_ignore_down:
            cor_r = False
            cor_b = False
            cor_l = False
            
            
        if cor_t:
            self.position[1] -= 1
        if cor_l:
            self.position[0] -= 1
        if cor_b:
            self.position[1] += 1
        if cor_r:
            self.position[0] += 1
        

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

        if keys[pygame.K_ESCAPE]:
            self.position = [self.start.x, self.start.y]
            self.velocity = [0, 0]
        # Check if player is jumping
        if keys[pygame.K_UP] and move_ignore_down:
            self.velocity[1] = jump_strength

        # Check if player is going right
        if keys[pygame.K_RIGHT]:

            if self.velocity[0] < 0:
                self.velocity[0] = 0
            self.velocity[0] += run_acc * td
            if self.velocity[0] > max_run_vel:
                self.velocity[0] = max_run_vel
        
        # Check if player is going left
        if keys[pygame.K_LEFT]:
         
            if self.velocity[0] > 0:
                self.velocity[0] = 0
            self.velocity[0] -= run_acc * td
            if self.velocity[0] < -max_run_vel:
                self.velocity[0] = -max_run_vel
        
        # Update animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= ANIMATION_COOLDOWN:

            self.last_update = current_time
            if keys[pygame.K_RIGHT]:
                self.images_right.rotate(-1)
                self.image = self.images_right[0]
            elif keys[pygame.K_LEFT]:    
                self.images_left.rotate(-1)
                self.image = self.images_left[0]
            else:
                self.images_idle.rotate(-1)
                self.image = self.images_idle[0]
        return False