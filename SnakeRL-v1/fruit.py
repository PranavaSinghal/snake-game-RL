import pygame
import sys
import random
from pygame.math import Vector2


class Fruit:
    '''displays a fruit on the game screen
       appears at a new random position every time it is eaten by the snake'''

    def __init__(self, cell_size, cell_number, screen):
        # initialises the fruit with a random position, loads the source image
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.screen = screen
        self.apple = pygame.image.load('graphics/apple.png').convert_alpha()
        self.randomize()

    def draw_fruit(self):
        # displays the fruit
        fruit_rect = pygame.Rect(int(self.pos.x*self.cell_size),
                                 int(self.pos.y*self.cell_size),
                                 self.cell_size, self.cell_size)
        self.screen.blit(self.apple, fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        # randomizes the fruit position
        self.x = random.randint(0, self.cell_number-1)
        self.y = random.randint(0, self.cell_number-1)
        self.pos = Vector2(self.x, self.y)
