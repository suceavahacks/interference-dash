import random
import json
import os
import pygame
from entities.obstacle import Obstacle
from entities.collectible import EnergyDrink
from entities.platform import Platform
from entities.trampoline import Trampoline
from entities.animated_obstacle import AnimatedObstacle
from data.levels import LEVELS
from utils.constants import *

class Level:
    def __init__(self):
        self.obstacles = []
        self.collectibles = []
        self.platforms = []
        self.trampolines = []
        self.animated_obstacles = []  
        self.ground_y = SCREEN_HEIGHT - 100
        self.current_level_index = 0
        self.score_in_level = 0
        self.bg_color = LEVELS[0]["bg_color"]
        self.level_completed = False
        self.pattern_offset = 0
        self.procedural_next_obstacle_x = SCREEN_WIDTH
        self.procedural_next_collectible_x = SCREEN_WIDTH + 300
        self.procedural_next_platform_x = SCREEN_WIDTH + 600
        self.procedural_next_trampoline_x = SCREEN_WIDTH + 500
        self.procedural_next_animated_x = SCREEN_WIDTH + 400  
        self.pattern_cycle = 0
        self.last_generated_x = SCREEN_WIDTH
        self.max_level_x = 0
        self.progress_file = "levels_progress.txt"
        self.bg_scroll_x = 0
        
        self.background_images = []
        for i in range(1, 6):
            try:
                bg = pygame.image.load(f"assets/bg_level{i}.jpeg")
                bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.background_images.append(bg)
            except Exception as e:
                print(f"Error loading background {i}: {e}")
                self.background_images.append(None)
        
        self.load_level_patterns()

    def save_progress(self):
        """Save the highest unlocked level to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump({
                    'highest_level': self.current_level_index,
                    'total_levels': len(LEVELS)
                }, f)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def load_progress(self):
        """Load progress from file"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    return data.get('highest_level', 0)
        except Exception as e:
            print(f"Error loading progress: {e}")
        return 0

    def get_current_level(self):
        return LEVELS[self.current_level_index]

    def load_level_patterns(self):
        self.obstacles.clear()
        self.collectibles.clear()
        self.platforms.clear()
        self.trampolines.clear()
        self.animated_obstacles.clear()
        
        current = self.get_current_level()
        
        if current.get("procedural", False):
            self.procedural_next_obstacle_x = SCREEN_WIDTH
            self.procedural_next_collectible_x = SCREEN_WIDTH + 300
            self.procedural_next_platform_x = SCREEN_WIDTH + 600
            self.procedural_next_trampoline_x = SCREEN_WIDTH + 500
            self.procedural_next_animated_x = SCREEN_WIDTH + 400
            return
        
        self.max_level_x = 0
        
        for obs_data in current["obstacles"]:
            if obs_data["type"] == "spike":
                size = 80
                zombie = AnimatedObstacle(obs_data["x"], self.ground_y - size + 20, size)
                self.animated_obstacles.append(zombie)
                if obs_data["x"] > self.max_level_x:
                    self.max_level_x = obs_data["x"]
            elif obs_data["type"] == "double_spike":
                size = 80
                zombie1 = AnimatedObstacle(obs_data["x"], self.ground_y - size + 20, size)
                zombie2 = AnimatedObstacle(obs_data["x"] + size, self.ground_y - size + 20, size)
                self.animated_obstacles.append(zombie1)
                self.animated_obstacles.append(zombie2)
                if obs_data["x"] > self.max_level_x:
                    self.max_level_x = obs_data["x"]
            elif obs_data["type"] == "block":
                height = obs_data.get("height", 60)
                width = OBSTACLE_WIDTH
                obs = Obstacle(obs_data["x"], self.ground_y - height, width, height, obs_data["type"])
                self.obstacles.append(obs)
                if obs_data["x"] > self.max_level_x:
                    self.max_level_x = obs_data["x"]
        
        for coll_data in current["collectibles"]:
            drink = EnergyDrink(coll_data["x"], self.ground_y - coll_data["y"])
            self.collectibles.append(drink)
            if coll_data["x"] > self.max_level_x:
                self.max_level_x = coll_data["x"]
        
        for plat_data in current["platforms"]:
            platform = Platform(plat_data["x"], self.ground_y - plat_data["y"], plat_data["width"], 20)
            self.platforms.append(platform)
            if plat_data["x"] > self.max_level_x:
                self.max_level_x = plat_data["x"]
        
        for tramp_data in current.get("trampolines", []):
            trampoline = Trampoline(tramp_data["x"], self.ground_y - tramp_data["y"], tramp_data.get("width", 100), 30)
            self.trampolines.append(trampoline)
            if tramp_data["x"] > self.max_level_x:
                self.max_level_x = tramp_data["x"]
        
        self.last_generated_x = self.max_level_x + 500
        self.pattern_cycle = 0

    def repeat_level_pattern(self):
        current = self.get_current_level()
        
        if current.get("procedural", False):
            return
        
        offset = self.last_generated_x
        
        for obs_data in current["obstacles"]:
            if obs_data["type"] == "spike":
                size = 80
                zombie = AnimatedObstacle(obs_data["x"] + offset, self.ground_y - size + 20, size)
                self.animated_obstacles.append(zombie)
            elif obs_data["type"] == "double_spike":
                size = 80
                zombie1 = AnimatedObstacle(obs_data["x"] + offset, self.ground_y - size + 20, size)
                zombie2 = AnimatedObstacle(obs_data["x"] + offset + size, self.ground_y - size + 20, size)
                self.animated_obstacles.append(zombie1)
                self.animated_obstacles.append(zombie2)
            elif obs_data["type"] == "block":
                height = obs_data.get("height", 60)
                width = OBSTACLE_WIDTH
                obs = Obstacle(obs_data["x"] + offset, self.ground_y - height, width, height, obs_data["type"])
                self.obstacles.append(obs)
        
        for coll_data in current["collectibles"]:
            drink = EnergyDrink(coll_data["x"] + offset, self.ground_y - coll_data["y"])
            self.collectibles.append(drink)
        
        for plat_data in current["platforms"]:
            platform = Platform(plat_data["x"] + offset, self.ground_y - plat_data["y"], plat_data["width"], 20)
            self.platforms.append(platform)
        
        for tramp_data in current.get("trampolines", []):
            trampoline = Trampoline(tramp_data["x"] + offset, self.ground_y - tramp_data["y"], tramp_data.get("width", 100), 30)
            self.trampolines.append(trampoline)
        
        self.last_generated_x = offset + self.max_level_x + 500
        self.pattern_cycle += 1

    def check_level_progression(self, score):
        current = self.get_current_level()
        if current["end_score"] != -1 and score >= current["end_score"]:
            if self.current_level_index < len(LEVELS) - 1:
                self.current_level_index += 1
                self.score_in_level = 0
                self.bg_color = LEVELS[self.current_level_index]["bg_color"]
                self.level_completed = False

                self.save_progress()
                
                self.pattern_cycle = 0
                self.last_generated_x = SCREEN_WIDTH
                self.max_level_x = 0
                self.procedural_next_obstacle_x = SCREEN_WIDTH
                self.procedural_next_collectible_x = SCREEN_WIDTH + 300
                self.procedural_next_platform_x = SCREEN_WIDTH + 600
                self.procedural_next_trampoline_x = SCREEN_WIDTH + 500
                self.procedural_next_animated_x = SCREEN_WIDTH + 400
                
                self.load_level_patterns()
                return True
        return False

    def generate_procedural_obstacle(self, difficulty=1.0):
        current = self.get_current_level()
        if not current.get("procedural", False):
            return
        
        frequency = current["obstacle_frequency"] * difficulty
        if random.random() > min(frequency, 0.95):
            return
        
        obstacle_type = random.choice(current["obstacle_types"])
        
        if obstacle_type == "spike":
            size = 80
            zombie = AnimatedObstacle(self.procedural_next_obstacle_x, self.ground_y - size + 20, size)
            self.animated_obstacles.append(zombie)
            spacing = random.randint(200, 400) / difficulty
            self.procedural_next_obstacle_x += int(spacing)
        elif obstacle_type == "double_spike":
            size = 80
            zombie1 = AnimatedObstacle(self.procedural_next_obstacle_x, self.ground_y - size + 20, size)
            zombie2 = AnimatedObstacle(self.procedural_next_obstacle_x + size, self.ground_y - size + 20, size)
            self.animated_obstacles.append(zombie1)
            self.animated_obstacles.append(zombie2)
            spacing = random.randint(200, 400) / difficulty
            self.procedural_next_obstacle_x += int(spacing)
        elif obstacle_type == "block":
            height = random.randint(40, 100)
            width = OBSTACLE_WIDTH
            obs = Obstacle(self.procedural_next_obstacle_x, self.ground_y - height, width, height, obstacle_type)
            self.obstacles.append(obs)
            spacing = random.randint(200, 400) / difficulty
            self.procedural_next_obstacle_x += int(spacing)

    def generate_procedural_collectible(self):
        current = self.get_current_level()
        if not current.get("procedural", False):
            return
        
        if random.random() > current["collectible_frequency"]:
            return
        
        y_pos = self.ground_y - random.randint(50, 250)
        drink = EnergyDrink(self.procedural_next_collectible_x, y_pos)
        self.collectibles.append(drink)
        self.procedural_next_collectible_x += random.randint(400, 700)

    def generate_procedural_platform(self):
        current = self.get_current_level()
        if not current.get("procedural", False):
            return
        
        if random.random() > current["platform_frequency"]:
            return
        
        width = random.randint(80, 150)
        height = 20
        y_pos = self.ground_y - random.randint(80, 180)
        platform = Platform(self.procedural_next_platform_x, y_pos, width, height)
        self.platforms.append(platform)
        self.procedural_next_platform_x += random.randint(300, 600)
    
    def generate_procedural_trampoline(self):
        current = self.get_current_level()
        if not current.get("procedural", False):
            return
        
        if random.random() > 0.15:
            return
        
        width = random.randint(90, 120)
        y_pos = self.ground_y - random.randint(50, 120)
        trampoline = Trampoline(self.procedural_next_trampoline_x, y_pos, width, 30)
        self.trampolines.append(trampoline)
        self.procedural_next_trampoline_x += random.randint(400, 800)

    def update(self, speed, difficulty=1.0, player_x=None):
        self.bg_scroll_x -= speed * 0.3
        if self.bg_scroll_x <= -SCREEN_WIDTH:
            self.bg_scroll_x = 0
        
        for obs in self.obstacles:
            obs.update(speed)
        
        for drink in self.collectibles:
            drink.update(speed)
        
        for animated_obs in self.animated_obstacles:
            animated_obs.update(speed, player_x)

        for platform in self.platforms:
            platform.update(speed)
        
        for trampoline in self.trampolines:
            trampoline.update(speed)

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]
        self.collectibles = [drink for drink in self.collectibles if not drink.is_off_screen()]
        self.platforms = [p for p in self.platforms if not p.is_off_screen()]
        self.trampolines = [t for t in self.trampolines if not t.is_off_screen()]
        self.animated_obstacles = [anim for anim in self.animated_obstacles if not anim.is_off_screen()]

        current = self.get_current_level()
        if current.get("procedural", False):
            if self.procedural_next_obstacle_x < SCREEN_WIDTH + 500:
                self.generate_procedural_obstacle(difficulty)
            
            if self.procedural_next_collectible_x < SCREEN_WIDTH + 600:
                self.generate_procedural_collectible()

            if self.procedural_next_platform_x < SCREEN_WIDTH + 700:
                self.generate_procedural_platform()
            
            if self.procedural_next_trampoline_x < SCREEN_WIDTH + 750:
                self.generate_procedural_trampoline()
        else:
            rightmost_x = 0
            for obs in self.obstacles:
                if obs.x > rightmost_x:
                    rightmost_x = obs.x
            for drink in self.collectibles:
                if drink.x > rightmost_x:
                    rightmost_x = drink.x
            for plat in self.platforms:
                if plat.x > rightmost_x:
                    rightmost_x = plat.x
            
            if rightmost_x < SCREEN_WIDTH + 1000:
                self.repeat_level_pattern()

    def draw(self, screen, shake_offset):
        if self.current_level_index < len(self.background_images) and self.background_images[self.current_level_index]:
            bg = self.background_images[self.current_level_index]
            bg_x1 = self.bg_scroll_x
            bg_x2 = self.bg_scroll_x + SCREEN_WIDTH
            
            screen.blit(bg, (bg_x1, 0))
            screen.blit(bg, (bg_x2, 0))
        else:
            screen.fill(self.bg_color)
        
        offset_x, offset_y = shake_offset
        
        for platform in self.platforms:
            shifted_platform = Platform(platform.x + offset_x, platform.y + offset_y, platform.width, platform.height)
            shifted_platform.draw(screen)
        
        for trampoline in self.trampolines:
            shifted_trampoline = Trampoline(trampoline.x + offset_x, trampoline.y + offset_y, trampoline.width, trampoline.height)
            shifted_trampoline.bounce_animation = trampoline.bounce_animation
            shifted_trampoline.draw(screen)
        
        for obs in self.obstacles:
            screen_obs = Obstacle(obs.x + offset_x, obs.y + offset_y, obs.width, obs.height, obs.type)
            screen_obs.draw(screen)
        
        for animated_obs in self.animated_obstacles:
            temp_x = animated_obs.x
            animated_obs.x += offset_x
            animated_obs.y += offset_y
            animated_obs.draw(screen)
            animated_obs.x = temp_x
            animated_obs.y -= offset_y
        
        for drink in self.collectibles:
            if not drink.collected:
                rect = drink.get_rect()
                shifted_drink = EnergyDrink(rect.x + offset_x, rect.y + offset_y)
                shifted_drink.draw(screen)