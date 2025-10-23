import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, font, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.action = action
        self.is_hovered = False
        self.normal_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.text_color = WHITE
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        # Update rect in case position or size changed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return self.action
        return None
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw button border
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
    
    def update(self, health):
        self.current_health = health
    
    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        
        # Calculate health width
        health_width = int(self.width * (self.current_health / self.max_health))
        
        # Draw health
        if self.current_health > 0:
            # Color changes based on health percentage
            if self.current_health / self.max_health > 0.7:
                color = GREEN
            elif self.current_health / self.max_health > 0.3:
                color = YELLOW
            else:
                color = RED
            
            pygame.draw.rect(surface, color, (self.x, self.y, health_width, self.height))
        
        # Draw border
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Draw text
        font = pygame.font.Font(None, 20)
        text = font.render(f"Health: {self.current_health}/{self.max_health}", True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)

class ScoreDisplay:
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.score = 0
        self.display_score = 0
        self.last_update_time = 0
    
    def update(self, score):
        self.score = score
    
    def reset(self):
        """Force immediate update of displayed score"""
        self.display_score = self.score
    
    def draw(self, surface):
        # Animate score counting up/down
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 50:  # Update every 50ms
            self.last_update_time = current_time
            
            if self.display_score < self.score:
                self.display_score += max(1, (self.score - self.display_score) // 10)
            elif self.display_score > self.score:
                self.display_score -= max(1, (self.display_score - self.score) // 10)
        
        # Format score with commas for better readability
        formatted_score = f"{self.display_score:,}"
        
        # Draw score
        text = self.font.render(f"Score: {formatted_score}", True, WHITE)
        surface.blit(text, (self.x, self.y))

class LivesDisplay:
    def __init__(self, x, y, font, ship_image):
        self.x = x
        self.y = y
        self.font = font
        self.lives = 3
        self.ship_image = ship_image
        
        # Scale down the ship image for the lives display
        self.scaled_ship = pygame.transform.scale(self.ship_image, (20, 20))
    
    def update(self, lives):
        self.lives = lives
    
    def draw(self, surface):
        # Draw text
        text = self.font.render("Lives:", True, WHITE)
        surface.blit(text, (self.x, self.y))
        
        # Draw ship icons
        for i in range(self.lives):
            surface.blit(self.scaled_ship, (self.x + 60 + i * 25, self.y))

class PowerupIndicator:
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.active_powerups = {}
    
    def update(self, player):
        self.active_powerups = player.active_powerups
    
    def draw(self, surface):
        if not self.active_powerups:
            return
        
        # Draw header
        text = self.font.render("Active Power-ups:", True, WHITE)
        surface.blit(text, (self.x, self.y))
        
        # Draw each active powerup
        y_offset = 25
        for powerup_type, end_time in self.active_powerups.items():
            remaining = max(0, (end_time - pygame.time.get_ticks()) // 1000)
            
            if powerup_type == "double_shot":
                color = PURPLE
                name = "Double Shot"
            elif powerup_type == "shield":
                color = BLUE
                name = "Shield"
            elif powerup_type == "speed":
                color = YELLOW
                name = "Speed Boost"
            else:
                color = WHITE
                name = powerup_type.capitalize()
            
            # Draw powerup indicator
            pygame.draw.rect(surface, color, (self.x, self.y + y_offset, 10, 10))
            
            # Draw powerup name and timer
            text = self.font.render(f"{name}: {remaining}s", True, color)
            surface.blit(text, (self.x + 15, self.y + y_offset - 2))
            
            y_offset += 20

class EnergyBar:
    def __init__(self, x, y, width, height, max_energy):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_energy = max_energy
        self.current_energy = 0
        self.is_charged = False
        self.pulse_value = 0
        self.pulse_direction = 1
    
    def reset(self):
        """Reset energy bar after blast"""
        self.current_energy = 0
        self.is_charged = False
    
    def update(self):
        # Pulse effect when fully charged
        if self.is_charged:
            self.pulse_value += 0.1 * self.pulse_direction
            if self.pulse_value >= 1.0:
                self.pulse_direction = -1
            elif self.pulse_value <= 0.0:
                self.pulse_direction = 1
    
    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        
        # Calculate energy width
        energy_width = int(self.width * (self.current_energy / self.max_energy))
        
        # Draw energy
        if self.current_energy > 0:
            if self.is_charged:
                # Pulsing cyan when fully charged
                pulse_color = (0, 
                              int(128 + 127 * self.pulse_value), 
                              int(192 + 63 * self.pulse_value))
                color = pulse_color
            else:
                # Gradient from blue to cyan based on charge level
                blue_component = int(128 + (self.current_energy / self.max_energy) * 127)
                color = (0, blue_component, 255)
            
            pygame.draw.rect(surface, color, (self.x, self.y, energy_width, self.height))
        
        # Draw border
        border_color = (0, 255, 255) if self.is_charged else WHITE
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), 2)
        
        # Draw text
        font = pygame.font.Font(None, 20)
        if self.is_charged:
            text = font.render("ENERGY BLAST READY! (X)", True, (0, 255, 255))
        else:
            text = font.render(f"Energy: {self.current_energy}/{self.max_energy}", True, WHITE)
        
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)
