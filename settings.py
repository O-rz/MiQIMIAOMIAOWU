class Settings():
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 50
        self.bullet_height = 50
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 10
        # 外星人设置
        self.fleet_drop_speed = 5
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
       self.ship_speed_factor *= self.speedup_scale
       self.bullet_speed_factor *= self.speedup_scale
       self.alien_speed_factor *= self.speedup_scale