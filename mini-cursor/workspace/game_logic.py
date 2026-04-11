import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.food = self.generate_food()

    def generate_food(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'

        head = self.snake[-1]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])

        self.snake.append(new_head)
        if self.snake[-1] == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop(0)

        if (self.snake[-1][0] < 0 or self.snake[-1][0] >= WIDTH or
            self.snake[-1][1] < 0 or self.snake[-1][1] >= HEIGHT or
            self.snake[-1] in self.snake[:-1]):
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.fill(WHITE)
        for x, y in self.snake:
            pygame.draw.rect(self.screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (*self.food, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

def main():
    game = SnakeGame()
    while True:
        game.update()
        game.draw()
        game.clock.tick(FPS)

if __name__ == '__main__':
    main()