import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = 15
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20  # Standard height for obstacles
WIDE_OBSTACLE_WIDTH = 40
TALL_OBSTACLE_HEIGHT = 40
SPEED = 3  # Speed for obstacles
GROUND_HEIGHT = HEIGHT - 70  # Ground height
MIN_SPAWN_DISTANCE = 150  # Minimum distance between obstacles
MAX_SPAWN_DISTANCE = 300  # Maximum distance between obstacles

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, GROUND_HEIGHT - 50, 10, 50)  # Vertical line dimensions
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Ground collision
        if self.rect.y >= GROUND_HEIGHT - self.rect.height:
            self.rect.y = GROUND_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0

    def draw(self, screen):
        # Draw vertical line player
        pygame.draw.line(screen, GREEN, (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 5)


# Base Obstacle class
class Obstacle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, GROUND_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    def update(self):
        self.rect.x -= SPEED


# Wide Obstacle class
class WideObstacle(Obstacle):
    def __init__(self, x):
        super().__init__(x)
        self.rect.width = WIDE_OBSTACLE_WIDTH
        self.rect.height = OBSTACLE_HEIGHT


# Tall Obstacle class
class TallObstacle(Obstacle):
    def __init__(self, x):
        super().__init__(x)
        self.rect.width = OBSTACLE_WIDTH
        self.rect.height = TALL_OBSTACLE_HEIGHT
        self.rect.y = GROUND_HEIGHT - TALL_OBSTACLE_HEIGHT  # Set position for tall obstacle


# Function to display game over message and handle restart
def display_game_over(screen, score):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render('Game Over!', True, RED)
    score_text = font.render(f'Score: {score}', True, BLACK)
    restart_text = font.render('Press R to Restart', True, BLACK)

    screen.fill(WHITE)  # Clear the screen
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False  # Exit the waiting loop


# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Endless Runner")
    clock = pygame.time.Clock()

    player = Player()
    obstacles = []
    score = 0
    spawn_timer = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    player.jump()

        if not game_over:
            # Update player
            player.update()

            # Spawn obstacles
            spawn_timer += 1
            if spawn_timer > random.randint(MIN_SPAWN_DISTANCE, MAX_SPAWN_DISTANCE):  # Random spacing
                obstacle_type = random.choice([Obstacle, WideObstacle, TallObstacle])
                obstacles.append(obstacle_type(WIDTH))
                spawn_timer = 0

            # Update obstacles
            for obstacle in obstacles:
                obstacle.update()

            # Remove off-screen obstacles
            obstacles = [o for o in obstacles if o.rect.x > -max(OBSTACLE_WIDTH, WIDE_OBSTACLE_WIDTH)]

            # Check for collisions
            for obstacle in obstacles:
                if player.rect.colliderect(obstacle.rect):
                    game_over = True
                    break  # Exit the loop if game over

            # Score increase
            score += 1

            # Drawing
            screen.fill(WHITE)
            player.draw(screen)  # Draw the vertical line player
            for obstacle in obstacles:
                pygame.draw.rect(screen, RED, obstacle.rect)

            # Draw the ground line
            pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 5)

            # Display score
            font = pygame.font.SysFont(None, 36)
            text = font.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)
        else:
            display_game_over(screen, score)  # Show game over message
            # Reset game state
            player = Player()
            obstacles = []
            score = 0
            spawn_timer = 0
            game_over = False


if __name__ == "__main__":
    main()
