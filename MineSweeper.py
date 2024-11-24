#Timothy Pearman - 28856139
#entry for 2024 camjam competition
#PEP8 Compliant :D
 import pygame
import random

# Initialize pygame
pygame.init()

rigged_chance = 0.1
# Window setup
window_width, window_height = 500, 600
window = pygame.display.set_mode((window_width, window_height))
icon = pygame.image.load("assets/icon_bomb.png")
pygame.display.set_caption("\"NOT RIGGED\" Mine Sweeper")
pygame.display.set_icon(icon)

# Font
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Tile class
class Tile:
    def __init__(self, state):
        self.state = state  # 0 for empty, 1 for mine
        self.revealed = False  # Track if the tile has been revealed

    def __repr__(self):
        return str(self.state)

# Game settings
number_of_rows, number_of_columns = 15, 15
number_of_mines, number_of_flags = 50, 50
mine_field = [[Tile(0) for _ in range(number_of_columns)] for _ in range(number_of_rows)]
for _ in range(number_of_mines):
    Row = random.randrange(0, number_of_rows)
    Column = random.randrange(0, number_of_columns)
    mine_field[Row][Column].state = 1

# Load button images
tile_image = pygame.image.load("assets/tile.png").convert_alpha()
bomb_image = pygame.image.load("assets/bomb.png").convert_alpha()
flag_image = pygame.image.load("assets/flag.png").convert_alpha()

button_image = pygame.image.load("assets/button.png").convert_alpha()
secret_button_image = pygame.image.load("assets/secret.png").convert_alpha()

#tile numbers
tile_image_0 = pygame.image.load("assets/numbers/0.png").convert_alpha()
tile_image_1 = pygame.image.load("assets/numbers/1.png").convert_alpha()
tile_image_2 = pygame.image.load("assets/numbers/2.png").convert_alpha()
tile_image_3 = pygame.image.load("assets/numbers/3.png").convert_alpha()
tile_image_4 = pygame.image.load("assets/numbers/4.png").convert_alpha()
tile_image_5 = pygame.image.load("assets/numbers/5.png").convert_alpha()
tile_image_6 = pygame.image.load("assets/numbers/6.png").convert_alpha()
tile_image_7 = pygame.image.load("assets/numbers/7.png").convert_alpha()
tile_image_8 = pygame.image.load("assets/numbers/8.png").convert_alpha()
tile_image_9 = pygame.image.load("assets/numbers/9.png").convert_alpha()


# Button class
class Button:
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.original_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.left_clicked = False
        self.right_clicked = False

    def set_image(self, new_image):
        """Update the button's image."""
        self.image = pygame.transform.scale(new_image, self.rect.size)

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = None
        if self.rect.collidepoint(pos):
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and not self.left_clicked:  # Left click
                self.left_clicked = True
                action = "left_clicked"
            if mouse_buttons[2] and not self.right_clicked:  # Right click
                self.right_clicked = True
                action = "right_clicked"

            if not mouse_buttons[0]:  # Reset left click
                self.left_clicked = False
            if not mouse_buttons[2]:  # Reset right click
                self.right_clicked = False

        # Draw the current button image
        window.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Buttons
start_button = Button(180, 255, button_image, 2)
exit_button = Button(180, 355, button_image, 2)
secret_button = Button(0, 0, secret_button_image)#

# Create grid of tile buttons
tile_buttons = []
for row in range(number_of_rows):
    button_row = []
    for col in range(number_of_columns):
        x = col * 31 + 18
        y = row * 31 + 118
        button = Button(x, y, tile_image)
        button_row.append(button)
    tile_buttons.append(button_row)

def update_tile(row, col, action, mine_field=mine_field):
    global number_of_flags
    if action == "left_clicked":
        match mine_field[row][col].state:
            case 0:
                # Calculate number and update image
                check_surrounding_tiles(row, col)
                return "left clicked a normal space"
            case 1:
                tile_buttons[row][col].set_image(bomb_image)
                reveal_bombs()
                return "left clicked a bomb space"
            case _:
                return "error"
    elif action == "right_clicked":
        match mine_field[row][col].state:
            case 0:
                tile_buttons[row][col].set_image(flag_image)
                mine_field[row][col].state = 2
                number_of_flags -= 1
                return "right clicked a normal space"
            case 1:
                tile_buttons[row][col].set_image(flag_image)
                mine_field[row][col].state = 3
                number_of_flags -= 1
                return "right clicked a bomb space"
            case 2:
                tile_buttons[row][col].set_image(tile_image)
                number_of_flags += 1
                mine_field[row][col].state = 0  # Remove the flag
                mine_field[row][col].revealed = False  # Reset the revealed status
                return "right clicked a flag space"
            case 3:
                tile_buttons[row][col].set_image(tile_image)
                number_of_flags += 1
                mine_field[row][col].state = 1  # Remove the flag from bomb
                mine_field[row][col].revealed = False  # Reset the revealed status
                return "right clicked a flagged bomb space"
            case _:
                return "error"
            
# Modify check_surrounding_tiles to handle recursive revealing
def check_surrounding_tiles(row, col):
    if mine_field[row][col].revealed:
        return  # Exit if this tile is already revealed

    # Mark the tile as revealed
    mine_field[row][col].revealed = True

    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the target element itself
            if i == 0 and j == 0:
                continue

            # Check bounds
            new_row, new_col = row + i, col + j
            if 0 <= new_row < len(mine_field) and 0 <= new_col < len(mine_field[0]):
                if mine_field[new_row][new_col].state == 1 or mine_field[new_row][new_col].state == 3:
                    total += 1

    # Update the button image for the given tile based on the total surrounding mines
    tile_buttons[row][col].set_image(get_tile_image(total))

    if total == 0:
        reveal_surrounding_tiles(row, col)  # Reveal surrounding tiles recursively

# Modify reveal_surrounding_tiles to correctly reveal adjacent tiles
def reveal_surrounding_tiles(row, col):
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the target element itself
            if i == 0 and j == 0:
                continue

            # Check bounds
            new_row, new_col = row + i, col + j
            if 0 <= new_row < len(mine_field) and 0 <= new_col < len(mine_field[0]):
                # Only check and reveal if not already revealed
                if not mine_field[new_row][new_col].revealed:
                    check_surrounding_tiles(new_row, new_col)

                    
def get_tile_image(total):
    match total:
        case 0:
            return tile_image_0
        case 1:
            return tile_image_1
        case 2:
            return tile_image_2
        case 3:
            return tile_image_3
        case 4:
            return tile_image_4
        case 5:
            return tile_image_5
        case 6:
            return tile_image_6
        case 7:
            return tile_image_7
        case 8:
            return tile_image_8
        case 9:
            return tile_image_9
        case _:
            return tile_image_0  # Default if something goes wrong
   
def reveal_bombs():
    global current_screen, program_start_ticks
    # Reveal bombs
    for row in range(number_of_rows):
        for col in range(number_of_columns):
            if mine_field[row][col].state == 1:
                tile_buttons[row][col].set_image(bomb_image)


# screen state
current_screen = "main"
def main_screen():
    global current_screen, program_start_ticks
    window.fill("grey")
    title_text_line1 = my_font.render("(totally normal)", True, "black")
    title_text_line2 = my_font.render("Minesweeper!", True, "black")
    window.blit(title_text_line1, (140, 100))
    window.blit(title_text_line2, (150, 140))

    pygame.draw.rect(window, "black", (175, 250, 150, 75))
    pygame.draw.rect(window, "black", (175, 350, 150, 75))

    if start_button.draw():
        print("start button pushed :D")
        current_screen = "game"
        program_start_ticks = pygame.time.get_ticks() # start timer
        pygame.time.wait(250) # wait before switching screen as to not accidentally press another button
    if exit_button.draw():
        print("exit button pushed :C")
        return False # exit the program
    if secret_button.draw():
        global rigged_chance
        rigged_chance = 1
        print("Secret button pushed >:D")

    title_text_line3 = my_font.render("play :D", True, "black")
    title_text_line4 = my_font.render("exit :C", True, "black")
    window.blit(title_text_line3, (200, 260))
    window.blit(title_text_line4, (200, 360))
    return True

program_start_ticks = 0  # Timer reference
def game_screen():
    global current_screen, program_start_ticks

    elapsed_time = (pygame.time.get_ticks() - program_start_ticks) // 1000

    window.fill("dark grey")
    pygame.draw.rect(window, "light grey", (20, 20, 460, 80))
    pygame.draw.rect(window, "black", (18, 118, 464, 464))

    number_of_flags_left = my_font.render(str(number_of_flags), True, "black")
    game_timer = my_font.render(str(elapsed_time), True, "black")
    window.blit(number_of_flags_left, (100, 35))
    window.blit(game_timer, (375, 35))

    # Draw the tile buttons
    for row in range(number_of_rows):
        for col in range(number_of_columns):
            tile_button = tile_buttons[row][col]
            action = tile_button.draw()
            if action == "left_clicked":
                print(f"Left-clicked on tile ({row}, {col})")
                print(update_tile(row, col, action))

            elif action == "right_clicked":
                print(f"Right-clicked on tile ({row}, {col})")
                print(update_tile(row, col, action))


# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if current_screen == "main":
        run = main_screen()
    elif current_screen == "game":
        game_screen()

    pygame.display.update()

pygame.quit()
