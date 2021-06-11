# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:59:17 2021

@author: Ivo
"""

import pygame, sys

class Player(pygame.sprite.Sprite):
    # first inherit everything from the above mentioned Sprite class built into pygame
    def __init__(self):
        
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
        #now to define some attributes of our health bar, starting with current health, which we want to track
        self.current_health = 200
        #another to track maximum health:
        self.maximum_health = 1000
        #another for health bar length (this will be, in pixels, how long our health bar will be):
        #so the above two now measure our HEALTH, the one below measures a DISTANCE
        self.health_bar_length = 400
        #So the above attributes are essentially still 'disconnected'. We need something that says, 
        #at our maximal health of 1000, the health bar should be 400 pixels long
        # so now to convert our health to the health bar length:
        self.health_ratio = self.maximum_health / self.health_bar_length
            
    
    def update(self):
        pass
        
    #So now we have our health but no way to INFLUENCE our health, that's where we need some other methods    
    #method 1: get the damage received:
    # this function takes are parameters ITSELF, which is the own Player class it is in, this means we
    #can get the self.current_health in here for example. It means we can get methods defined within the same class
    
    #
    
    #Secondly, the amount of damage taken
    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    
    #similarly we can make a method that ADDS health:
    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health   
    
    #Now to test these above methods, let's call them in our event loop.
    #Easy way to do this is by using a key press to trigger them
        
    
    

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
                #here we make that all important function call, if the key UP is pressed, call:
                player.sprite.get_health(200)
                #the first 'player' refers to the above 'player = pygame.sprite.GroupSingle(Player())'
                #so the sprite group containing a single sprite, 
                # which is controlled by the Player class mentioned at the end of that statement
                # is placed in 'player'
                #I think the .sprite that follows, is called because as we defined Player above, 
                #Player inherits all the attributes of the sprite class that pygame provides,
                #Because we wrote this: Player(pygame.sprite.Sprite)
                # So it understands a sprite call. I'm assuming as apply to this sprite, or group of sprites
                #The sprite here is the healthbar. So when UP is pressed, increase health by 200
         #Now same with key DOWN, but then you get damage
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                #here we make that all important function call, if the key UP is pressed, call:
                    player.sprite.get_damage(200)
                
            
            
    screen.fill((30,30,30))
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)