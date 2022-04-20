import pygame

class Obstacle:
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mask = pygame.mask.from_surface(self.image)


    def draw(self, win):
        win.blit(self.image, (self.x, self.y, self.width, self.height))

