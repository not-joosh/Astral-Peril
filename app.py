import math
from numpy import angle
import pygame
import sys
import time
import random
from scripts.entities import UFO, Bullet, Earth, PowerUps
from scripts.extrapolation.lagrange_method import Lagrange
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
                    break
            # If the asteroid overlaps, generate new random coordinates
            while overlapping:
                astroid.rect.center = random.randint(50, 480), random.randint(50, 430)
                overlapping = False
                for existing_astroid in self.astroids:
                    if astroid.rect.colliderect(existing_astroid.rect):
                        overlapping = True
                        break
            self.astroids.append(astroid)
        self.rotation_directions = [1, 1, 1, -1, -1] * (len(self.astroids) // len(self.rotation_directions))
        self.rotation_directions += [1] * (len(self.astroids) % len(self.rotation_directions))

        #Load powerups
        self.powerups_images = []
        for i in range(0, 4):
            image_path = f"./Data/images/powerups/shield/{i}power.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (30, 30))
            image.set_colorkey((255, 255, 255))  # Set white color as transparent
            self.powerups_images.append(image.convert_alpha())
        self.powerups = []
        for _ in range(num_of_powerups):
            powerup = PowerUps(self.powerups_images)
            # Check if the powerup overlaps with any existing asteroids
            overlapping = True
            while overlapping:
                powerup.rect.center = random.randint(50, 480), random.randint(50, 430)
                overlapping = False
                for asteroid in self.astroids:
                    if powerup.rect.colliderect(asteroid.rect):
                        overlapping = True
                        break
            self.powerups.append(powerup)
            
        # Game Prompts
        self.level_clear = self.font.render("MISSION SUCCESS", True, (255, 255, 255))
        self.level_clear_rect = self.level_clear.get_rect(center=(640 // 2, 480 // 2))
        self.level_fail = self.font.render("MISSION FAILED", True, (255, 255, 255))
        self.level_fail_rect = self.level_fail.get_rect(center=(640 // 2, 480 // 2))

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
            image = pygame.transform.rotate(image, 180)  # Rotate the image 180 degrees
            self.bullet_moving_images.append(image)  
        self.bullet = Bullet(-20, 220, self.bullet_moving_images)  # Set initial position of bullet off-screen

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
        self.ufo = UFO(15, 232, self.ufo_idle_images, self.ufo_moving_images)

        # Game Mechanic Variables
        self.timer = 50
        
        # Load Music & Sound Effects
        pygame.mixer.music.load("./Data/sounds/bg-music/bgMusic.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set the volume to 50% (adjust as needed)
        pygame.mixer.music.play(-1)
        self.sound_effects = {
            "bullet": pygame.mixer.Sound("./Data/sounds/sound-fx/bullet_fx.mp3"),
            "powerup": pygame.mixer.Sound("./Data/sounds/sound-fx/powerup_fx.mp3"),
            # "bullet": pygame.mixer.Sound("./Data/sounds/effects/bullet.wav"),
            # "powerup": pygame.mixer.Sound("./Data/sounds/effects/powerup.wav"),
            # "victory": pygame.mixer.Sound("./Data/sounds/effects/victory.wav"),
            # "defeat": pygame.mixer.Sound("./Data/sounds/effects/defeat.wav")
        }
    def run(self):
        while True:

            # Clearing the Screen
            self.display.fill((0, 0, 0))
            
            
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
                    if prediction[1] <= 500: # Already reached earth, lets not shoot it if its greater than 530
                        self.bullet.fire_towards(prediction[1])
                    # Printing the Lagrange Shooting Prediction
                    print("\n--------------------------------\n\tLAGRANGE SHOOTING")
                    print("\tPREDICTION: ", prediction)
                    print("\tEXPECTED: ", self.ufo.rect.center, "\n--------------------------------\n\t")
                    
                    filtered_data.clear()
                self.ufo.is_moving = False
                self.timer = 50
                self.ufo.visited_coords.clear()


            # Checking if bullet collision worked    
            if self.bullet.rect.colliderect(self.ufo.rect):
                if self.ufo.armor == 0 or self.bullet.count is 1: 
                    print("hit!")
                    self.ufo.defeat = 1 
                    self.bullet.count = 0
                else:
                    self.bullet.count = 1    # Increments Bullet Count
                    self.bullet.rect.x = -20 # Resets the Bullet




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
            
            
            # Update
            self.ufo.update()
            self.bullet.update()
            for powerup in self.powerups:
                powerup.update()
            
            # Check if powerup was collected
            for powerup in self.powerups:
                if self.ufo.rect.colliderect(powerup.rect):
                    powerup.collected = True
                    self.ufo.armor = 1
                    self.bullet.count = 0
                    powerup.rect.center = (0, 0)
                    # We need to reset the bullet position
                    print("Powerup collected")
                    self.sound_effects["powerup"].play()


            # Draw
            self.display.blit(pygame.image.load("./data/images/backdrops/Astralbg.png"), (0,0))
            self.display.blit(self.earth.image, self.earth.rect)
            # Draw asteroids
            self.angle += 1  # Increase the angle of rotation
            for i, astroid in enumerate(self.astroids):
                rotated_image = pygame.transform.rotate(astroid.image, self.angle * self.rotation_directions[i])
                rotated_rect = rotated_image.get_rect(center=astroid.rect.center)
                self.display.blit(rotated_image, rotated_rect)
            for powerup in self.powerups:
                if not powerup.collected:
                    self.display.blit(powerup.images[powerup.current_frame], powerup.rect)
            if self.ufo.defeat == 0 and self.ufo.victory == 0:
                if self.bullet.rect.center[0] == 640 and self.bullet.rect.center[1] <= 480:
                    self.sound_effects["bullet"].play()
                self.display.blit(self.bullet.image, self.bullet.rect)
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
            # lets print the mouse x coordinates
            print(pygame.mouse.get_pos())
if __name__ == "__main__":
    Game().run()
