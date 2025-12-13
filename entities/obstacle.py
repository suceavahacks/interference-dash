import pygame 
from utils.constants import *

class Obstacle:
    def __init__(self,x,y,width,height,obstacle_type="spike"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type

    def update(self,speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.width < 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self,screen):
        if self.type == "spike":
            points = [
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, RED, points)

        else:
            pygame.draw.rect(screen, RED, self.get_rect())