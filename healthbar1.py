# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:59:17 2021

@author: Ivo
"""

import pygame, sys

class Player(pygame.sprite.Sprite):
    # first inherit everything from the above mentioned Sprite class built into pygame
    def __init__(self):
        #use the super method to get the attributes of the Sprite class
        super().__init__()
        #Then we are creating an image and a rectanlgle (rect), which a sprite class ALWAYS NEEDS
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
            
        #then include an update method, which doesn't do anything yet
        #for now only used because below we call player.update()
    def update(self):
        pass
        
    

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
            
    screen.fill((30,30,30))
    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(60)