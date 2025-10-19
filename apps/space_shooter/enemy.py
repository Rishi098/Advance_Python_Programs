import pygame
import random
from config import *

class Enemy:
    """
    Represents an asteroid in the game.
    Asteroids rotate while falling and can collide with the player or bullets.
    """
    
    def __init__(self, assets):
        # Check if assets are valid
        if not assets or 'enemy_ship' not in assets:
            print("Warning: Invalid assets provided to Enemy constructor")
            # Create placeholder images
            placeholder = pygame.Surface((40, 40))
            placeholder.fill((0, 255, 0))  # Green square
            self.original_image = placeholder
            self.image = placeholder
        else:
            # Store the original image
            self.original_image = assets['enemy_ship']
            # Make a copy for initial use
            self.image = self.original_image.copy()
            
        self.rect = self.image.get_rect()
        
        # Position the asteroid at a random location at the top of the screen
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        
        # Movement attributes
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(1, 3)
        
        # Rotation for tumbling effect
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)
        if self.rotation_speed == 0:
            self.rotation_speed = 1
        
        # Sound effects
        self.explosion_sound = assets.get('explosion_sound', None)
    
    def update(self):
        """Update the asteroid position and rotation"""
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Randomly change horizontal direction occasionally
        if random.random() < 0.01:
            self.speed_x = random.randint(-2, 2)
        
        # Keep asteroid within screen bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x = -abs(self.speed_x)
        
        # Store the center position before rotation
        center = self.rect.center
        
        # Rotate the asteroid for tumbling effect
        self.angle = (self.angle + self.rotation_speed) % 360
        
        try:
            # Create a rotated copy of the original image
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Update the rectangle and maintain the center position
            self.rect = self.image.get_rect(center=center)
        except Exception as e:
            print(f"Error rotating asteroid: {e}")
            # If rotation fails, keep the original image
            self.image = self.original_image
            self.rect = self.image.get_rect(center=center)
    
    def draw(self, surface):
        """Draw the asteroid on the given surface"""
        # Make sure we have a valid image before drawing
        if self.image is not None and hasattr(self, 'rect'):
            surface.blit(self.image, self.rect)
        else:
            # Fallback to a red square if image is missing
            pygame.draw.rect(surface, RED, pygame.Rect(self.rect.x, self.rect.y, 50, 50))
