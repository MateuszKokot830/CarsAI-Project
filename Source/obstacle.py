import pygame

class Obstacle:
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, width, height)
    


    def draw(self, win):
        #rect = self.mask.get_rect()
        #rect = rect.move(self.x, self.y)
        #col = (100, 100, 100)
        
        win.blit(self.image, (self.x, self.y, self.width, self.height))
        #pygame.draw.rect(win, col, rect)

