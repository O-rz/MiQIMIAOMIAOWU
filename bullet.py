import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """蹦蹦炸弹"""
    def __init__(self,ai_settings, screen, ship):
        """创"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/bull.jpeg.png')
        self.image = pygame.transform.scale(self.image, (ai_settings.bullet_width,ai_settings.bullet_height ))
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.screen.blit(self.image, self.rect)
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        pygame.display.flip()
    def update(self):
        self.y -= self.speed_factor
#更新表示子弹的rect的位置
        self.rect.y = self.y

    # def draw_bullet(self):
    #      pygame.draw.rect(self.screen, self.color, self.rect)


