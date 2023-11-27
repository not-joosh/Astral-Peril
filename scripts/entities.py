import pygame
class UFO:
    def __init__(self, x, y, images):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.current_frame = 0

    def update(self):
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the direction vector from the UFO to the mouse cursor
        direction = (mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)

        # Set the velocity of the UFO to the direction vector scaled down by a factor
        velocity_factor = 0.1  # Adjust this value to control the speed of the UFO
        self.velocity[0] = direction[0] * velocity_factor
        self.velocity[1] = direction[1] * velocity_factor

        # Update the position of the UFO based on its velocity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Update the current frame of the UFO animation
        self.current_frame = (self.current_frame + 1) % len(self.images)