import pygame
from car import *
from obstacle import *
from genetic import *

class States:
    def __init__(self):
        self.state = 'build'

    def state_manager(self):
        if self.state == 'build':
            self.build_state()
        if self.state == 'run':
            self.run_state()

    def build_state(self):
        draw(WIN, images, cars, textBuild)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    correct_pos = [pos[0] - (OBS_WIDTH/2), pos[1] - (OBS_HEIGHT/2)]
                    obstacles.append(Obstacle(WALL_IMAGEL, correct_pos, OBS_WIDTH, OBS_HEIGHT))
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    correct_pos = [pos[0] - (OBS_HEIGHT/2), pos[1] - (OBS_WIDTH/2)]
                    obstacles.append(Obstacle(WALL_IMAGER, correct_pos, OBS_HEIGHT, OBS_WIDTH))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                     self.state = 'run'


    def run_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        global START_POS
        global NUM_OF_CARS
        global VELOCITY 
        global CAR_WIDTH
        global CAR_HEIGHT
        global OBS_WIDTH
        global OBS_HEIGHT
        global FINISH_X 
        global FINISH_Y
        global COUNTER
        global MUTATION_RATE 
        global GENERATION
        global INPUTLAYER
        global HIDDENLAYER
        global OUTPUTLAYER

    
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
                    car.success = True
                if car.alive:
                    car.calc_fitness()
                    car.feed_forward()
                    car.turn_car()                
                    car.move()  
                    car.collision_lines(obstacle.rect, obstacles)
                    car.calculate_coll_dist() 
                    car.time += 1 
                        
        textRun = 'Generation: ' + str(GENERATION)
        draw(WIN, images, cars, textRun)
        COUNTER += 1

        if (checkEND == True): 
            cars.sort(key=lambda x: x.score, reverse=True)
            parent1 = cars[0]
            parent2 = cars[1]
            cars.clear()
            COUNTER = 0
            GENERATION += 1
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
                    mutate_weights(cars[i], testCar)
                    mutate_weights(testCar, cars[i])
                    mutate_biases(cars[i], testCar)
                    mutate_biases(testCar, cars[i])

pygame.init()
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarsAI")

FPS = 30
START_POS = 10, 290
NUM_OF_CARS = 100
VELOCITY = 5
CAR_WIDTH = 20
CAR_HEIGHT = 40
OBS_WIDTH = 50
OBS_HEIGHT = 200
FINISH_X = 1100
FINISH_Y = 260
COUNTER = 0
MUTATION_RATE = 90
GENERATION = 1

INPUTLAYER = 6
HIDDENLAYER = 6
OUTPUTLAYER = 2


CAR_IMAGE = pygame.image.load("Assets/white-car.png")
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
RED_CAR_IMAGE = pygame.image.load("Assets/red-car.png")
RED_CAR_IMAGE = pygame.transform.scale(RED_CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
WALL_IMAGEL = pygame.image.load("Assets/walls.jpg")
WALL_IMAGEL = pygame.transform.scale(WALL_IMAGEL, (OBS_WIDTH, OBS_HEIGHT))
WALL_IMAGER = pygame.image.load("Assets/walls.jpg")
WALL_IMAGER = pygame.transform.scale(WALL_IMAGER, (OBS_HEIGHT, OBS_WIDTH))
BACKGROUND = pygame.image.load("Assets/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
FINISH_LINE = pygame.image.load("Assets/finish.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (40, 80))
FINISH_MASK = pygame.mask.from_surface(FINISH_LINE)

images = [(BACKGROUND, (0,0)), (FINISH_LINE, (FINISH_X , FINISH_Y))]
textBuild = 'Click LPM or PPM to place an obstacle, press Enter to start'

def draw(win, images, cars, text):
    for img, pos in images:
        win.blit(img, pos)
    for obstacle in obstacles:
        obstacle.draw(win)
    for car in cars:
        car.draw(win)
        #car.draw_lines(win)
    font = pygame.font.SysFont("comicsansms", 30)
    info = font.render(text, True, (255,0,0))
    infoXY = info.get_rect().move(10, 10)
    win.blit(info, infoXY)
    pygame.display.update()


run = True
clock = pygame.time.Clock()

state = States()
cars = []
obstacles = []
testCar = (Car(CAR_IMAGE, START_POS, VELOCITY, CAR_WIDTH, CAR_HEIGHT, [INPUTLAYER, HIDDENLAYER, OUTPUTLAYER]))
for x in range (NUM_OF_CARS):
    cars.append(Car(CAR_IMAGE, START_POS, VELOCITY, CAR_WIDTH, CAR_HEIGHT, [INPUTLAYER, HIDDENLAYER, OUTPUTLAYER]))

while run:
    state.state_manager()
    clock.tick(FPS)

        
            

pygame.quit()
