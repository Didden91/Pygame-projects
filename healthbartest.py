# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:20:42 2021

@author: Ivo
"""


# Import and initialize the pygame library
import pygame
import time



pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
game_over2 = font_medium.render("Your score was: ", True, BLACK)

# Set up the drawing window
DISPLAYSURF = pygame.display.set_mode([960, 640])
playerhp = 100
newhp = 50


# def hbanimated():
#     global playerhp
    
#     print('IN FUNCTION hbanimated')
    
HBsurf = pygame.Surface((playerhp, 30))   
HBsurf.fill(RED) 
DISPLAYSURF.fill((255, 255, 255))

# Run until the user asks to quit
running = True
while running:
    print('START OF NEW LOOP')
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
    for hp in range (playerhp, newhp, -1):
        print('current playerhp, newhp, hp:',playerhp, newhp, hp)
        time.sleep(0.2)
               
        
        healthleft = font_small.render(str(hp), True, BLACK)
        DISPLAYSURF.blit(healthleft, (700,300))
        playerhp = hp
        HBsurf = pygame.Surface((playerhp, 30))   
        HBsurf.fill(RED)    
        DISPLAYSURF.blit(HBsurf, (720,playerhp))
        pygame.display.update()
        #Need to display and then REMOVE again...although that should be done by the above update() call
            
    

    # Fill the background with white
    
    
    
    # Draw a solid blue circle in the center
    pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (250, 250), 75)

    FramePerSec.tick(FPS)

# Done! Time to quit.
pygame.quit()