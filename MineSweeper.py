import pygame

# initializing the constructor 
pygame.init() 
  
# screen resolution 
res = (500,500) 
# opens up a window 
screen = pygame.display.set_mode(res) 
  
# stores the dimentions of the screen into a variables
width = screen.get_width() 
height = screen.get_height() 

#title and icon
pygame.display.set_caption("Mine Sweeper")
icon = pygame.image.load('bomb.png')
pygame.display.set_icon(icon)

#game loop
while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 

    #background RGB values
    screen.fill((128,128,128))
    
    #update any changes onto the window screen
    pygame.display.update()

            
        
