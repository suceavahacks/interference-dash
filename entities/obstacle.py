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
        elif self.type == "block":
            pygame.draw.rect(screen, RED, self.get_rect())
            pygame.draw.rect(screen, (255, 100, 100), self.get_rect(), 3)
        elif self.type == "platform":
            pygame.draw.rect(screen, (200, 0, 0), self.get_rect())
            for i in range(0, int(self.width), 20):
                pygame.draw.line(screen, (150, 0, 0), (self.x + i, self.y), (self.x + i, self.y + self.height), 2)
        elif self.type == "double_spike":
            spike_width = self.width // 2
            points1 = [
                (self.x + spike_width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + spike_width, self.y + self.height)
            ]
            points2 = [
                (self.x + spike_width + spike_width // 2, self.y),
                (self.x + spike_width, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, RED, points1)
            pygame.draw.polygon(screen, RED, points2)
        else:
            pygame.draw.rect(screen, RED, self.get_rect())