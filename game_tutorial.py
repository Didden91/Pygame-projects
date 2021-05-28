import pygame
from pygame.locals import *

#This line is compulsory to add anytime you want to use the Pygame library.
#It must be added before any other pygame function, else an initialization error may occur.
pygame.init()

#Game loop begins
while True:
      # Code
      # Code
      .
      .
      # create a tuple called DISPLAYSURF which contains the width and height of the display
      DISPLAYSURF = pygame.display.set_mode((300,300))

      # we can draw a circle @ coords 200 and 50, like so:
      # Remember, both of these values start from the TOP-LEFT HAND SIDE

      pygame.draw.circle(DISPLAYSURF, BLACK, (200,50), 30)

      # we can create colors using RGB values ranging from 0 - 255

      color1 = pygame.Color(0, 0, 0)         # Black
      color2 = pygame.Color(255, 255, 255)   # White
      color3 = pygame.Color(128, 128, 128)   # Grey
      color4 = pygame.Color(255, 0, 0)       # Red

      #We use the fill(color) method to fill in objects. For instance, assigning a rectangle the color green will only turn the borders green.   If you use the fill() method and pass a green color object, the rectangle will become completely green.

      #FPS: limit the FPS like so:

      FPS = pygame.time.Clock()
      FPS.tick(60)


      #Changes in the game are not implemented until the display.update() has been called. Since games are constantly changing values, the update function is in the game loop, constantly updating.
      pygame.display.update()

      #We can find out which events have happened by calling the pygame.event.get() function (shown previously),
      # which returns a list of pygame.event.Event objects (which we will just call Event objects for short).

      # One of the many attributes (or properties) held by event objects is type.
      # The type attribute tells us what kind of event the object represents.

      #  event.type == QUIT to determine whether the game was to be closed or not.

      for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
