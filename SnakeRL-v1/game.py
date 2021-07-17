import pygame
import sys
import random
from pygame.math import Vector2
from fruit import *
from snake import *


class Game:
    '''The main functions for the snake game'''

    def __init__(self, update_time=150):
        '''initialises the game display, clock and snake and fruit objects'''
        # dimensions of game board
        self.cell_size = 40
        self.cell_number = 20
        self.game_config(update_time)
        self.snake = Snake(self.cell_size, self.cell_number, self.screen)
        self.fruit = Fruit(self.cell_size, self.cell_number, self.screen)
        self.load_sounds()
        self.game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)
        self.start_display()

    def start_display(self):
        self.screen.fill((146, 239, 83))
        self.draw_elements()
        pygame.display.update()

    def play_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.SCREEN_UPDATE:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    left = Vector2(-1, 0)
                    right = Vector2(1, 0)
                    up = Vector2(0, -1)
                    down = Vector2(0, 1)

                    og_x, og_y = self.snake.direction
                    if event.key == pygame.K_UP and not og_y == 1:
                        self.snake.direction = up
                    elif event.key == pygame.K_DOWN and not og_y == -1:
                        self.snake.direction = down
                    elif event.key == pygame.K_LEFT and not og_x == 1 and not (og_x == 0 and og_y == 0):
                        self.snake.direction = left
                    elif event.key == pygame.K_RIGHT and not og_x == -1:
                        self.snake.direction = right

            self.screen.fill((146, 239, 83))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(60)

    def game_config(self, update_time):
        pygame.mixer.pre_init(44100, -16, 2, 512)  # sound configuration
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.cell_size*self.cell_number,
                                               self.cell_size*self.cell_number))  # width,height
        self.clock = pygame.time.Clock()
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, update_time)

    def load_sounds(self):
        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
        # self.crunch_sound.set_volume(0.2)
        self.crunch_sound.set_volume(0)
        self.game_over_sound = pygame.mixer.Sound('sound/end.wav')
        # self.game_over_sound.set_volume(0.1)
        self.game_over_sound.set_volume(0)

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()

    def update(self):
        self.snake.move_snake()
        self.collided = False
        self.failed = False
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.play_crunch_sound()
            self.collided = True
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        # hits walls
        if not (0 <= head.x < self.cell_number) or not (0 <= head.y < self.cell_number):
            self.game_over()
        # hits self
        for block in self.snake.body[1:]:
            if head == block:
                self.game_over()

    def game_over(self):
        self.play_game_over_sound()
        self.failed = True
        self.snake.reset()

    def draw_grass(self):
        grass_color = (113, 227, 21)
        for col in range(self.cell_number):
            for row in range(self.cell_number):
                if (col+row) % 2 == 0:
                    grass_rect = pygame.Rect(col*self.cell_size, row *
                                             self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, grass_color, grass_rect)
                else:
                    pass

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(self.cell_size*self.cell_number-60)
        score_y = int(self.cell_size*self.cell_number-40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width+score_rect.width+6, apple_rect.height)
        pygame.draw.rect(self.screen, (167, 220, 61), bg_rect)
        # rect frame with color = text color
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.fruit.apple, apple_rect)


if __name__ == '__main__':
    game = Game()
    game.play_game()
