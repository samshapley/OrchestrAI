import pygame
from pygame.locals import *
from car import Car
from race_track import RaceTrack
from scoreboard import Scoreboard
from sound_manager import SoundManager
from ui_manager import UIManager

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.ui_manager = UIManager(self.screen_width, self.screen_height)
        self.sound_manager = SoundManager()

    def start(self):
        self.running = True
        self.main_menu()

    def main_menu(self):
        while self.running:
            self.ui_manager.display_menu()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_1:
                        self.new_game()
                    elif event.key == K_2:
                        self.view_high_scores()
                    elif event.key == K_q:
                        self.quit_game()

    def new_game(self):
        # Initialize game objects
        car = Car()
        race_track = RaceTrack()
        scoreboard = Scoreboard()
        self.sound_manager.play_music()

        while self.running:
            self.play_game()
            if player_wins:
                scoreboard.update_scores(player_score)
                self.ui_manager.display_menu()
            else:
                self.game_over()

    def view_high_scores(self):
        scoreboard = Scoreboard()
        scoreboard.display_scores()
        self.ui_manager.display_menu()

    def play_game(self):
        while self.running:
            # Game logic and event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause_game()

            # Update game objects
            car.move()
            race_track.check_collision()
            race_track.update_checkpoint()
            race_track.update_power_up()

            # Render game objects
            race_track.display_track()
            car.display()
            self.ui_manager.display_timer()
            self.ui_manager.display_score()
            self.ui_manager.display_power_up()
            self.ui_manager.display_checkpoint()

            pygame.display.flip()
            self.clock.tick(60)

    def pause_game(self):
        self.ui_manager.display_menu()
        self.sound_manager.stop_music()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.ui_manager.display_menu()
                    elif event.key == K_r:
                        self.resume_game()
                    elif event.key == K_q:
                        self.quit_game()

    def resume_game(self):
        self.sound_manager.play_music()
        self.play_game()

    def game_over(self):
        self.ui_manager.display_menu()
        self.sound_manager.stop_music()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_1:
                        self.new_game()
                    elif event.key == K_2:
                        self.view_high_scores()
                    elif event.key == K_q:
                        self.quit_game()

    def quit_game(self):
        self.running = False
        pygame.quit()
