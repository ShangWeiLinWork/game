# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 22:09:49 2022

@author: saral
"""

import xlwings as xw
from string import ascii_uppercase
from random import randint
from time import sleep
from sys import exit

'''
conventions: 
index cell: pos for python index e.g. (0, 0); ad/address for excel index e.g. $A$1
'''

class Snake:
    def __init__(self, speed, width, height):
        
        # book setup
        self.book = xw.Book()
        self.sheet = self.book.sheets[0]
        self.sheet.name = 'snake'
        
        # board setup
        self.speed = 1 / speed
        self.width = width
        self.height = height
        self.board_setup()

        # snake setup
        self.body = [(int(height / 2), 5), (int(height / 2), 4), (int(height / 2), 3)]# first element is head
        self.direction = (0, 1)
        self.eaten = False
        self.create_apple()
        
    def board_setup(self):
        
        # background colors
        ## code form tutorial
        ## game_cells = f'B2:{ascii_uppercase[self.width]}{self.height + 1}'
        ## self.sheet[game_cells].color = board_color
        game_cells = self.sheet[1: self.height + 1, 1 : self.width + 1]
        game_cells.color = board_color
        
        control_cells = self.sheet[self.height + 1: self.height + 6, 1 : self.width + 1]
        control_cells.color = control_color
        
        # buttons
        self.exit_cell = control_cells[-1, -1]
        self.left_cell = control_cells[2, 1]
        self.up_cell = control_cells[1, 2]
        self.right_cell = control_cells[2, 3]
        self.down_cell = control_cells[3, 2]
        
        self.exit_cell.value = 'quit'
        self.left_cell.value = 'left'
        self.up_cell.value = 'up'
        self.right_cell.value = 'right'
        self.down_cell.value = 'down'
        
        # button styling
        for button in [self.exit_cell, self.left_cell, self.up_cell, self.right_cell, self.down_cell]:
            button.color = button_color
            button.font.color = text_color
            
        # cell dimensions
        self.sheet[1: self.height + 6, 1].row_height = 40
        
    def create_apple(self):
        overlap = True
        while overlap:
            # get a random cell
            row = randint(1, self.height) # note randint include left and right bounds, so don't need +1
            col = randint(1, self.width)
        
            # check if apple is below snake
            overlap = (row, col) in self.body
        
        self.apple_pos = (row, col)
        
    def display_game_elements(self):
        
        '''
        draw snake after apple so snake will be on top of apple
        '''
        # apple display
        self.sheet[self.apple_pos].color = apple_color
        
        # snake display
        for index, pos in enumerate(self.body):
            if index == 0:
                self.sheet[pos].color = head_color
            else:
                self.sheet[pos].color = body_color
   
    def input(self):
        selected_cell_ad = self.book.selection.address
        if selected_cell_ad == self.left_cell.address:
            self.direction = (0, -1)
        elif selected_cell_ad == self.up_cell.address:
            self.direction = (-1, 0)
        elif selected_cell_ad == self.right_cell.address:
            self.direction = (0, 1)
        elif selected_cell_ad ==self.down_cell.address:
            self.direction = (1, 0)
            
    def exit_game(self):
        selected_cell_ad = self.book.selection.address
        if selected_cell_ad == self.exit_cell.address:
            self.book.close()
            exit()
    
    def move_snake(self):
        if self.eaten:
            new_body = self.body
            self.eaten = False
        else:
            lost_cell = self.body[-1]
            new_body = self.body[:-1]
            self.sheet[lost_cell].color = board_color
        new_head = self.add_direction(new_body[0], self.direction)
        new_body.insert(0, new_head)
        
        self.body = new_body
    
    def add_direction(self, cell, direction):
        row = cell[0] + direction[0]
        col = cell[1] + direction[1]
        return (row, col)
    
    def check_apple_collision(self):
        if self.body[0] == self.apple_pos:
            self.eaten = True
            self.create_apple()
            
    def check_fail(self):
        head = self.body[0] 
        body = self.body[1:]
        
        if head in body\
            or head[1] <= 0 or head[1] >= self.width + 1\
            or head[0] <= 0 or head[0] >= self.height + 1:
            self.book.close()
            exit()
        
    def run(self):
        while True:
            # eixt_game -> sleep -> input
            self.exit_game()
            sleep(self.speed)# pause code for a certain amount of time
            self.input()
            self.move_snake()
            self.check_apple_collision()
            self.check_fail()
            self.display_game_elements()

# colors
board_color = (226, 227, 223)
control_color = (46, 50, 51)
button_color = (81, 91, 94)
text_color = (255, 255, 255)
apple_color = (0, 255, 100)
head_color = (255, 0, 0)
body_color = (200, 0, 0)

snake = Snake(2, 12, 8)
snake.run()