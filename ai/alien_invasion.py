import sys
import pygame
from pygame.sprite import Group
from ai.settings import Settings
from ai.game_stats import GameStats
from ai.scoreboard import Scoreboard
from ai.button import Button
from ai.ship import Ship
from ai.alien import Alien
from ai.boss import Boss
import ai.game_functions as gf


def run_game():
    # Uruchom gre i zimportuj ustawienia z settings.py.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Stworz przycisk do uruchomienia gry
    play_button = Button(ai_settings, screen, "Graj")

    # Stworz instancje do przetrzymywania statystyk gry i tworzenia scoreboardu
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Stworz statek, kule i kosmitow
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alienBullets = Group()
    aliens = Group()
    boss = Boss(ai_settings, screen)

    # Stworz flote kosmitow
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Stworz petle dla gry
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            bullets.update()
            alienBullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alienBullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alienBullets)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                             play_button, alienBullets)


run_game()
