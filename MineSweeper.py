#Timothy Pearman - 28856139
#entry for 2024 camjam competition
#PEP8 Compliant :D
 
import pygame
import random
import time

# initializing the constructor 
pygame.init() 

"""
 defines the window resolution 
 creates a display object with defined resolution
 sets the caption and icon attributes
"""
window_width, window_height = 500, 600
window = pygame.display.set_mode((window_width, window_height)) 
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
number_of_mines, number_of_flags = 75, 75
mine_field = [[Tile(0) for _ in range(number_of_columns)] for _ in range(number_of_rows)]
for _ in range(number_of_mines):
    Row = random.randrange(0, number_of_rows)
    Column = random.randrange(0, number_of_columns)
    mine_field[Row][Column].state = 1
print(mine_field)

# Load the button images
button_image = pygame.image.load("assets/button.png").convert_alpha()
secret_button_image = pygame.image.load("assets/secret.png").convert_alpha()
tile_button_image = pygame.image.load("assets/flag.png").convert_alpha()

class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.left_clicked = False

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.left_clicked: 
                self.left_clicked = True
                return True
        else:
            self.left_clicked = False

        # draw button onto window
        window.blit(self.image, (self.rect.x, self.rect.y))
        return False

# Create buttons
start_button = Button(180, 255, button_image, 2)
exit_button = Button(180, 355, button_image, 2)
secret_button = Button(0, 0, secret_button_image)

# Game state variable
current_screen = "main"  # Can be "main" or "game"

# Initialize timer variables
program_start_ticks = 0
timer_started = False  # To track if the timer has been started

def main_screen():
    global current_screen, program_start_ticks, timer_started

    window.fill("grey")
    title_text_line1 = my_font.render("(totally normal)", True, "black")
    title_text_line2 = my_font.render("Minesweeper!", True, "black")
    window.blit(title_text_line1, (140, 100))
    window.blit(title_text_line2, (150, 140))

    pygame.draw.rect(window, "black", (175, 250, 150, 75))
    pygame.draw.rect(window, "black", (175, 350, 150, 75))
    
    # Draw buttons
    if start_button.draw():
        current_screen = "game"  # Switch to game screen
        program_start_ticks = pygame.time.get_ticks()  # Reset timer
        timer_started = True  # Mark the timer as started
    if exit_button.draw():
        return False  # Signal to quit the game
    if secret_button.draw():
        print("secret button pushed >:D")
    
    title_text_line3 = my_font.render("play :D", True, "black")
    title_text_line4 = my_font.render("exit :C", True, "black")
    window.blit(title_text_line3, (200, 260))
    window.blit(title_text_line4, (200, 360))
    
    return True

def game_screen():
    global timer_started
    if not timer_started:
        return  # Skip drawing the game screen if the timer hasn't started

    elapsed_time = (pygame.time.get_ticks() - program_start_ticks) // 1000

    window.fill("dark grey")
    pygame.draw.rect(window, "light grey", (20, 20, 460, 80))
    pygame.draw.rect(window, "black", (18, 118, 464, 464))

    number_of_flags_left = my_font.render(str(number_of_flags), True, "black")
    game_timer = my_font.render(str(elapsed_time), True, "black")
    window.blit(number_of_flags_left, (100, 35))
    window.blit(game_timer, (375, 35))

# Main game loop
run = True
while run: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False

    if current_screen == "main":
        run = main_screen()  # If False is returned, quit
    elif current_screen == "game":
        game_screen()

    pygame.display.update()

pygame.quit()
