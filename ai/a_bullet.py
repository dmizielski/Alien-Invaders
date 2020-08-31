import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    def __init__(self, ai_settings, screen, alien):
        """ Stworz obiekt kula na aktualnej pozycji statku """
        super().__init__()
        self.screen = screen

        # Stworz kule w punkcie (0, 0) i ustaw na odpowiednia pozycje
        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width,
                                ai_settings.alien_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom

        # Zapisz pozycje kuli
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Przesun kule na gore ekranu """
        # Zaktualizuj pozycje kuli
        self.y += self.speed_factor
        # Zaktualizuj pozycje
        self.rect.y = self.y

    def draw_bullet(self):
        """ Narysuj kule na ekranie """
        pygame.draw.rect(self.screen, self.color, self.rect)