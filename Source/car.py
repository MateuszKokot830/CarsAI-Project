import pygame
import math

class Car:
    def __init__(self, image, start_pos, velocity, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.posX, self.posY = start_pos
        self.width, self.height = width, height
        self.velocity = velocity
        self.angle = 270
        self.alive = True
        self.c1, self.c2, self.c3, self.c4, self.c5 = (0,0), (0,0), (0,0), (0,0), (0,0)
        self.d1, self.d2, self.d3, self.d4, self.d5 = 0, 0, 0, 0, 0


    def rotate(self, turn):
        self.angle += turn
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360 + self.angle


    def draw(self, win):
        self.rotate_center(win, self.image, (self.posX, self.posY), self.angle)
        

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
        offset = (int(self.posX - x), int(self.posY - y))
        poi = mask.overlap(self.mask, offset)
        return poi


    def move_lines(self, point, angle, unit):
        x = point[0]
        y = point[1]
        rad = math.radians(angle % 360)
        x -= unit*math.sin(rad)
        y -= unit*math.cos(rad)
        return x, y


    def collision_lines(self, mask, arr):
        self.c1 = self.move_lines((self.posX + 10, self.posY + 20), self.angle, 5)
        self.c2 = self.move_lines((self.posX + 10, self.posY + 20), self.angle - 45, 5)
        self.c3 = self.move_lines((self.posX + 10, self.posY + 20), self.angle + 45, 5)
        self.c4 = self.move_lines((self.posX + 10, self.posY + 20), self.angle - 90, 5)
        self.c5 = self.move_lines((self.posX + 10, self.posY + 20), self.angle + 90, 5)
        check1 = True
        while self.c1[0] < 1200 and self.c1[0] >= 0 and self.c1[1] >= 0 and self.c1[1] < 600 and check1: 
            for obstacle in arr:
                offset = (int(self.c1[0] - obstacle.x), int(self.c1[1] - obstacle.y))
                if mask.overlap(self.mask, offset) != None: 
                    check1 = False
            self.c1 = self.move_lines((self.c1[0], self.c1[1]), self.angle, 10)
        check2 = True
        while self.c2[0] < 1200 and self.c2[0] >= 0 and self.c2[1] >= 0 and self.c2[1] < 600 and check2: 
            for obstacle in arr:
                offset = (int(self.c2[0] - obstacle.x), int(self.c2[1] - obstacle.y))
                if mask.overlap(self.mask, offset) != None: 
                    check2 = False
            self.c2 = self.move_lines((self.c2[0], self.c2[1]), self.angle - 45, 10)
        check3 = True
        while self.c3[0] < 1200 and self.c3[0] >= 0 and self.c3[1] >= 0 and self.c3[1] < 600 and check3: 
            for obstacle in arr:
                offset = (int(self.c3[0] - obstacle.x), int(self.c3[1] - obstacle.y))
                if mask.overlap(self.mask, offset) != None: 
                    check3 = False
            self.c3 = self.move_lines((self.c3[0], self.c3[1]), self.angle + 45, 10)
        check4 = True
        while self.c4[0] < 1200 and self.c4[0] >= 0 and self.c4[1] >= 0 and self.c4[1] < 600 and check4: 
            for obstacle in arr:
                offset = (int(self.c4[0] - obstacle.x), int(self.c4[1] - obstacle.y))
                if mask.overlap(self.mask, offset) != None: 
                    check4 = False
            self.c4 = self.move_lines((self.c4[0], self.c4[1]), self.angle - 90, 10)
        check5 = True
        while self.c5[0] < 1200 and self.c5[0] >= 0 and self.c5[1] >= 0 and self.c5[1] < 600 and check5: 
            for obstacle in arr:
                offset = (int(self.c5[0] - obstacle.x), int(self.c5[1] - obstacle.y))
                if mask.overlap(self.mask, offset) != None: 
                    check5 = False
            self.c5 = self.move_lines((self.c5[0], self.c5[1]), self.angle + 90, 10)
    

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
        win.blit(rotated_image, new_rect.topleft)
