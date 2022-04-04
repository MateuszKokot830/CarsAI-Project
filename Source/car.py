from tkinter import SW
import pygame
import math

class Car:
    def __init__(self, image, start_pos, velocity, rotation_vel):
        self.img = image
        self.posX, self.posY = start_pos
        self.velocity = velocity
        self.rotation_vel = rotation_vel
        self.angle = 270
        self.alive = True
        self.subsurface = pygame.Surface((20, 40))


    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def draw(self, win):
        rotate_center(win, self.img, (self.posX, self.posY), self.angle)


    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        
        self.posY -= vertical
        self.posX -= horizontal


    def check_collision(self, array):
        if self.posX + 20 > 1200 or self.posX < 0 or self.posY < 0 or self.posY + 40 > 600:
            self.alive = False
        for item in array:
            if self.subsurface.get_rect(topleft=(self.posX, self.posY)).colliderect(item.subsurface.get_rect(topleft=(item.x, item.y))):
                self.alive = False


def rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)