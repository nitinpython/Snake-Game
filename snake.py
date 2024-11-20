import pygame as pg
from pygame.locals import *
from random import randrange


class Snake:
    def __init__(self, surface: pg.Surface, BLOCK_SIZE: int, BLOCKS: int):
        self.surface = surface
        self.BLOCK_SIZE = BLOCK_SIZE
        self.BLOCKS = BLOCKS

        self.initial_length = 3                # Initially snake's body consists of 3 blocks
        self.color = 'green'

        # To move the snake
        self.move_x = self.BLOCK_SIZE
        self.move_y = 0
        
        HEAD_ROW_BLOCK = self.BLOCKS // 5           # Display head of the snake in the 6th block of the row
        HEAD_COLUMN_BLOCK = self.BLOCKS // 2        # Display head of the snake in the 13th block of the row
        
        self.body = list()                     # Snake body alongwith the head
        
        # Creating Rect objects for the body of the snake
        for blocks in range(self.initial_length):
            rectangle = pg.Rect((HEAD_ROW_BLOCK - blocks) * self.BLOCK_SIZE, HEAD_COLUMN_BLOCK * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
            self.body.append(rectangle)
        
        # The above code is same as this code:
        # self.body = [
        #     pg.Rect(HEAD_ROW_BLOCK * BLOCK_SIZE, HEAD_COLUMN_BLOCK * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
        #     pg.Rect((HEAD_ROW_BLOCK - 1) * BLOCK_SIZE, HEAD_COLUMN_BLOCK * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
        #     pg.Rect((HEAD_ROW_BLOCK - 2) * BLOCK_SIZE, HEAD_COLUMN_BLOCK * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        #     ]

        self.head = self.body[0]                    # Snake's head


    def draw(self):
        for block in self.body:
            pg.draw.rect(self.surface, self.color, block)


    # Moving the snake
    def update(self):

        # Placing the last cell before the first cell (head) to create moving effect
        self.body[-1].x = self.head.x + self.move_x
        self.body[-1].y = self.head.y + self.move_y
        
        # Moving last item of the list to the first position (i.e Changing the head)
        self.body.insert(0, self.body.pop())

        # Updating the head
        self.head = self.body[0]


    # Methods to turn the snake according to the arrow keys
    def move_left(self):
        if self.move_x != self.BLOCK_SIZE:
            self.move_x = - self.BLOCK_SIZE
            self.move_y = 0
    
    
    def move_right(self):
        if self.move_x != - self.BLOCK_SIZE:
            self.move_x = self.BLOCK_SIZE
            self.move_y = 0
    
    
    def move_up(self):
        if self.move_y != self.BLOCK_SIZE:
            self.move_y = - self.BLOCK_SIZE
            self.move_x = 0
    
    
    def move_down(self):
        if self.move_y != - self.BLOCK_SIZE:
            self.move_y = self.BLOCK_SIZE
            self.move_x = 0


    # Reset the snake's position
    def reset(self):
        self.__init__(self.surface, self.BLOCK_SIZE, self.BLOCKS)


    def increase_length(self):
        self.body.append(pg.Rect(self.head.x, self.head.y, self.BLOCK_SIZE, self.BLOCK_SIZE))


class Food:
    def __init__(self, surface: pg.Surface, BLOCK_SIZE: int):
        self.surface = surface
        self.BLOCK_SIZE = BLOCK_SIZE
        
        self.food = pg.Rect(self.gen_random_coordinate()[0], self.gen_random_coordinate()[1], self.BLOCK_SIZE, self.BLOCK_SIZE)
        self.color = 'red'


    def draw(self):
        pg.draw.rect(self.surface, self.color, self.food)

    
    def update(self):
        self.food.left = self.gen_random_coordinate()[0]
        self.food.top = self.gen_random_coordinate()[1]


    def gen_random_coordinate(self):
        left = randrange(0, self.surface.get_width(), self.BLOCK_SIZE)
        top = randrange(0, self.surface.get_height(), self.BLOCK_SIZE)

        return (left, top)


# Main game class
class SnakeGame:
    def __init__(self):
        pg.init()

        # CONSTANTS
        self.BLOCK_SIZE = 20
        self.BLOCKS = 25                        # 25 blocks in each row and column
        self.__SCREEN_WIDTH = self.BLOCK_SIZE * self.BLOCKS
        self.__SCREEN_HEIGHT = self.BLOCK_SIZE * self.BLOCKS
        self.CAPTION = 'Snake Slither'
        self.FPS = 8
        self.BG_COLOR = 'black'
        self.FONT_NAME = 'consolas'
        self.FONT_SIZE = 28
        self.SCORE_DISPLAY_BLOCK = 10
        self.SCORE_X = self.SCORE_DISPLAY_BLOCK * self.BLOCK_SIZE
        self.SCORE_Y = 0
        self.TRANSPARENCY = 180


        # Defining welcome text
        self.WELCOME_TEXT = 'Press spacebar to start.'
        self.TEXT_COLOR = 'white'
        self.WELCOME_TEXT_X = self.__SCREEN_WIDTH//7
        self.WELCOME_TEXT_Y = self.__SCREEN_HEIGHT//2

        # Game Sounds
        self.sounds = {'hit': 'Sounds/hit.mp3', 'food': 'Sounds/food.mp3'}
        
        # GAME VARIABLES
        self.playing = False
        self.score = 0

        # Clock object
        self.clock = pg.time.Clock()

        # Defining font
        self.font = pg.font.SysFont(self.FONT_NAME, self.FONT_SIZE, True)

        # Creating game window and setting the caption
        self.SCREEN = pg.display.set_mode((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        pg.display.set_caption(self.CAPTION)

        # Rendering welcome text to image
        self.rendered_welcome_text = self.font.render(self.WELCOME_TEXT, True, self.TEXT_COLOR)

        # Snake object
        self.snake = Snake(self.SCREEN, self.BLOCK_SIZE, self.BLOCKS)

        # Food object
        self.food = Food(self.SCREEN, self.BLOCK_SIZE)


    def draw_grid(self):
        # Draw Grid
        for coordinate in range(self.BLOCK_SIZE, self.__SCREEN_WIDTH, self.BLOCK_SIZE):
                    
            # Drawing vertical lines
            pg.draw.line(self.SCREEN, self.TEXT_COLOR, (coordinate, 0), (coordinate, self.__SCREEN_HEIGHT))
                    
            # Drawing Horizontal lines
            pg.draw.line(self.SCREEN, self.TEXT_COLOR, (0, coordinate), (self.__SCREEN_WIDTH, coordinate))
    
    
    def reset_game(self):
        self.play_sound(self.sounds['hit'])
        self.snake.reset()
        self.food.update()                  # Move food to a new position
        self.score = 0

    
    def eat_food(self):
        if pg.Rect.colliderect(self.snake.head, self.food.food):
            self.play_sound(self.sounds['food'])
            self.score += 1
            self.food.update()
            self.snake.increase_length()
    

    def play_sound(self, filename: str):
        sound = pg.mixer.Sound(filename)
        sound.play()


    # Method to display the score on screen
    def display_score(self):
        score_text = f'Score: {self.score}'             # Text to display

        # Rendering score to image
        rendered_score = self.font.render(score_text, True, self.TEXT_COLOR)
        rendered_score.set_alpha(self.TRANSPARENCY)

        # Displaying the rendered score
        self.SCREEN.blit(rendered_score, (self.SCORE_X, self.SCORE_Y))

    
    def event_handler(self):
        
        # Event loop
        for event in pg.event.get():
            
            # Close the game
            if event.type == QUIT:
                pg.quit()
                exit()

            # Keyboard events
            elif event.type == KEYDOWN:

                # Start the game
                if event.key == K_SPACE:
                    self.playing = True

                # Move the snake according to the arrow keys
                if self.playing:
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    
                    elif event.key == K_UP:
                        self.snake.move_up()
                    
                    elif event.key == K_DOWN:
                        self.snake.move_down()


    def run(self):
        
        # Game loop
        while True:

            self.clock.tick(self.FPS)
            
            self.event_handler()

            self.SCREEN.fill(self.BG_COLOR)             # Refreshing the screen

            # Displaying the welcome text
            if not self.playing:
                self.SCREEN.blit(self.rendered_welcome_text, (self.WELCOME_TEXT_X, self.WELCOME_TEXT_Y))

            # Game started
            else:
                
                # Drawing the grid
                self.draw_grid()

                # Drawing the snake
                self.snake.draw()

                # Moving the snake
                self.snake.update()

                # Handling collision with the game window
                if (
                    self.snake.head.x not in range(0, self.__SCREEN_WIDTH) or 
                    self.snake.head.y not in range(0, self.__SCREEN_HEIGHT)
                    ):
                    self.reset_game()

                # Handling collision of snake's head with its body
                for block in self.snake.body[1:]:
                    if pg.Rect.collidepoint(self.snake.head, block.x, block.y):
                        self.reset_game()

                # Drawing the food
                self.food.draw()

                # Checking the collision with the food
                self.eat_food()

                # Display score
                self.display_score()
            
            
            pg.display.update()


if __name__ == '__main__':
    snake_game = SnakeGame()
    snake_game.run()