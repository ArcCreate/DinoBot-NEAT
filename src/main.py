# Importing Packages for the project
# Drawing game
import math
import pygame
import os
import random
import sys
import neat

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
    Velocity = 8

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
        if self.jumpHeight < -self.Velocity: 
            self.isRunning = True       
            self.isJumping = False
            self.jumpHeight = self.Velocity

    def run(self):
        #tick counting, switch every 5 for animation
        self.image = RUNNING[self.step // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.Y
        self.step += 1

    def duck(self):
        #tick counting, switch every 5 for animation
        self.image = DUCKING[self.step // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X
        self.rect.y = self.YDuck
        self.step += 1
        self.isDucking = False
        self.isRunning = True

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

#Obstacles
class Obstacle:
    def __init__(self, image, amount):
        self.image = image
        self.type = amount
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
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
        rand = random.randint(0,1)
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
#-----------------------------------------------------------------------------------------

#main method for simple playing
def main():
    #global variables 
    global GAME_SPEED, x_pos, y_pos, obstacles, dinosaurs, SCORE
    
    GAME_SPEED = 14
    x_pos = 0
    y_pos = 380
    SCORE = 0
    obstacles = []
    dinosaurs = Dinosaur()
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

        #spawning obstacles
        if len(obstacles) == 0:
            #randomized obstacle
            rand = random.randint(0,2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand == 2:
                obstacles.append(Bird(BIRD, 1))

        #drawing obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dino in enumerate(dinosaurs):
                if dino.rect.colliderect(obstacle.rect):
                    pygame.draw.rect(SCREEN, (255, 0, 0), dino.rect, 2)

        #end game if there are no more dinosaurs left
        if len(dinosaurs) == 0:
            break

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()

#-----------------------------------------------------------------------------------------

#remove after death for AI
def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(posa, posb):
    dx = posa[0] - posb[0]
    dy = posa[1] - posb[1]
    return math.sqrt(dx**2+dy**2)

#AI method for evalutation of subject
def eval_genomes(genomes, config):    
    #global variables 
    global GAME_SPEED, x_pos, y_pos, obstacles, dinosaurs, ge, nets, SCORE
    
    GAME_SPEED = 14
    x_pos = 0
    y_pos = 380
    SCORE = 0
    obstacles = []
    
    #List of dino objects for NEAT
    dinosaurs = []
    #will store stats on each dinosaur
    ge = []
    nets = []

    clock = pygame.time.Clock()
    cloud = Cloud()

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

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
    
    

    def statistics():
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480)) 

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
        statistics()    

        #spawning obstacles
        if len(obstacles) == 0:
            #randomized obstacle
            rand = random.randint(0,1)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand == 2:
                obstacles.append(Bird(BIRD, 1))

        #collision
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dino in enumerate(dinosaurs):
                if dino.rect.colliderect(obstacle.rect):
                    ge[i].fitness += SCORE
                    remove(i)
        #Drawing dino
        for dino in dinosaurs:            
            dino.update()
            dino.draw(SCREEN)
        
        for i, dino in enumerate(dinosaurs):
            output = nets[i].activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacle.rect.midtop)))
            #get outputs
            #jumping
            if  output[0] < 0:                
                dino.isJumping = True
                dino.isRunning = False
                dino.isDucking = False
                ge[i].fitness -= 1

        #Drawing clouds
        cloud.draw(SCREEN)
        cloud.update()

        #end game if there are no more dinosaurs left
        if len(dinosaurs) == 0:
            break

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()

#Neat setup
def run(config_path):
    global pop
    #configurate neat algorithm
    config = neat.config.Config(
        #default algorithms for simplicity
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        #file path
        config_path
    )

    #population of dinosaurs
    pop = neat.Population(config)
    #run evolution/fitness function 50 times
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

#call main method to run game
main()
