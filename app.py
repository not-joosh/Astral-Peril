import math
from numpy import angle
import pygame
import sys
import time
import random
from scripts.entities import UFO, Bullet, Earth, PowerUps, Explosion, Debree, Aura
from scripts.extrapolation.lagrange_method import Lagrange
from scripts.utils import Button
import random

class Game:
    def __init__(self):
        # Initialize the Game Window
        pygame.init()
        pygame.display.set_caption("Astral Peril")
        pygame.display.set_icon(pygame.image.load("./data/images/icons/00_icon.png"))
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,36)
        self.start_game = False
        
        # Game Mechanic Variables
        self.timer = 50
        num_of_powerups = random.randint(3, 10)
        
        #Button creations
        self.retry_button = Button((640-50) // 2, (480+50) // 2, 50, 25, "Retry")
        self.play_again = Button((640-75) // 2, (480+50) // 2, 100, 25, "Play Again")
        # Setting up Explosion Effects
        self.explosion_images = []
        for i in range(0, 7):
            image_path = f"./Data/images/effects/explosion/{i:02d}_explosion.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (60, 60))
            self.explosion_images.append(image)
        self.explosion = Explosion(0, 0, self.explosion_images)
        
        # Setting up Aura Effect
        self.aura_images = []
        for i in range(0, 8):
            image_path = f"./Data/images/effects/aura/{i:02d}_aura.png"
            image = pygame.image.load(image_path)
            # Scale down the UFO image
            image = pygame.transform.scale(image, (60, 60))
            # lets remove all black pixels from the images
            image.set_colorkey((0, 0, 0))
            self.aura_images.append(image)
        self.aura = Aura(0, 0, self.aura_images)

        # Background Setup
        self.background_offset = 0
        self.background_image = pygame.image.load("./data/images/backdrops/Astralbg.png")
        self.background_image_reverse = pygame.transform.flip(self.background_image, True, False)

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

        # Debree Setup
        self.debree_images = []
        for i in range(0, 5):
            image_path = f"./Data/images/decors/debree/{i:02d}_debree.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (20, 20))
            self.debree_images.append(image)
        self.debree = Debree(0, 0, self.debree_images)
        # Scatter debris randomly across the screen
        num_of_debris = random.randint(5, 10)
        self.debris = []
        for _ in range(num_of_debris):
            debris = pygame.sprite.Sprite()
            debris.image = self.debree_images[random.randint(0, len(self.debree_images) - 1)]
            debris.rect = debris.image.get_rect()
            debris.rect.center = random.randint(50, 480), random.randint(50, 430)
            # Check if the debris overlaps with any existing debris or asteroids
            overlapping = True
            while overlapping:
                debris.rect.center = random.randint(50, 480), random.randint(50, 430)
                overlapping = False
                for existing_debris in self.debris:
                    if debris.rect.colliderect(existing_debris.rect):
                        overlapping = True
                        break
                for asteroid in self.astroids:
                    if debris.rect.colliderect(asteroid.rect):
                        overlapping = True
                        break
            self.debris.append(debris)

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
        self.main_menu = self.font.render("ASTRAL PERIL", True, (255, 255, 255), (0, 0, 0))
        self.main_menu_rect = self.main_menu.get_rect(center=(640 // 2, 480 // 2))
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

        # Load Music & Sound Effects
        pygame.mixer.music.load("./Data/sounds/bg-music/bgMusic.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set the volume to 50% (adjust as needed)
        pygame.mixer.music.play(-1)
        self.sound_effects = {
            "bullet": pygame.mixer.Sound("./Data/sounds/sound-fx/bullet_fx.mp3"),
            "powerup": pygame.mixer.Sound("./Data/sounds/sound-fx/powerup_fx.mp3"),
            "ufo": pygame.mixer.Sound("./Data/sounds/sound-fx/ufo_fx2.mp3"),
            "astroid": pygame.mixer.Sound("./Data/sounds/sound-fx/astroid_fx2.mp3"),
            "explosion": pygame.mixer.Sound("./Data/sounds/sound-fx/explosion_fx2.mp3")
        }
        pass
    def render_main_menu(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        pygame.draw.rect(self.screen, (255,255,255), self.main_menu_rect)
        self.start = Button((640-50) // 2, (480+50) // 2, 50, 25, "Start")
        self.screen.blit(self.main_menu,self.main_menu_rect)
        self.start.draw(self.screen)
        pass
    def run(self):
        while True:
            if self.start_game:
                # Clearing the Screen
                self.display.fill((0, 0, 0))
    #--------------------- GAME EVENTS ---------------------#
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and self.ufo.defeat == 0 and self.ufo.victory == 0:
                        # If the mouse is moving and the mouse button is pressed, launch the UFO
                        if self.ufo.is_moving:
                            self.ufo.is_moving = False
                        else:
                            #set a whie loop that loops ufo.launch until timer for 2 seconds expires
                            self.ufo.is_moving = True
                            self.ufo.target = pygame.mouse.get_pos() 
                            # play ufo sound
                            self.sound_effects["ufo"].set_volume(50)  # Set the volume to maximum (1.0)
                            self.sound_effects["ufo"].play()
                    if event.type == pygame.MOUSEBUTTONDOWN and (self.ufo.defeat == 1 or self.ufo.victory == 1):
                        if self.play_again.rect.collidepoint(event.pos):
                            Game().run()
                            #reset all states
    #--------------------- UFO MOVING ---------------------#
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
                        if self.ufo.rect.centerx <= 500: # Already reached earth, lets not shoot it if its greater than 530
                            self.bullet.fire_towards(prediction[1])
                            # Printing the Lagrange Shooting Prediction
                            print("\n--------------------------------\n\tLAGRANGE SHOOTING")
                            print("\tPREDICTION: ", prediction)
                            print("\tEXPECTED: ", self.ufo.rect.center, "\n--------------------------------\n\t")
                        filtered_data.clear()
                    self.ufo.is_moving = False
                    self.timer = 50
                    self.ufo.visited_coords.clear()

    #--------------------- BULLET ---------------------#
                # Checking if bullet collision worked    
                if self.bullet.rect.colliderect(self.ufo.rect):
                    if self.ufo.armor >= 1:
                        self.bullet.count = 1
                        self.bullet.rect.x = -20
                        self.ufo.armor -= 1
                    else:
                        print("hit!")
                        self.ufo.defeat = 1 
                        self.bullet.count = 0
                        self.explosion.rect = self.ufo.rect
                        self.explosion.life_span = 10
                        self.sound_effects["explosion"].play()
    #--------------------- ASTROIDS ---------------------#
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
                        self.sound_effects["astroid"].play()
                        
                
                # Update
                self.ufo.update()
                self.bullet.update()
                for powerup in self.powerups:
                    powerup.update()
    #--------------------- POWERUPS ---------------------#
                # Check if powerup was collected
                for powerup in self.powerups:
                    if self.ufo.rect.colliderect(powerup.rect):
                        powerup.collected = True
                        self.ufo.armor += 1
                        self.bullet.count = 0
                        powerup.rect.center = (0, 0)
                        # We need to reset the bullet position
                        print("Powerup collected")
                        self.sound_effects["powerup"].play()

    #--------------------- DRAWING ---------------------#
                # Draw background
                self.background_offset += 1  # Increase the background offset
                background_rect = self.background_image.get_rect()
                background_rect.x -= self.background_offset  # Adjust the x-coordinate based on the offset
                self.display.blit(self.background_image, background_rect)
                # Draw reverse background
                reverse_background_rect = self.background_image_reverse.get_rect()
                reverse_background_rect.x = background_rect.x + background_rect.width
                self.display.blit(self.background_image_reverse, reverse_background_rect)
                # Check if the background offset exceeds the width of the image
                if self.background_offset >= background_rect.width:
                    # Calculate the remaining offset after reaching the end of the image
                    remaining_offset = self.background_offset - background_rect.width
                    # Draw the remaining portion of the background at the beginning of the image
                    remaining_rect = self.background_image.get_rect()
                    remaining_rect.x = -remaining_offset
                    self.display.blit(self.background_image, remaining_rect)
                    # Draw the remaining portion of the reverse background at the end of the image
                    remaining_reverse_rect = self.background_image_reverse.get_rect()
                    remaining_reverse_rect.x = remaining_rect.x + remaining_rect.width
                    self.display.blit(self.background_image_reverse, remaining_reverse_rect)
                    # Reset the background offset to the remaining offset
                    self.background_offset = remaining_offset
                    # Flip the background images
                    self.background_image, self.background_image_reverse = self.background_image_reverse, self.background_image
                self.display.blit(self.earth.image, self.earth.rect)


    #--------------------- UFO AURA ---------------------#
                if self.ufo.armor > 0:
                    # Draw aura
                    # Cycle through aura images
                    self.aura.current_frame += 1
                    if self.aura.current_frame >= len(self.aura.images):
                        self.aura.current_frame = 0
                    aura_image = self.aura.images[self.aura.current_frame]
                    aura_rect = aura_image.get_rect(center=self.ufo.rect.center)
                    self.display.blit(aura_image, aura_rect)
    
                # Draw debris
                for debris in self.debris:
                    self.display.blit(debris.image, debris.rect)

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
                    self.retry_button.draw(self.display)
                elif self.ufo.victory == 1:
                    self.display.blit(self.level_clear, self.level_clear_rect)
                    self.play_again.draw(self.display)
                    self.ufo.armor = 0
                    
                # Draw explosion
                if(self.explosion.life_span > 0):
                    if self.explosion.current_frame < len(self.explosion.images):
                        self.display.blit(self.explosion.images[self.explosion.current_frame], self.explosion.rect)
                        self.explosion.current_frame += 1
                        self.explosion.life_span = self.explosion.life_span - 1
                    else:
                        self.explosion.current_frame = 0
                self.screen.blit(pygame.transform.scale(self.display, (640, 480)), (0, 0))
                pygame.display.update()
                self.clock.tick(60)  # Decreased the frames per second to 60
            else: # Main Menu
                self.render_main_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.start.rect.collidepoint(mouse_pos):
                            self.start_game = True

            # Update the display after rendering the main menu
                pygame.display.update()
                self.clock.tick(60)
#--------------------- MAIN ---------------------#
if __name__ == "__main__":
    Game().run()
