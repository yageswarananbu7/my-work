import pygame
import random

# Initialize Pygamewww
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human Fighting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS (frames per second)
FPS = 60
clock = pygame.time.Clock()

# Player class
class Player:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.velocity = 5
        self.jump_height = 10
        self.is_jumping = False
        self.jump_count = 10
        self.weapon = None
        self.is_fighting = False
        self.health = 100
        self.name = name
        self.facing_right = True

    # Draw the player
    def draw(self):
        # Draw body as a rectangle
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        if self.weapon:
            # Draw weapon depending on the type
            if self.weapon == "sword":
                pygame.draw.line(screen, BLACK, (self.x + self.width, self.y + self.height // 2), (self.x + self.width + 30, self.y + self.height // 2), 4)
            elif self.weapon == "gun":
                pygame.draw.line(screen, BLACK, (self.x + self.width, self.y + self.height // 2), (self.x + self.width + 50, self.y + self.height // 2), 4)
            elif self.weapon == "shield":
                pygame.draw.circle(screen, BLACK, (self.x - 20, self.y + self.height // 2), 20)

    # Handle movement
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
            self.facing_right = True
        if not self.is_jumping:
            if keys[pygame.K_UP]:
                self.is_jumping = True
        else:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

    # Handle fighting
    def fight(self, other_player):
        if abs(self.x - other_player.x) < 60:
            damage = random.randint(5, 15)
            other_player.health -= damage
            print(f"{self.name} attacks {other_player.name} for {damage} damage!")
        else:
            print(f"{self.name} missed!")

    # Pick up or drop weapons
    def handle_weapon(self, keys):
        if keys[pygame.K_SPACE]:
            if not self.weapon:
                self.weapon = random.choice(["sword", "gun", "shield"])
                print(f"{self.name} picked up a {self.weapon}!")
        if keys[pygame.K_LSHIFT]:
            if self.weapon:
                print(f"{self.name} dropped the {self.weapon}!")
                self.weapon = None

# Health bar
def draw_health_bar(player, x, y):
    pygame.draw.rect(screen, RED, (x, y, 100, 10))
    pygame.draw.rect(screen, GREEN, (x, y, player.health, 10))

# Game loop
def main():
    running = True

    # Create players
    player1 = Player(100, HEIGHT - 150, "Player 1")
    player2 = Player(WIDTH - 200, HEIGHT - 150, "Player 2 (AI)")

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        keys = pygame.key.get_pressed()
        player1.move(keys)

        # Fighting and weapon handling
        if keys[pygame.K_w]:
            player1.fight(player2)
        player1.handle_weapon(keys)

        # Simple AI behavior (moves toward the player and attacks)
        if player2.x > player1.x:
            player2.x -= player2.velocity
        elif player2.x < player1.x:
            player2.x += player2.velocity

        if random.random() < 0.02:  # Random AI attack
            player2.fight(player1)

        # Draw players
        player1.draw()
        player2.draw()

        # Draw health bars
        draw_health_bar(player1, 50, 50)
        draw_health_bar(player2, WIDTH - 150, 50)

        # Check for win/lose conditions
        if player1.health <= 0:
            print("AI wins!")
            running = False
        elif player2.health <= 0:
            print("Player 1 wins!")
            running = False

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
