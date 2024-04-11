import pygame
import time
import random


# Initialize the game
pygame.init()

# Set the clock
clock = pygame.time.Clock()

# Set the display parameters
display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Define the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (50, 153, 213)
green = (0, 255, 0)

# Set the snake block and speed
snake_block = 10
snake_speed = 20
snake_list = []


# Define the function to draw the snake
def draw_snake(snake_block: int, snake_list: list) -> None:
    for x in snake_list:
        pygame.draw.rect(display, white, [x[0], x[1], snake_block, snake_block])


# Define the game loop
def gameLoop():
    # Initialize the game variables
    game_over = False
    game_close = False

    # Set the initial position of the snake
    x1 = display_width / 2
    y1 = display_height / 2

    # Set the initial change in position of the snake
    x1_change = 0
    y1_change = 0

    # Set the initial length of the snake
    snake_List = []
    Length_of_snake = 1

    # Set the initial position of the food
    food_x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    


def main():
    gameLoop()


if __name__ == '__main__':
    main()
