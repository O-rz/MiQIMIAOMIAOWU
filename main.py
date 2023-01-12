import pygame
from settings import Settings
from ship import Ship
import game_fuction as gf
from pygame.sprite import Group
from game_stats  import GameState
from button import Button
from alien import Alien
from scoreboard import Scoreboard
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    bullets = Group()
    pygame.display.set_caption("宇宙大战")
    aliens = Group()
    gf.create_fleet(ai_settings, screen,ship, aliens)
    stats = GameState(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, "Play")
    while True:
        gf.check_events(ai_settings, screen ,stats,play_button, ship,aliens, bullets)
        gf.update_screen(ai_settings, screen,stats,sb,  ship, aliens, bullets,play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats,sb,ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
run_game()
