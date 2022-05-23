from tabnanny import check
import pygame
import time
import math
import random
from car import *
from obstacle import *
from genetic import *

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarsAI")

FPS = 60
START_POS = 10, 290
NUM_OF_CARS = 30
VELOCITY = 5
CAR_WIDTH = 20
CAR_HEIGHT = 40
OBS_WIDTH = 50
OBS_HEIGHT = 200
FINISH_X = 1180
FINISH_Y = 260
COUNTER = 0
MUTATION_RATE = 90


INPUTLAYER = 5
HIDDENLAYER = 6
OUTPUTLAYER = 2


CAR_IMAGE = pygame.image.load("Assets/white-car.png")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
RED_CAR_IMAGE = pygame.image.load("Assets/red-car.png")
RED_CAR_IMAGE = pygame.transform.scale(RED_CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
WALL_IMAGE = pygame.image.load("Assets/walls.jpg")
WALL_IMAGE = pygame.transform.scale(WALL_IMAGE, (OBS_WIDTH, OBS_HEIGHT))
BACKGROUND = pygame.image.load("Assets/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
FINISH_LINE = pygame.image.load("Assets/finish.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (20, 80))
FINISH_MASK = pygame.mask.from_surface(FINISH_LINE)


def draw(win, images, cars):
    for img, pos in images:
        win.blit(img, pos)
    for obstacle in obstacles:
        obstacle.draw(win)
    for car in cars:
        car.draw(win)
        #car.draw_lines(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()

images = [(BACKGROUND, (0,0)), (FINISH_LINE, (FINISH_X , FINISH_Y))]

cars = []
for x in range (NUM_OF_CARS):
    cars.append(Car(CAR_IMAGE, START_POS, VELOCITY, CAR_WIDTH, CAR_HEIGHT, [INPUTLAYER, HIDDENLAYER, OUTPUTLAYER]))

checkCar = (Car(CAR_IMAGE, START_POS, VELOCITY, CAR_WIDTH, CAR_HEIGHT, [INPUTLAYER, HIDDENLAYER, OUTPUTLAYER]))

obstacles = []
obstacles.append(Obstacle(WALL_IMAGE, 900, 200, OBS_WIDTH, OBS_HEIGHT))
obstacles.append(Obstacle(WALL_IMAGE, 600, 0, OBS_WIDTH, OBS_HEIGHT))
obstacles.append(Obstacle(WALL_IMAGE, 600, 400, OBS_WIDTH, OBS_HEIGHT))
obstacles.append(Obstacle(WALL_IMAGE, 300, 200, OBS_WIDTH, OBS_HEIGHT))


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    checkEND = True

    if COUNTER >= 600:
        for car in cars:
            car.alive = False

    for car in cars:
        if car.alive:
            checkEND = False
            for obstacle in obstacles:
                if car.collision_objects(obstacle.mask, obstacle.x, obstacle.y) != None:
                    car.alive = False
            if car.collision_screen():
                car.alive = False
            if car.collision_objects(FINISH_MASK, FINISH_X, FINISH_Y):
                car.alive = False
            if car.alive:
                car.feed_forward()
                car.turn_car()                
                car.move()  
                car.collision_lines(obstacle.rect, obstacles)
                car.calculate_coll_dist()  
                car.calc_fitness()
                    
    
    draw(WIN, images, cars)
    COUNTER += 1

    if (checkEND == True): 
        cars.sort(key=lambda x: x.score, reverse=True)
        parent1 = cars[0]
        parent2 = cars[1]
        cars.clear()
        COUNTER = 0
        for i in range (NUM_OF_CARS):
            cars.append(Car(CAR_IMAGE, START_POS, VELOCITY, CAR_WIDTH, CAR_HEIGHT, [INPUTLAYER, HIDDENLAYER, OUTPUTLAYER]))
        for i in range (0, NUM_OF_CARS-2, 2):
            crossover_weights(parent1, parent2, cars[i], cars[i+1])
            crossover_biases(parent1, parent2, cars[i], cars[i+1])
        cars[NUM_OF_CARS-2] = parent1
        cars[NUM_OF_CARS-1] = parent2
        cars[NUM_OF_CARS-2].image = RED_CAR_IMAGE
        cars[NUM_OF_CARS-1].image = RED_CAR_IMAGE
        cars[NUM_OF_CARS-2].reset_position(START_POS)
        cars[NUM_OF_CARS-1].reset_position(START_POS)
        for i in range (NUM_OF_CARS-2):
            for j in range(MUTATION_RATE):
                mutate_weights(cars[i], checkCar)
                mutate_weights(checkCar, cars[i])
                mutate_biases(cars[i], checkCar)
                mutate_biases(checkCar, cars[i])
    
            

pygame.quit()
