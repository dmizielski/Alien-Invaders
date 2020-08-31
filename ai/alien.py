import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Reprezentacja kosmity """

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Pokaz kosmite i ustaw atrybuty
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Spawnuj nowego kosmite w lewym gornym rogu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Dokladna pozycja kosmity w danym momencie
        self.x = float(self.rect.x)

    # def __getitem__(self, key):
    #     return self._alien[key]

    def check_edges(self):
        """ Zwroc True jest statek dotarl do krawedzi ekranu """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Kosmita przesuwa sie w prawo lub lewo """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """ Narysuj kosmite w obecnej pozycji """
        self.screen.blit(self.image, self.rect)
