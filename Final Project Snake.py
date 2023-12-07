# Snake in Pygame
import pygame
import sys
import random

# Initializing Pygame
pygame.init()

# Game Window
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
random_color = (random.randrange(50,125), random.randrange(50,255), random.randrange(50,255))
off_white = (255, 255, 215)
red = (255, 0, 0)

# Snake
snake_size = 20
snake_speed = 15
snake = [(width // 2, height // 2)]
snake_direction = (1, 0)

# Food
food_size = 20
food = (random.randrange(0, width - food_size, food_size),
        random.randrange(0, height - food_size, food_size))

# Obstacles
obstacle_size = 20
obstacle_count = 10
obstacles = [(random.randrange(0, width - obstacle_size, obstacle_size),
               random.randrange(0, height - obstacle_size, obstacle_size))
              for _ in range(obstacle_count)]

# Scoreboard
global score
score = 0
font = pygame.font.SysFont(None, 30)

# Pause state
paused = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Controls: Up, Down, Left, Right, Pause
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)
            elif event.key == pygame.K_SPACE:
                paused = not paused  # Toggle the pause state

    if not paused:
        # Moving snake
        x, y = snake[0]
        x += snake_direction[0] * snake_size
        y += snake_direction[1] * snake_size
        snake.insert(0, (x, y))

        # Food Collisions
        if x == food[0] and y == food[1]:
            food = (random.randrange(0, width - food_size, food_size),
                    random.randrange(0, height - food_size, food_size))
            score += 1  # Increase the score when food is consumed
        else:
            snake.pop()

        # Side Wall Collisions
        if x < 0 or x >= width or y < 0 or y >= height:
            print(f"Game Over! Your Score: {score}")
            pygame.quit()
            sys.exit()

        # Self Collisions
        if len(snake) > 1 and (x, y) in snake[1:]:
            print(f"Game Over! Your Score: {score}")
            pygame.quit()
            sys.exit()

        # Obstacle Collisions
        for obstacle in obstacles:
                if (x, y) == obstacle:
                    print(f"Game Over! Your Score: {score}")
                    pygame.quit()
                    sys.exit()

    # Draw
    # Background
    win.fill(black)

    # Obstacles
    for obstacle in obstacles:
        pygame.draw.rect(win, random_color, (obstacle[0], obstacle[1], obstacle_size, obstacle_size))

    # Snake
    for segment in snake:
        pygame.draw.rect(win, white, (segment[0], segment[1], snake_size, snake_size))

    # Food
    pygame.draw.rect(win, red, (food[0], food[1], food_size, food_size))

    # Scoreboard
    score_text = font.render(f"Score: {score}", True, white)
    win.blit(score_text, (10, 10))

    # Pause text
    if paused:
        pause_text = font.render("Paused", True, white)
        win.blit(pause_text, (width // 2 - 30, height // 2))

    # Update the display
    pygame.display.flip()

    # Control the snake speed
    pygame.time.Clock().tick(snake_speed)
