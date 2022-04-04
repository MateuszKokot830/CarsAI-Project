import pygame
import time
import math
import random
from car import *
from obstacle import *

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarsAI")

FPS = 60
START_POS = 10, 290
NUM_OF_CARS = 50
OBS_WIDTH = 50
OBS_HEIGHT = 300

CAR_IMAGE = pygame.image.load("Assets/white-car.png")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (20, 40))
WALL_IMAGE = pygame.image.load("Assets/wall.jfif")
WALL_IMAGE = pygame.transform.scale(WALL_IMAGE, (OBS_WIDTH, OBS_HEIGHT))
BACKGROUND = pygame.image.load("Assets/back.jpg")
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
    pygame.display.update()


run = True
clock = pygame.time.Clock()

images = [(BACKGROUND, (0,0)), (FINISH_LINE, (1180, 260))]
cars = []
for x in range (NUM_OF_CARS):
    cars.append(Car(CAR_IMAGE, START_POS, 4,4))
obstacles = []
for x in range (1):
    obstacles.append(Obstacle(WALL_IMAGE, 600, 150, OBS_WIDTH, OBS_HEIGHT))

while run:
    clock.tick(FPS)
    draw(WIN, images, cars)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    for car in cars:
        if car.alive:
            car.check_collision(obstacles)
            random_val = (random.randint(0, 100))
            if random_val % 2:
                car.rotate(left=True)
            else:
                car.rotate(right=True)
            car.move()

pygame.quit()
