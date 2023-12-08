import pygame
import random
import math 
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

        # Step 5: Add the UFO's current position to the visited_coords list
        self.visited_coords.append(self.rect.center)

        # Step 6: Update the UFO's position
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
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Attributes
        # Sprite Image & Position
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [-10,0]
        self.aimed.y = 0
        # self.collide = pygame.rect.colliderect(self.ufo.rect)
    def extrapolate_next(self, x, data_points): #using Lagrange for AI attacks
        needs_sum = []   # mutable list of Li(x0)(), Li(x1)(), Li(x2)(), Li(x3)()
        for i in range(data_points.__len__()):
            prodOfLi_n = 1
            temp = 1
            for j in range(data_points.__len__()):
                if i != j: 
                    prodOfLi_n *= (x - data_points[j][0]) / (data_points[i][0] - data_points[j][0])
                    temp = prodOfLi_n * data_points[i][1] # Li * fx
            needs_sum.append(temp)
        fx = 0
        for i in range(needs_sum.__len__()):
            fx += needs_sum[i]
        self.rect.center = (int(x) + self.velocity[0], int(fx) + self.velocity[1])
        self.rect.x = int(x)
        self.aimed.y = int(fx)

        #return result
    
    def update(self):
        # Update the enemy's position or state
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x <= 0:
            self.rect.x = 640
            self.rect.y = random.randint(50, 480 - 50)
        pass

# class PowerUp(pygame.sprite.Sprite):
#     def __init__(self, x, y, image):
#         # Attributes
#         # Sprite Image & Position
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def generate(SCREEN_WIDTH, SCREEN_HEIGHT, image):
#         # Create enemy birds
# #enemy_birds = pygame.sprite.Group()
#      for _ in range(5):
#         x = random.randint(640 // 2, 480 - 50)
#         y = random.randint(50, 480 - 50)
#         #enemy_bird = Bird(x, y, image)
#         #enemy_birds.add(enemy_bird)

#     def apply_power(self, player):
#         # Apply power to the player
#         pass

#     def update(self):
#         # Update the power-up's position or state
#         pass
    


