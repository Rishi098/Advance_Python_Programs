import pygame
from bullet import Bullet
from config import *

class Player:
    def __init__(self, assets):
        if not assets or 'player_ship' not in assets:
            print("Warning: Invalid assets provided to Player constructor")
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 0))  
            self.image = placeholder
        else:
            self.image = assets['player_ship']
            
        self.rect = self.image.get_rect()
        
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        
        self.speed = PLAYER_SPEED
        self.dx = 0
        self.dy = 0
        
        # Shooting attributes
        self.last_shot = 0
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.bullets = []
        
        # Player stats
        self.lives = PLAYER_LIVES
        self.score = 0
        
        # Power-up states
        self.double_shot = False
        self.invincible = False
        self.powerup_end_times = {
            'double': 0,
            'shield': 0,
            'speed': 0
        }
        
        # Dictionary to track active powerups for UI
        self.active_powerups = {}
        
        # Invincibility after hit
        self.hit_invincibility_end = 0
        
        # Animation
        self.explosion_anim = assets.get('explosion_anim', [])
        self.exploding = False
        self.explosion_frame = 0
        
        # Sound effects
        self.shoot_sound = assets.get('shoot_sound', None)
        self.explosion_sound = assets.get('explosion_sound', None)
        
        # Energy Blast mechanic
        self.energy = 0
        self.max_energy = ENERGY_MAX
        self.is_blasting = False
        self.blast_frame = 0
        self.blast_max_frames = ENERGY_BLAST_DURATION
        self.blast_radius = ENERGY_BLAST_RADIUS
        self.screen_shake = 0
        
        # Energy Blast mechanic
        self.energy = 0
        self.max_energy = ENERGY_MAX
        self.is_blasting = False
        self.blast_frame = 0
        self.blast_max_frames = ENERGY_BLAST_DURATION
        self.blast_radius = ENERGY_BLAST_RADIUS
        self.screen_shake = 0
    
    def handle_input(self, event):
        # Key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.dx = -self.speed
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.dx = self.speed
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.dy = -self.speed
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.dy = self.speed
            # We'll handle shooting in the main game loop with get_pressed()
        
        # Key release events
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.dx < 0:
                self.dx = 0
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.dx > 0:
                self.dx = 0
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.dy < 0:
                self.dy = 0
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.dy > 0:
                self.dy = 0
    
    def update(self):
        # Check for power-up expirations
        current_time = pygame.time.get_ticks()
        
        if self.double_shot and current_time > self.powerup_end_times['double']:
            self.double_shot = False
        
        if self.invincible and current_time > self.powerup_end_times['shield'] and current_time > self.hit_invincibility_end:
            self.invincible = False
        
        if self.speed > PLAYER_SPEED and current_time > self.powerup_end_times['speed']:
            self.speed = PLAYER_SPEED
        
        # Update active_powerups dictionary for UI
        self.active_powerups = {}
        if self.double_shot:
            self.active_powerups['Double Shot'] = self.powerup_end_times['double'] - current_time
        if self.invincible:
            if current_time <= self.powerup_end_times['shield']:
                self.active_powerups['Shield'] = self.powerup_end_times['shield'] - current_time
            elif current_time <= self.hit_invincibility_end:
                self.active_powerups['Invincibility'] = self.hit_invincibility_end - current_time
        if self.speed > PLAYER_SPEED:
            self.active_powerups['Speed Boost'] = self.powerup_end_times['speed'] - current_time
        
        # Update position
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def shoot(self):
        """
        Attempt to fire a bullet. Returns a list of bullets fired or an empty list if on cooldown.
        """
        # Check if enough time has passed since the last shot
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            bullets_fired = []
            
            if self.double_shot:
                # Create two bullets side by side
                bullet1 = Bullet(self.rect.left + 10, self.rect.top, -1)
                bullet2 = Bullet(self.rect.right - 10, self.rect.top, -1)
                bullets_fired.extend([bullet1, bullet2])
            else:
                # Create a single bullet at the player's position
                bullet = Bullet(self.rect.centerx, self.rect.top, -1)
                bullets_fired.append(bullet)
            
            # Play shoot sound if available
            if self.shoot_sound:
                self.shoot_sound.play()
            
            return bullets_fired
        
        return []
    
    def hit(self):
        """Handle player being hit by an enemy"""
        if not self.invincible:
            self.lives -= 1
            if self.explosion_sound:
                self.explosion_sound.play()
            
            # Temporary invincibility after being hit
            self.invincible = True
            self.hit_invincibility_end = pygame.time.get_ticks() + INVINCIBILITY_DURATION
            
            return True
        return False
    
    def is_dead(self):
        """Check if the player is dead (no lives left)"""
        return self.lives <= 0
    
    def draw(self, surface):
        # If invincible, make the player blink
        if self.invincible:
            if pygame.time.get_ticks() % 200 < 100:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        # Draw shield effect if active
        if self.invincible and pygame.time.get_ticks() <= self.powerup_end_times['shield']:
            pygame.draw.circle(surface, BLUE, self.rect.center, self.rect.width // 2 + 5, 2)
    
    # Energy Blast mechanic methods
    def add_energy(self, amount=1):
        """Add energy to the player's energy meter"""
        self.energy = min(self.energy + amount, self.max_energy)
        return self.energy >= self.max_energy
    
    def trigger_blast(self):
        """Trigger the energy blast if enough energy is available"""
        if self.energy >= self.max_energy and not self.is_blasting:
            self.is_blasting = True
            self.blast_frame = 0
            self.energy = 0
            self.screen_shake = 10
            # Play blast sound if available
            if self.explosion_sound:
                self.explosion_sound.play()
            return True
        return False
    
    def update_blast(self, enemies):
        """Update the energy blast animation and check for collisions"""
        if not self.is_blasting:
            return 0
        
        self.blast_frame += 1
        current_radius = (self.blast_frame / self.blast_max_frames) * self.blast_radius
        
        # Check for enemy collisions with the blast
        enemies_destroyed = 0
        for enemy in enemies[:]:
            distance = ((enemy.rect.centerx - self.rect.centerx) ** 2 + 
                       (enemy.rect.centery - self.rect.centery) ** 2) ** 0.5
            if distance <= current_radius:
                enemies.remove(enemy)
                enemies_destroyed += 1
        
        # End blast animation when complete
        if self.blast_frame >= self.blast_max_frames:
            self.is_blasting = False
        
        return enemies_destroyed
    
    def draw_blast(self, surface):
        """Draw the energy blast effect"""
        if not self.is_blasting:
            return
        
        current_radius = (self.blast_frame / self.blast_max_frames) * self.blast_radius
        alpha = 255 - int((self.blast_frame / self.blast_max_frames) * 200)
        
        # Create a surface for the blast with transparency
        blast_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(blast_surface, (200, 230, 255, alpha), 
                         (current_radius, current_radius), current_radius)
        
        # Draw the blast centered on the player
        surface.blit(blast_surface, 
                   (self.rect.centerx - current_radius, self.rect.centery - current_radius))
    # Energy Blast mechanic methods
    def add_energy(self, amount=1):
        """Add energy to the player's energy meter"""
        self.energy = min(self.energy + amount, self.max_energy)
        return self.energy >= self.max_energy
    
    def trigger_blast(self):
        """Trigger the energy blast if enough energy is available"""
        if self.energy >= self.max_energy and not self.is_blasting:
            self.is_blasting = True
            self.blast_frame = 0
            self.energy = 0
            self.screen_shake = 10
            # Play blast sound if available
            if self.explosion_sound:
                self.explosion_sound.play()
            return True
        return False
    
    def update_blast(self, enemies):
        """Update the energy blast animation and check for collisions"""
        if not self.is_blasting:
            return 0
        
        self.blast_frame += 1
        current_radius = (self.blast_frame / self.blast_max_frames) * self.blast_radius
        
        # Check for enemy collisions with the blast
        enemies_destroyed = 0
        for enemy in enemies[:]:
            distance = ((enemy.rect.centerx - self.rect.centerx) ** 2 + 
                       (enemy.rect.centery - self.rect.centery) ** 2) ** 0.5
            if distance <= current_radius:
                enemies.remove(enemy)
                enemies_destroyed += 1
        
        # End blast animation when complete
        if self.blast_frame >= self.blast_max_frames:
            self.is_blasting = False
        
        return enemies_destroyed
    
    def draw_blast(self, surface):
        """Draw the energy blast effect"""
        if not self.is_blasting:
            return
        
        current_radius = (self.blast_frame / self.blast_max_frames) * self.blast_radius
        alpha = 255 - int((self.blast_frame / self.blast_max_frames) * 200)
        
        # Create a surface for the blast with transparency
        blast_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(blast_surface, (200, 230, 255, alpha), 
                         (current_radius, current_radius), current_radius)
        
        # Draw the blast centered on the player
        surface.blit(blast_surface, 
                   (self.rect.centerx - current_radius, self.rect.centery - current_radius))
