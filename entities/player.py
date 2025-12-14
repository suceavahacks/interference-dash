import pygame # type: ignore
from utils.constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.velocity_y = 0
        self.on_ground = False
        self.alive = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, ground_y, platforms=[]):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.on_ground = False

        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.velocity_y = 0
            self.on_ground = True

        for platform in platforms:
            if self.velocity_y > 0:
                player_rect = self.get_rect()
                platform_rect = platform.get_rect()
                
                if player_rect.colliderect(platform_rect):
                    if player_rect.bottom <= platform_rect.top + 15:
                        self.y = platform_rect.top - self.height
                        self.velocity_y = 0
                        self.on_ground = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, NEON_GREEN, self.get_rect())
