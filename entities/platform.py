import pygame
from utils.constants import *

class Platform:
    platform_image = None
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        if Platform.platform_image is None:
            try:
                Platform.platform_image = pygame.image.load("assets/platform.png")
            except Exception as e:
                print(f"Error loading platform image: {e}")
                Platform.platform_image = False

    def update(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if Platform.platform_image and Platform.platform_image is not False:
            scaled_img = pygame.transform.scale(Platform.platform_image, (self.width, self.height))
            screen.blit(scaled_img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (60, 60, 60), self.get_rect())
            for i in range(0, int(self.width), 20):
                pygame.draw.line(screen, (40, 40, 40), (self.x + i, self.y), (self.x + i, self.y + self.height), 2)
            pygame.draw.rect(screen, (120, 120, 120), self.get_rect(), 2)
