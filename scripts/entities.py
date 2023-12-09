import pygame
import random
import math 

class Earth(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Attributes
        # Sprite Image & Position
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 100
        self.defeat = 0

class UFO(pygame.sprite.Sprite):
    def __init__(self, x, y, idle_images, moving_images):
        # Attributes
        # Sprite Images & Position
        self.idle_images = idle_images
        self.moving_images = moving_images
        self.rect = self.idle_images[0].get_rect()
        self.rect.center = (x, y)
        self.current_frame = 0
        self.victory = 0
        self.defeat = 0
        # Physics Attributes
        self.velocity = [0, 0]

        # Movement Attributes
        self.is_moving = False
        self.visited_coords = []

        # Attributes
        self.armor = 0
        # self.health = 100

    def launch(self, mouse_pos):
        # Step 1: Cap the UFO's speed, the velocity can vary, based on the how far the mouse is from the UFO
        max_speed = 5

        # Step 2: Calculate the UFO's velocity based on the mouse's position
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        distance = max(1, ((dx ** 2) + (dy ** 2)) ** 0.5)
        velocity_x = (dx / distance) * max_speed
        velocity_y = (dy / distance) * max_speed
        
        # Step 3: Set the UFO's velocity
        self.velocity = [velocity_x, velocity_y]

        # Step 4: Set the UFO's is_moving boolean to True
        self.is_moving = True

        # Step 5: Check if the current x value is already in the visited_coords list
        current_x = self.rect.centerx
        if current_x not in [coord[0] for coord in self.visited_coords]:
            # Step 6: Add the UFO's current position to the visited_coords list
            self.visited_coords.append((self.rect.centerx, self.rect.centery))

        # Step 7: Update the UFO's position
        self.rect.center = (self.rect.centerx + self.velocity[0], self.rect.centery + self.velocity[1])
        if self.rect.center[0] >= 536:
            self.victory = 1 
    def update(self):
        # Conditionally Render the UFO's images to be moving or not moving based on self.is_moving boolean
        if self.is_moving:
            self.current_frame = (self.current_frame + 1) % len(self.moving_images)
            self.image = self.moving_images[self.current_frame]
        else:
            self.current_frame = (self.current_frame + 1) % len(self.idle_images)
            self.image = self.idle_images[self.current_frame]
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        # Attributes
        # Sprite Image & Position
        self.images = images
        self.current_frame = 0
        self.rect = self.images[0].get_rect()
        self.rect.center = (x, y)
        self.velocity = [-10,0]
        
        # self.collide = pygame.rect.colliderect(self.ufo.rect)
        self.count = 0
    def fire_towards(self, y_in):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x <= 0:
            self.rect.x = 640
            self.rect.y = y_in
    def update(self):
        # Update the enemy's position or state
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image = self.images[self.current_frame]

class PowerUps(pygame.sprite.Sprite):
    def __init__(self, images):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.current_frame = 0
        self.collected = False
        self.rect.center = random.randint(640 // 2, 480 - 50), random.randint(50, 480 - 50)

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image = self.images[self.current_frame]