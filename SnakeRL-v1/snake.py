import pygame
import sys
import random
from pygame.math import Vector2


class Snake:
    '''displays a moving snake on the game screen'''

    def __init__(self, cell_size, cell_number, screen):
        '''initialises a snake at rest'''
        self.body = [Vector2(5, 9), Vector2(4, 9), Vector2(3, 9)]
        self.direction = Vector2(0, 0)  # initially at rest
        self.new_block = False
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.screen = screen
        self.load_images()

    def load_images(self):
        '''loads images corresponding to various configurations of the body of the snake'''
        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        # displays the snake
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x*self.cell_size),
                                     int(block.y*self.cell_size),
                                     self.cell_size, self.cell_size)
            if index == 0:
                self.screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                self.screen.blit(self.tail, block_rect)
            else:
                left = Vector2(-1, 0)
                right = Vector2(1, 0)
                up = Vector2(0, -1)
                down = Vector2(0, 1)
                # position of current block with respect to the previous block
                previous_block = block - self.body[index+1]
                # position of current block with respect to the next block
                next_block = block - self.body[index-1]
                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block == up and next_block == right or previous_block == right and next_block == up:
                        self.screen.blit(self.body_bl, block_rect)
                    elif previous_block == up and next_block == left or previous_block == left and next_block == up:
                        self.screen.blit(self.body_br, block_rect)
                    elif previous_block == down and next_block == right or previous_block == right and next_block == down:
                        self.screen.blit(self.body_tl, block_rect)
                    elif previous_block == down and next_block == left or previous_block == left and next_block == down:
                        self.screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
        # updates head graphics
        left = Vector2(-1, 0)
        right = Vector2(1, 0)
        up = Vector2(0, -1)
        down = Vector2(0, 1)
        if self.direction == left:
            self.head = self.head_left
        elif self.direction == right:
            self.head = self.head_right
        elif self.direction == up:
            self.head = self.head_up
        elif self.direction == down:
            self.head = self.head_down
        else:
            self.head = self.head_right

    def update_tail_graphics(self):
        # updates tail graphics
        left = Vector2(-1, 0)
        right = Vector2(1, 0)
        up = Vector2(0, -1)
        down = Vector2(0, 1)

        last = len(self.body)
        direction = self.body[last-1]-self.body[last-2]
        if direction == left:
            self.tail = self.tail_left
        elif direction == right:
            self.tail = self.tail_right
        elif direction == up:
            self.tail = self.tail_up
        elif direction == down:
            self.tail = self.tail_down
        else:
            self.tail = self.tail_left

    def move_snake(self):
        '''moves the snake body to its new position based on the direction of motion if the snake is moving'''
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        if self.direction != Vector2(0, 0):
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        '''increases snake length on each move while self.new_block is True'''
        self.new_block = True

    def reset(self):
        '''returns snake to the starting position with initial length
        the snake is at rest'''
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
