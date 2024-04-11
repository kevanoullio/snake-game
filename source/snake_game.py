import pygame
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
        self.block_size: int = 10
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
        # Prevent the snake from moving in the opposite direction
        if self.vector.dy == self.block_size:
            return
        self.vector.dy = -self.block_size
        self.vector.dx = 0

    def move_down(self) -> None:
        # Prevent the snake from moving in the opposite direction
        if self.vector.dy == -self.block_size:
            return
        self.vector.dy = self.block_size
        self.vector.dx = 0
    
    def move_left(self) -> None:
        # Prevent the snake from moving in the opposite direction
        if self.vector.dx == self.block_size:
            return
        self.vector.dx = -self.block_size
        self.vector.dy = 0
    
    def move_right(self) -> None:
        # Prevent the snake from moving in the opposite direction
        if self.vector.dx == -self.block_size:
            return
        self.vector.dx = self.block_size
        self.vector.dy = 0
    
    def get_head_position(self) -> tuple:
        return self.list[-1]
    
    def update_body(self) -> None:
        # Get the head position
        x1, y1 = self.get_head_position()

        # Update the head position
        x1 += self.vector.dx
        y1 += self.vector.dy
        self.vector.x = x1
        self.vector.y = y1
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
            pygame.draw.rect(display, colors.white, [x[0], x[1], self.block_size, self.block_size])


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
        self.game_quit: bool = False

        # Create the snake object and initial settings
        self.snake = Snake()
        self.snake.set_initial_position(self.display_width, self.display_height)
        self.snake.set_initial_change_in_position(0, 0)

        # Create the food object and initial settings
        self.food: Food = Food(
            int(round(random.randrange(0, self.display_width - self.snake.block_size) / 10.0) * 10.0),
            int(round(random.randrange(0, self.display_height - self.snake.block_size) / 10.0) * 10.0)
        )

    def check_boundary(self, x1: int, y1: int) -> bool:        
        # Check if the snake has hit the boundary
        return x1 >= self.display_width or x1 < 0 or y1 >= self.display_height or y1 < 0

    def check_collision(self, snake_Head: list) -> bool:       
        # Check if the snake has collided with itself (i.e. the snake head collides with the snake body)
        for x in self.snake.list[:-1]:
            if x == snake_Head:
                return True
        return False

    def check_food_consumption(self) -> None:       
        # Check if the snake has consumed the food
        if self.snake.vector.x == self.food.vector.x and self.snake.vector.y == self.food.vector.y:
            self.food.vector.x = int(round(random.randrange(0, self.display_width - self.snake.block_size) / 10.0) * 10.0)
            self.food.vector.y = int(round(random.randrange(0, self.display_height - self.snake.block_size) / 10.0) * 10.0)
            self.snake.length += 1
            self.snake.update_body()
    
    def check_boundaries(self):
        x1, y1 = self.snake.get_head_position()
        if x1 >= self.display_width or x1 < 0 or y1 >= self.display_height or y1 < 0:
            self.game_quit = True
    
    def draw_game_over_screen(self) -> None:        
        # Display the game over screen
        self.display.fill(self.colors.blue)

        # Define the font style
        font_style = pygame.font.SysFont(None, 50) # type: ignore
        
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

        # Game over loop
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        self.reset_game()
                        game_over = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.game_quit = True
            elif event.type == pygame.KEYDOWN:
                # Handle snake movement when game is active
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.snake.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                # Handle game over controls (quit, play again)
                elif self.game_over:
                    if event.key == pygame.K_q:
                        self.game_quit = True
                    elif event.key == pygame.K_c:
                        self.reset_game()

    def game_loop(self):
        # Start the game loop
        while not self.game_quit:
            # Check if the game is over
            while self.game_over:
                self.draw_game_over_screen()
                self.handle_events()
                # Break out of the outer loop if game is reset
                if not self.game_over:
                    break

            # Handle the events
            self.handle_events()
            self.check_boundaries()

            # Fill the background color
            self.display.fill(self.colors.blue)

            # Draw the food
            self.food.draw(self.display, self.colors)

            # Check if the snake has consumed the food
            self.check_food_consumption()

            # Update and draw the snake
            self.snake.update_body()
            self.snake.draw(self.display, self.colors)

            # Check if the snake has collided with itself
            if self.snake.check_self_collision():
                self.game_over = True

            # Update the display
            pygame.display.update()

            # Update the clock
            self.clock.tick(self.snake.speed)
    
    def run(self) -> None:
        while not self.game_over:
            self.game_loop()

            if self.game_quit:
                self.draw_game_over_screen()
            
        pygame.quit()
        quit()
    
    def reset_game(self) -> None:
        # Reset the snake
        self.snake = Snake()
        self.snake.set_initial_position(self.display_width, self.display_height)
        self.snake.set_initial_change_in_position(0, 0)

        # Reset the food
        self.food = Food(
            int(round(random.randrange(0, self.display_width - self.snake.block_size) / 10.0) * 10.0),
            int(round(random.randrange(0, self.display_height - self.snake.block_size) / 10.0) * 10.0)
        )

        # Reset the game state
        self.game_over = False
        self.game_quit = False


def main():
    game = SnakeGame()
    game.run()


if __name__ == '__main__':
    main()
