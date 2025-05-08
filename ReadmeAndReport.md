# Accessible Snake Game

This project is a modified version of the classic Snake game with accessibility features specifically designed for players with motor impairments. The implementation uses PyGame and focuses on making the game more playable for people who may have difficulty with precise or rapid movements.

## Accessibility Features

### 1. Adaptive Game Speed
- Players can adjust the game speed to match their comfort level and abilities
- Speed can be reduced to as low as 3 FPS for players who need more time to react
- Speed can be increased up to 15 FPS for more experienced players
- Adjustable through the accessibility menu (press TAB to access)

### 2. Alternative Control Schemes
- Traditional arrow key controls are available by default
- WASD control scheme provides an alternative layout for directional movement
- Single-key turning system (Q and E keys):
  - Q turns the snake counter-clockwise (left relative to current direction)
  - E turns the snake clockwise (right relative to current direction)
  - This simplifies control to just two keys, reducing the need for precise directional inputs

### 3. Visual Guidance System
- Optional guidance mode helps players see the optimal path to the food
- Visual indicators include:
  - Yellow highlight around the food item
  - Yellow circle on the snake's head showing the current direction
  - Blue highlight appears when a turn would be beneficial
  - These visual cues provide guidance without making the game too easy

### 4. Dark Mode
- High-contrast dark color scheme designed to reduce eye strain
- Helps players with visual sensitivity or those playing in low-light environments
- Toggled through the accessibility menu
- Maintains clear visual distinction between game elements

### 5. Accessibility Menu
- Press TAB at any time to access a comprehensive accessibility menu
- All accessibility features can be toggled on/off through this menu
- Clear visual instructions for using each feature
- Game pauses while in the menu to prevent accidental loss

## How to Use

1. Run the game using Python:
   ```
   python game.py
   ```

2. Press TAB at any time to open the Accessibility Settings menu

3. In the menu:
   - Press + or - to adjust game speed
   - Press G to toggle guidance mode
   - Press C to toggle alternative controls
   - Press D to toggle dark mode
   - Press TAB again to close the menu

4. If alternative controls are enabled:
   - Use WASD for directional movement, or
   - Use Q (turn left) and E (turn right) for simplified control

## Target Audience

This implementation is specifically designed for players with motor impairments, including:
- Players with limited dexterity or fine motor control
- Players with tremors or involuntary movements
- Players who fatigue easily with rapid or continuous movements
- Players who use adaptive input devices
- Players with visual sensitivity or who prefer reduced eye strain

The combination of adjustable game speed, alternative control schemes, visual guidance, and dark mode makes the game more accessible while maintaining the core gameplay and challenge.
