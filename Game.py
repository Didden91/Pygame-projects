#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
HEALTH = 100

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
game_over2 = font_medium.render("Your score was: ", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")



class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("p2.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40)
                                                 , 0))

      def move(self):
        global SCORE
        global HEALTH
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        elif pygame.sprite.spritecollideany(P1, enemies):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            HEALTH -= 10
            pygame.mixer.Sound('crash.wav').play()
            
       


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("p1.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
    def playerhealthbar():
         global HEALTH
         return HEALTH
            
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    healthleft = font_small.render(str(HEALTH), True, BLACK)
    DISPLAYSURF.blit(healthleft, (10,30))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, enemies):
          
    #       pygame.mixer.Sound('crash.wav').play()
    #       HEALTH -= 10
    #       time.sleep(0.2)
    #       pygame.display.update()
    #       # for entity in enemies:
    #       #     entity.kill() 
              
              
    #       pygame.display.update()
          
    
    if Player.playerhealthbar() <= 0:               
          DISPLAYSURF.fill(RED)
          scores = font_medium.render(str(SCORE), True, BLACK)
          DISPLAYSURF.blit(game_over, (30,250))
          DISPLAYSURF.blit(game_over2, (15,350))
          DISPLAYSURF.blit(scores, (340,352))
          
          pygame.display.update()
          for entity in all_sprites:
              entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
    

