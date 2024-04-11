import pygame
import time
import random


class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (50, 153, 213)
        self.green = (0, 255, 0)


def initialize_game() -> tuple:
    # Initialize the game
    pygame.init()

    # Set the clock
    clock = pygame.time.Clock()

    # Set the display parameters
    display_width = 800
    display_height = 600
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Snake Game")

    # Set the snake block and speed
    snake_block = 10
    snake_speed = 20
    snake_list = []
    length_of_snake = 1

    return clock, display, display_width, display_height, snake_block, snake_speed, snake_list, length_of_snake


def check_boundary(x1: int, y1: int, display_width: int, display_height: int) -> bool:
    return x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0


# def check_collision(snake_list: list, snake_Head: list) -> bool:
#     for x in snake_list[:-1]:
#         if x == snake_Head:
#             return True
#     return False


def check_food_consumption(x1: int, y1: int, food_x: int, food_y: int, display_width: int, display_height: int, snake_block: int, snake_length: int) -> tuple:
    if x1 == food_x and y1 == food_y:
        food_x = int(round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0)
        food_y = int(round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0)
        snake_length += 1
    return food_x, food_y, snake_length


def draw_snake(display: pygame.Surface, colors: Colors, snake_list: list, snake_block: int) -> None:
    for x in snake_list:
        pygame.draw.rect(display, colors.white, [x[0], x[1], snake_block, snake_block])


# Define the game loop
def gameLoop():
    # Initialize the game variables
    clock, display, display_width, display_height, snake_block, snake_speed, snake_list, snake_length = initialize_game()
    colors = Colors()
    game_over = False
    game_close = False

    # Set the initial position of the snake
    x1 = display_width / 2
    y1 = display_height / 2

    # Set the initial change in position of the snake
    x1_change = 0
    y1_change = 0

    # Set the initial position of the food
    food_x = int(round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0)
    food_y = int(round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0)

    # Start the game loop
    while not game_over:

        # Display the game over screen
        while game_close == True:
            display.fill(colors.blue)
            pygame.display.update()

            # Define the font style
            font_style = pygame.font.SysFont(None, 50) # Ignore the error for None
            
            # Define the game over text
            game_over_text = ["You Lost!", "Press 'Q' to Quit", "or 'C' to Play Again"]

            # Define the starting y-coordinate
            y = display_height / 3

            # Display the game over message
            for line in game_over_text:
                message = font_style.render(line, True, colors.red)
                display.blit(message, [display_width / 6, y])
                y += font_style.get_height()

            # Update the display
            pygame.display.update()

            # Set the event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Set the event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Fill the display with the background color
        display.fill(colors.blue)

        # Draw the food
        pygame.draw.rect(display, colors.green, [food_x, food_y, snake_block, snake_block])

        # Initialize the snake head
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)

        # Draw the snake
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(display, colors, snake_list, snake_block)
        pygame.display.update()

        # Check if the snake has consumed the food
        food_x, food_y, snake_length = check_food_consumption(x1, y1, food_x, food_y,
                                                              display_width, display_height,
                                                              snake_block, snake_length)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


def main():
    gameLoop()


if __name__ == '__main__':
    main()
