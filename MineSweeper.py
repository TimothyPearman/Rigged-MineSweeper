#Timothy Pearman - 28856139
#entry for 2024 camjam competition
#PEP8 Compliant :D

import pygame
import random
import time

# initializing the constructor 
pygame.init() 

program_start_ticks = pygame.time.get_ticks()
  

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

my_font = pygame.font.SysFont('Comic Sans MS', 30)

class Tile():
    def __init__(self, state):
        self.state = 0
    
    def __repr__(self):
        return str(self.state)

"""
defines a 2D array of dimensions 15x15 and initializes each element to a Tile object
iterates through the 2D array and randomly assigns 75 mines by updating the state of the tile object to 1
"""
number_of_rows, number_of_columns = 15, 15
number_of_mines,number_of_flags = 75, 75
mine_field = [[Tile(0) for _ in range(number_of_columns)] for _ in range(number_of_rows)]
for _ in range(number_of_mines):
    Row = random.randrange(0,number_of_rows)
    Column = random.randrange(0,number_of_columns)
    
    mine_field[Row][Column].state = 1
print(mine_field)


button = pygame.image.load("assets/flag.png").convert_alpha()

class Button():
    def __init__(self, x, y, image, scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.left_clicked = False
        self.right_clicked = False

    def draw(self):
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.left_clicked == False: 
                self.left_clicked = True
                return "left_clicked"
            if pygame.mouse.get_pressed()[2] == 1 and self.right_clicked == False: 
                self.right_clicked = True
                return "right_clicked"
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.left_clicked = False
        if pygame.mouse.get_pressed()[2] == 0:
            self.right_clicked = False
        
        #draw button onto window
        window.blit(self.image, (self.rect.x, self.rect.y))

#create button instance
start_button = Button(50, 50, button, 10)
exit_button = Button(50, 100, button)
secret_button = Button(0, 0, button)
tile_button = Button(50, 50, button)


#game loop
run = True
while run: 
    elapsed_time = (pygame.time.get_ticks() - program_start_ticks) // 1000

    window.fill("dark grey")
    #window.fill((128,128,128))
    pygame.draw.rect(window, "light grey", (20, 20, 460, 80))
    pygame.draw.rect(window, "light grey", (20, 120, 460, 460))
    
    number_of_flags_left = my_font.render(str(number_of_flags), True, "black")
    game_timer = my_font.render(str(elapsed_time), True, "black")
    
    window.blit(number_of_flags_left, (10, 10))
    window.blit(game_timer, (410, 10))
    

    start_button_action = start_button.draw()
    if start_button_action == "left_clicked" and number_of_flags > 0:
        print("left  button left clicked")
        number_of_flags -= 1
    if start_button_action == "right_clicked" and number_of_flags < 75:
        print("right button right clicked")
        number_of_flags += 1

    exit_button_action = exit_button.draw()
    if exit_button_action == "left_clicked":
        run = False
        print("Exit button clicked")

    secret_button_action = secret_button.draw()
    if secret_button_action == "left_clicked":
        rigged_chance = 100
        print("secret button clicked")



    for i in range(number_of_rows):
        for j in range((number_of_columns)):
            pygame.draw.rect(window, "light grey", (100 + (15 * i), 100 + (15 * j), 10, 10))


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
            
