#Imports
import pygame, sys
from pygame.locals import *
import random, time
import pygame_menu



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
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SPEED = 5
SCORE = 0
PLAYERHEALTH = 100
ENEMYHEALTH = 100
moveused = 0


#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
game_over2 = font_medium.render("Your score was: ", True, BLACK)

backgroundtop = pygame.image.load("pokebackground.png")
backgroundbottom = pygame.image.load("pokebackground2.png")
icon = pygame.image.load("icon.jpg")

#testje voor move names
move1name = 'floopie'
move2name = 'drill peck'

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((960,640))
# HBSURF = pygame.display.set_mode((80,80))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Pokemans")
pygame.display.set_icon(icon)

     
   
#Defining the move buttons (have to be seperate):
    
def move1():
    global ENEMYHEALTH
    global moveused
    print('chosen move 1')
    ENEMYHEALTH -= 10
    moveused = 1
    
    #End of choosing a move is toggling current menu off and next one on
    movemenu.toggle()
    
def move2():
    global PLAYERHEALTH
    global moveused
    print('chosen move 2')
    moveused = 2
    PLAYERHEALTH -= 10
    
def move3():
    global moveused
    print('chosen move 3')
    moveused = 3
    
def move4():
    global moveused
    print('chosen move 4')
    moveused = 4
    

    

#creating a first 'menu' for wild pokemon appeared
openingmenu = pygame_menu.Menu(
        columns=1,
        height=190,
        menu_position=(100,100),
        onclose=pygame_menu.events.EXIT,
        rows=1,
        theme=pygame_menu.themes.THEME_GREEN,
        title='Prompt',
        width=960)

#creating button for openingmenu:
openingmenu.add_button('A WILD POKEMON APPEARED!', openingmenu.toggle)

#creating a move menu:
    
movemenu = pygame_menu.Menu(
        columns=2,
        height=190,
        menu_position=(100,100),
        onclose=pygame_menu.events.EXIT,
        rows=2,
        theme=pygame_menu.themes.THEME_GREEN,
        title='Choose a move!',
        width=960)

#creating buttons for menu:
movemenu.add_button(move1name, move1)
movemenu.add_button('MOVE3', move3)
movemenu.add_button(move2name, move2)
movemenu.add_button('MOVE4', move4)

#creating a postmovemenu1:
postmovemenu1 = pygame_menu.Menu(
        columns=1,
        height=190,
        menu_position=(100,100),
        onclose=pygame_menu.events.EXIT,
        rows=1,
        theme=pygame_menu.themes.THEME_GREEN,
        title='Result',
        width=960)

#creating button for postmovemenu1:
    
postmovemenu1.add_button('You used move %s' % (moveused), postmovemenu1.toggle)





  






class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("p2.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (720, 150))
        
        # return a width and height of an image
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))

      # def move(self):
      #   global SCORE
      #   global PLAYERHEALTH
      #   self.rect.move_ip(0,SPEED)
      #   if (self.rect.bottom > 600):
      #       SCORE += 1
      #       self.rect.top = 0
      #       self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
      #   elif pygame.sprite.spritecollideany(P1, enemies):
      #       self.rect.top = 0
      #       self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
      #       PLAYERHEALTH -= 10
      #       pygame.mixer.Sound('crash.wav').play()
            
      def enemyhealthbar():
         global ENEMYHEALTH
         return ENEMYHEALTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("p1.png")
        self.surf = pygame.Surface((80, 75))
        self.rect = self.surf.get_rect(center = (250, 340))
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        # draw bigger image to screen at x=100 y=100 position
        # self.surf.blit(self.bigger_img, [80,75])
       
    # def move(self):
    #     pressed_keys = pygame.key.get_pressed()
    #    #if pressed_keys[K_UP]:
    #         #self.rect.move_ip(0, -5)
    #    #if pressed_keys[K_DOWN]:
    #         #self.rect.move_ip(0,5)
        
    #     if self.rect.left > 0:
    #           if pressed_keys[K_LEFT]:
    #               self.rect.move_ip(-5, 0)
    #     if self.rect.right < SCREEN_WIDTH:        
    #           if pressed_keys[K_RIGHT]:
    #               self.rect.move_ip(5, 0)
    def playerhealthbar():
         global PLAYERHEALTH
         return PLAYERHEALTH
     

        
def draw_background():
    
    
       #Creating a playerhealth bar:

    HBsurf = pygame.Surface((PLAYERHEALTH*2, 30))
        #Fill the surface with a color
    HBsurf.fill(RED)
    
    #create enemy healthbar
    enemyHBsurf = pygame.Surface((ENEMYHEALTH*2, 30))
        #Fill the surface with a color
    enemyHBsurf.fill(RED)
            
   
    DISPLAYSURF.blit(backgroundtop, (0,0))
    DISPLAYSURF.blit(backgroundbottom, (0,450))
    DISPLAYSURF.blit(HBsurf, (720,380))
    DISPLAYSURF.blit(enemyHBsurf, (100,80))
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    healthleft = font_small.render(str(PLAYERHEALTH), True, BLACK)
    DISPLAYSURF.blit(healthleft, (10,30))
    
    for entity in all_sprites:  
        DISPLAYSURF.blit(entity.bigger_img, entity.rect)
    
    
                  

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


print('GAME INITIALIZED, WAITING 2 SECONDS')
time.sleep(2)

print('DRAWING BACKGROUND and waiting 2 seconds')
draw_background()
time.sleep(2)

#Game Loop
while True:
    
    
   
    
     #run opening menu
    
    while openingmenu.is_enabled():
    
        # menu.update(events)
        print('currently in opening menu')
        openingmenu.mainloop(DISPLAYSURF, bgfun=draw_background)
       
        print('STILL in opening menu')
        
        pygame.display.update()
        
    while ENEMYHEALTH > 0 and PLAYERHEALTH > 0:                

        while movemenu.is_enabled():
            print('Starting MOVEmenu')
           
            
            movemenu.mainloop(DISPLAYSURF, bgfun=draw_background)
    
            pygame.display.update()
            
            
        while postmovemenu1.is_enabled():
            print('Starting postmovemenu1')
            postmovemenu1.mainloop(DISPLAYSURF, bgfun=draw_background)
            pygame.display.update()
            
        movemenu.toggle()
        postmovemenu1.toggle()
        
                    

    #Cycles through all events occuring  
    for event in pygame.event.get():
         
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                print("Player pressed enter!")
            elif event.key == pygame.K_a:
                print("Player moved left!")
            elif event.key == pygame.K_s:
                print("Player moved down!")
            elif event.key == pygame.K_d:
                print("Player moved right!")
            
            
            
   
    
        
    #run menu:
    
    

    #Moves and Re-draws all Sprites
    # for entity in all_sprites:
    #     DISPLAYSURF.blit(entity.image, entity.rect)
    #     entity.move()

    #To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, enemies):
          
    #       pygame.mixer.Sound('crash.wav').play()
    #       PLAYERHEALTH -= 10
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
    

