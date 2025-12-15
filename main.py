import pygame
from utils.constants import *
from entities.player import Player
from systems.level import Level
from systems.interference import InterferenceSystem
from systems.menu import Menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("interference-dash")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def reset_game(starting_level=0):
    player = Player(200, SCREEN_HEIGHT - 100 - PLAYER_SIZE)
    level = Level()
    level.current_level_index = starting_level
    level.bg_color = level.get_current_level()["bg_color"]
    level.load_level_patterns()
    interference = InterferenceSystem()
    score = 0
    speed = BASE_SPEED
    multiplier = SCORE_MULTIPLIER_BASE
    difficulty = 1.0
    return player, level, interference, score, speed, multiplier, difficulty

menu = Menu()
player, level, interference, score, speed, multiplier, difficulty = reset_game()
running = True
game_over = False
in_game = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if menu.in_menu:
            if menu.handle_input(event):
                in_game = True
                player, level, interference, score, speed, multiplier, difficulty = reset_game(menu.selected_level)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    player, level, interference, score, speed, multiplier, difficulty = reset_game(menu.selected_level)
                    game_over = False
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        menu.in_menu = True
                        in_game = False
                        game_over = False
                    else:
                        running = False

    if menu.in_menu:
        menu.draw(screen)
    else:
        if not game_over and in_game:
            player.update(level.ground_y, level.platforms, level.trampolines)
            level.update(speed, difficulty, player.x)
            interference.update()

            for drink in level.collectibles:
                if not drink.collected and player.get_rect().colliderect(drink.get_rect()):
                    drink.collected = True
                    speed += SPEED_INCREMENT
                    multiplier += 0.2
                    difficulty += 0.15
                    interference.add_interference(INTERFERENCE_PER_DRINK)

            for obs in level.obstacles:
                if player.get_rect().colliderect(obs.get_rect()):
                    game_over = True
            
            for animated_obs in level.animated_obstacles:
                if player.get_rect().colliderect(animated_obs.get_rect()):
                    game_over = True

            score += int(1 * multiplier)
            
            level_changed = level.check_level_progression(score)
            if level_changed:
                menu.unlock_next_level()
                
                speed = BASE_SPEED
                multiplier = 1.0
                difficulty = 1.0
                interference.level = 0
                player.x = 100
                player.y = level.ground_y - PLAYER_SIZE
                player.velocity_y = 0
                player.on_ground = False
                score = 0
                
                font_big = pygame.font.Font(None, 72)
                level_up_text = font_big.render(f"LEVEL UP: {level.get_current_level()['name'].upper()}", True, NEON_GREEN)
                screen.blit(level_up_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(1500)

        shake_offset = interference.get_shake_offset()
        level.draw(screen, shake_offset)

        player.draw(screen)

        panel_x = 20
        panel_y = 20
        panel_width = 280
        panel_height = 210
        panel_padding = 15
        
        panel_bg = pygame.Surface((panel_width, panel_height))
        panel_bg.set_alpha(180)
        panel_bg.fill((20, 10, 30))
        screen.blit(panel_bg, (panel_x, panel_y))
        
        pygame.draw.rect(screen, (100, 255, 200), (panel_x, panel_y, panel_width, panel_height), 3, 8)
        
        corner_size = 10
        corner_color = (100, 255, 200)
        corners = [
            (panel_x, panel_y),
            (panel_x + panel_width - corner_size, panel_y),
            (panel_x, panel_y + panel_height - corner_size),
            (panel_x + panel_width - corner_size, panel_y + panel_height - corner_size)
        ]
        for cx, cy in corners:
            pygame.draw.rect(screen, corner_color, (cx, cy, corner_size, corner_size))
        
        text_x = panel_x + panel_padding
        text_y = panel_y + panel_padding
        line_height = 38
        
        font_label = pygame.font.Font(None, 28)
        font_value = pygame.font.Font(None, 42)
        
        level_name = level.get_current_level()["name"].upper()
        level_label = font_label.render("LEVEL", True, (150, 150, 150))
        level_value = font_value.render(level_name, True, (100, 255, 200))
        screen.blit(level_label, (text_x, text_y))
        screen.blit(level_value, (text_x, text_y + 18))
        
        score_label = font_label.render("SCORE", True, (150, 150, 150))
        score_value = font_value.render(str(score), True, (255, 200, 120))
        screen.blit(score_label, (text_x, text_y + line_height * 1 + 10))
        screen.blit(score_value, (text_x, text_y + line_height * 1 + 28))
        
        interference_label = font_label.render("INTERFERENCE", True, (150, 150, 150))
        interference_value = font_value.render(str(int(interference.level)), True, (255, 100, 150))
        screen.blit(interference_label, (text_x, text_y + line_height * 2 + 20))
        screen.blit(interference_value, (text_x, text_y + line_height * 2 + 38))
        
        diff_label = font_label.render("DIFFICULTY", True, (150, 150, 150))
        diff_value = font_value.render(f"{difficulty:.1f}x", True, (255, 150, 50))
        screen.blit(diff_label, (text_x, text_y + line_height * 3 + 30))
        screen.blit(diff_value, (text_x, text_y + line_height * 3 + 48))
        
        bar_panel_x = SCREEN_WIDTH - 260
        bar_panel_y = SCREEN_HEIGHT - 80
        bar_panel_width = 240
        bar_panel_height = 60
        
        bar_bg = pygame.Surface((bar_panel_width, bar_panel_height))
        bar_bg.set_alpha(180)
        bar_bg.fill((20, 10, 30))
        screen.blit(bar_bg, (bar_panel_x, bar_panel_y))
        
        pygame.draw.rect(screen, (100, 255, 200), (bar_panel_x, bar_panel_y, bar_panel_width, bar_panel_height), 3, 8)
        
        corners_bar = [
            (bar_panel_x, bar_panel_y),
            (bar_panel_x + bar_panel_width - corner_size, bar_panel_y),
            (bar_panel_x, bar_panel_y + bar_panel_height - corner_size),
            (bar_panel_x + bar_panel_width - corner_size, bar_panel_y + bar_panel_height - corner_size)
        ]
        for cx, cy in corners_bar:
            pygame.draw.rect(screen, corner_color, (cx, cy, corner_size, corner_size))
        
        speed_bar_width = 200
        speed_bar_height = 20
        speed_bar_x = bar_panel_x + 20
        speed_bar_y = bar_panel_y + 30
        
        pygame.draw.rect(screen, (40, 30, 50), (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 0, 5)
        
        speed_display = speed / BASE_SPEED
        speed_fill = min((speed / (BASE_SPEED * 3)) * speed_bar_width, speed_bar_width)
        fill_width = int(speed_fill)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(speed_bar_x, speed_bar_y, fill_width, speed_bar_height)
            if speed_display < 1.5:
                bar_color = (100, 255, 200)
            elif speed_display < 2.5:
                bar_color = (255, 200, 100)
            else:
                bar_color = (255, 100, 150)
            pygame.draw.rect(screen, bar_color, fill_rect, 0, 5)
        
        pygame.draw.rect(screen, (100, 255, 200), (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 2, 5)
        
        speed_label = font_label.render(f"SPEED: {speed_display:.1f}x", True, WHITE)
        screen.blit(speed_label, (speed_bar_x + 5, bar_panel_y + 8))

        if game_over:
            game_over_text = font.render("GAME OVER - R: restart | ESC: menu", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()