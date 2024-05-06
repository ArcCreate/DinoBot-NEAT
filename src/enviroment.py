import pygame
import os
import random

#Global Variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Assets
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

#-----------------------------------------------------------------------------------------        

#Cloud Object
class Cloud:
    #Constructor
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self, GAME_SPEED):
        self.x -= GAME_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
    
    def draw(self, SCREEN): 
        SCREEN.blit(self.image, (self.x, self.y))

#Obstacles
class Obstacle:
    def __init__(self, image, amount):
        self.image = image
        self.type = amount
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, GAME_SPEED, obstacles):
        self.rect.x -= GAME_SPEED
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

#small cacti
class SmallCactus(Obstacle):
    def __init__(self, image, amount):
        super().__init__(image, amount)
        self.rect.y = 325

#large cacti
class LargeCactus(Obstacle):
    def __init__(self, image, amount):
        super().__init__(image, amount)
        self.rect.y = 300

#bird
class Bird(Obstacle):
    def __init__(self, image, amount):
        super().__init__(image, amount)
        rand = random.randint(1,1)
        if rand == 0:
            self.rect.y = 250
        else:
            self.rect.y = 300
        self.step = 0

    def draw(self, SCREEN):
        if self.step >= 9:
            self.step = 0
        SCREEN.blit(self.image[self.step//5], self.rect)
        self.step += 1