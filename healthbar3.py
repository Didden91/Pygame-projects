# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:59:17 2021

@author: Ivo
"""

import pygame, sys

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
        
        self.current_health = 200
        
        self.maximum_health = 1000
       
        self.health_bar_length = 400
     
        self.health_ratio = self.maximum_health / self.health_bar_length
            
    
    def update(self):
        self.basic_health()
        
  
    
    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    
    
    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health   
    
    #Now to create our actual healthbar! and to place this healthabr in the update method!
    def basic_health(self):
        #first create a rect. Which needs a couple of attributes (4 in this case): 
        # 1: what surface, 2: what color(or color code), 
        # 3: a rect object, which is defined by (X coordinate, Y coordinate, Width, Height)
        pygame.draw.rect(screen, (255,0,0), (10, 10,self.current_health/self.health_ratio,25))
        
        #and now for a nice white outline around the bar. Make a same rectangle, however:
        #difference 1 is make it the length of health_bar_length
        #difference 2 is add another attribbute, the stroke width, which we can set to 4 pixels,
        # to make a nice thin line
        pygame.draw.rect(screen, (255,255,255), (10, 10, self.health_bar_length, 25), 4)
       
    
    
    

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.sprite.get_health(200)
           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.sprite.get_damage(200)
                
            
            
    screen.fill((30,30,30))
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)