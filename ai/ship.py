import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """ Zainicjuj statek i ustaw pozycje startowa """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Zaladuj obraz statku i ustaw rect
        self.image = pygame.image.load('images/ship.bmp')
        # self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Kazdy nowy statek spawnuj na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

        # Przechowaj wartosc dla srodka statku
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Flaga poruszania sie
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """ Odswiez pozycje statku bazujac na wartosci srodka ekranu """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        # Aktualizuj rect z self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """ Narysuj statek na biezacej pozycji """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Wycentruj statek """
        self.center = self.screen_rect.centerx
