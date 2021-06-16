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
        #Now to add some NEW attributes for the animated health bar:
        self.target_health = 500
        self.health_change_speed = 5
            
    
    def update(self):
        self.basic_health()
        self.advanced_health()
  # now to change ALL these current_health to target_health
  # so that when our player is HIT, we change the target_health and our current_health 
  # is CATCHING UP to the target health
  #so we never actively change our current_health, we only change the target_health
    
    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0
    
    
    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health   
    
    #Here we also change the current_health to target_health
    def basic_health(self):
        pygame.draw.rect(screen, (255,0,0), (10, 10,self.target_health/self.health_ratio,25))
        pygame.draw.rect(screen, (255,255,255), (10, 10, self.health_bar_length, 25), 4)
   
    # now to create the advanced healthbar
    def advanced_health(self):
        #The width and the color of the second health bar, the animated one, the transition bar,
        #which will be placed on top of the first one
        #by default the transition bar should be invisible, so width = 0 and the same color as our healthbar
        transition_width = 0
        transition_color = (255,0,0)
        #now to calculate the difference between current and target health
        # and to change current health towards the target health at the speed we defined
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            #now we need to change the transition bar width, so it becomes visible.
            #the number we need is target_health minus current_health 
            # and then divide that by our RATIO, so it is 'scaled' properly
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            #now to change the color of the tranisition bar. Currently we are 'getting' health, so green:
            transition_color = (0, 255, 0)
            
        #and now the same but then for LOSING health:
        
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)
            
        #now we need to use all of the above info, and create two rect's with them
        health_bar_rect = pygame.Rect(10, 45, self.current_health / self.health_ratio, 25)
        #two things to change for the transition bar, first is the X coordinate, where it starts, is wherever our health bar ENDS
        # we can do this by calling the above health bar, and just adding the nifty .right method, cool!
        #the second is, out width, which we calculated above as transition_width
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)
        
        #now all that's left is to finally DRAW them
        
        pygame.draw.rect(screen,(255,0,0), health_bar_rect)
        pygame.draw.rect(screen,transition_color, transition_bar_rect)
        #now finally finally, a small outline, same as for the basic health bar
        pygame.draw.rect(screen,(255,255,255), (10,45,self.health_bar_length,25),4)

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