import pygame
from config import *

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(0, 0, 5, 10)
        self.rect.centerx = x
        self.rect.centery = y
        
        # Direction: -1 for up (player bullet), 1 for down (enemy bullet)
        self.direction = direction
        self.speed = BULLET_SPEED
        
        # Bullet color
        self.color = BLUE if direction < 0 else RED
    
    def update(self):
        # Move the bullet
        self.rect.y += self.direction * self.speed
    
    def is_off_screen(self):
        # Check if the bullet has gone off the screen
        return self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT
    
    def check_collision(self, sprite):
        # Check if the bullet has collided with another sprite
        return self.rect.colliderect(sprite.rect)
    
    def draw(self, surface):
        # Draw the bullet
        pygame.draw.rect(surface, self.color, self.rect)
