import pygame
from data.levels import LEVELS
from utils.constants import *

class Menu:
    def __init__(self):
        self.selected_level = 0
        self.unlocked_levels = 1
        self.in_menu = True
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def unlock_next_level(self):
        if self.unlocked_levels < len(LEVELS):
            self.unlocked_levels += 1

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = max(0, self.selected_level - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(self.unlocked_levels - 1, self.selected_level + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.in_menu = False
                return True
        return False

    def draw(self, screen):
        screen.fill((20, 0, 20))
        
        title = self.font_large.render("INTERFERENCE DASH", True, NEON_GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - 350, 50))
        
        subtitle = self.font_small.render("escape the apocalypse, reach rosen shingle creek", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - 350, 130))
        
        instructions = self.font_small.render("use arrow keys to select, enter to start", True, (150, 150, 150))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60))
        
        start_y = 220
        for i, level in enumerate(LEVELS):
            if i < self.unlocked_levels:
                color = NEON_PINK if i == self.selected_level else WHITE
                level_name = level["name"].upper()
                
                if i == self.selected_level:
                    arrow = "> "
                else:
                    arrow = "  "
                
                level_text = self.font_medium.render(f"{arrow}{i + 1}. {level_name}", True, color)
                screen.blit(level_text, (SCREEN_WIDTH // 2 - 250, start_y + i * 70))
                
                if level["end_score"] == -1:
                    mode_text = self.font_small.render("(endless)", True, (150, 150, 150))
                else:
                    mode_text = self.font_small.render(f"(goal: {level['end_score']} pts)", True, (150, 150, 150))
                screen.blit(mode_text, (SCREEN_WIDTH // 2 + 100, start_y + i * 70 + 10))
            else:
                level_text = self.font_medium.render(f"  {i + 1}. LOCKED", True, (80, 80, 80))
                screen.blit(level_text, (SCREEN_WIDTH // 2 - 250, start_y + i * 70))
