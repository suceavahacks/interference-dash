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
            pygame.draw.polygon(screen, (200, 0, 0), points)
            pygame.draw.polygon(screen, (255, 50, 50), points, 3)
        elif self.type == "block":
            pygame.draw.rect(screen, (150, 0, 0), self.get_rect())
            pygame.draw.rect(screen, (200, 50, 50), self.get_rect(), 3)
            for i in range(int(self.height / 10)):
                y_line = self.y + (i * 10)
                pygame.draw.line(screen, (100, 0, 0), (self.x, y_line), (self.x + self.width, y_line), 2)
        elif self.type == "platform":
            pygame.draw.rect(screen, (180, 0, 0), self.get_rect())
            for i in range(0, int(self.width), 20):
                pygame.draw.line(screen, (120, 0, 0), (self.x + i, self.y), (self.x + i, self.y + self.height), 2)
            pygame.draw.rect(screen, (220, 50, 50), self.get_rect(), 2)
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
            pygame.draw.polygon(screen, (200, 0, 0), points1)
            pygame.draw.polygon(screen, (200, 0, 0), points2)
            pygame.draw.polygon(screen, (255, 50, 50), points1, 3)
            pygame.draw.polygon(screen, (255, 50, 50), points2, 3)
        else:
            pygame.draw.rect(screen, (150, 0, 0), self.get_rect())