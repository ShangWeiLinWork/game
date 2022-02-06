# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 11:36:25 2022

@author: saral
"""
'''
display surface (main screen), can draw directly on it with `pygame.draw`
Surface, can draw on it as well
Rect, can draw around surface to manipulate

- pygame.Rect(x, y, height, width)
- pygame.draw.<shape>(surface, color, rect)
    <shape>: e.g. ellipse, rect
- pygame.color(color_string)
- pygame.draw.aaline(surface, color, start_pos, end_pos)
- surface.fill(color)
- rect.colliderect(rect)
- pygame.font.Font(<file_path>, size)
- Font.render('', antialias, color)
- pygame.blit(surface, pos)
'''


import pygame
from sys import exit
from random import choice

class BALL:
    def __init__(self):
        self.rect = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
        self.speed_x = 0
        self.speed_y = 0
        
    def draw(self):
        pygame.draw.ellipse(screen, ball_color, self.rect)
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def restart(self):
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.speed_x = 0
        self.speed_y = 0
    
    def start_ball(self):
        self.speed_x = choice((1, -1)) * ball_speed
        self.speed_y = choice((1, -1)) * ball_speed
    
class PLAYER:
    def __init__(self):
        self.rect = pygame.Rect(screen_width - 20, screen_height / 2 - 30, 10, 60)
        self.speed = 0
        
    def draw(self):
        pygame.draw.rect(screen, racket_color, self.rect)
        
    def move(self):
        self.rect.y += self.speed
        
        if self.rect.top <= 0: self.rect.top =0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height
    
    def restart(self):
        self.rect.centery = screen_height / 2
        self.speed = 0
        
class OPP:
    def __init__(self):
        self.rect = pygame.Rect(10, screen_height / 2 - 30, 10, 60)
        
    def draw(self):
        pygame.draw.rect(screen, racket_color, self.rect)

    def restart(self):
        self.rect.centery = screen_height / 2
        
class MAIN:
    def __init__(self):
        self.ball = BALL()
        self.player = PLAYER()
        self.opp = OPP()
        
        # score
        self.player_score = 0
        self.opp_score = 0
        
        # timer
        self.score_time = pygame.time.get_ticks()
        self.countdown = 3
        
        self.font = pygame.font.Font('font/Little Comet Demo Version.otf', 30)
        self.font2 = pygame.font.Font('font/Little Comet Demo Version.otf', 100)
        
    def draw(self):
        # ball, player, opponent
        self.ball.draw()
        self.player.draw()
        self.opp.draw()
        
        # middle line
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
        
        # scroes
        player_text = self.font.render(f'{self.player_score}', True, light_grey)
        opp_text = self.font.render(f'{self.opp_score}', True, light_grey)
        screen.blit(player_text, (screen_width / 2 + 10, screen_height / 2))
        screen.blit(opp_text, (screen_width / 2 - 30, screen_height / 2))
        
        # timer
        if self.countdown:
            timer_text = self.font2.render(f'{self.countdown}', True, countdown_color)
            screen.blit(timer_text, (screen_width / 2 - 30 , screen_height / 2 - 30))
        
    def check_collide(self):
        
        if self.ball.rect.colliderect(self.player.rect) or self.ball.rect.colliderect(self.opp.rect):
            self.ball.speed_x *= -1
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= screen_height:
            self.ball.speed_y *= -1
            
        if self.ball.rect.left <= 0:
            self.score_time = pygame.time.get_ticks()
            self.restart()
            self.player_score += 1 
        if self.ball.rect.right >= screen_width:
            self.score_time = pygame.time.get_ticks()
            self.restart()
            self.opp_score += 1

    def update(self):
        if self.countdown:
            self.get_countdown()
        
        if not self.countdown:
            self.ball.move()
            self.player.move()
            self.move_opp()
            self.check_collide()
            
    def get_countdown(self):
        countdown = 3 - (pygame.time.get_ticks() - self.score_time) // 1000
        if countdown > 0:
            self.countdown = countdown
            self.player.speed = 0
        else:
            self.countdown = None
            self.ball.start_ball()
        
    def restart(self):
        self.ball.restart()
        self.player.restart()
        self.opp.restart()
        self.countdown = 3
            
    def input_response(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP\
            or event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.player.speed -= player_speed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN\
            or event.type == pygame.KEYUP and event.key == pygame.K_UP:
            self.player.speed += player_speed
    
    def move_opp(self):
        if self.opp.rect.y < self.ball.rect.y: 
            self.opp.rect.y += opp_speed
        if self.opp.rect.y > self.ball.rect.y:
            self.opp.rect.y -= opp_speed
        
        if self.opp.rect.bottom >= screen_height: self.opp.rect.bottom = screen_height
        if self.opp.rect.top <= 0: self.opp.rect.top = 0
    def update_score(self):
        self.score_player        

# game params
ball_speed = 7
player_speed = 6
opp_speed = 6

bg_color = (3, 36, 252)
light_grey = (200, 200, 200)
racket_color = (156, 31 , 20)
ball_color = (252, 165, 3)
countdown_color = (20, 156, 115)

# general setup
pygame.init() 
clock = pygame.time.Clock()

# set up main window
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

main = MAIN()

# LOOP: draw, update
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        main.input_response(event)
                
    
    screen.fill(bg_color)
    main.draw()
    main.update()

    # update window
    pygame.display.flip()# take everything before the loop and draw a picture
    clock.tick(60)# control speed of loop
    