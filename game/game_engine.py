import pygame
import numpy as np

from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
AUDIO_SR = 44100

def make_tone(freq_hz, duration_ms, volume=0.5, waveform="sine", decay=5.0):
    """Create a pygame Sound from a NumPy buffer; auto-match mono/stereo mixer."""
    # Ensure mixer is initialized; if not, default to stereo to match common defaults
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=AUDIO_SR, size=-16, channels=2)
    _, _, channels = pygame.mixer.get_init()

    t = np.linspace(0, duration_ms / 1000.0, int(AUDIO_SR * duration_ms / 1000.0), endpoint=False)
    if waveform == "sine":
        wave = np.sin(2 * np.pi * freq_hz * t)
    elif waveform == "square":
        wave = np.sign(np.sin(2 * np.pi * freq_hz * t))
    elif waveform == "noise":
        wave = np.random.uniform(-1.0, 1.0, size=t.shape)
    else:
        wave = np.sin(2 * np.pi * freq_hz * t)

    # Exponential decay to reduce clicks
    env = np.exp(-decay * t)
    wave = np.clip(wave * env * volume, -1.0, 1.0)

    # Convert to int16 mono
    mono = np.int16(wave * 32767)

    # Match mixer channels: 1D for mono, 2D (N,2) for stereo
    audio = mono if channels == 1 else np.column_stack((mono, mono))

    return pygame.sndarray.make_sound(audio)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)

        # Synthesize sounds (no files required)
        self.snd_paddle = make_tone(900, 80, volume=0.6, waveform="square")
        self.snd_wall   = make_tone(600, 60, volume=0.5, waveform="sine")
        self.snd_score  = make_tone(300, 200, volume=0.6, waveform="sine")

        # Inject sounds into Ball for paddle and wall bounces
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height,
                         paddle_snd=self.snd_paddle, wall_snd=self.snd_wall)

        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 64)

        self.game_over = False
        self.winner_text = ""
        self.game_over_time = None
        self.exit_requested = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.game_over:
            if event.key == pygame.K_3:
                self.set_series(3)
            elif event.key == pygame.K_5:
                self.set_series(5)
            elif event.key == pygame.K_7:
                self.set_series(7)
            elif event.key == pygame.K_ESCAPE:
                self.exit_requested = True

    def set_series(self, best_of):
        self.target_score = best_of // 2 + 1
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.game_over = False
        self.winner_text = ""
        self.game_over_time = None

    def check_game_over(self):
        if self.player_score >= self.target_score and not self.game_over:
            self.game_over = True
            self.winner_text = "Player Wins!"
            self.game_over_time = pygame.time.get_ticks()
            return True
        if self.ai_score >= self.target_score and not self.game_over:
            self.game_over = True
            self.winner_text = "AI Wins!"
            self.game_over_time = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.snd_score.play()
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.snd_score.play()
            self.ball.reset()

        self.check_game_over()
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        score_text = self.font.render(f"{self.player_score} - {self.ai_score}", True, WHITE)
        target_text = self.font.render(f"Target: {self.target_score}", True, WHITE)
        screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 20))
        screen.blit(target_text, (self.width//2 - target_text.get_width()//2, 50))

        if self.game_over:
            msg_surface = self.big_font.render(self.winner_text, True, WHITE)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height // 2 - 80))
            screen.blit(msg_surface, msg_rect)

            lines = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit",
            ]
            y = self.height // 2
            for line in lines:
                s = self.font.render(line, True, WHITE)
                r = s.get_rect(center=(self.width // 2, y))
                screen.blit(s, r)
                y += 40
