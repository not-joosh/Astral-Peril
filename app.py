import pygame
import sys
import time
from scripts.entities import UFO, Enemy

class Game:
    def __init__(self):
        # Initialize the Game Window
        self.timer = 50
        pygame.init()
        pygame.display.set_caption("Astral Peril")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,36)
        self.level_clear = self.font.render("MISSION SUCCESS", True, (255, 255, 255))
        self.level_clear_rect = self.level_clear.get_rect(center=(640 // 2, 480 // 2))
        self.level_fail = self.font.render("MISSION FAILED", True, (255, 255, 255))
        self.level_fail_rect = self.level_fail.get_rect(center=(640 // 2, 480 // 2))
        image = pygame.image.load("./data/images/player/earth.png")
        self.earth_image = pygame.transform.scale(image, (960, 540))
        self.earth = Enemy(750,240, self.earth_image)
        image = pygame.image.load("./data/images/effects/bullet/03_bullet.png")
        self.attack_image = pygame.transform.scale(image, (20, 20))
        self.attack = Enemy(640,220, self.attack_image)
        # Load UFO images
        self.ufo_moving_images = []
        self.ufo_idle_images = []
        for i in range(1, 12):
            image_path = f"./Data/images/player/moving/{i:02d}_UFO.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (30, 30))
            self.ufo_moving_images.append(image)
        for i in range(0, 4):
            image_path = f"./Data/images/player/idle/{i:02d}_UFO.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (30, 30))
            self.ufo_idle_images.append(image)
        self.ufo = UFO(15, 120, self.ufo_idle_images, self.ufo_moving_images)

    def run(self):
        while True:
            # Setting Fill
            self.display.fill((0, 0, 0))
            # Listing Event Scenarios
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.ufo.defeat == 0:
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
            # if self.attack.collide == True:
            #     print("hit!")
            else:
                if(self.ufo.is_moving):
                    print(self.ufo.visited_coords)
  
                    # print length of list for me in python
                    # print(len(self.ufo.visited_coords))
                    # Maybe call lagrange here because it stopped moving here
                    # We would flush, then call lagrange, and shoot the bitch possibly.
                self.ufo.is_moving = False
                self.timer = 50
            if self.attack.rect.colliderect(self.ufo.rect):
                print("hit!")
                self.ufo.defeat = 1    
            # Update
            self.ufo.update()
            self.attack.update()

            # Draw
            self.display.blit(self.earth.image, self.earth.rect)
            
            if self.ufo.defeat == 0 and self.ufo.victory == 0:
                self.display.blit(self.attack.image, self.attack.rect)
                if self.ufo.is_moving:
                    self.display.blit(self.ufo.moving_images[self.ufo.current_frame], self.ufo.rect)
                else:
                    self.display.blit(self.ufo.idle_images[1], self.ufo.rect)
            elif self.ufo.defeat == 1:
                self.display.blit(self.level_fail, self.level_fail_rect)
            elif self.ufo.victory == 1:
                self.display.blit(self.level_clear, self.level_clear_rect)

            self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)  # Decreased the frames per second to 60
if __name__ == "__main__":
    Game().run()

