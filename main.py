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

        level_name = level.get_current_level()["name"].upper()
        level_text = font.render(f"level: {level_name}", True, WHITE)
        screen.blit(level_text, (20, 20))

        score_text = font.render(f"score: {score}", True, WHITE)
        screen.blit(score_text, (20, 60))

        speed_display = speed / BASE_SPEED
        speed_text = font.render(f"speed: {speed_display:.1f}x", True, (0, 255, 200))
        screen.blit(speed_text, (20, 100))

        interference_text = font.render(f"interference: {int(interference.level)}", True, NEON_PINK)
        screen.blit(interference_text, (20, 140))
        
        difficulty_text = font.render(f"difficulty: {difficulty:.1f}x", True, (255, 200, 0))
        screen.blit(difficulty_text, (20, 180))
        
        speed_bar_width = 200
        speed_bar_height = 15
        speed_bar_x = SCREEN_WIDTH - speed_bar_width - 20
        speed_bar_y = SCREEN_HEIGHT - 40
        pygame.draw.rect(screen, (50, 50, 50), (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height))
        speed_fill = min((speed / (BASE_SPEED * 3)) * speed_bar_width, speed_bar_width)
        color_intensity = min(255, int(speed_fill / speed_bar_width * 255))
        pygame.draw.rect(screen, (0, 255 - color_intensity, color_intensity), (speed_bar_x, speed_bar_y, int(speed_fill), speed_bar_height))
        pygame.draw.rect(screen, WHITE, (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 2)
        speed_label = pygame.font.Font(None, 24).render("SPEED", True, WHITE)
        screen.blit(speed_label, (speed_bar_x - 60, speed_bar_y - 2))

        if game_over:
            game_over_text = font.render("GAME OVER - R: restart | ESC: menu", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()