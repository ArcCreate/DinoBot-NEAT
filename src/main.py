# Importing Packages for the project
# Drawing game
import pygame
import os
import random
import sys

#initializing pygame
pygame.init()

#Global Variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_SPEED = 14
x_pos = 0
y_pos = 380
SCORE = 0

#Importing Assets by looking in project folder
#Actions
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

#Enviroment
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
GROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

#Text
FONT = pygame.font.Font('freesansbold.ttf', 20)

#-----------------------------------------------------------------------------------------

#Dinosaur Object
class Dinosaur: 
    #variables
    X = 60
    Y = 310
    YDuck = 340
    Velocity = 8.5

    #constructor
    def __init__(self, img = RUNNING[0]):
        #defaults and variables
        self.image = img
        self.isRunning = True
        self.isJumping = False
        self.isDucking = False
        self.jumpHeight = self.Velocity
        #creating rect object to store co ordinates [X,Y correspog to top left of dino image]
        self.rect = pygame.Rect(self.X, self.Y, img.get_width(), img.get_height())
        #animation loop
        self.step = 0

    #functions with parameters
    def update(self):
        #check what dino is doing
        if self.isRunning:
            self.run()
        if self.isJumping:
            self.jump()
        if self.isDucking:
            self.duck()
        if self.step >= 10:
            self.step = 0


    def jump(self):
        self.image = JUMPING
        #jumping physics
        if self.isJumping:
            #going up is actually decreasing in pygame
            self.rect.y -= self.jumpHeight * 4
            self.jumpHeight -= 0.8
        if self.jumpHeight < - self.Velocity:        
            self.isJumping = False
            self.jumpHeight = self.Velocity

    def run(self):
        #tick counting, switch every 5 for animation
        self.image = RUNNING[self.step // 5]
        self.rect.x = self.X
        self.rect.y = self.Y
        self.step += 1

    def duck(self):
        #tick counting, switch every 5 for animation
        self.image = DUCKING[self.step // 5]
        self.rect.x = self.X
        self.rect.y = self.YDuck
        self.step += 1
        self.isDucking = False

    def draw(self, SCREEN): 
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

#Cloud Object
class Cloud:
    #Constructor
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= GAME_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
    
    def draw(self, SCREEN): 
        SCREEN.blit(self.image, (self.x, self.y))


#-----------------------------------------------------------------------------------------

#main method
def main():
    clock = pygame.time.Clock()
    cloud = Cloud()

    #List of dino objects for when NEAT is being used
    dinosaurs = [Dinosaur()]

    #Score
    def score():
        global SCORE, GAME_SPEED
        SCORE += 1
        if SCORE % 100 == 0:
            GAME_SPEED += 1
        text = FONT.render(str(SCORE), True, (0,0,0))
        SCREEN.blit(text, (1000, 50))

    #background
    def background():
        global x_pos, y_pos
        image_width = GROUND.get_width()
        SCREEN.blit(GROUND, (x_pos, y_pos))
        SCREEN.blit(GROUND, (image_width + x_pos, y_pos))
        if x_pos <= -image_width:
            SCREEN.blit(GROUND, (image_width + x_pos, y_pos))
            x_pos = 0
        x_pos -= GAME_SPEED

    #game loop
    run = True
    while run:
        #exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        #Drawing white backgorund
        SCREEN.fill((255,255,255))
        score()
        background()

        #Drawing dino
        for dino in dinosaurs:            
            dino.update()
            dino.draw(SCREEN)
        #Getting input
        input = pygame.key.get_pressed()
        for i, dino in enumerate(dinosaurs):
            #jumping
            if input[pygame.K_UP] and not dino.isJumping:
                dino.isJumping = True
                dino.isRunning = False
                dino.isDucking = False
            #ducking
            elif input[pygame.K_DOWN] and not dino.isJumping:
                dino.isJumping = False
                dino.isRunning = False
                dino.isDucking = True
            #running
            elif not (dino.isJumping or input[pygame.K_DOWN]):
                dino.isJumping = False
                dino.isRunning = True
                dino.isDucking = False

        #Drawing clouds
        cloud.draw(SCREEN)
        cloud.update()

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()


#call main method to run game
main()