import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, paddle_snd=None, wall_snd=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Sound references (injected by GameEngine)
        self.paddle_snd = paddle_snd
        self.wall_snd = wall_snd

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.wall_snd:
                self.wall_snd.play()

    def check_collision(self, player, ai):
        b = self.rect()
        pr = player.rect()
        ar = ai.rect()

        # Left paddle (player)
        if b.colliderect(pr):
            # Snap to paddle face then reflect to the right
            self.x = pr.right
            self.velocity_x = abs(self.velocity_x)
            if self.paddle_snd:
                self.paddle_snd.play()

        # Right paddle (AI)
        elif b.colliderect(ar):
            # Snap to paddle face then reflect to the left
            self.x = ar.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            if self.paddle_snd:
                self.paddle_snd.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        # Flip serve direction for variety
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
