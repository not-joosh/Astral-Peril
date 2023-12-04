import pygame
import os
class UFO(pygame.sprite.Sprite):
    def __init__(self, x, y, idle_images, moving_images):
        # Attributes
        # Sprite Images & Position
        self.idle_images = idle_images
        self.moving_images = moving_images
        self.rect = self.idle_images[0].get_rect()
        self.rect.center = (x, y)
        self.current_frame = 0

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

    def update(self):
        # Conditionally Render the UFO's images to be moving or not moving based on self.is_moving boolean
        if self.is_moving:
            self.current_frame = (self.current_frame + 1) % len(self.moving_images)
            self.image = self.moving_images[self.current_frame]
        else:
            self.current_frame = (self.current_frame + 1) % len(self.idle_images)
            self.image = self.idle_images[self.current_frame]
