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

#Importing Assets by looking in project folder
#Actions
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = [pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))]
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
GROUND = [pygame.image.load(os.path.join("Assets/Other", "Track.png"))]

#Text
FONT = pygame.font.Font('freesansbold.ttf', 20)

#-----------------------------------------------------------------------------------------

#Dinosaur Object
class Dinosaur: 
    #variables
    X = 80
    Y = 310
    JumpHeight = 8.5

    #constructor
    def __init__(self, img = RUNNING[0]):
        #defaults and variables
        self.image = img
        self.running = True
        self.jumping = False
        self.ducking = False
        self.jumpHeight = self.JumpHeight
        #creating rect object to store co ordinates [X,Y correspog to top left of dino image]
        self.rect = pygame.Rect(self.X, self.Y, img.get_width(), img.get_height())
        #animation loop
        self.step = 0

    #functions with parameters
    def update(self):
        #check what dino is doing
        if self.running:
            self.run()
        if self.jumping:
            self.jump()
        if self.ducking:
            self.duck()
        if self.step >= 10:
            self.step = 0


    def jump(self):
        print("jumping")
        self.jumping = False

    def run(self):
        #tick counting, switch every 5
        self.image = RUNNING[self.step // 5]
        self.rect.x = self.X
        self.rect.y = self.Y
        self.step += 1

    def duck(self):
        print("ducking")
        self.ducking = False
        
    def draw(self, SCREEN): 
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))



#-----------------------------------------------------------------------------------------

#main method
def main():
    #clock variable
    clock = pygame.time.Clock()
    dinosaurs = [Dinosaur()]

    #game loop
    run = True
    while run:
        #exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        #Drawing screen
        SCREEN.fill((255,255,255))

        for dino in dinosaurs:            
            dino.update()
            dino.draw(SCREEN)

        #Getting input
        input = pygame.key.get_pressed()
        for i, dino in enumerate(dinosaurs):
            #jumping
            if input[pygame.K_UP] and not dino.jumping:
                dino.jumping = True
                dino.running = False
                dino.ducking = False
            #ducking
            elif input[pygame.K_DOWN] and not dino.jumping:
                dino.jumping = False
                dino.running = False
                dino.ducking = True
            #running
            elif not (dino.jumping or input[pygame.K_DOWN]):
                dino.jumping = False
                dino.running = True
                dino.ducking = False

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()


#call main method to run game
main()