# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:38:39 2022

@author: saral
"""

import pygame, sys, random
from pygame.math import Vector2

'''
convention
:pos: grid index. coord: pixel index 
'''

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(# (x, y, w, h)
            int(self.pos.x) * cell_size, int(self.pos.y) * cell_size, cell_size, cell_size
        )# Rect takes integers, while Vector2 stores float, so convert explicitly
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)# (surface, color, rect)
    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)# randint includes both bounds, but pos is at upper left, so may be outside
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]# first element is head
        self.direction = Vector2(0, 0)
        self.eaten = False
        
        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()
        
        self.turn_up_right = pygame.image.load('graphics/turn_up_right.png').convert_alpha()
        self.turn_right_down = pygame.image.load('graphics/turn_right_down.png').convert_alpha()
        self.turn_down_left = pygame.image.load('graphics/turn_down_left.png').convert_alpha()
        self.turn_left_up = pygame.image.load('graphics/turn_left_up.png').convert_alpha()
    
        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()
        
        self.eat_sound = pygame.mixer.Sound('sound/eat.wav')
        
    def draw_snake(self):
        # for each block in body, create rectangle and draw it
        for index, block in enumerate(self.body):
            x_coord = int(block.x) * cell_size
            y_coord = int(block.y) * cell_size
            block_rect = pygame.Rect(x_coord, y_coord, cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.get_head_graphics(), block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.get_tail_graphics(), block_rect)
            else:
                pre_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                screen.blit(self.get_body_graphics(next_block, pre_block), block_rect)
                
    def get_head_graphics(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(0, -1): return self.head_up
        elif head_relation == Vector2(1, 0): return self.head_right
        elif head_relation == Vector2(0, 1): return self.head_down
        elif head_relation == Vector2(-1, 0): return self.head_left
        
    def get_tail_graphics(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == Vector2(0, -1): return self.tail_up
        elif tail_relation == Vector2(1, 0): return self.tail_right
        elif tail_relation == Vector2(0, 1): return self.tail_down
        elif tail_relation == Vector2(-1, 0): return self.tail_left
    
    def get_body_graphics(self, next_block, pre_block):
        if next_block.y == pre_block.y: 
            return self.body_horizontal
        elif next_block.x == pre_block.x: 
            return self.body_vertical
        elif next_block.y == -1 and pre_block.x == 1 or next_block.x == 1 and pre_block.y == -1:
            return self.turn_up_right
        elif next_block.x == 1 and pre_block.y == 1 or next_block.y == 1 and pre_block.x == 1:
            return self.turn_right_down
        elif next_block.x == -1 and pre_block.y == 1 or next_block.y == 1 and pre_block.x == -1: 
            return self.turn_down_left
        elif next_block.y == -1 and pre_block.x == -1 or next_block.x == -1 and pre_block.y == -1:
            return self.turn_left_up 
        # is like this, but cannot use set
        # relation_set = set([next_block, pre_block])
        # if relation_set == {Vector2(1, 0), Vector2(-1, 0)}:return self.body_horizontal
        # elif relation_set == {Vector2(0, -1), Vector2(0, 1)}: return self.body_vertical   
        # elif relation_set == {Vector2(0, -1), Vector2(1, 0)}: return self.turn_up_right
        # elif relation_set == {Vector2(1, 0), Vector2(0, 1)}: return self.turn_right_down
        # elif relation_set == {Vector2(-1, 0), Vector2(0, 1)}: return self.turn_down_left
        # elif relation_set == {Vector2(0, -1), Vector2(-1, 0)}: return self.turn_left_up

    def move_snake(self):
    
        if self.eaten == True:
            body_copy = self.body
        elif self.eaten == False:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy
        self.eaten = False
        
    def reset(self):
        self.body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]
        self.direction = Vector2(0, 0)
        
class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()

    def update(self):
        self.snake.move_snake()
        self.check_eat_apple()
        self.check_apple_body_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_eat_apple(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.eaten = True
            self.snake.eat_sound.play()
            
    def check_apple_body_collision(self):
        if self.fruit.pos in self.snake.body[1:]: 
            self.fruit.randomize()
        
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number\
            or not 0 <= self.snake.body[0].y < cell_number\
            or self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
            
    def game_over(self):
        self.snake.reset()
    
    def draw_grass(self):
        grass_color = (167, 209, 61)
        
        for col in range(cell_number):
            for row in range(cell_number):                
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12)) # (text, aa, color)
        
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        background_rect = pygame.Rect(apple_rect.left, apple_rect.top - 3, 
                                      apple_rect.width + score_rect.width + 6, 
                                      apple_rect.height + 6)# (x, y, w, h)
        
        pygame.draw.rect(screen, (167, 209, 61), background_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), background_rect, 2)# the last number is the line width
        
pygame.init()
cell_size = 40
cell_number = 10
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))# (width, height) in pixels
clock = pygame.time.Clock()
apple = pygame.image.load('graphics/apple.png').convert_alpha()# convert to pygame format
game_font = pygame.font.Font('Font/Little Comet Demo Version.otf', 30)# (font, font_size)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 500) # in milli-sceonds

main_game = MAIN()


while True: # close loop inside
    for event in pygame.event.get():# check for every possible event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()# ends any code
            
        if event.type == SCREEN_UPDATE:
            main_game.update()
            
        if event.type == pygame.KEYDOWN:# triggered when we press any key
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                
    
    screen.fill((175, 215, 70))# (r, g, b), 0~255
    main_game.draw_elements()
    
    pygame.display.update()
    clock.tick(60)# framerate, how many times the while loop can run per second