#!/usr/bin/env python3
import pygame
import sys
import os
import random
import json
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp, spawn_random_powerup
from ui import Button, HealthBar, ScoreDisplay, LivesDisplay, PowerupIndicator, EnergyBar
from config import *
from utils import load_assets, check_collisions, create_floating_text, update_floating_texts, draw_floating_texts

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Astro Space Game")
        
        # Set up the game window
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Store original window size for toggling fullscreen
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Load assets
        self.assets = load_assets()
        
        # Load high score first
        self.high_score = self.load_high_score()
        
        # Store final score separately
        self.final_score = 0
        
        # Game state
        self.state = STATE_SPLASH
        self.splash_start_time = pygame.time.get_ticks()
        
        # Initialize UI elements first so they exist when reset_game is called
        self.init_ui()
        
        # Initialize game objects
        self.reset_game()
        
        # Background scrolling
        self.bg_y = 0
        
        # Floating text effects
        self.floating_texts = []
        
        # Screen shake effect
        self.screen_shake_offset = (0, 0)
        
        # Fullscreen confirmation dialog
        self.show_fullscreen_dialog = False
        self.dialog_result = None
        
        # Load display preferences if enabled
        if SAVE_DISPLAY_PREFERENCES:
            try:
                self.load_display_preferences()
            except Exception as e:
                print(f"Error loading display preferences: {e}")
        
        # Start background music
        if 'background_music' in self.assets and self.assets['background_music']:
            try:
                pygame.mixer.music.load(self.assets['background_music'])
                pygame.mixer.music.play(-1)  # Loop indefinitely
            except pygame.error as e:
                print(f"Error playing background music: {e}")
                # Continue without music if there's an error
    
    def toggle_fullscreen(self, save_preference=True):
        """Toggle between fullscreen and windowed mode with smooth transition"""
        self.fullscreen = not self.fullscreen
        
        # Create a fade out effect
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, 0))
        
        # Fade out
        for alpha in range(0, 128, 8):
            fade_surface.fill((0, 0, 0, alpha))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)
        
        # Get current display info for better fullscreen handling
        display_info = pygame.display.Info()
        
        if self.fullscreen:
            # Save current window size before going fullscreen
            self.window_size = self.screen.get_size()
            # Switch to fullscreen mode using native display resolution
            self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
            print(f"Switched to fullscreen: {display_info.current_w}x{display_info.current_h}")
        else:
            # Return to windowed mode with previous size
            self.screen = pygame.display.set_mode(self.window_size)
            print(f"Switched to windowed mode: {self.window_size[0]}x{self.window_size[1]}")
        
        # Recalculate UI positions based on new screen size
        self.adjust_ui_for_screen()
        
        # Save user preference if enabled
        if save_preference and SAVE_DISPLAY_PREFERENCES:
            self.save_display_preferences()
        
        # Fade back in
        for alpha in range(128, 0, -8):
            # Redraw the current screen content
            self.render()
            # Apply fade
            fade_surface.fill((0, 0, 0, alpha))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)
    
    def reset_game(self):
        """Reset the game state for a new game"""
        print("Resetting game...")
        
        # Create player
        self.player = Player(self.assets)
        print(f"Player created with {self.player.lives} lives")
        
        # Reset score
        self.player.score = 0
        
        # Create lists for game objects
        self.enemies = []
        self.bullets = []
        self.powerups = []
        
        # Reset floating texts
        self.floating_texts = []
        
        # Reset screen shake
        self.screen_shake_offset = (0, 0)
        
        # Reset UI elements
        self.health_bar.update(self.player.lives)
        self.score_display.update(0)  # Explicitly set to 0
        self.score_display.reset()    # Force immediate update
        self.lives_display.update(self.player.lives)
        self.energy_bar.current_energy = 0
        self.energy_bar.is_charged = False
        
        print(f"Lives display updated with {self.player.lives} lives")
        print(f"Score reset to {self.player.score}")
        
        # Spawn initial enemies
        for _ in range(5):
            self.spawn_enemy()
    
    def spawn_enemy(self):
        """Spawn a new enemy at a random position"""
        try:
            if len(self.enemies) < MAX_ENEMIES:
                enemy = Enemy(self.assets)
                self.enemies.append(enemy)
        except Exception as e:
            print(f"Error spawning enemy: {e}")
    
    def init_ui(self):
        """Initialize UI elements"""
        # Fonts
        self.main_font = self.assets['main_font']
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # UI elements
        self.health_bar = HealthBar(SCREEN_WIDTH - 150, 20, 130, 20, PLAYER_LIVES)
        self.score_display = ScoreDisplay(20, 20, self.main_font)
        self.lives_display = LivesDisplay(20, 60, self.small_font, self.assets['player_ship'])
        self.powerup_indicator = PowerupIndicator(SCREEN_WIDTH - 200, 50, self.small_font)
        self.energy_bar = EnergyBar(20, 100, 150, 20, ENERGY_MAX)
        
        # Menu buttons
        button_width, button_height = 200, 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.menu_buttons = [
            Button(center_x, 200, button_width, button_height, "Start Game", self.main_font, STATE_GAMEPLAY),
            Button(center_x, 270, button_width, button_height, "Best Score", self.main_font, STATE_BEST_SCORE),
            Button(center_x, 340, button_width, button_height, "Instruction", self.main_font, STATE_INSTRUCTIONS),
            Button(center_x, 410, button_width, button_height, "Settings", self.main_font, STATE_SETTINGS),
            Button(center_x, 480, button_width, button_height, "Quit", self.main_font, "quit")
        ]
        
        # Pause buttons
        self.pause_buttons = [
            Button(center_x, 250, button_width, button_height, "Resume", self.main_font, STATE_GAMEPLAY),
            Button(center_x, 320, button_width, button_height, "Main Menu", self.main_font, STATE_MENU),
            Button(center_x, 390, button_width, button_height, "Quit", self.main_font, "quit")
        ]
        
        # Game over buttons
        self.game_over_buttons = [
            Button(center_x, 350, button_width, button_height, "Try Again", self.main_font, "retry"),
            Button(center_x, 420, button_width, button_height, "Main Menu", self.main_font, STATE_MENU)
        ]
        
        # Settings buttons
        self.settings_buttons = [
            Button(center_x, 350, button_width, button_height, "Back", self.main_font, STATE_MENU)
        ]
        
        # Fullscreen toggle button for settings
        fullscreen_text = "Switch to Windowed Mode" if self.fullscreen else "Switch to Fullscreen Mode"
        self.settings_fullscreen_button = Button(
            center_x, 280, button_width, button_height, 
            fullscreen_text, self.small_font, "toggle_fullscreen"
        )
        
        # Best score buttons
        self.best_score_buttons = [
            Button(center_x, 350, button_width, button_height, "Back", self.main_font, STATE_MENU)
        ]
        
        # Instructions buttons
        self.instructions_buttons = [
            Button(center_x, 500, button_width, button_height, "Back", self.main_font, STATE_MENU)
        ]
    
    def adjust_ui_for_screen(self):
        """Adjust UI elements based on current screen size"""
        # Get current screen dimensions
        screen_width, screen_height = self.screen.get_size()
        
        # Calculate scale factors compared to original design
        scale_x = screen_width / SCREEN_WIDTH
        scale_y = screen_height / SCREEN_HEIGHT
        
        # Recalculate UI positions
        # Health bar
        if hasattr(self, 'health_bar'):
            self.health_bar.x = int(screen_width - 150 * scale_x)
            self.health_bar.y = int(20 * scale_y)
            self.health_bar.width = int(130 * scale_x)
            self.health_bar.height = int(20 * scale_y)
        
        # Score display
        if hasattr(self, 'score_display'):
            self.score_display.x = int(20 * scale_x)
            self.score_display.y = int(20 * scale_y)
        
        # Lives display
        if hasattr(self, 'lives_display'):
            self.lives_display.x = int(20 * scale_x)
            self.lives_display.y = int(60 * scale_y)
        
        # Powerup indicator
        if hasattr(self, 'powerup_indicator'):
            self.powerup_indicator.x = int(screen_width - 200 * scale_x)
            self.powerup_indicator.y = int(50 * scale_y)
        
        # Energy bar
        if hasattr(self, 'energy_bar'):
            self.energy_bar.x = int(20 * scale_x)
            self.energy_bar.y = int(100 * scale_y)
            self.energy_bar.width = int(150 * scale_x)
            self.energy_bar.height = int(20 * scale_y)
        
        # Menu buttons
        button_width, button_height = int(200 * scale_x), int(50 * scale_y)
        center_x = screen_width // 2 - button_width // 2
        
        # Update menu buttons
        if hasattr(self, 'menu_buttons'):
            positions = [200, 270, 340, 410, 480]
            for i, button in enumerate(self.menu_buttons):
                button.x = center_x
                button.y = int(positions[i] * scale_y)
                button.width = button_width
                button.height = button_height
        
        # Update fullscreen button
        if hasattr(self, 'fullscreen_button'):
            self.fullscreen_button.x = center_x
            self.fullscreen_button.y = int(550 * scale_y)
            self.fullscreen_button.width = button_width
            self.fullscreen_button.height = button_height
        
        # Update pause buttons
        if hasattr(self, 'pause_buttons'):
            positions = [250, 320, 390]
            for i, button in enumerate(self.pause_buttons):
                button.x = center_x
                button.y = int(positions[i] * scale_y)
                button.width = button_width
                button.height = button_height
        
        # Update game over buttons
        if hasattr(self, 'game_over_buttons'):
            positions = [350, 420]
            for i, button in enumerate(self.game_over_buttons):
                button.x = center_x
                button.y = int(positions[i] * scale_y)
                button.width = button_width
                button.height = button_height
        
        # Update settings buttons
        if hasattr(self, 'settings_buttons'):
            for button in self.settings_buttons:
                button.x = center_x
                button.y = int(350 * scale_y)
                button.width = button_width
                button.height = button_height
        
        # Update settings fullscreen button
        if hasattr(self, 'settings_fullscreen_button'):
            self.settings_fullscreen_button.x = center_x
            self.settings_fullscreen_button.y = int(280 * scale_y)
            self.settings_fullscreen_button.width = button_width
            self.settings_fullscreen_button.height = button_height
        
        # Update best score buttons
        if hasattr(self, 'best_score_buttons'):
            for button in self.best_score_buttons:
                button.x = center_x
                button.y = int(350 * scale_y)
                button.width = button_width
                button.height = button_height
        
        # Update instructions buttons
        if hasattr(self, 'instructions_buttons'):
            for button in self.instructions_buttons:
                button.x = center_x
                button.y = int(500 * scale_y)
                button.width = button_width
                button.height = button_height
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_GAMEPLAY:
                        self.state = STATE_PAUSE
                    elif self.state == STATE_PAUSE:
                        self.state = STATE_GAMEPLAY
                
                if event.key == pygame.K_p and self.state == STATE_GAMEPLAY:
                    self.state = STATE_PAUSE
                
                if event.key == pygame.K_m:
                    # Toggle music
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                
                # Toggle fullscreen with F1 key
                if event.key == pygame.K_F1:
                    # Show confirmation dialog
                    new_mode = "windowed" if self.fullscreen else "fullscreen"
                    self.show_confirmation_dialog(
                        f"Switch to {new_mode} mode?",
                        lambda: self.toggle_fullscreen(True),
                        None
                    )
                
                # Energy Blast trigger with X key
                if event.key == pygame.K_x and self.state == STATE_GAMEPLAY:
                    if self.player.trigger_blast():
                        # Apply screen flash effect
                        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        flash.fill((255, 255, 255, 100))  # Semi-transparent white
                        self.screen.blit(flash, (0, 0))
                        # Reset energy bar UI
                        self.energy_bar.reset()
            
            # Handle player input in gameplay state
            if self.state == STATE_GAMEPLAY:
                self.player.handle_input(event)
            
            # Handle button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == STATE_MENU:
                for button in self.menu_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "quit":
                            self.quit_game()
                        elif action == STATE_GAMEPLAY:
                            # Reset the game before starting gameplay from the menu
                            self.reset_game()
                            self.state = action
                        else:
                            self.state = action
            
            elif self.state == STATE_PAUSE:
                for button in self.pause_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "quit":
                            self.quit_game()
                        elif action == STATE_MENU:
                            # Reset game when going back to menu
                            self.reset_game()
                            self.state = action
                        else:
                            self.state = action
            
            elif self.state == STATE_GAME_OVER:
                for button in self.game_over_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "retry":
                            self.reset_game()
                            self.state = STATE_GAMEPLAY
                        elif action == STATE_MENU:
                            # Make sure we reset the game when going back to menu
                            self.reset_game()
                            self.state = action
                        else:
                            self.state = action
            
            elif self.state == STATE_SETTINGS:
                for button in self.settings_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        self.state = action
                
                # Handle fullscreen button in settings
                self.settings_fullscreen_button.update(mouse_pos)
                action = self.settings_fullscreen_button.handle_event(event)
                if action == "toggle_fullscreen":
                    new_mode = "windowed" if self.fullscreen else "fullscreen"
                    self.show_confirmation_dialog(
                        f"Switch to {new_mode} mode?",
                        lambda: self.toggle_fullscreen(True),
                        None
                    )
            
            elif self.state == STATE_BEST_SCORE:
                for button in self.best_score_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        self.state = action
            
            elif self.state == STATE_INSTRUCTIONS:
                for button in self.instructions_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        self.state = action
    
    def show_confirmation_dialog(self, message, yes_action, no_action=None):
        """Show a confirmation dialog with Yes/No options"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Get current screen dimensions
        screen_width, screen_height = self.screen.get_size()
        
        # Calculate scale factors
        scale_x = screen_width / SCREEN_WIDTH
        scale_y = screen_height / SCREEN_HEIGHT
        
        # Create dialog box
        dialog_width, dialog_height = int(400 * scale_x), int(200 * scale_y)
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2
        
        # Draw dialog background
        dialog_bg = pygame.Surface((dialog_width, dialog_height))
        dialog_bg.fill((50, 50, 50))  # Dark gray
        pygame.draw.rect(dialog_bg, (200, 200, 200), (0, 0, dialog_width, dialog_height), 3)  # Light gray border
        self.screen.blit(dialog_bg, (dialog_x, dialog_y))
        
        # Draw message
        message_font = pygame.font.Font(None, int(30 * scale_y))
        message_text = message_font.render(message, True, WHITE)
        message_rect = message_text.get_rect(center=(screen_width // 2, dialog_y + dialog_height // 3))
        self.screen.blit(message_text, message_rect)
        
        # Create buttons
        button_width, button_height = int(100 * scale_x), int(40 * scale_y)
        button_y = dialog_y + int(dialog_height * 0.65)
        
        # Yes button
        yes_button_x = dialog_x + dialog_width // 4 - button_width // 2
        yes_button = pygame.Rect(yes_button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (100, 200, 100), yes_button)  # Green
        pygame.draw.rect(self.screen, (200, 255, 200), yes_button, 2)  # Light green border
        
        yes_text = message_font.render("Yes", True, WHITE)
        yes_text_rect = yes_text.get_rect(center=yes_button.center)
        self.screen.blit(yes_text, yes_text_rect)
        
        # No button
        no_button_x = dialog_x + dialog_width * 3 // 4 - button_width // 2
        no_button = pygame.Rect(no_button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 100, 100), no_button)  # Red
        pygame.draw.rect(self.screen, (255, 200, 200), no_button, 2)  # Light red border
        
        no_text = message_font.render("No", True, WHITE)
        no_text_rect = no_text.get_rect(center=no_button.center)
        self.screen.blit(no_text, no_text_rect)
        
        # Update display
        pygame.display.flip()
        
        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if yes_button.collidepoint(mouse_pos):
                        waiting = False
                        if yes_action:
                            yes_action()
                    
                    elif no_button.collidepoint(mouse_pos):
                        waiting = False
                        if no_action:
                            no_action()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_y:
                        waiting = False
                        if yes_action:
                            yes_action()
                    
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                        waiting = False
                        if no_action:
                            no_action()
    
    def update_gameplay(self):
        """Update game objects during gameplay"""
        current_time = pygame.time.get_ticks()
        
        # Update player
        self.player.update()
        
        # Handle energy blast
        self.handle_energy_blast()
        
        # Update energy bar
        self.update_energy_bar()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Respawn enemies that go off screen
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.spawn_enemy()
        
        # Update powerups
        for powerup in self.powerups[:]:
            if powerup.update():
                self.powerups.remove(powerup)
        
        # Check collisions
        collision_results = check_collisions(self.player, self.enemies, self.bullets, self.powerups)
        
        # Handle enemy destruction
        for enemy in collision_results['enemies_destroyed']:
            if enemy in self.enemies:
                # Play explosion sound
                if enemy.explosion_sound:
                    enemy.explosion_sound.play()
                
                # Remove the enemy
                self.enemies.remove(enemy)
                
                # Add energy when destroying an asteroid
                self.player.add_energy(1)
                
                # Add score for destroying asteroid
                self.player.score += SCORE_ASTEROID_DESTROYED
                print(f"Asteroid destroyed, score increased to {self.player.score}")
                
                # Create floating score text
                self.floating_texts.append(
                    create_floating_text(f"+{SCORE_ASTEROID_DESTROYED}", 
                                        (enemy.rect.centerx, enemy.rect.centery))
                )
                
                # Chance to spawn powerup
                powerup = spawn_random_powerup(enemy.rect.centerx, enemy.rect.centery, self.assets)
                if powerup:
                    self.powerups.append(powerup)
                
                # Spawn a new enemy
                self.spawn_enemy()
        
        # Handle bullet removal
        for bullet in collision_results['bullets_to_remove']:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        
        # Handle player hit
        if collision_results['player_hit']:
            # Call player's hit method to reduce lives and trigger invincibility
            self.player.hit()
            
            # Reduce score
            self.player.score = max(0, self.player.score + SCORE_HIT_PENALTY)
            
            # Create floating score text
            self.floating_texts.append(
                create_floating_text(str(SCORE_HIT_PENALTY), 
                                    (self.player.rect.centerx, self.player.rect.centery),
                                    color=RED)
            )
            
            # Check if player is dead
            if self.player.is_dead():
                self.final_score = self.player.score
                if self.final_score > self.high_score:
                    self.high_score = self.final_score
                    self.save_high_score()
                self.state = STATE_GAME_OVER
        
        # Handle powerup collection
        if collision_results['powerup_collected']:
            powerup = collision_results['powerup_collected']
            
            # Apply powerup effect
            powerup.apply(self.player)
            
            # Remove the powerup
            if powerup in self.powerups:
                self.powerups.remove(powerup)
            
            # Add score
            self.player.score += SCORE_POWERUP_COLLECTED
            
            # Create floating score text
            self.floating_texts.append(
                create_floating_text(f"+{SCORE_POWERUP_COLLECTED}", 
                                    (self.player.rect.centerx, self.player.rect.centery),
                                    color=GREEN)
            )
        
        # Update player score
        self.score_display.update(self.player.score)
        
        # Force immediate update of displayed score for better feedback
        self.score_display.reset()
        
        # Update health bar
        self.health_bar.update(self.player.lives)
        
        # Update lives display
        self.lives_display.update(self.player.lives)
        
        # Update powerup indicator
        self.powerup_indicator.update(self.player)
        
        # Update floating texts
        update_floating_texts(self.floating_texts)
        
        # Check for continuous shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            new_bullets = self.player.shoot()
            self.bullets.extend(new_bullets)
        
        # Spawn enemies over time
        if len(self.enemies) < MAX_ENEMIES and random.random() < 0.02:
            self.spawn_enemy()
    
    def update_splash(self):
        """Update splash screen"""
        current_time = pygame.time.get_ticks()
        if current_time - self.splash_start_time > 2000:  # 2 seconds
            self.state = STATE_MENU
    
    def update_menu(self):
        """Update menu screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.update(mouse_pos)
    
    def update_pause(self):
        """Update pause screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.pause_buttons:
            button.update(mouse_pos)
    
    def update_game_over(self):
        """Update game over screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.game_over_buttons:
            button.update(mouse_pos)
    
    def update_settings(self):
        """Update settings screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.settings_buttons:
            button.update(mouse_pos)
        
        # Update fullscreen button text
        fullscreen_text = "Switch to Windowed Mode" if self.fullscreen else "Switch to Fullscreen Mode"
        self.settings_fullscreen_button.text = fullscreen_text
        self.settings_fullscreen_button.update(mouse_pos)
    
    def update_best_score(self):
        """Update best score screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.best_score_buttons:
            button.update(mouse_pos)
    
    def update_instructions(self):
        """Update instructions screen"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.instructions_buttons:
            button.update(mouse_pos)
    
    def update(self):
        """Update game state based on current state"""
        # Update background scrolling
        self.bg_y = (self.bg_y + 1) % SCREEN_HEIGHT
        
        if self.state == STATE_SPLASH:
            self.update_splash()
        
        elif self.state == STATE_MENU:
            self.update_menu()
        
        elif self.state == STATE_GAMEPLAY:
            self.update_gameplay()
        
        elif self.state == STATE_PAUSE:
            self.update_pause()
        
        elif self.state == STATE_GAME_OVER:
            self.update_game_over()
        
        elif self.state == STATE_SETTINGS:
            self.update_settings()
        
        elif self.state == STATE_BEST_SCORE:
            self.update_best_score()
        
        elif self.state == STATE_INSTRUCTIONS:
            self.update_instructions()
    
    def render_splash(self):
        """Render the splash screen"""
        # Draw background
        self.screen.fill(BLACK)
        
        # Draw logo
        logo_text = self.large_font.render("ASTRO SPACE", True, WHITE)
        logo_rect = logo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(logo_text, logo_rect)
        
        # Draw loading text
        loading_text = self.small_font.render("Loading...", True, WHITE)
        loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(loading_text, loading_rect)
    
    def render_menu(self):
        """Render the menu screen"""
        # Draw background
        self.screen.blit(self.assets['background_menu'], (0, 0))
        
        # Draw title
        title_text = self.large_font.render("ASTRO SPACE", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(self.screen)
        
        # Draw F1 shortcut hint
        hint_text = self.small_font.render("Press F1 to toggle fullscreen mode", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(hint_text, hint_rect)
    
    def render_gameplay(self):
        """Render the gameplay screen"""
        # Draw scrolling background
        self.screen.blit(self.assets['background'], (0, self.bg_y))
        self.screen.blit(self.assets['background'], (0, self.bg_y - SCREEN_HEIGHT))
        
        # Apply screen shake if active
        offset_x, offset_y = self.screen_shake_offset
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw UI elements
        self.health_bar.draw(self.screen)
        self.score_display.draw(self.screen)
        self.lives_display.draw(self.screen)
        self.energy_bar.draw(self.screen)
        
        # Draw energy blast effect if active
        if self.player.is_blasting:
            self.player.draw_blast(self.screen)
        
        # Draw floating texts
        draw_floating_texts(self.screen, self.floating_texts)
    
    def render_pause(self):
        """Render the pause screen overlay"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw buttons
        for button in self.pause_buttons:
            button.draw(self.screen)
    
    def render_game_over(self):
        """Render the game over screen overlay"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))  # More opaque black
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Format scores with commas for better readability
        formatted_score = f"{self.final_score:,}"
        formatted_high_score = f"{self.high_score:,}"
        
        # Draw score text
        score_text = self.main_font.render(f"Score: {formatted_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Draw high score text
        high_score_text = self.main_font.render(f"High Score: {formatted_high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Draw new high score text if applicable
        if self.final_score >= self.high_score:
            new_high_score_text = self.main_font.render("New High Score!", True, YELLOW)
            new_high_score_rect = new_high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(new_high_score_text, new_high_score_rect)
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(self.screen)
    
    def render_settings(self):
        """Render the settings screen"""
        # Draw background
        self.screen.blit(self.assets['background_menu'], (0, 0))
        
        # Draw title
        title_text = self.large_font.render("SETTINGS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw settings options
        settings_text = self.main_font.render("Display Settings", True, WHITE)
        settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(settings_text, settings_rect)
        
        # Draw fullscreen option
        self.settings_fullscreen_button.draw(self.screen)
        
        # Draw current display mode
        mode_text = "Current mode: " + ("Fullscreen" if self.fullscreen else "Windowed")
        mode_display = self.small_font.render(mode_text, True, WHITE)
        mode_rect = mode_display.get_rect(center=(SCREEN_WIDTH // 2, 240))
        self.screen.blit(mode_display, mode_rect)
        
        # Draw resolution info
        current_w, current_h = self.screen.get_size()
        res_text = f"Resolution: {current_w}x{current_h}"
        res_display = self.small_font.render(res_text, True, WHITE)
        res_rect = res_display.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(res_display, res_rect)
        
        # Draw buttons
        for button in self.settings_buttons:
            button.draw(self.screen)
    
    def render_best_score(self):
        """Render the best score screen"""
        # Draw background
        self.screen.blit(self.assets['background_menu'], (0, 0))
        
        # Draw title
        title_text = self.large_font.render("BEST SCORE", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Format high score with commas for better readability
        formatted_high_score = f"{self.high_score:,}"
        
        # Draw high score
        high_score_text = self.main_font.render(f"High Score: {formatted_high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Draw buttons
        for button in self.best_score_buttons:
            button.draw(self.screen)
    
    def render_instructions(self):
        """Render the instructions screen"""
        # Draw background
        self.screen.blit(self.assets['background_menu'], (0, 0))
        
        # Draw title
        title_text = self.large_font.render("INSTRUCTIONS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 70))
        self.screen.blit(title_text, title_rect)
        
        # Create a semi-transparent white background for instructions
        instructions_bg = pygame.Surface((500, 300), pygame.SRCALPHA)  # Width and height for the background
        instructions_bg.fill((255, 255, 255, 180))  # Semi-transparent white
        instructions_bg_rect = instructions_bg.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(instructions_bg, instructions_bg_rect)
        
        # Draw instructions
        instructions = [
            "Arrow Keys or WASD: Move ship",
            "Space: Fire bullets",
            "P: Pause game",
            "M: Mute sound",
            "F1: Toggle fullscreen",
            "X: Trigger Energy Blast (when fully charged)",
            "",
            "Destroy asteroids to earn points and energy",
            "Collect power-ups for special abilities",
            "Avoid collisions with asteroids"
        ]
        
        y_pos = 180
        for instruction in instructions:
            text = self.small_font.render(instruction, True, BLACK)  # Black text on white background
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(text, rect)
            y_pos += 30
        
        # Draw buttons
        for button in self.instructions_buttons:
            button.draw(self.screen)
    
    def render(self):
        """Render the game based on current state"""
        if self.state == STATE_SPLASH:
            self.render_splash()
        
        elif self.state == STATE_MENU:
            self.render_menu()
        
        elif self.state == STATE_GAMEPLAY:
            self.render_gameplay()
        
        elif self.state == STATE_PAUSE:
            # First render the gameplay screen
            self.render_gameplay()
            # Then render the pause overlay
            self.render_pause()
        
        elif self.state == STATE_GAME_OVER:
            # First render the gameplay screen
            self.render_gameplay()
            # Then render the game over overlay
            self.render_game_over()
        
        elif self.state == STATE_SETTINGS:
            self.render_settings()
        
        elif self.state == STATE_BEST_SCORE:
            self.render_best_score()
        
        elif self.state == STATE_INSTRUCTIONS:
            self.render_instructions()
        
        # Update the display
        pygame.display.flip()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def load_display_preferences(self):
        """Load display preferences from file"""
        try:
            if os.path.exists(DISPLAY_PREFERENCES_FILE):
                with open(DISPLAY_PREFERENCES_FILE, 'r') as f:
                    prefs = json.load(f)
                
                # Apply saved preferences
                self.fullscreen = prefs.get('fullscreen', False)
                saved_size = prefs.get('window_size', (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.window_size = (int(saved_size[0]), int(saved_size[1]))
                
                # Apply display mode
                if self.fullscreen:
                    display_info = pygame.display.Info()
                    self.screen = pygame.display.set_mode(
                        (display_info.current_w, display_info.current_h), 
                        pygame.FULLSCREEN
                    )
                else:
                    self.screen = pygame.display.set_mode(self.window_size)
                
                print(f"Display preferences loaded: fullscreen={self.fullscreen}, size={self.window_size}")
                return True
        except Exception as e:
            print(f"Error loading display preferences: {e}")
        
        return False
    
    def save_display_preferences(self):
        """Save display preferences to file"""
        try:
            prefs = {
                'fullscreen': self.fullscreen,
                'window_size': self.window_size
            }
            
            with open(DISPLAY_PREFERENCES_FILE, 'w') as f:
                json.dump(prefs, f)
                
            print(f"Display preferences saved: fullscreen={self.fullscreen}, size={self.window_size}")
        except Exception as e:
            print(f"Error saving display preferences: {e}")
    
    def quit_game(self):
        """Quit the game"""
        # Save display preferences before quitting
        if SAVE_DISPLAY_PREFERENCES:
            self.save_display_preferences()
        
        pygame.quit()
        sys.exit()
    
    def handle_energy_blast(self):
        """Handle the energy blast mechanic"""
        # Check if energy blast is active
        if self.player.is_blasting:
            # Update blast and check for collisions
            asteroids_destroyed = self.player.update_blast(self.enemies)
            
            # Add score for destroyed asteroids (regular + bonus)
            if asteroids_destroyed > 0:
                base_points = asteroids_destroyed * SCORE_ASTEROID_DESTROYED
                bonus_points = asteroids_destroyed * SCORE_BLAST_BONUS
                total_points = base_points + bonus_points
                
                self.player.score += total_points
                self.score_display.update(self.player.score)
                
                # Create floating text for bonus
                self.floating_texts.append(
                    create_floating_text(f"+{total_points}", 
                                        (self.player.rect.centerx, self.player.rect.centery),
                                        color=(0, 255, 255))
                )
                
                print(f"Energy blast destroyed {asteroids_destroyed} asteroids, adding {total_points} points")
            
            # Apply screen shake
            if self.player.screen_shake > 0:
                self.screen_shake_offset = (random.randint(-5, 5), random.randint(-5, 5))
                self.player.screen_shake -= 1
            else:
                self.screen_shake_offset = (0, 0)
    
    def update_energy_bar(self):
        """Update the energy bar UI element"""
        if hasattr(self, 'energy_bar') and hasattr(self, 'player'):
            self.energy_bar.current_energy = self.player.energy
            self.energy_bar.is_charged = self.player.energy >= self.player.max_energy
    
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
