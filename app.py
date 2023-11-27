import pygame
import sys
from scripts.entities import UFO

class Game:
    def __init__(self):
        # Initialize the Game Window
        pygame.init()
        pygame.display.set_caption("Lagrange Extrapolation")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        # Load UFO images
        self.ufo_images = []
        for i in range(1, 13):
            image_path = f"./data/images/player/idle/{i:02d}_UFO.png"
            image = pygame.image.load(image_path)
            # Scale down the image
            scaled_image = pygame.transform.scale(image, (32, 32))
            self.ufo_images.append(scaled_image)

        # Create UFO instance
        self.ufo = UFO(15, 120, self.ufo_images)
    def run(self):
        while True:
            # Setting Fill
            self.display.fill((0, 0, 0))

            # Listing Event Scenarios
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update
            self.ufo.update()
            # Draw
            self.display.blit(self.ufo.images[self.ufo.current_frame], self.ufo.rect)
            self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(30)  # Decreased the frames per second to 30

Game().run()
