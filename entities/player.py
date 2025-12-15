import pygame
from utils.constants import *
import os

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.velocity_y = 0
        self.on_ground = False
        self.alive = True
        
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        
        self.walking_frames = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join(assets_dir, f'walking{i}.png'))
            img = pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
            self.walking_frames.append(img)
        
        self.jumping_frames = []
        for i in range(1, 4):
            img = pygame.image.load(os.path.join(assets_dir, f'jumping{i}.png'))
            img = pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
            self.jumping_frames.append(img)
        
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, ground_y, platforms=[], trampolines=[]):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.on_ground = False

        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.velocity_y = 0
            self.on_ground = True

        for platform in platforms:
            player_rect = self.get_rect()
            platform_rect = platform.get_rect()
            
            if (player_rect.colliderect(platform_rect) and 
                self.velocity_y >= 0 and
                player_rect.bottom - self.velocity_y <= platform_rect.top + 5):
                self.y = platform_rect.top - self.height
                self.velocity_y = 0
                self.on_ground = True
                break
        
        for trampoline in trampolines:
            player_rect = self.get_rect()
            trampoline_rect = trampoline.get_rect()
            
            if (player_rect.colliderect(trampoline_rect) and 
                self.velocity_y >= 0 and
                player_rect.bottom - self.velocity_y <= trampoline_rect.top + 5):
                self.y = trampoline_rect.top - self.height
                self.velocity_y = JUMP_STRENGTH * 1.8
                self.on_ground = False
                trampoline.activate_bounce()
                break
        
        self.animation_counter += self.animation_speed
        if self.on_ground:
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
        else:
            if self.velocity_y < -5: 
                self.current_frame = 0
            elif self.velocity_y < 0: 
                self.current_frame = 1
            else:  
                self.current_frame = 2

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.on_ground:
            frame = self.walking_frames[self.current_frame]
        else:
            frame = self.jumping_frames[self.current_frame]
        
        screen.blit(frame, (self.x, self.y))
