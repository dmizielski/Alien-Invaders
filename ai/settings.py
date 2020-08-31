class Settings:
    """ Klasa do przechowywania ustawien dla Alien Invasion """

    def __init__(self):
        """ Inicjalizacja ustawien dla gry """

        # Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienia kul
        self.bullet_speed_factor = 1
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Ustawienia kul kosmitow
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15

        self.fleet_drop_speed = 3

        # Jak szybko wzrastaja punkty za zbite statki
        self.score_scale = 1.5

        # Zwieksz poziom trudnosci
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Ustawienia zmieniajce sie w trakcie gry
        self.ship_health = 100
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        self.alien_speed_factor = 1
        # fleet_dierction = 1 reprezentuje prawo -1 lewo
        self.fleet_direction = 1

        # Uderzenie
        self.alien_points = 50

    def increase_speed(self):
        """ Zwieksz predkosc gry i punkty za zbite statki """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
