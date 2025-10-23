import pygame
import random
from config import *

class PowerUp:
    """Power-up class for player enhancements"""
    
    TYPES = {
        'double': {
            'name': 'Double Shot',
            'color': PURPLE,
            'image_key': 'powerup_double',
            'duration': POWERUP_DURATION
        },
        'shield': {
            'name': 'Shield',
            'color': BLUE,
            'image_key': 'powerup_shield',
            'duration': POWERUP_DURATION
        },
        'speed': {
            'name': 'Speed Boost',
            'color': YELLOW,
            'image_key': 'powerup_speed',
            'duration': POWERUP_DURATION
        },
        'life': {
            'name': 'Extra Life',
            'color': RED,
            'image_key': 'powerup_life',
            'duration': 0  # Instant effect
        }
    }
    
    def __init__(self, x, y, powerup_type, assets):
        """Initialize a power-up at the given position"""
        self.type = powerup_type
        self.info = self.TYPES[powerup_type]
        
        # Load the appropriate image
        self.image = assets[self.info['image_key']]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Movement
        self.speed = POWERUP_FALL_SPEED
        
        # Sound
        self.sound = assets['powerup_sound']
    
    def update(self):
        """Update the power-up position"""
        self.rect.y += self.speed
        
        # Return True if the power-up is off the screen
        return self.rect.top > SCREEN_HEIGHT
    
    def apply(self, player):
        """Apply the power-up effect to the player"""
        self.sound.play()
        
        if self.type == 'double':
            player.double_shot = True
            player.powerup_end_times['double'] = pygame.time.get_ticks() + self.info['duration']
        
        elif self.type == 'shield':
            player.invincible = True
            player.powerup_end_times['shield'] = pygame.time.get_ticks() + self.info['duration']
        
        elif self.type == 'speed':
            player.speed = PLAYER_SPEED * 1.5
            player.powerup_end_times['speed'] = pygame.time.get_ticks() + self.info['duration']
        
        elif self.type == 'life':
            player.lives += 1
    
    def draw(self, surface):
        """Draw the power-up"""
        surface.blit(self.image, self.rect)

def spawn_random_powerup(x, y, assets):
    """Spawn a random power-up at the given position with the given chance"""
    if random.random() < POWERUP_SPAWN_CHANCE:
        powerup_type = random.choice(list(PowerUp.TYPES.keys()))
        return PowerUp(x, y, powerup_type, assets)
    return None
