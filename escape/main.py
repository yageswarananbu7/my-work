import pygame
import random
import time
import os

# --- Game Constants ---
WIDTH, HEIGHT = 800, 400
FPS = 60
PLAYER_SIZE = 50
OBSTACLE_WIDTHS = [30, 60, 120]
OBSTACLE_HEIGHT = 80
BOOM_SIZE = 40
GROUND = HEIGHT - PLAYER_SIZE
GRAVITY = 1
JUMP_POWER = -18

LEVELS = 200
LEVEL_TIME_LIMITS = [(5*60, 3), (6*60, 2), (8*60, 1)]

# --- High Score File ---
HIGH_SCORE_FILE = "highscore.txt"

# --- Initialize pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Endless Runner")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# --- Helper Functions ---
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def draw_stickman(x, y):

    pygame.draw.circle(screen, (0,0,0), (x+PLAYER_SIZE//2, y+15), 13)  # Head
    pygame.draw.line(screen, (0,0,0), (x+PLAYER_SIZE//2, y+28), (x+PLAYER_SIZE//2, y+PLAYER_SIZE-5), 4)  # Body
    pygame.draw.line(screen, (0,0,0), (x+PLAYER_SIZE//2, y+40), (x+PLAYER_SIZE//2-15, y+60), 3)  # Left arm
    pygame.draw.line(screen, (0,0,0), (x+PLAYER_SIZE//2, y+40), (x+PLAYER_SIZE//2+15, y+60), 3)  # Right arm
    pygame.draw.line(screen, (0,0,0), (x+PLAYER_SIZE//2, y+PLAYER_SIZE-5), (x+PLAYER_SIZE//2-10, y+PLAYER_SIZE+15), 3)  # Left leg
    pygame.draw.line(screen, (0,0,0), (x+PLAYER_SIZE//2, y+PLAYER_SIZE-5), (x+PLAYER_SIZE//2+10, y+PLAYER_SIZE+15), 3)  # Right leg

def draw_obstacle(obs):
    if obs['type'] == 'wall':
        pygame.draw.rect(screen, (139,69,19), obs['rect'])  # Brown wall
    elif obs['type'] == 'boom':
        pygame.draw.circle(screen, (255,0,0), obs['rect'].center, BOOM_SIZE//2)
        pygame.draw.line(screen, (255, 215, 0), obs['rect'].center, (obs['rect'].centerx, obs['rect'].centery-30), 4)

def get_star_reward(elapsed):
    for limit, stars in LEVEL_TIME_LIMITS:
        if elapsed <= limit:
            return stars
    return 1

def show_level_complete(level, stars, high_score):
    screen.fill((245,245,245))
    msg = font.render(f"Level {level} Complete!", True, (0,128,0))
    screen.blit(msg, (WIDTH//2-120, HEIGHT//2-80))
    star_msg = font.render(f"Stars: {'★'*stars}{'☆'*(3-stars)}", True, (255, 215, 0))
    screen.blit(star_msg, (WIDTH//2-70, HEIGHT//2-30))
    hs_msg = font.render(f"High Score: {high_score}", True, (0,0,0))
    screen.blit(hs_msg, (WIDTH//2-90, HEIGHT//2+20))
    pygame.display.flip()
    pygame.time.wait(2500)


def main():
    high_score = load_high_score()
    level = 1
    total_score = 0

    while level <= LEVELS:

        obstacle_speed = 7 + level // 10
        spawn_rate = max(30, 100 - level)
        obstacles = []
        player_x, player_y = 80, GROUND
        player_vel_y = 0
        is_jumping = False
        running = True
        score = 0
        spawn_timer = 0
        start_time = time.time()
        level_complete = False

        while running:
            clock.tick(FPS)
            screen.fill((245,245,245))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not is_jumping:
                player_vel_y = JUMP_POWER
                is_jumping = True


            player_vel_y += GRAVITY
            player_y += player_vel_y
            if player_y >= GROUND:
                player_y = GROUND
                is_jumping = False

            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)


            spawn_timer += 1
            if spawn_timer >= spawn_rate:
                kind = random.choice(['wall', 'boom', 'wall'])
                if kind == 'wall':
                    width = random.choice(OBSTACLE_WIDTHS)
                    rect = pygame.Rect(WIDTH, GROUND+PLAYER_SIZE-OBSTACLE_HEIGHT, width, OBSTACLE_HEIGHT)
                else:
                    rect = pygame.Rect(WIDTH, GROUND+PLAYER_SIZE-BOOM_SIZE, BOOM_SIZE, BOOM_SIZE)
                obstacles.append({'rect': rect, 'type': kind})
                spawn_timer = 0

            for obs in obstacles:
                obs['rect'].x -= obstacle_speed


            obstacles = [obs for obs in obstacles if obs['rect'].right > 0]


            draw_stickman(player_x, player_y)
            for obs in obstacles:
                draw_obstacle(obs)

            # Score
            score += 1
            elapsed = int(time.time() - start_time)
            score_text = font.render(f"Level: {level}  Score: {score}  Time: {elapsed//60}:{elapsed%60:02d}", True, (0,0,0))
            screen.blit(score_text, (10, 10))
            hs_text = font.render(f"High Score: {high_score}", True, (0,0,0))
            screen.blit(hs_text, (WIDTH-250, 10))

            # Collision detection
            for obs in obstacles:
                if player_rect.colliderect(obs['rect']):
                    running = False  # Game over
                    break


            if elapsed >= 30 + level//2:
                level_complete = True
                break

            pygame.display.flip()


        if level_complete:
            stars = get_star_reward(elapsed)
            total_score += score * stars
            if total_score > high_score:
                high_score = total_score
                save_high_score(high_score)
            show_level_complete(level, stars, high_score)
            level += 1
        else:

            screen.fill((255,255,255))
            over_msg = font.render("Game Over!", True, (255,0,0))
            screen.blit(over_msg, (WIDTH//2-80, HEIGHT//2-40))
            score_msg = font.render(f"Your Score: {total_score}", True, (0,0,0))
            screen.blit(score_msg, (WIDTH//2-80, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

    pygame.quit()

if __name__ == "__main__":
    main()
