import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 30
        self.height = 30
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.width // 2)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y - 5)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)


# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.gap = 150
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom_y = self.top_height + self.gap
        self.speed = 5
        self.scored = False

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y))

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.top_height)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)


# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_counter = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.jump()
        return True

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        # Check if bird is out of bounds
        if self.bird.y < 0 or self.bird.y > SCREEN_HEIGHT:
            self.game_over = True
            return

        # Add pipes
        self.pipe_counter += 1
        if self.pipe_counter > 90:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_counter = 0

        # Update pipes
        for pipe in self.pipes:
            pipe.update()

        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # Check collisions
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                self.game_over = True
                return

            # Score point
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

    def draw(self):
        self.screen.fill(BLUE)

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw bird
        self.bird.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = pygame.font.Font(None, 24).render("Press SPACE to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# Main
if __name__ == "__main__":
    game = Game()
    game.run()
