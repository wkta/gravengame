# app/interface.py

__version__ = 'V.0.0.1'
__name__ = 'Comet Game'
__author__ = 'Flavien HUGS'


import math, sys
import katagames_engine as kengi

from app.game import Game

pygame = kengi.pygame



def main():

    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1080, 700))
    pygame.display.set_caption("COMMET FALL GAME".upper())

    background = pygame.image.load("src/bg.jpg").convert()
    background_position = background.get_rect()
    background_position.x = 0
    background_position.y = -200

    banner = pygame.image.load("src/banner.png")
    banner = pygame.transform.scale(banner, (500, 500))
    banner_rect = banner.get_rect()
    banner_rect.x = math.ceil(screen.get_width() / 4)

    play_button = pygame.image.load("src/button.png")
    play_button = pygame.transform.scale(play_button, (400, 150))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = math.ceil(screen.get_width() / 3.33)
    play_button_rect.y = math.ceil(screen.get_height() / 2)

    game = Game()
    gameover = False

    while not gameover:
        # (1) gestion evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                gameover = True

            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_F2:
                    # Toggle mechanism (cest comme un interrupteur qui bascule)
                    if game.show_fps:
                        game.show_fps = False
                    else:
                        game.show_fps = True
                        game.reset_fps()

                if event.key == pygame.K_SPACE:
                    if game.is_playing:
                        game.player.launch_weapon()
                    else:
                        game.start()
                        game.sound_manager.play('click')
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game.start()
                    game.sound_manager.play('click')
        # (2) mise a jour logique
        if game.show_fps:
            game.update_fps()

        # (3) mise a jour graphique
        screen.blit(background, background_position)

        if game.is_playing:
            game.start_game(screen)
            if game.show_fps:
                # affiche fps
                game.paint_fps(screen)
        else:
            screen.blit(play_button, play_button_rect)
            screen.blit(banner, banner_rect)

        # flip OU display, utiliser les deux nest pas necessaire
        pygame.display.flip()

        # pygame.display.update()
        clock.tick(45)  # permet de placer une limite sur la vitesse de
        # rafraichissement du jeu -> max 45 passages dans la boucle de jeu
        # chaque seconde

    # en sortant de la boucle de jeu,
    # ne pas oublier de remettre a zero pygame
    pygame.quit()
