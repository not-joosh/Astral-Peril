import pygame
import sys
import time
from scripts.entities import UFO, Bullet, Earth, PowerUps
from scripts.extrapolation.lagrange_method import Lagrange



class Game:
    def __init__(self):
        # Initialize the Game Window
        pygame.init()
        pygame.display.set_caption("Astral Peril")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,36)

        # Game Prompts
        self.level_clear = self.font.render("MISSION SUCCESS", True, (255, 255, 255))
        self.level_clear_rect = self.level_clear.get_rect(center=(640 // 2, 480 // 2))
        self.level_fail = self.font.render("MISSION FAILED", True, (255, 255, 255))
        self.level_fail_rect = self.level_fail.get_rect(center=(640 // 2, 480 // 2))

        #Load powerups
        self.powerups_images = []
        for i in range(0, 4):
            image_path = f"./Data/images/powerups/shield/{i}power.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (30, 30))
            image.set_colorkey((255, 255, 255))  # Set white color as transparent
            self.powerups_images.append(image.convert_alpha())
        self.powerups = PowerUps(self.powerups_images)
        self.powerup_sound = pygame.mixer.Sound("./data/sounds/powerup_fx.mp3")

        # Earth Asset
        image = pygame.image.load("./data/images/player/earth.png")
        self.earth_image = pygame.transform.scale(image, (960, 540))
        self.earth = Earth(750,240, self.earth_image)
       
        # Load Bullet images
        self.bullet_moving_images = []
        for i in range(0, 3):
            image_path = f"./Data/images/effects/bullet/{i:02d}_bullet.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (20, 20))
            self.bullet_moving_images.append(image)  
        self.bullet = Bullet(640, 220, self.bullet_moving_images)
        self.bullet_sound = pygame.mixer.Sound("./data/sounds/bullet_fx.mp3")
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

        #Load music
        pygame.mixer.music.load("./data/sounds/bgMusic.mp3")
        pygame.mixer.music.play(-1)

        
        # Main menu
        self.start_button = pygame.Rect(270, 220, 100, 50)  # x, y, width, height
        self.start_button_color = (0,0,139)  # Dark blue
        self.start_game = False

    def render_main_menu(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        pygame.draw.rect(self.screen, self.start_button_color, self.start_button)  # Draw the start button
        
    # Render the text on the start button
        start_text = self.font.render("START", True, (0, 255, 0))
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)
        # Game Mechanic Variables
        self.timer = 50
    
    def run(self):
        while True:
            self.display.fill((255, 255, 255))
            if self.start_game:
            # Clearing the Screen
            
                
                
                # Game Events
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

                # Check if the UFO stopped moving across the screen. If it did, set the UFO.is_moving to false
                if self.ufo.is_moving and self.timer > 0 and len(self.ufo.visited_coords) < 15:
                    self.timer -= 1
                    self.ufo.launch(self.ufo.target) # Mouse Coordinate
                else:
                    # If it is not moving anymore or if there is more than 15 data points, then we will
                    # perform extrapolation and shoot down the UFO. We will then clear the UFO visited lsit
                    if(self.ufo.is_moving or len(self.ufo.visited_coords) > 15): 
                        filtered_data = self.ufo.visited_coords[-9:-2]
                        prediction = Lagrange.extrapolate_next(self, self.ufo.visited_coords[-1][0], filtered_data)
                        self.bullet.fire_towards(prediction[1])
                        filtered_data.clear()
                    self.ufo.is_moving = False
                    self.timer = 50
                    self.ufo.visited_coords.clear()


                # Checking if bullet collision worked    
                if self.bullet.rect.colliderect(self.ufo.rect): 
                    if self.ufo.armor == 0 or self.bullet.count >5: 
                        print("hit!")
                        self.ufo.defeat = 1 
                        self.bullet.count = 0
                    else:
                        self.bullet.count += 1    
                # Update
                self.ufo.update()
                self.bullet.update()
                self.powerups.update()
                
                # Check if powerup was collected
                if self.ufo.rect.colliderect(self.powerups.rect):
                    self.powerup_sound.play()
                    self.powerups.collected = True
                    self.ufo.armor = 1
                    self.bullet.count = 0
                    self.powerups.rect.center = (0,0)
                    print("powerup collected")
                    
                # Draw
                self.display.blit(pygame.image.load("./data/images/backdrops/Astralbg.png"), (0,0))
                self.display.blit(self.earth.image, self.earth.rect)
                if self.powerups.collected == False:
                    self.display.blit(self.powerups.images[self.powerups.current_frame], self.powerups.rect)
                if self.ufo.defeat == 0 and self.ufo.victory == 0:
                    if(self.bullet.rect.center[0] == 640):
                        self.bullet_sound.play()
                    self.display.blit(self.bullet.image, self.bullet.rect)
                    if self.ufo.is_moving:
                        self.display.blit(self.ufo.moving_images[self.ufo.current_frame], self.ufo.rect)
                    else:
                        self.display.blit(self.ufo.idle_images[1], self.ufo.rect)
                elif self.ufo.defeat == 1:
                    self.display.blit(self.level_fail, self.level_fail_rect)
                elif self.ufo.victory == 1:
                    self.display.blit(self.level_clear, self.level_clear_rect)
            else:
                self.render_main_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.start_button.collidepoint(mouse_pos):
                            self.start_game = True
                pygame.display.update()    
                self.clock.tick(30)  # Decreased the frames per second to 60
            self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)  # Decreased the frames per second to 60
if __name__ == "__main__":
    Game().run()