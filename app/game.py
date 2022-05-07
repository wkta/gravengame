# app/game.py

import katagames_engine as kengi

from app.player import Player
from app.sound import SoundManager
from app.monster import Mummy, Alien
from app.comet_event import CometFallEvent
import time

pygame = kengi.pygame

class Game:
    def __init__(self):

        self.show_fps = False
        self.is_playing = False

        self.players = pygame.sprite.Group()
        self.player = Player(self)
        self.players.add(self.player)

        self.sound_manager = SoundManager()

        self.comet_event = CometFallEvent(self)

        self.monsters = pygame.sprite.Group()
        self.score_font = self.fps_font = pygame.font.Font(
            "src/fonts/permanent_marker_regular.ttf", 30
        )
        self.help_text_font = pygame.font.Font(
            "src/fonts/permanent_marker_regular.ttf", 16
        )
        self.score = 0

        self.pressed = {}

        # pour affichage valeur FPS
        self.frame_count = None
        self.elapsed_time = None  # temps écoulé
        self.last_t = None  # date dernier rafraichissement/update
        self.mesure_fps = None  # nombre qui est la mesure des FPS
        self.reset_fps()

    def reset_fps(self):
        # remise a zero comptage FPS

        self.frame_count = 0
        self.elapsed_time = 0  # temps écoulé
        self.last_t = time.time()  # date dernier rafraichissement/update
        self.mesure_fps = None  # nombre qui est la mesure des FPS

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, points=10):
        self.score += points

    def game_over(self):
        self.monsters = pygame.sprite.Group()
        self.comet_event.comets = pygame.sprite.Group()
        self.player.player_health = self.player.player_max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')

    def update_fps(self):
        self.frame_count += 1
        t_now = time.time()
        self.elapsed_time += t_now - self.last_t
        self.last_t = t_now

        # mise a jour compteur FPS toutes les 2 sec
        if self.elapsed_time > 2:
            self.mesure_fps = round(self.frame_count / self.elapsed_time, 2)
            self.frame_count = 0
            self.elapsed_time = 0

    def paint_fps(self, screen):
        # uniquement:
        # le dessin de la mesure des FPS,
        # a condition qu'une mesure soit disponible!
        if self.mesure_fps is None:
            texte = f"FPS : ?"
        else:
            fps = self.mesure_fps
            texte = f"FPS : {fps}"

        fps_image = self.fps_font.render(texte, 1, (225, 225, 225))
        screen.blit(fps_image, (50, 50))

    def start_game(self, screen):
        text_color = (225, 225, 225)
        score_text = self.score_font.render(f"Score : {self.score}", 1, text_color)
        screen.blit(score_text, (20, 20))

        help_text_exit = self.help_text_font.render("'esc', pour sortir".upper(), 1, text_color)
        screen.blit(help_text_exit, (800, 40))

        help_text_fps = self.help_text_font.render("'F2', cacher/afficher FPS".upper(), 1, text_color)
        screen.blit(help_text_fps, (800, 80))

        screen.blit(self.player.image, self.player.rect)
        self.player.update_player_health_bar(screen)
        self.player.animate_player()

        self.comet_event.update_bar(screen)

        for weapon in self.player.weapon:
            weapon.move()
        self.player.weapon.draw(screen)

        for monster in self.monsters:
            monster.forward()
            monster.monster_update_health_bar(screen)
            monster.animate_monster()
        self.monsters.draw(screen)

        for comet in self.comet_event.comets:
            comet.fall()
        self.comet_event.comets.draw(screen)

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 910:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -35:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.monsters.add(monster_class_name.__call__(self))
