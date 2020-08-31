import json
import sys
import pygame
import random
from time import sleep
from ai.bullet import Bullet
from ai.a_bullet import AlienBullet
from ai.settings import Settings
from ai.alien import Alien
from ai.boss import Boss

filename = 'score.json'


def check_keydown_events(event, ai_settings, stats, screen, ship, sb, aliens, bullets):
    """ Reaguj na wcisniecie klawisza """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        if stats.high_score == 0:
            with open(filename, 'w') as f_obj:
                json.dump(stats.score, f_obj)
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, sb, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Stworz nowa kule i dodaj ja do grupy
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# def alien_fire_bullet(aliens, alien_bullet):
#     x = random.choice(aliens)
#     alien_bullet.draw(x)
#     sleep(0.5)


def check_keyup_events(event, ship):
    """ Reaguj na zwolnienie klawisza """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, alien_bullet):
    """ Odswiezaj gre """
    # Odswiezaj ekran przy koncu kazdej petli
    screen.fill(ai_settings.bg_color)
    # Narysuj wszystkie kule za statkiem i kosmitami
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # alien_fire_bullet(aliens, alien_bullet)

    # Wyswietl informacje o wyniku
    sb.show_score()

    # Wyswietl przycisk Play jesli gra jest nieaktywna
    if not stats.game_active:
        sb.prep_start()

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    # Usun niewidoczne kule
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    check_bullet_ship_collision(ai_settings, screen, stats, sb, ship, aliens,
                                alien_bullets, bullets)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, boss)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets, boss):
    # Zniszcz amunicje, stworz nowa flote i utrudnij gre oraz zacznij nowy level
    bullets.empty()
    ai_settings.increase_speed()

    # Zwieksz level
    stats.level += 1
    sb.prep_level()

    if stats.level % 5 != 0:
        create_fleet(ai_settings, screen, ship, aliens)
    else:
        spawn_boss(ai_settings, screen, boss)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, boss):
    # Sprawdz czy kula trafila w kosmite
    # Jesli tak to pozbadz sie kuli i kosmity
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets, boss)


def check_bullet_ship_collision(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets):
    # Sprawdz czy kula trafila w statek
    # Jesli tak to odejmij 50 hp
    collisions = pygame.sprite.groupcollide(alien_bullets, ship, True, True)
    if collisions and ai_settings.ship_health <= 0:
        start_game(ai_settings, screen, stats, ship, sb, aliens, bullets)
        sleep(0.5)
    elif collisions:
        ai_settings.ship_health -= 50


def start_game(ai_settings, screen, stats, ship, sb, aliens, bullets):
    # Ukryj kursor myszy
    pygame.mouse.set_visible(False)
    # Zresetuj statystyki
    stats.reset_stats()
    stats.game_active = True

    # Zresetuj tabele wynikow
    sb.prep_images()
    sb.prep_ships()

    # Oczysc liste kosmitow i kul
    aliens.empty()
    bullets.empty()

    # Stworz nowa flote i wycentruj statek
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Reaguj na klawiature i myszke """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, ship, sb, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, ship, sb, play_button, aliens, bullets, mouse_x, mouse_y):
    """ Zacznij nowa gre gdy gracz nacisnie Play """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, stats, ship, sb, aliens, bullets)


def spawn_boss(ai_settings, screen, boss):
    boss = Boss(ai_settings, screen)
    boss_width = boss.rect.width
    boss.rect.x = boss.x
    boss.rect.y = boss.rect.height
    boss.add(boss)


def get_number_aliens_x(ai_settings, alien_width):
    """ znajdz liczbe kosmitow ktore wpasuja sie w rzedzie """
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """ Wyznacz ilosc rzedow kosmitow ktora dopasuje sie do rozmiaru ekranu """
    avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Stworz flote kosmitow """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # Stworz pierwszy rzad kosmitow
    # Stworz kosmite i umiesc go w rzedzie
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Stworz rzad kosmitow
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ Odpowiedz jesli kosmita dotarl do krawedzi ekranu """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Przesun flote w dol i zmien ich kierunek """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Odpowiedz statku na uderzenie przez kosmite """
    if stats.ships_left > 0:
        # Usun 1 statek
        stats.ships_left -= 1

        # Zaktualizuj tabele wynikow
        sb.prep_ships()

        # Oproznij liste kosmitow i kul
        aliens.empty()
        bullets.empty()

        # Stworz nowa flote i statek na srodku ekranu
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pauza
        sleep(0.5)

    elif ai_settings.ship_health <= 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Sprawdz czy jakikolwiek kosmita dotarl do dolu ekranu """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Traktuj to tak jakby uderzyl w statek
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullet):
    """ Zaktualizuj pozycje kosmitow we flocie """
    # alien_fire_bullet(aliens, alien_bullet)
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detekcja statku i kosmity
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Sprawdz czy kosmici dotarli do dolu ekranu
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """ Sprawdz czy jest ktos ustanowil nowy najwyzszy wynik """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open(filename, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)
        sb.prep_high_score()
