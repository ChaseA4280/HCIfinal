import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BASE_FPS = 10  # Base game speed
MIN_FPS = 3    # Minimum game speed for accessibility
MAX_FPS = 15   # Maximum game speed

# Colors - Light mode (default)
LIGHT_MODE = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'BACKGROUND': (255, 255, 255),
    'GRID': (200, 200, 200),
    'TEXT': (0, 0, 0),
    'MENU_BG': (255, 255, 255),
    'MENU_BORDER': (0, 0, 0)
}

# Colors - Dark mode
DARK_MODE = {
    'BLACK': (255, 255, 255),
    'WHITE': (25, 25, 25),
    'GREEN': (0, 200, 0),
    'RED': (255, 50, 50),
    'BLUE': (50, 100, 255),
    'YELLOW': (255, 255, 100),
    'PURPLE': (170, 50, 200),
    'BACKGROUND': (40, 40, 45),
    'GRID': (70, 70, 75),
    'TEXT': (220, 220, 220),
    'MENU_BG': (60, 60, 65),
    'MENU_BORDER': (180, 180, 180)
}

# Current color scheme - starts with light mode
COLORS = LIGHT_MODE.copy()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - With Accessibility Features")
clock = pygame.time.Clock()

# Font for text - size could be adjustable for accessibility
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Accessibility settings
class AccessibilitySettings:
    def __init__(self):
        self.game_speed = BASE_FPS
        self.guidance_mode = False
        self.alternative_controls = False
        self.settings_menu_active = False
        self.dark_mode = False
    
    def toggle_guidance_mode(self):
        self.guidance_mode = not self.guidance_mode
        
    def toggle_alternative_controls(self):
        self.alternative_controls = not self.alternative_controls
        
    def increase_game_speed(self):
        self.game_speed = min(self.game_speed + 1, MAX_FPS)
        
    def decrease_game_speed(self):
        self.game_speed = max(self.game_speed - 1, MIN_FPS)
    
    def toggle_settings_menu(self):
        self.settings_menu_active = not self.settings_menu_active
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        global COLORS
        COLORS = DARK_MODE if self.dark_mode else LIGHT_MODE
    
    def draw_settings_menu(self, surface):
        if not self.settings_menu_active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        surface.blit(overlay, (0, 0))
        
        # Draw menu box
        menu_width, menu_height = 500, 350  # Increased height for dark mode option
        menu_x = (WIDTH - menu_width) // 2
        menu_y = (HEIGHT - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(surface, COLORS['MENU_BG'], menu_rect)
        pygame.draw.rect(surface, COLORS['MENU_BORDER'], menu_rect, 3)
        
        # Draw title
        title = font.render("Accessibility Settings", True, COLORS['TEXT'])
        surface.blit(title, (menu_x + (menu_width - title.get_width()) // 2, menu_y + 20))
        
        # Draw settings options
        y_pos = menu_y + 80
        spacing = 40
        
        # Game Speed
        speed_text = font.render(f"Game Speed: {self.game_speed}", True, COLORS['TEXT'])
        surface.blit(speed_text, (menu_x + 30, y_pos))
        speed_help = small_font.render("Press + or - to adjust", True, COLORS['TEXT'])
        surface.blit(speed_help, (menu_x + 30, y_pos + 30))
        y_pos += spacing + 30
        
        # Guidance Mode
        guidance_text = font.render(f"Guidance Mode: {'ON' if self.guidance_mode else 'OFF'}", True, COLORS['TEXT'])
        surface.blit(guidance_text, (menu_x + 30, y_pos))
        guidance_help = small_font.render("Press G to toggle - Shows path to food", True, COLORS['TEXT'])
        surface.blit(guidance_help, (menu_x + 30, y_pos + 30))
        y_pos += spacing + 30
        
        # Alternative Controls
        controls_text = font.render(f"Alternative Controls: {'ON' if self.alternative_controls else 'OFF'}", True, COLORS['TEXT'])
        surface.blit(controls_text, (menu_x + 30, y_pos))
        controls_help = small_font.render("Press C to toggle - WASD or single key (Q/E) to turn", True, COLORS['TEXT'])
        surface.blit(controls_help, (menu_x + 30, y_pos + 30))
        y_pos += spacing + 30
        
        # Dark Mode
        dark_mode_text = font.render(f"Dark Mode: {'ON' if self.dark_mode else 'OFF'}", True, COLORS['TEXT'])
        surface.blit(dark_mode_text, (menu_x + 30, y_pos))
        dark_mode_help = small_font.render("Press D to toggle - Reduces eye strain", True, COLORS['TEXT'])
        surface.blit(dark_mode_help, (menu_x + 30, y_pos + 30))
        y_pos += spacing + 30
        
        # Close menu instructions
        smaller_font = pygame.font.SysFont(None, 18)
        close_text = smaller_font.render("Press TAB to close this menu", True, COLORS['TEXT'])
        surface.blit(close_text, (menu_x + (menu_width - close_text.get_width()) // 2 + 150, menu_y + menu_height - 50))

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Initial snake position (middle of screen)
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN])
        self.color = COLORS['GREEN']
        self.score = 0
        self.next_direction = None  # For buffering the next direction in alternative control mode
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = head
        
        # Apply buffered direction change if available
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        
        if self.direction == pygame.K_RIGHT:
            x += 1
        elif self.direction == pygame.K_LEFT:
            x -= 1
        elif self.direction == pygame.K_UP:
            y -= 1
        elif self.direction == pygame.K_DOWN:
            y += 1
            
        # Check if snake hits the wall
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True  # Game over
            
        # Check if snake hits itself
        if (x, y) in self.positions[1:]:
            return True  # Game over
        
        # Move snake
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return False
    
    def draw(self, surface):
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(
                position[0] * GRID_SIZE, 
                position[1] * GRID_SIZE, 
                GRID_SIZE, GRID_SIZE
            )
            # Make head a different color
            color = COLORS['PURPLE'] if i == 0 else COLORS['GREEN']
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, COLORS['BLACK'], rect, 1)
    
    def handle_keys(self, key, accessibility):
        # Standard arrow key controls
        if not accessibility.alternative_controls:
            if key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                self.direction = pygame.K_RIGHT
            elif key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                self.direction = pygame.K_LEFT
            elif key == pygame.K_UP and self.direction != pygame.K_DOWN:
                self.direction = pygame.K_UP
            elif key == pygame.K_DOWN and self.direction != pygame.K_UP:
                self.direction = pygame.K_DOWN
        else:
            # Alternative control scheme using WASD
            if key == pygame.K_d and self.direction != pygame.K_LEFT:
                self.direction = pygame.K_RIGHT
            elif key == pygame.K_a and self.direction != pygame.K_RIGHT:
                self.direction = pygame.K_LEFT
            elif key == pygame.K_w and self.direction != pygame.K_DOWN:
                self.direction = pygame.K_UP
            elif key == pygame.K_s and self.direction != pygame.K_UP:
                self.direction = pygame.K_DOWN
            # Simplified single key turning (Q = turn left, E = turn right)
            elif key == pygame.K_q:  # Turn left (counter-clockwise)
                if self.direction == pygame.K_UP:
                    self.next_direction = pygame.K_LEFT
                elif self.direction == pygame.K_LEFT:
                    self.next_direction = pygame.K_DOWN
                elif self.direction == pygame.K_DOWN:
                    self.next_direction = pygame.K_RIGHT
                elif self.direction == pygame.K_RIGHT:
                    self.next_direction = pygame.K_UP
            elif key == pygame.K_e:  # Turn right (clockwise)
                if self.direction == pygame.K_UP:
                    self.next_direction = pygame.K_RIGHT
                elif self.direction == pygame.K_RIGHT:
                    self.next_direction = pygame.K_DOWN
                elif self.direction == pygame.K_DOWN:
                    self.next_direction = pygame.K_LEFT
                elif self.direction == pygame.K_LEFT:
                    self.next_direction = pygame.K_UP

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = COLORS['RED']
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        
    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, COLORS['BLACK'], rect, 1)

def draw_grid(surface):
    # Optional grid drawing - could be toggled for accessibility
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, COLORS['GRID'], (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, COLORS['GRID'], (0, y), (WIDTH, y))

def draw_score(surface, score):
    # Score display - font size and color could be customizable
    text = font.render(f"Score: {score}", True, COLORS['TEXT'])
    surface.blit(text, (5, 5))

def draw_accessibility_hint(surface):
    # Display hint for accessibility menu
    hint = small_font.render("Press TAB for Accessibility Settings", True, COLORS['TEXT'])
    surface.blit(hint, (WIDTH - hint.get_width() - 10, 10))

def draw_guidance_path(surface, snake, food, accessibility):
    if not accessibility.guidance_mode:
        return
        
    # Get the head position and food position
    head_x, head_y = snake.get_head_position()
    food_x, food_y = food.position
    
    # Create a gradient color based on distance
    max_distance = math.sqrt((GRID_WIDTH ** 2) + (GRID_HEIGHT ** 2))
    
    # Draw a path indicator - simplified to just show direction
    # Calculate direction vector
    dir_x = food_x - head_x
    dir_y = food_y - head_y
    
    # Normalize to get unit vector
    length = max(1, math.sqrt(dir_x**2 + dir_y**2))
    dir_x, dir_y = dir_x/length, dir_y/length
    
    # Draw a line indicating the general direction to the food
    start_pos = ((head_x * GRID_SIZE) + (GRID_SIZE // 2), 
                 (head_y * GRID_SIZE) + (GRID_SIZE // 2))
    
    # Draw directional indicator on snake's head
    pygame.draw.circle(surface, COLORS['YELLOW'], start_pos, GRID_SIZE // 2 - 2, 2)
    
    # Draw the food highlight
    food_rect = pygame.Rect(
        food_x * GRID_SIZE - 2, 
        food_y * GRID_SIZE - 2,
        GRID_SIZE + 4, GRID_SIZE + 4
    )
    pygame.draw.rect(surface, COLORS['YELLOW'], food_rect, 2)
    
    # Draw some guidance dots in the direction of the food
    # But not creating a direct path to avoid making it too easy
    intensity = int(min(255, 255 * (1 - (length / max_distance))))
    highlight_color = (intensity, intensity, 0)  # Yellow with varying intensity
    
    # Decision point highlights - show where turns would be beneficial
    if abs(dir_x) > abs(dir_y):  # Mostly horizontal movement needed
        if snake.direction == pygame.K_UP or snake.direction == pygame.K_DOWN:
            # Should turn left or right
            turn_indicator = pygame.Rect(
                head_x * GRID_SIZE, 
                head_y * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, COLORS['BLUE'], turn_indicator, 3)
    else:  # Mostly vertical movement needed
        if snake.direction == pygame.K_LEFT or snake.direction == pygame.K_RIGHT:
            # Should turn up or down
            turn_indicator = pygame.Rect(
                head_x * GRID_SIZE, 
                head_y * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, COLORS['BLUE'], turn_indicator, 3)

def main():
    snake = Snake()
    food = Food()
    accessibility = AccessibilitySettings()
    
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle accessibility menu toggle
                if event.key == pygame.K_TAB:
                    accessibility.toggle_settings_menu()
                
                # If settings menu is active, handle its controls
                if accessibility.settings_menu_active:
                    if event.key == pygame.K_g:
                        accessibility.toggle_guidance_mode()
                    elif event.key == pygame.K_c:
                        accessibility.toggle_alternative_controls()
                    elif event.key == pygame.K_d:
                        accessibility.toggle_dark_mode()
                        # Update colors of existing objects
                        snake.color = COLORS['GREEN']
                        food.color = COLORS['RED']
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        accessibility.increase_game_speed()
                    elif event.key == pygame.K_MINUS:
                        accessibility.decrease_game_speed()
                # If game over, handle restart
                elif game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
                # Normal gameplay controls
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        snake.handle_keys(event.key, accessibility)
        
        if not game_over and not accessibility.settings_menu_active:
            # Update snake and check for game over
            game_over = snake.update()
            
            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
                
                # Ensure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Drawing
        screen.fill(COLORS['BACKGROUND'])
        draw_grid(screen)
        
        # Draw guidance path first (below snake and food)
        draw_guidance_path(screen, snake, food, accessibility)
        
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        draw_accessibility_hint(screen)
        
        if game_over:
            # Game over text - could be customizable for accessibility
            game_over_text = font.render("Game Over! Press SPACE to restart", True, COLORS['TEXT'])
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        
        # Draw accessibility settings menu on top if active
        accessibility.draw_settings_menu(screen)
        
        pygame.display.update()
        clock.tick(accessibility.game_speed)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()