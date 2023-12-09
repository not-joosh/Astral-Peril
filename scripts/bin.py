import math
from numpy import angle
import pygame
import sys
import time
import random
from scripts.entities import UFO, Bullet, Earth, PowerUps
from scripts.extrapolation.lagrange_method import Lagrange
import random
import math

class Game:
    def __init__(self):
        # Initialize the Game Window
        pygame.init()
        pygame.display.set_caption("Astral Peril")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,36)
        num_of_powerups = 3
        
        # Astroid Setup
        self.astroid_images = []
        for i in range(0, 7):
            image_path = f"./Data/images/decors/astroids/{i:02d}_astroid.png"
            image = pygame.image.load(image_path)
            # Randomly generate the scaling of the asteroid image
            scale = random.randint(40, 50), random.randint(40, 50)
            image = pygame.transform.scale(image, scale)
            self.astroid_images.append(image)
        # ...

        class Game:
            def __init__(self):
                # ...

            def run(self):
                while True:
                    # ...

                    # Check collision with asteroids
                    for asteroid in self.astroids:
                        if self.ufo.rect.colliderect(asteroid.rect):
                            # Calculate the direction of the bounce
                            dx = self.ufo.rect.centerx - asteroid.rect.centerx
                            dy = self.ufo.rect.centery - asteroid.rect.centery
                            direction = math.atan2(dy, dx)

                            # Calculate the new position after the bounce
                            new_x = self.ufo.rect.centerx + math.cos(direction) * 50
                            new_y = self.ufo.rect.centery + math.sin(direction) * 50

                            # Update the UFO position gradually
                            self.ufo.target = (new_x, new_y)
                            self.ufo.is_moving = True

                    # ...

                    # Update the UFO position gradually
                    if self.ufo.is_moving and self.timer > 0 and len(self.ufo.visited_coords) < 15:
                        self.timer -= 1
                        self.ufo.launch(self.ufo.target)  # Mouse Coordinate
                    else:
                        # ...

                    # ...

        if __name__ == "__main__":
            Game().run()
