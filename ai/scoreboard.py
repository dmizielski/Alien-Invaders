import pygame.font
from pygame.sprite import Group

from ai.ship import Ship


class Scoreboard:
    """ Klasa zbierająca informacje o wyniku """

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Ustawienia czcionki dla informacji o wyniku
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def prep_images(self):
        # Wstepna informacja o wyniku
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """ Zamien informacje w renderowany obraz """
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("Punkty " + score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Wyswietl wynik w prawym-gornym rogu
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Zamien high_score w obrazek """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("Najwiecej punktow " + high_score_str, True, self.text_color,
                                                 self.ai_settings.bg_color)

        # Wycentruj na środku gory ekranu
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Zamien level w obrazek """
        self.level_image = self.font.render("Level " + str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)

        # Ustaw pod wynikiem
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Pokaz ile zyc ci zostalo """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_start(self):
        """ Wyswietl informacje jak zaczac gre """
        self.start_image = self.font.render("Wcisnij 'p' aby rozpoczac", True, self.text_color,
                                            self.ai_settings.bg_color)
        # Ustaw na środku ekranu
        self.start_rect = self.start_image.get_rect()
        self.start_rect.centerx = self.screen_rect.centerx
        self.start_rect.centery = self.screen_rect.centery
        self.screen.blit(self.start_image, self.start_rect)

    def show_score(self):
        """ Wyswietl wynik na ekranie """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Narysuj statek
        self.ships.draw(self.screen)
