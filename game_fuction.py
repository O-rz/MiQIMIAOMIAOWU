import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from random import *
def check_events(ai_settings,screen,stats,play_button, ship,aliens, bullets):
    '''响应案件和鼠标'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
              check_keydown_events(event, ai_settings,screen, ship ,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                                                                          aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event , ai_settings,screen,ship,bullets):
    """响应摁键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
 #     响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
         ship.moving_left = False


def update_screen(ai_settings, screen,stats,sb, ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.screen.blit(bullet.image, bullet.rect)
    ship.blitme()
    aliens.draw(screen)
    # for bullet in bullets:
        # bullet.draw_bullet()
    # aliens.blitme()
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen,stats,sb,ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen,ship, aliens):
# 创建一个外星人，并计算一行可容纳多少个外星人
# 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                alien.rect.height)

# 创建第一行外星人
    n = 4
    for row_number in range(number_rows):
               n=n+1
               for alien_number in range(number_aliens_x-n):
                      create_alien(ai_settings, screen, aliens, alien_number,
row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y =  alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3*alien_height)- ship_height)
    number_rows = int (available_space_y/(2*alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():

       if alien.check_edges():
          change_fleet_direction(ai_settings, aliens)
          break
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    aliens.empty()
    bullets.empty()
# 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
# 暂停
    sleep(0.5)
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0:
    # 将ships_left减1
       stats.ships_left -= 1
    # 暂停一会儿
       sleep(0.5)
    else:
       stats.game_active = False
       pygame.mouse.set_visible(True)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
      ai_settings.initialize_dynamic_settings()
      pygame.mouse.set_visible(False)
      if play_button.rect.collidepoint(mouse_x, mouse_y):
# 重置游戏统计信息
       stats.reset_stats()
       stats.game_active = True
# 清空外星人列表和子弹列表
       aliens.empty()
       bullets.empty()
# 创建一群新的外星人，并让飞船居中
       create_fleet(ai_settings, screen, ship, aliens)
       ship.center_ship()
