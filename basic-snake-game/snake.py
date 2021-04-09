import pygame
import sys
import random
from pygame.math import Vector2


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),
                                 int(self.pos.y*cell_size),
                                 cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)  # initially at rest
        self.new_block = False
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

        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
        self.game_over_sound = pygame.mixer.Sound('sound/end.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x*cell_size),
                                     int(block.y*cell_size),
                                     cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                left = Vector2(-1, 0)
                right = Vector2(1, 0)
                up = Vector2(0, -1)
                down = Vector2(0, 1)
                previous_block = block - self.body[index+1]
                next_block = block - self.body[index-1]
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block == up and next_block == right or previous_block == right and next_block == up:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block == up and next_block == left or previous_block == left and next_block == up:
                        screen.blit(self.body_br, block_rect)
                    elif previous_block == down and next_block == right or previous_block == right and next_block == down:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block == down and next_block == left or previous_block == left and next_block == down:
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
        if self.direction == Vector2(-1, 0):
            self.head = self.head_left
        elif self.direction == Vector2(1, 0):
            self.head = self.head_right
        elif self.direction == Vector2(0, -1):
            self.head = self.head_up
        elif self.direction == Vector2(0, 1):
            self.head = self.head_down
        else:
            self.head = self.head_right

    def update_tail_graphics(self):
        last = len(self.body)
        direction = self.body[last-1]-self.body[last-2]
        if direction == Vector2(-1, 0):
            self.tail = self.tail_left
        elif direction == Vector2(1, 0):
            self.tail = self.tail_right
        elif direction == Vector2(0, -1):
            self.tail = self.tail_up
        elif direction == Vector2(0, 1):
            self.tail = self.tail_down
        else:
            self.tail = self.tail_left

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        if self.direction != Vector2(0, 0):
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
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
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        # hits walls
        if not (0 <= head.x < cell_number) or not (0 <= head.y < cell_number):
            self.game_over()
        # hits self
        for block in self.snake.body[1:]:
            if head == block:
                self.game_over()

    def game_over(self):
        self.snake.play_game_over_sound()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (113, 227, 21)
        for col in range(cell_number):
            for row in range(cell_number):
                if (col+row) % 2 == 0:
                    grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
                else:
                    pass

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size*cell_number-60)
        score_y = int(cell_size*cell_number-40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width+score_rect.width+6, apple_rect.height)
        pygame.draw.rect(screen, (167, 220, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)  # rect frame with color = text color
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))  # width,height
clock = pygame.time.Clock()
apple = pygame.image.load('graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            og_x, og_y = main_game.snake.direction
            if event.key == pygame.K_UP and not og_y == 1:
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and not og_y == -1:
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and not og_x == 1 and not (og_x == 0 and og_y == 0):
                main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and not og_x == -1:
                main_game.snake.direction = Vector2(1, 0)

    screen.fill((146, 239, 83))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
