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



































import math
from numpy import angle
import pygame
import sys
import time
import random
from scripts.entities import UFO, Bullet, Earth, PowerUps
from scripts.extrapolation.lagrange_method import Lagrange
import random
import pygame
import sys
import math
import random

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
        self.background_offset = 0
        # Astroid Setup
        self.astroid_images = []
        for i in range(0, 7):
            image_path = f"./Data/images/decors/astroids/{i:02d}_astroid.png"
            image = pygame.image.load(image_path)
            # Randomly generate the scaling of the asteroid image
            scale = random.randint(40, 50), random.randint(40, 50)
            image = pygame.transform.scale(image, scale)
            self.astroid_images.append(image)
        self.angle = 0
        self.rotation_directions = [1, 1, 1, -1, -1]  # Added rotation directions for each asteroid
        # We will now spawn 20 different astroids around the screen
        self.astroids = []
        for i in range(0, 15):
            astroid = pygame.sprite.Sprite()
            astroid.image = self.astroid_images[random.randint(0, len(self.astroid_images) - 1)]
            astroid.rect = astroid.image.get_rect()
            astroid.rect.center = random.randint(50, 480), random.randint(50, 430)
            # Check if the asteroid overlaps with any existing asteroids
            overlapping = False
            for existing_astroid in self.astroids:
                if astroid.rect.colliderect(existing_astroid.rect):
                    overlapping = True
                    class Game:
                        def __init__(self):
                            pygame.init()
                            self.clock = pygame.time.Clock()
                            self.display = pygame.Surface((960, 540))
                            self.screen = pygame.display.set_mode((640, 480))
                            self.font = pygame.font.Font(None, 36)
                            self.background_offset = 0
                            self.angle = 0

                            # Load background images
                            self.background_image = pygame.image.load("./data/images/backdrops/Astralbg.png")
                            self.background_image_reverse = pygame.transform.flip(self.background_image, True, False)

                            # ... rest of the code ...

                        def run(self):
                            while True:
                                # Clearing the Screen
                                self.display.fill((0, 0, 0))

                                # Draw background
                                self.background_offset += 1  # Increase the background offset
                                background_rect = self.background_image.get_rect()
                                background_rect.x -= self.background_offset  # Adjust the x-coordinate based on the offset
                                self.display.blit(self.background_image, background_rect)

                                # Draw reverse background
                                reverse_background_rect = self.background_image_reverse.get_rect()
                                reverse_background_rect.x = background_rect.x + background_rect.width
                                self.display.blit(self.background_image_reverse, reverse_background_rect)

                                # ... rest of the code ...

                                self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
                                pygame.display.update()
                                self.clock.tick(60)  # Decreased the frames per second to 60

                                # ... rest of the code ...

                    if __name__ == "__main__":
                        Game().run()
