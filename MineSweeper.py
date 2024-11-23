#Timothy Pearman - 28856139
#entry for 2024 camjam competition
#PEP8 Compliant :D

import random
import pygame

light_grey = (192, 192, 192)
dark_grey = (160, 160, 160)

# initializing the constructor 
pygame.init() 
  

"""
 defines the window resolution 
 creates a display object with defined resolution
 sets the caption and icon attributes
"""
window_width, window_height = 500, 600
window = pygame.display.set_mode((window_width,window_height)) 
icon = pygame.image.load("assets/bomb.png")
pygame.display.set_caption("\"NOT RIGGED\" Mine Sweeper")
pygame.display.set_icon(icon)


"""
NumberOfRows, NumberOfColumns = 15, 15
NumberOfMines = 45
MineField = [[0 for _ in range(NumberOfColumns)] for _ in range(NumberOfRows)]
for _ in range(Mines):
    Row = random.randrange(0,NumberOfRows)
    Column = random.randrange(0,NumberOfColumns)
    
    MineField[Row][Column] = 1
#print(MineField)
"""

img = pygame.image.load("assets/flag.png").convert_alpha()


class Button():
    def __init__(self, x, y, image, scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button onto window
        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


#create button instance
start_button = Button(50, 50, img, 10)
exit_button = Button(50, 100, img)

#game loop
run = True
while run: 

    window.fill("cyan")
    #window.fill((128,128,128))

    if start_button.draw():
        print("Start button clicked")
    if exit_button.draw():
        run = False
        print("Exit button clicked")


    """
    pygame.draw.rect(window, "light grey", (100, 100, 40, 40))
    pygame.draw.rect(window, "dark grey", (200, 200, 25, 25))
    
    
    #window.blit(img, (10, 10))
    #window.blit(img, (20, 20))
    """

    #event handler
    for event in pygame.event.get(): 
        #quit game
        if event.type == pygame.QUIT: 
            run = False
    
    #update any changes onto the window screen
    pygame.display.update()

pygame.quit() 
            
