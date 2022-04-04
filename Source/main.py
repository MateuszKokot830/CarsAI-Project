import pygame
import time
import math
import random

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarsAI")

CAR_IMAGE = pygame.image.load("Assets/red-car.png")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (20, 40))
BACKGROUND = pygame.image.load("Assets/Background.jfif")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

FPS = 60
START_POS = 10, 290

class Car:
    def __init__(self, max_vel, rotation_vel):
        self.img = CAR_IMAGE
        self.posX, self.posY = START_POS
        self.max_vel = max_vel
        self.velocity = 0
        self.rotation_vel = rotation_vel
        self.acceleration = 0.2
        self.angle = 270

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        rotate_center(win, self.img, (self.posX, self.posY), self.angle)

    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        
        self.posY -= vertical
        self.posX -= horizontal


def rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def draw(win, cars):
    win.blit(BACKGROUND, (0,0))
    for car in cars:
        car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()

cars = []
for x in range (50):
    cars.append(Car(4,4))

while run:
    clock.tick(FPS)
    draw(WIN, cars)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    for car in cars:
        random_val = (random.randint(0, 100))
        if random_val % 2:
            car.rotate(left=True)
        else:
            car.rotate(right=True)
        car.move_forward()

pygame.quit()
