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


class Vector:
    def __init__(self, x: int, y: int, dx: int = 0, dy: int = 0) -> None:
        self.x = x
        self.y = y
        self.dx = dx  # Change in x (direction along x-axis)
        self.dy = dy  # Change in y (direction along y-axis)

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> tuple:
        return self.x, self.y


class Snake:
    def __init__(self) -> None:
        # Snake parameters
        self.block: int = 10
        self.speed: int = 20
        # Snake head and body
        self.head: list = []
        self.list: list = []
        self.length: int = 1
        # Snake vector
        self.vector: Vector = Vector(0, 0)

    def set_initial_position(self, display_width: int, display_height: int) -> None:
        self.vector.x = int(display_width / 2)
        self.vector.y = int(display_height / 2)
        self.list.append([self.vector.x, self.vector.y])

    def set_initial_change_in_position(self, x1_change: int, y1_change: int) -> None:
        self.vector.dx = x1_change
        self.vector.dy = y1_change

    def move_up(self) -> None:
        self.vector.dy = -self.block
        self.vector.dx = 0

    def move_down(self) -> None:
        self.vector.dy = self.block
        self.vector.dx = 0
    
    def move_left(self) -> None:
        self.vector.dx = -self.block
        self.vector.dy = 0
    
    def move_right(self) -> None:
        self.vector.dx = self.block
        self.vector.dy = 0
    
    def get_head_position(self) -> tuple:
        return self.list[-1]
    
    def update_body(self) -> None:
        # Get the head position
        x1, y1 = self.get_head_position()

        # Update the head position
        x1 += self.vector.dx
        y1 += self.vector.dy
        self.list.append([x1, y1])

        # Check if the length of the snake is greater than the required length
        if len(self.list) > self.length:
            del self.list[0]
    
    def check_self_collision(self) -> bool:
        # Get the head position
        x1, y1 = self.get_head_position()

        # Check if the snake has collided with itself
        for x in self.list[:-1]:
            if x == [x1, y1]:
                return True
        return False

    def draw(self, display: pygame.Surface, colors: Colors) -> None:
        for x in self.list:
            pygame.draw.rect(display, colors.white, [x[0], x[1], self.block, self.block])


class Food:
    def __init__(self, x: int, y: int) -> None:
        # Food parameters
        self.block_size: int = 10
        # Food vector
        self.vector: Vector = Vector(x, y)
    
    def draw(self, display: pygame.Surface, colors: Colors) -> None:
        pygame.draw.rect(display, colors.green, [self.vector.x, self.vector.y, self.block_size, self.block_size])


class SnakeGame:
    def __init__(self):
        # Initialize the colors object
        self.colors = Colors()

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
        self.snake = Snake()
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

    def check_food_consumption(self) -> tuple:       
        # Check if the snake has consumed the food
        if self.snake.vector.x == self.food.vector.x and self.snake.vector.y == self.food.vector.y:
            self.food.vector.x = int(round(random.randrange(0, self.display_width - self.snake.block) / 10.0) * 10.0)
            self.food.vector.y = int(round(random.randrange(0, self.display_height - self.snake.block) / 10.0) * 10.0)
            self.snake.length += 1
        return self.food.vector.x, self.food.vector.y
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.move_up()
                elif event.key == pygame.K_DOWN:
                    self.snake.move_down()
                elif event.key == pygame.K_LEFT:
                    self.snake.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.snake.move_right()
    
    def check_boundaries(self):
        x1, y1 = self.snake.get_head_position()
        if x1 >= self.display_width or x1 < 0 or y1 >= self.display_height or y1 < 0:
            self.game_close = True
    
    # def draw_snake(self, colors: Colors) -> None:
    #     # Check if the display width and height are set
    #     if self.display is None:
    #         raise ValueError("The display must be set.")
        
    #     # Check if the snake block is set
    #     if self.snake.block is None:
    #         raise ValueError("The snake block must be set.")
        
    #     # Check if the snake list is set
    #     if self.snake.list is None:
    #         raise ValueError("The length of the snake must be set.")
        
    #     # Draw the snake
    #     for x in self.snake.list:
    #         pygame.draw.rect(self.display, colors.white, [x[0], x[1], self.snake.block, self.snake.block])
    
    def draw_game_over_screen(self) -> None:
        # Check if the display is set
        if self.display is None:
            raise ValueError("The display must be set.")
        
        # Check if the display width and height are set
        if self.display_width is None or self.display_height is None:
            raise ValueError("The display width and height must be set.")
        
        # Display the game over screen
        self.display.fill(self.colors.blue)

        # Define the font style
        font_style = pygame.font.SysFont(None, 50) # Ignore the error for None
        
        # Define the game over text
        game_over_text = ["You Lost!", "Press 'Q' to Quit", "or 'C' to Play Again"]

        # Define the starting y-coordinate
        y = self.display_height / 3

        # Display the game over message
        for line in game_over_text:
            message = font_style.render(line, True, self.colors.red)
            self.display.blit(message, [self.display_width / 6, y])
            y += font_style.get_height()

        # Update the display
        pygame.display.update()
    
    def game_loop(self):
        while not self.game_over:
            while self.game_close == True:
                self.draw_game_over_screen()
                self.handle_events()

            self.handle_events()
            self.check_boundaries()
            self.display.fill(self.colors.blue)
            self.food.draw(self.display, self.colors)
            self.snake.update_body()
            self.snake.check_self_collision()
            self.check_food_consumption()
            pygame.display.update()
            self.clock.tick(self.snake.speed)

        pygame.quit()
        quit()

def main():
    snake_game = SnakeGame()
    snake_game.game_loop()


if __name__ == '__main__':
    main()
