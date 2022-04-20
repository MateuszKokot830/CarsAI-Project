import pygame
import time
import math
import random
from car import *
from obstacle import *

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarsAI")

FPS = 30
START_POS = 10, 290
NUM_OF_CARS = 2
CAR_WIDTH = 20
CAR_HEIGHT = 40
OBS_WIDTH = 50
OBS_HEIGHT = 200

CAR_IMAGE = pygame.image.load("Assets/white-car.png")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
WALL_IMAGE = pygame.image.load("Assets/walls.jpg")
WALL_IMAGE = pygame.transform.scale(WALL_IMAGE, (OBS_WIDTH, OBS_HEIGHT))
BACKGROUND = pygame.image.load("Assets/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
FINISH_LINE = pygame.image.load("Assets/finish.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (20, 80))


def draw(win, images, cars):
    for img, pos in images:
        win.blit(img, pos)
    for obstacle in obstacles:
        obstacle.draw(win)
    for car in cars:
        car.draw(win)
        car.draw_lines(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()

images = [(BACKGROUND, (0,0)), (FINISH_LINE, (1180, 260))]
cars = []
for x in range (NUM_OF_CARS):
    cars.append(Car(CAR_IMAGE, START_POS, 1, CAR_WIDTH, CAR_HEIGHT))
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
    
    for car in cars:
        if car.alive:
            for obstacle in obstacles:
                if car.collision_objects(obstacle.mask, obstacle.x, obstacle.y) != None:
                    car.alive = False
                elif car.collision_screen():
                    car.alive = False
            car.collision_lines(obstacle.mask, obstacles)
            car.calculate_coll_dist()
            random_val = (random.randint(0, 100))
            if random_val % 2:
                car.rotate(5)
            else:
                car.rotate(-5)
                car.move()
    
    draw(WIN, images, cars)

            

pygame.quit()
