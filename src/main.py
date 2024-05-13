# Importing Packages for the project
# Drawing game
import math
import pygame
import os
import random
import sys
import neat
from dinosaur import Dinosaur
from enviroment import Cloud, Obstacle, SmallCactus, LargeCactus, Bird

#initializing pygame
pygame.init()

#Global Variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
best = 0
lastBest = 0

#Storing best genome
best_genome = None
best_fitness = 0

#Assets
GROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
FONT = pygame.font.Font('freesansbold.ttf', 20)
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

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
    global GAME_SPEED, x_pos, y_pos, obstacles, dinosaurs, ge, nets, SCORE, best, lastBest
    global best_genome, best_fitness
    
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
        dinosaur = Dinosaur(obstacles)
        dinosaurs.append(dinosaur)
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
    
    #Screen stats
    def statistics():
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Gen Score:  {lastBest}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480)) 
        SCREEN.blit(text_3, (50, 510))

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
            rand = random.randint(0,2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand == 2:
                obstacles.append(Bird(BIRD, 1))

        #collision
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(GAME_SPEED, obstacles)
            for i, dino in enumerate(dinosaurs):
                if dino.rect.colliderect(obstacle.rect):
                    ge[i].fitness += SCORE
                    best = SCORE
                    if best > best_fitness:
                        best_genome = nets[0]
                        best_fitness = best
                        #save_best_genome(best_genome, best_fitness)
                    remove(i)

        #Drawing dino
        for dino in dinosaurs:            
            dino.update()
            dino.draw(SCREEN)
        
        for i, dino in enumerate(dinosaurs):
            #inputs to NEAT (Y position of dino, top of obstacles, bottom of obstacle)
            output = nets[i].activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacle.rect.topleft), distance((dino.rect.x, dino.rect.y), obstacle.rect.topright), GAME_SPEED))

            #get outputs
            decision = output.index(max(output))
            #jumping
            if  decision == 0 and dino.rect.y == dino.Y:                
                dino.isJumping = True
                dino.isRunning = False
                dino.isDucking = False
                ge[i].fitness -= 20

        #Drawing clouds
        cloud.draw(SCREEN)
        cloud.update(GAME_SPEED)

        #end game if there are no more dinosaurs left
        if len(dinosaurs) == 0:
            lastBest = best
            print(lastBest)
            break

        #frames per second
        clock.tick(30)

        #update screen
        pygame.display.update()

#Saving genome
def save_best_genome(genome, fitness):
    with open('best_genome.txt', 'w') as file:
        file.write(str(fitness) + '\n')
        file.write(str(genome))

def load_best_genome():
    global best_genome, best_fitness
    with open('best_genome.txt', 'r') as file:
        best_fitness = float(file.readline().strip())
        best_genome = file.read()

#Neat setup
def run(config_path):
    global pop, best_genome, best_fitness
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

    #if running from loaded genome uncommet the following lines
    # try:
    #     load_best_genome()
    #     print("Loaded best genome with fitness:", best_fitness)
    # except FileNotFoundError:
    #     print("No previous best genome found. Starting from scratch.")


    #run evolution/fitness function x times
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    for _ in range (10):
        print("trial", _+1)
        run(config_path)

