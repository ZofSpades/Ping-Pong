import pygame
from game.game_engine import GameEngine

# Initialize audio first (stereo 16-bit at 44.1kHz)
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

        if engine.exit_requested:
            pygame.time.delay(800)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
