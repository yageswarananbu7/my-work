import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Ball Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
ball_radius = 20
ball_x = 100
ball_y = HEIGHT - ball_radius - 10
ball_y_velocity = 0
gravity = 1
jump_power = -15

obstacle_width = 40
obstacle_height = 60
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 10
obstacle_velocity = 6

score = 0
font = pygame.font.Font(None, 36)

# Game loop control
clock = pygame.time.Clock()
running = True
game_over = False

# Main game loop
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE and ball_y == HEIGHT - ball_radius - 10:
                ball_y_velocity = jump_power

    if not game_over:
        # Ball physics
        ball_y_velocity += gravity
        ball_y += ball_y_velocity

        # Prevent the ball from falling below the ground
        if ball_y > HEIGHT - ball_radius - 10:
            ball_y = HEIGHT - ball_radius - 10
            ball_y_velocity = 0

        # Obstacle movement
        obstacle_x -= obstacle_velocity
        if obstacle_x < -obstacle_width:
            obstacle_x = WIDTH
            score += 1

        # Collision detection
        if obstacle_x < ball_x + ball_radius < obstacle_x + obstacle_width:
            if ball_y + ball_radius > obstacle_y:
                game_over = True

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.draw.rect(screen, BLACK, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            ball_y = HEIGHT - ball_radius - 10
            obstacle_x = WIDTH
            score = 0

    pygame.display.flip()

pygame.quit()

