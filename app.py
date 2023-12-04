import pygame
import sys
import time
from scripts.entities import UFO

class Game:
    def __init__(self):
        # Initialize the Game Window
        self.timer = 50
        pygame.init()
        pygame.display.set_caption("Astral Peril")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()

        # Load UFO images
        self.ufo_moving_images = []
        self.ufo_idle_images = []
        for i in range(1, 12):
            image_path = f"./Data/images/player/moving/{i:02d}_UFO.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (50, 50))
            self.ufo_moving_images.append(image)
        for i in range(0, 4):
            image_path = f"./Data/images/player/idle/{i:02d}_UFO.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (50, 50))
            self.ufo_idle_images.append(image)
        self.ufo = UFO(15, 120, self.ufo_idle_images, self.ufo_moving_images)

    def run(self):
        while True:
            # Setting Fill
            self.display.fill((100, 149, 237))
            # Listing Event Scenarios
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse is moving and the mouse button is pressed, launch the UFO
                    if self.ufo.is_moving:
                        self.ufo.is_moving = False
                    else:
                        #set a whie loop that loops ufo.launch until timer for 2 seconds expires
                        self.ufo.is_moving = True
                        self.ufo.target = pygame.mouse.get_pos() 
            # Check if the UFO stopped moving across the screen
            # If it did, set the UFO.is_moving to false
            if self.ufo.is_moving and self.timer > 0:
                self.timer -= 1
                self.ufo.launch(self.ufo.target) # Mouse Coordinate
            else:
                if(self.ufo.is_moving):
                    print(self.ufo.visited_coords)
                    
                    # print length of list for me in python
                    # print(len(self.ufo.visited_coords))
                    # Maybe call lagrange here because it stopped moving here
                    # We would flush, then call lagrange, and shoot the bitch possibly.
                self.ufo.is_moving = False
                self.timer = 50
                
            # Update
            self.ufo.update()

            # Draw
            if self.ufo.is_moving:
                self.display.blit(self.ufo.moving_images[self.ufo.current_frame], self.ufo.rect)
            else:
                self.display.blit(self.ufo.idle_images[self.ufo.current_frame], self.ufo.rect)
            self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)  # Decreased the frames per second to 30
if __name__ == "__main__":
    Game().run()

