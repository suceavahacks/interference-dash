LEVELS = [
    {
        "name": "tutorial",
        "bg_color": (100, 0, 0),
        "obstacle_patterns": [
            {"type": "spike", "x": 1000, "spacing": 500},
            {"type": "spike", "x": 3000, "spacing": 600},
        ],
        "collectible_positions": [
            {"x": 1200, "y": 150},
            {"x": 2500, "y": 200},
        ],
        "platform_positions": [
            {"x": 1800, "y": 120, "width": 120},
        ],
        "end_score": 2000,
        "speed_multiplier": 1.0
    },
    {
        "name": "warming up",
        "bg_color": (80, 20, 0),
        "obstacle_patterns": [
            {"type": "spike", "x": 1000, "spacing": 450},
            {"type": "block", "x": 2000, "spacing": 500},
            {"type": "spike", "x": 3500, "spacing": 400},
        ],
        "collectible_positions": [
            {"x": 1300, "y": 150},
            {"x": 2300, "y": 200},
            {"x": 3800, "y": 180},
        ],
        "platform_positions": [
            {"x": 1700, "y": 130, "width": 110},
            {"x": 3200, "y": 140, "width": 120},
        ],
        "end_score": 4000,
        "speed_multiplier": 1.1
    },
    {
        "name": "getting spicy",
        "bg_color": (60, 0, 20),
        "obstacle_patterns": [
            {"type": "spike", "x": 1000, "spacing": 400},
            {"type": "block", "x": 2200, "spacing": 450},
            {"type": "double_spike", "x": 3500, "spacing": 500},
        ],
        "collectible_positions": [
            {"x": 1400, "y": 180},
            {"x": 2600, "y": 150},
            {"x": 3900, "y": 200},
        ],
        "platform_positions": [
            {"x": 1800, "y": 130, "width": 100},
            {"x": 3000, "y": 150, "width": 110},
        ],
        "end_score": 6500,
        "speed_multiplier": 1.2
    },
    {
        "name": "apocalypse rising",
        "bg_color": (40, 0, 40),
        "obstacle_patterns": [
            {"type": "spike", "x": 900, "spacing": 350},
            {"type": "block", "x": 2000, "spacing": 400},
            {"type": "double_spike", "x": 3200, "spacing": 450},
            {"type": "spike", "x": 4500, "spacing": 380},
        ],
        "collectible_positions": [
            {"x": 1200, "y": 170},
            {"x": 2400, "y": 190},
            {"x": 3600, "y": 160},
            {"x": 4800, "y": 180},
        ],
        "platform_positions": [
            {"x": 1600, "y": 135, "width": 100},
            {"x": 2800, "y": 145, "width": 105},
            {"x": 4100, "y": 140, "width": 110},
        ],
        "end_score": 10000,
        "speed_multiplier": 1.3
    },
    {
        "name": "endless chaos",
        "bg_color": (20, 0, 60),
        "obstacle_patterns": [],
        "collectible_positions": [],
        "platform_positions": [],
        "end_score": -1,
        "speed_multiplier": 1.4,
        "procedural": True,
        "obstacle_frequency": 0.7,
        "collectible_frequency": 0.5,
        "platform_frequency": 0.6,
        "obstacle_types": ["spike", "block", "double_spike"]
    }
]
