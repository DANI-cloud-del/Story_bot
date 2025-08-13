# animation_controller.py
from settings import PLAYER_SPEED
import random

class AnimationController:
    def __init__(self, hero_sprite, villain_sprite):
        self.hero = hero_sprite
        self.villain = villain_sprite
        self.hero_movement = {"up": False, "down": False, "left": False, "right": False}
        self.villain_movement = {"up": False, "down": False, "left": False, "right": False}
        self.movement_speed = PLAYER_SPEED  # Now properly defined

    def apply_instructions(self, instructions):
        """Execute animation commands with validation"""
        if not instructions:
            return
            
        for cmd in instructions:
            char = cmd.get("character")
            action = cmd.get("action", "idle")
            direction = cmd.get("direction")
            
            if char == "hero":
                self._handle_action(self.hero, self.hero_movement, action, direction)
            elif char == "villain":
                self._handle_action(self.villain, self.villain_movement, action, direction)

    def _handle_action(self, sprite, movement_dict, action, direction):
        """Update sprite state based on validated instruction"""
        # Reset movement
        for key in movement_dict:
            movement_dict[key] = False
            
        # Handle movement
        if action == "walk" and direction:
            movement_dict[direction] = True
            
        # Update animation state
        if hasattr(sprite, 'set_state'):
            sprite.set_state(action)