import pygame
import numpy 
import math

class Car:
    def __init__(self, image, start_pos, velocity, width, height, sizes):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.posX, self.posY = start_pos
        self.width, self.height = width, height
        self.velocity = velocity
        self.angle = 270
        self.alive = True
        self.c1, self.c2, self.c3, self.c4, self.c5 = (0,0), (0,0), (0,0), (0,0), (0,0)
        self.d1, self.d2, self.d3, self.d4, self.d5 = 0, 0, 0, 0, 0
        self.input = numpy.array([[self.d1], [self.d2], [self.d3], [self.d4], [self.d5]])
        self.output = numpy.array([[0], [0]])
        self.score = 0
        self.sizes = sizes
        self.layers = len(sizes)
        self.biases = [numpy.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [numpy.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.mask_offset_X = -6
        self.mask_offset_Y = 4


    def rotate(self, turn):
        self.angle += turn
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360 + self.angle


    def draw(self, win):
        self.rotate_center(win, self.image, (self.posX, self.posY), self.angle)
        #---Mask Debug---
        #rect = self.mask.get_rect()
        #rect = rect.move(self.posX + self.mask_offset_X, self.posY + self.mask_offset_Y)
        #col = (100, 100, 100)
        #pygame.draw.rect(win, col, rect)
        

    def draw_lines(self, win):
        pygame.draw.line(win, (255, 0, 0), (self.posX + 10, self.posY + 20), self.c1, 2)
        pygame.draw.line(win, (255, 0, 0), (self.posX + 10, self.posY + 20), self.c2, 2)
        pygame.draw.line(win, (255, 0, 0), (self.posX + 10, self.posY + 20), self.c3, 2)
        pygame.draw.line(win, (255, 0, 0), (self.posX + 10, self.posY + 20), self.c4, 2)
        pygame.draw.line(win, (255, 0, 0), (self.posX + 10, self.posY + 20), self.c5, 2)


    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        
        self.posY -= vertical
        self.posX -= horizontal


    def collision_screen(self):
        if self.posX + self.width > 1200 or self.posX < 0 or self.posY < 0 or self.posY + self.height > 600:
            return True


    def collision_objects(self, mask, x=0, y=0):
        offset = (int(self.posX - x + self.mask_offset_X), int(self.posY - y + self.mask_offset_Y))
        poi = mask.overlap(self.mask, offset)
        return poi


    def move_lines(self, point, angle, unit):
        x = point[0]
        y = point[1]
        rad = math.radians(angle % 360)
        x -= unit*math.sin(rad)
        y -= unit*math.cos(rad)
        return x, y


    def collision_lines(self, rect, arr):
        self.c1 = self.move_lines((self.posX + 10, self.posY + 20), self.angle, 20)
        self.c2 = self.move_lines((self.posX + 10, self.posY + 20), self.angle - 45, 15)
        self.c3 = self.move_lines((self.posX + 10, self.posY + 20), self.angle + 45, 15)
        self.c4 = self.move_lines((self.posX + 10, self.posY + 20), self.angle - 90, 10)
        self.c5 = self.move_lines((self.posX + 10, self.posY + 20), self.angle + 90, 10)
        check1 = True
        while self.c1[0] < 1200 and self.c1[0] >= 0 and self.c1[1] >= 0 and self.c1[1] < 600 and check1: 
            for obstacle in arr:
                if obstacle.rect.collidepoint(self.c1[0], self.c1[1]):
                    check1 = False
            self.c1 = self.move_lines((self.c1[0], self.c1[1]), self.angle, 2)
        check2 = True
        while self.c2[0] < 1200 and self.c2[0] >= 0 and self.c2[1] >= 0 and self.c2[1] < 600 and check2: 
            for obstacle in arr:
                if obstacle.rect.collidepoint(self.c2[0], self.c2[1]):
                    check2 = False
            self.c2 = self.move_lines((self.c2[0], self.c2[1]), self.angle - 45, 2)
        check3 = True
        while self.c3[0] < 1200 and self.c3[0] >= 0 and self.c3[1] >= 0 and self.c3[1] < 600 and check3: 
            for obstacle in arr:
                if obstacle.rect.collidepoint(self.c3[0], self.c3[1]):
                    check3 = False
            self.c3 = self.move_lines((self.c3[0], self.c3[1]), self.angle + 45, 2)
        check4 = True
        while self.c4[0] < 1200 and self.c4[0] >= 0 and self.c4[1] >= 0 and self.c4[1] < 600 and check4: 
            for obstacle in arr:
                if obstacle.rect.collidepoint(self.c4[0], self.c4[1]): 
                    check4 = False
            self.c4 = self.move_lines((self.c4[0], self.c4[1]), self.angle - 90, 2)
        check5 = True
        while self.c5[0] < 1200 and self.c5[0] >= 0 and self.c5[1] >= 0 and self.c5[1] < 600 and check5: 
            for obstacle in arr:
                if obstacle.rect.collidepoint(self.c5[0], self.c5[1]):
                    check5 = False
            self.c5 = self.move_lines((self.c5[0], self.c5[1]), self.angle + 90, 2)
    

    def calculate_dist(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    def calculate_coll_dist(self):
        self.d1 = int(self.calculate_dist(self.posX, self.posY, self.c1[0], self.c1[1]))
        self.d2 = int(self.calculate_dist(self.posX, self.posY, self.c2[0], self.c2[1]))
        self.d3 = int(self.calculate_dist(self.posX, self.posY, self.c3[0], self.c3[1]))
        self.d4 = int(self.calculate_dist(self.posX, self.posY, self.c4[0], self.c4[1]))
        self.d5 = int(self.calculate_dist(self.posX, self.posY, self.c5[0], self.c5[1]))

       
    def rotate_center(self, win, image, top_left, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
        self.mask = pygame.mask.from_surface(rotated_image)
        win.blit(rotated_image, new_rect.topleft)

    def turn_car(self):
        if self.output.item(0) > 0.5:
            self.rotate(-5)
        if self.output.item(1) > 0.5:
            self.rotate(5)
        return

    def activation(self, z):
        return 1.0/(1.0+numpy.exp(-z))

    def feed_forward(self):
        self.input = numpy.array([[self.d1], [self.d2], [self.d3], [self.d4], [self.d5]])
        for b, w in zip(self.biases, self.weights):
            self.input = self.activation(numpy.dot(w, self.input)+b)
        self.output = self.input
        return self.output

    def reset_position(self, start_pos):
        self.posX, self.posY = start_pos
        self.angle = 270
        self.alive = True
        self.score = 0
        return

    def calc_fitness(self):
        self.score = 1/int(self.calculate_dist(self.posX, self.posY, 1190, 300))
        return
