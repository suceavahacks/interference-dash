import pygame
from utils.constants import *

class Apocalypse:
    def __init__(self):
        self.x = -200
        self.width = 200
        self.speed = APOCALYPSE_SPEED

    def update(self):
        self.x += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 0, 0), (self.x, 0, self.width, SCREEN_HEIGHT))
        for i in range(5):
            offset = i * 40
