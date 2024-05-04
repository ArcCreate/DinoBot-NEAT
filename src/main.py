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
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = [pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))]
GROUND = [pygame.image.load(os.path.join("Assets/Other", "Track.png"))]

#Text
FONT = pygame.font.Font('freesansbold.ttf', 20)

#main method
def main():
    #clock variable
    clock = pygame.time.Clock()

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

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()


#call main method to run game
main()