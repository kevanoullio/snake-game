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


class Snake:
    def __init__(self, snake_block: int, snake_speed: int) -> None:
        self.block: int = snake_block
        self.speed: int = snake_speed
        self.head: list = []
        self.list: list = []
        self.length: int = 1
        # Snake position
        self.x1: int = 0
        self.y1: int = 0
        # Snake direction
        self.x1_change: int = 0
        self.y1_change: int = 0

    def set_initial_position(self, display_width: int, display_height: int) -> None:
        self.x1 = int(display_width / 2)
        self.y1 = int(display_height / 2)

    def set_initial_change_in_position(self, x1_change: int, y1_change: int) -> None:
        self.x1_change = x1_change
        self.y1_change = y1_change


class Food:
    def __init__(self, food_x: int, food_y: int) -> None:
        # Food position
        self.food_x = food_x
        self.food_y = food_y

class SnakeGame:
    def __init__(self):
        # Initialize the game
        pygame.init()
        # Set the game parameters
        self.clock: pygame.time.Clock = pygame.time.Clock()
        # Set the display parameters
        self.display_width: int = 800
        self.display_height: int = 600
        self.display: pygame.Surface = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Snake Game")
        # Set the game state
        self.game_over: bool = False
        self.game_close: bool = False
        # Create the snake object and initial settings
        self.snake = Snake(10, 20)
        self.snake.set_initial_position(self.display_width, self.display_height)
        self.snake.set_initial_change_in_position(0, 0)
        # Create the food object and initial settings
        self.food: Food = Food(
            int(round(random.randrange(0, self.display_width - self.snake.block) / 10.0) * 10.0),
            int(round(random.randrange(0, self.display_height - self.snake.block) / 10.0) * 10.0)
        )

    def check_boundary(self, x1: int, y1: int) -> bool:
        # Check if the display width and height are set
        if self.display_width is None or self.display_height is None:
            raise ValueError("The display width and height must be set.")
        
        # Check if the snake has hit the boundary
        return x1 >= self.display_width or x1 < 0 or y1 >= self.display_height or y1 < 0

    def check_collision(self, snake_Head: list) -> bool:
        # Check if the snake list is set
        if self.snake.list is None:
            raise ValueError("The length of the snake must be set.")
        
        # Check if the snake has collided with itself (i.e. the snake head collides with the snake body)
        for x in self.snake.list[:-1]:
            if x == snake_Head:
                return True
        return False

    def check_food_consumption(self, x1: int, y1: int, food_x: int, food_y: int) -> tuple:
        # Check if the display width and height are set
        if self.display_width is None or self.display_height is None:
            raise ValueError("The display width and height must be set.")
        
        # Check if the snake block is set
        if self.snake.block is None:
            raise ValueError("The snake block must be set.")
        
        # Check if the snake length is set
        if self.snake.length is None:
            raise ValueError("The length of the snake must be set.")
        
        # Check if the snake has consumed the food
        if x1 == food_x and y1 == food_y:
            food_x = int(round(random.randrange(0, self.display_width - self.snake.block) / 10.0) * 10.0)
            food_y = int(round(random.randrange(0, self.display_height - self.snake.block) / 10.0) * 10.0)
            self.snake.length += 1
        return food_x, food_y
    
    def draw_snake(self, colors: Colors) -> None:
        # Check if the display width and height are set
        if self.display is None:
            raise ValueError("The display must be set.")
        
        # Check if the snake block is set
        if self.snake.block is None:
            raise ValueError("The snake block must be set.")
        
        # Check if the snake list is set
        if self.snake.list is None:
            raise ValueError("The length of the snake must be set.")
        
        # Draw the snake
        for x in self.snake.list:
            pygame.draw.rect(self.display, colors.white, [x[0], x[1], self.snake.block, self.snake.block])
    
    def draw_game_over_screen(self, colors: Colors) -> None:
        # Check if the display is set
        if self.display is None:
            raise ValueError("The display must be set.")
        
        # Check if the display width and height are set
        if self.display_width is None or self.display_height is None:
            raise ValueError("The display width and height must be set.")
        
        # Display the game over screen
        self.display.fill(colors.blue)

        # Define the font style
        font_style = pygame.font.SysFont(None, 50) # Ignore the error for None
        
        # Define the game over text
        game_over_text = ["You Lost!", "Press 'Q' to Quit", "or 'C' to Play Again"]

        # Define the starting y-coordinate
        y = self.display_height / 3

        # Display the game over message
        for line in game_over_text:
            message = font_style.render(line, True, colors.red)
            self.display.blit(message, [self.display_width / 6, y])
            y += font_style.get_height()

        # Update the display
        pygame.display.update()


# Define the game loop
def gameLoop():
    # Initialize the colors object
    colors = Colors()

    # Initialize the SnakeGame object
    snake_game = SnakeGame()

    # Start the game loop
    while not snake_game.game_over:

        # Display the game over screen
        while snake_game.game_close == True:
            # Check if the display width and height are set
            if snake_game.display is None:
                raise ValueError("The display must be set.")

            # Display the game over screen
            snake_game.draw_game_over_screen(colors)
            
            # Set the event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        snake_game.game_over = True
                        snake_game.game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Set the event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_game.game_over = True
                snake_game.game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_game.snake.y1_change = -snake_game.snake.block
                    snake_game.snake.x1_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_game.snake.y1_change = snake_game.snake.block
                    snake_game.snake.x1_change = 0
                elif event.key == pygame.K_LEFT:
                    snake_game.snake.x1_change = -snake_game.snake.block
                    snake_game.snake.y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_game.snake.x1_change = snake_game.snake.block
                    snake_game.snake.y1_change = 0

        if x1 >= snake_game.display_width or x1 < 0 or y1 >= snake_game.display_height or y1 < 0:
            snake_game.game_close = True
        x1 += snake_game.snake.x1_change
        y1 += snake_game.snake.y1_change

        # Fill the display with the background color
        snake_game.display.fill(colors.blue)

        # Draw the food
        pygame.draw.rect(snake_game.display, colors.green, [food_x, food_y, snake_game.snake.block, snake_game.snake.block])

        # Initialize the snake head
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_game.snake.list.append(snake_Head)

        # Draw the snake
        if len(snake_game.snake.list) > snake_length:
            del snake_game.snake.list[0]

        for x in snake_game.snake.list[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_game.display, colors, snake_game.snake.list, snake_game.snake.block)
        pygame.display.update()

        # Check if the snake has consumed the food
        food_x, food_y, snake_length = check_food_consumption(x1, y1, snake_game.food.food_x, food_y,
                                                              snake_game.display_width, snake_game.display_height,
                                                              snake_game.snake.block, snake_length)

        snake_game.clock.tick(snake_game.snake.speed)

    pygame.quit()
    quit()


def main():
    gameLoop()


if __name__ == '__main__':
    main()
