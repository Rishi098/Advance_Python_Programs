import pygame
import os
import random
from config import *

def load_image(filename):
    """Load an image and convert it for optimal use in pygame."""
    try:
        print(f"Attempting to load image: {filename}")
        if not os.path.exists(filename):
            print(f"File does not exist: {filename}")
            raise FileNotFoundError(f"Image file not found: {filename}")
            
        image = pygame.image.load(filename).convert_alpha()
        print(f"Successfully loaded image: {filename}")
        return image
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        # Return a placeholder colored rectangle if image can't be loaded
        placeholder = pygame.Surface((50, 50))
        placeholder.fill(RED)
        return placeholder

def load_sound(filename):
    """Load a sound file."""
    try:
        sound = pygame.mixer.Sound(filename)
        return sound
    except pygame.error as e:
        print(f"Error loading sound {filename}: {e}")
        # Return a dummy sound object if sound can't be loaded
        return pygame.mixer.Sound(buffer=bytearray(100))

def load_font(filename, size=36):
    """Load a font file."""
    try:
        font = pygame.font.Font(filename, size)
        return font
    except pygame.error as e:
        print(f"Error loading font {filename}: {e}")
        # Return the default font if custom font can't be loaded
        return pygame.font.Font(None, size)

def ensure_dir_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_collision(obj1, obj2):
    """Check if two objects are colliding using their rect attributes."""
    return obj1.rect.colliderect(obj2.rect)

def check_collisions(player, enemies, bullets, powerups=None):
    """
    Check all game collisions and handle their effects.
    Returns a dictionary with collision results.
    """
    results = {
        'player_hit': False,
        'enemies_destroyed': [],
        'bullets_to_remove': [],
        'powerup_collected': None,
        'score_change': 0
    }
    
    # Check bullet collisions with enemies
    for bullet in bullets[:]:
        if bullet.direction < 0:  # Player bullets go up
            for enemy in enemies[:]:
                if check_collision(bullet, enemy):
                    results['enemies_destroyed'].append(enemy)
                    results['bullets_to_remove'].append(bullet)
                    results['score_change'] += 10
                    break
    
    # Check player collision with enemies
    for enemy in enemies:
        if check_collision(player, enemy) and not player.invincible:
            results['player_hit'] = True
            results['enemies_destroyed'].append(enemy)
            results['score_change'] -= 50
            break
    
    # Check player collision with powerups
    if powerups:
        for powerup in powerups[:]:
            if check_collision(player, powerup):
                results['powerup_collected'] = powerup
                results['score_change'] += 20
    
    return results

def load_assets():
    """Load all game assets and return them in a dictionary."""
    # Ensure asset directories exist
    for directory in [ASSETS_DIR, IMAGES_DIR, SOUNDS_DIR, FONTS_DIR]:
        ensure_dir_exists(directory)
    
    assets = {}
    
    # Load images
    try:
        assets['player_ship'] = load_image(PLAYER_IMG)
        assets['enemy_ship'] = load_image(ENEMY_IMG)
        assets['background'] = load_image(BACKGROUND_IMG)
        assets['background_big'] = load_image(BACKGROUND_BIG_IMG)
        assets['background_space3'] = load_image(BACKGROUND_SPACE3_IMG)
        assets['background_menu'] = load_image(BACKGROUND_MENU_IMG)
        assets['bullet'] = load_image(BULLET_IMG)
        assets['player_exploded'] = load_image(PLAYER_EXPLODED_IMG)
        
        # Create placeholder explosion animation (since we don't have explosion frames)
        explosion_placeholder = pygame.Surface((50, 50))
        explosion_placeholder.fill(YELLOW)
        assets['explosion_anim'] = [explosion_placeholder] * 8
        
        # Create powerup images since we don't have them
        powerup_size = (20, 20)
        
        # Double shot powerup (purple)
        double_powerup = pygame.Surface(powerup_size)
        double_powerup.fill(PURPLE)
        assets['powerup_double'] = double_powerup
        
        # Shield powerup (blue)
        shield_powerup = pygame.Surface(powerup_size)
        shield_powerup.fill(BLUE)
        assets['powerup_shield'] = shield_powerup
        
        # Speed powerup (yellow)
        speed_powerup = pygame.Surface(powerup_size)
        speed_powerup.fill(YELLOW)
        assets['powerup_speed'] = speed_powerup
        
        # Life powerup (red)
        life_powerup = pygame.Surface(powerup_size)
        life_powerup.fill(RED)
        assets['powerup_life'] = life_powerup
    except Exception as e:
        print(f"Error loading images: {e}")
        # Create placeholder images
        placeholder = pygame.Surface((50, 50))
        placeholder.fill(RED)
        assets['player_ship'] = placeholder
        
        enemy_placeholder = pygame.Surface((40, 40))
        enemy_placeholder.fill(GREEN)
        assets['enemy_ship'] = enemy_placeholder
        
        bg_placeholder = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_placeholder.fill(BLACK)
        assets['background'] = bg_placeholder
        
        bullet_placeholder = pygame.Surface((5, 10))
        bullet_placeholder.fill(BLUE)
        assets['bullet'] = bullet_placeholder
        
        # Create placeholder explosion animation
        explosion_placeholder = pygame.Surface((50, 50))
        explosion_placeholder.fill(YELLOW)
        assets['explosion_anim'] = [explosion_placeholder] * 8
        
        # Create placeholder powerup images
        powerup_placeholder = pygame.Surface((20, 20))
        
        purple_powerup = powerup_placeholder.copy()
        purple_powerup.fill((128, 0, 128))  # Purple
        assets['powerup_double'] = purple_powerup
        
        blue_powerup = powerup_placeholder.copy()
        blue_powerup.fill(BLUE)
        assets['powerup_shield'] = blue_powerup
        
        yellow_powerup = powerup_placeholder.copy()
        yellow_powerup.fill(YELLOW)
        assets['powerup_speed'] = yellow_powerup
        
        red_powerup = powerup_placeholder.copy()
        red_powerup.fill(RED)
        assets['powerup_life'] = red_powerup
    
    # Load sounds
    try:
        pygame.mixer.init()
        assets['shoot_sound'] = load_sound(SHOOT_SOUND)
        assets['explosion_sound'] = load_sound(EXPLOSION_SOUND)
        assets['powerup_sound'] = load_sound(POWERUP_SOUND)
        
        # Handle background music separately to avoid pygame.error
        if os.path.exists(BACKGROUND_MUSIC):
            assets['background_music'] = BACKGROUND_MUSIC
        else:
            print(f"Background music file not found: {BACKGROUND_MUSIC}")
            assets['background_music'] = None
    except Exception as e:
        print(f"Error loading sounds: {e}")
        # Create dummy sounds
        dummy_sound = pygame.mixer.Sound(buffer=bytearray(100))
        assets['shoot_sound'] = dummy_sound
        assets['explosion_sound'] = dummy_sound
        assets['powerup_sound'] = dummy_sound
        assets['background_music'] = None
    
    # Load fonts
    try:
        assets['main_font'] = load_font(MAIN_FONT, 36)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        # Use default font
        assets['main_font'] = pygame.font.Font(None, 36)
    
    return assets

def create_floating_text(text, position, color=WHITE, duration=60, speed=1):
    """Create a floating text effect."""
    return {
        'text': text,
        'position': position,
        'color': color,
        'duration': duration,
        'speed': speed,
        'alpha': 255
    }

def update_floating_texts(floating_texts):
    """Update all floating text effects."""
    for text in floating_texts[:]:
        text['position'] = (text['position'][0], text['position'][1] - text['speed'])
        text['duration'] -= 1
        text['alpha'] = int(255 * (text['duration'] / 60))
        
        if text['duration'] <= 0:
            floating_texts.remove(text)

def draw_floating_texts(surface, floating_texts):
    """Draw all floating text effects."""
    font = pygame.font.Font(None, 24)
    for text in floating_texts:
        text_surface = font.render(text['text'], True, text['color'])
        text_surface.set_alpha(text['alpha'])
        surface.blit(text_surface, text['position'])
