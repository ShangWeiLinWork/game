# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 17:13:08 2022

@author: saral
"""

'''
rect can check for collision and have more control; surface can't
- rectangles
pygame.Rect(w, h, x, y)
surface.get_rect(<rect_position>)
'''

import pygame, sys, random

class FLOOR:
    def __init__(self):
        self.surface1 = pygame.image.load('graphics/base.png').convert_alpha()
        self.surface2 = pygame.image.load('graphics/base.png').convert_alpha()
        self.x = 0
        
    def move(self):
        if self.x < -screen_width:
            self.x = 0
        else:
            self.x -= move_speed
        
    def draw(self):
        screen.blit(self.surface1, (self.x, screen_height - 100))
        screen.blit(self.surface2, (self.x + screen_width, screen_height - 100))
    
class BIRD:
    def __init__(self):
        flap_up_surface = pygame.image.load('graphics/bluebird-upflap.png').convert_alpha()
        flap_mid_surface = pygame.image.load('graphics/bluebird-midflap.png').convert_alpha()
        flap_down_surface = pygame.image.load('graphics/bluebird-downflap.png').convert_alpha()
        self.surface_list = [flap_up_surface, flap_mid_surface, flap_down_surface]
        self.surface = flap_up_surface 
        self.surface_index = 0
        self.rect = flap_up_surface.get_rect(center=(screen_width / 8, screen_height / 2))
        
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)
        
        self.speed = 0
        
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

    def move(self):
        self.rect.y += self.speed
        self.speed += gravity
        
    def draw(self):
        surface = pygame.transform.rotozoom(self.surface, -self.speed * 4, 1)
        screen.blit(surface, self.rect)
        
    def event_response(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.speed = - jump
                self.flap_sound.play()
        if event.type == self.BIRDFLAP:
            self.surface_index += 1
            self.surface = self.surface_list[self.surface_index % 3]
            self.rect = self.surface.get_rect(center=(screen_width / 8, self.rect.centery))
                
    def reset(self):
        self.rect.y = screen_height / 2
        self.speed = 0
                
class PIPES:
    def __init__(self):
        self.surface_down = pygame.image.load('graphics/pipe-green.png').convert_alpha()
        self.surface_up = pygame.transform.flip(self.surface_down, False, True)
        
        self.rect_up_list = []
        self.rect_down_list = []
        
        self.pipe_pos = (80, 200, 250)
        
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 2000)
        
    def move(self):
        for rect in self.rect_up_list + self.rect_down_list:
            rect.x -= move_speed
    
    def draw(self):
        for rect in self.rect_up_list:
            screen.blit(self.surface_up, rect)
        for rect in self.rect_down_list:
            screen.blit(self.surface_down, rect)
    
    def create_pipes(self):
        random_pipe_pos = random.choice(self.pipe_pos)
        rect_up = self.surface_up.get_rect(midbottom=(screen_width + 10, random_pipe_pos))
        rect_down = self.surface_down.get_rect(midtop=(screen_width + 10, random_pipe_pos + 150))
        self.rect_up_list.append(rect_up)
        self.rect_down_list.append(rect_down)
    
    def event_response(self, event):
        if event.type == self.SPAWNPIPE:
            self.create_pipes()
            if len(self.rect_up_list) > 3: 
                self.rect_up_list = self.rect_up_list[1:]
                self.rect_down_list = self.rect_down_list[1:]
    
    def reset(self):
        self.rect_up_list = []
        self.rect_down_list = []
    
class MAIN:
    def __init__(self):
        self.floor = FLOOR()
        self.bird = BIRD()
        self.pipes = PIPES()
        self.game_active = False
        
        self.game_font = pygame.font.Font('font/04B_19.ttf', 30)
        self.score = 0
        self.high_score = 0
        self.score_countdown = 100
        
        self.gameover_surface = pygame.image.load('graphics/message.png').convert_alpha()
        
        self.death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        
    def move(self):
        self.floor.move()
        self.bird.move()
        self.pipes.move()
        
    def draw(self):        
        if self.game_active:
            self.floor.draw() 
            self.bird.draw()
            self.pipes.draw()
        
            # score
            score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))# text, antialias, color, 
            score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
            screen.blit(score_surface, score_rect)
        
        else:
            self.floor.draw()
            
            # score
            score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))# text, antialias, color, 
            score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
            screen.blit(score_surface, score_rect)
            
            # high score
            high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255)) 
            high_score_rect = high_score_surface.get_rect(center=(screen_width / 2, screen_height - 50))
            screen.blit(high_score_surface, high_score_rect)
            
            # game over screen
            gameover_rect = self.gameover_surface.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(self.gameover_surface, gameover_rect)
            
        
    def check_collision(self):
        if self.bird.rect.top <= -30 or self.bird.rect.bottom >= 412:# above screen too much or hit floor
            self.death_sound.play()
            self.reset()
            return
            
        for rect in self.pipes.rect_up_list + self.pipes.rect_down_list:
            if self.bird.rect.colliderect(rect):
                self.death_sound.play()
                self.reset()
            
    def event_response(self, event):
        if self.game_active:
            self.bird.event_response(event)
            self.pipes.event_response(event)
        if not self.game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_active = True
            self.score = 0
            
    
    def reset(self):
        self.game_active = False
        if self.score > self.high_score: self.high_score = self.score
        
        self.bird.reset()
        self.pipes.reset()
    
    def update(self):
        self.check_collision()
        if self.game_active:
            self.move()
            self.score += 0.01
            self.score_countdown -= 1
            if self.score_countdown == 0:
                self.score_sound.play()
                self.score_countdown = 100
        else:
            self.floor.move()

pygame.init()
clock = pygame.time.Clock()

screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
move_speed = 1
gravity = 0.125
jump = 3

bg_surface = pygame.image.load('graphics/background-day.png').convert_alpha()


main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        main.event_response(event)
            
    screen.blit(bg_surface, (0, 0))
    main.update()
    main.draw()
            
    pygame.display.update()
    clock.tick(120)