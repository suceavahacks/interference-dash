import random
from entities.obstacle import Obstacle
from entities.collectible import EnergyDrink
from entities.platform import Platform
from data.levels import LEVELS
from utils.constants import *

class Level:
    def __init__(self):
        self.obstacles = []
        self.collectibles = []
        self.platforms = []
        self.ground_y = SCREEN_HEIGHT - 100
        self.current_level_index = 0
        self.score_in_level = 0
        self.bg_color = LEVELS[0]["bg_color"]
        self.level_completed = False
        self.pattern_offset = 0
        self.procedural_next_obstacle_x = SCREEN_WIDTH
        self.procedural_next_collectible_x = SCREEN_WIDTH + 300
        self.procedural_next_platform_x = SCREEN_WIDTH + 600
        self.load_level_patterns()

    def get_current_level(self):
        return LEVELS[self.current_level_index]

    def load_level_patterns(self):
        self.obstacles.clear()
        self.collectibles.clear()
        self.platforms.clear()
        
        current = self.get_current_level()
        
        if current.get("procedural", False):
            return
        
        for pattern in current["obstacle_patterns"]:
            base_x = pattern["x"]
            for i in range(6):
                x_pos = base_x + (i * pattern["spacing"])
                
                if pattern["type"] == "spike":
                    height = OBSTACLE_HEIGHT
                    width = OBSTACLE_WIDTH
                elif pattern["type"] == "block":
                    height = random.randint(40, 100)
                    width = OBSTACLE_WIDTH
                elif pattern["type"] == "double_spike":
                    height = OBSTACLE_HEIGHT
                    width = OBSTACLE_WIDTH * 2
                
                obs = Obstacle(x_pos, self.ground_y - height, width, height, pattern["type"])
                self.obstacles.append(obs)
        
        for pos in current["collectible_positions"]:
            for i in range(5):
                x_pos = pos["x"] + (i * 700)
                drink = EnergyDrink(x_pos, self.ground_y - pos["y"])
                self.collectibles.append(drink)
        
        for pos in current["platform_positions"]:
            for i in range(4):
                x_pos = pos["x"] + (i * 800)
                platform = Platform(x_pos, self.ground_y - pos["y"], pos["width"], 20)
                self.platforms.append(platform)

    def check_level_progression(self, score):
        current = self.get_current_level()
        if current["end_score"] != -1 and score >= current["end_score"]:
            if self.current_level_index < len(LEVELS) - 1:
                self.current_level_index += 1
                self.score_in_level = 0
                self.bg_color = LEVELS[self.current_level_index]["bg_color"]
                self.level_completed = False
                self.load_level_patterns()
                return True
        return False

    def generate_procedural_obstacle(self):
        current = self.get_current_level()
        if not current.get("procedural", False):
            return
        
        if random.random() > current["obstacle_frequency"]:
            return
        
        obstacle_type = random.choice(current["obstacle_types"])
        
        if obstacle_type == "spike":
            height = OBSTACLE_HEIGHT
            width = OBSTACLE_WIDTH
        elif obstacle_type == "block":
            height = random.randint(40, 100)
            width = OBSTACLE_WIDTH
        elif obstacle_type == "double_spike":
            height = OBSTACLE_HEIGHT
            width = OBSTACLE_WIDTH * 2
        
        obs = Obstacle(self.procedural_next_obstacle_x, self.ground_y - height, width, height, obstacle_type)
        self.obstacles.append(obs)
        self.procedural_next_obstacle_x += random.randint(200, 400)

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

    def update(self, speed):
        for obs in self.obstacles:
            obs.update(speed)
        
        for drink in self.collectibles:
            drink.update(speed)

        for platform in self.platforms:
            platform.update(speed)

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]
        self.collectibles = [drink for drink in self.collectibles if not drink.is_off_screen()]
        self.platforms = [p for p in self.platforms if not p.is_off_screen()]

        current = self.get_current_level()
        if current.get("procedural", False):
            if self.procedural_next_obstacle_x < SCREEN_WIDTH + 500:
                self.generate_procedural_obstacle()
            
            if self.procedural_next_collectible_x < SCREEN_WIDTH + 600:
                self.generate_procedural_collectible()

            if self.procedural_next_platform_x < SCREEN_WIDTH + 700:
                self.generate_procedural_platform()

    def draw(self, screen, shake_offset):
        offset_x, offset_y = shake_offset
        
        for platform in self.platforms:
            shifted_platform = Platform(platform.x + offset_x, platform.y + offset_y, platform.width, platform.height)
            shifted_platform.draw(screen)
        
        for obs in self.obstacles:
            screen_obs = Obstacle(obs.x + offset_x, obs.y + offset_y, obs.width, obs.height, obs.type)
            screen_obs.draw(screen)
        
        for drink in self.collectibles:
            if not drink.collected:
                rect = drink.get_rect()
                shifted_drink = EnergyDrink(rect.x + offset_x, rect.y + offset_y)
                shifted_drink.draw(screen)