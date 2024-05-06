import pygame
import os
import random

#Actions
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

#Dinosaur Object
class Dinosaur: 
    #variables
    X = 60
    Y = 310
    YDuck = 340
    Velocity = 8

    #constructor
    def __init__(self, obstacles, img = RUNNING[0]):
        #defaults and variables
        self.image = img
        self.isRunning = True
        self.isJumping = False
        self.isDucking = False
        self.jumpHeight = self.Velocity
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #creating rect object to store co ordinates [X,Y correspog to top left of dino image]
        self.rect = pygame.Rect(self.X, self.Y, img.get_width(), img.get_height())
        #animation loop
        self.step = 0
        self.obstacles = obstacles

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
        if self.isDucking:
            self.rect.y = self.Y
        if self.isJumping:
            #going up is actually decreasing in pygame
            self.rect.y -= self.jumpHeight * 4
            self.jumpHeight -= 0.8
        if self.jumpHeight < -self.Velocity: 
            self.isRunning = True       
            self.isJumping = False
            self.isDucking = False
            self.jumpHeight = self.Velocity

    def run(self):
        #tick counting, switch every 5 for animation
        self.image = RUNNING[self.step // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.step += 1
        self.isJumping = False
        self.isDucking = False

    def duck(self):
        #tick counting, switch every 5 for animation
        self.image = DUCKING[self.step // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.YDuck
        self.step += 1
        self.isDucking = False
        self.isRunning = True
        self.isJumping = False

    def draw(self, SCREEN): 
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        #draw hitbox
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        #draw line of sight
        for obstacle in self.obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x+54, self.rect.y+12), obstacle.rect.midtop, 2)