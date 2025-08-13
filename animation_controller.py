# animation_controller.py
class AnimationController:
    def __init__(self, hero_sprite, villain_sprite):
        self.hero = hero_sprite
        self.villain = villain_sprite
        self.hero_movement = {"up": False, "down": False, "left": False, "right": False}
        self.villain_movement = {"up": False, "down": False, "left": False, "right": False}
        self.movement_speed = 300  # Default speed, can be overridden

    def apply_instructions(self, instructions):
        """Process animation instructions"""
        if not instructions:
            return
            
        print(f"Applying instructions: {instructions}")
        
        for cmd in instructions:
            char = cmd.get("character")
            action = cmd.get("action")
            direction = cmd.get("direction", "right")
            
            if char == "hero":
                self._handle_action(self.hero, self.hero_movement, action, direction)
            elif char == "villain":
                self._handle_action(self.villain, self.villain_movement, action, direction)

    def _handle_action(self, sprite, movement_dict, action, direction):
        """Set sprite state based on action"""
        # Reset all movements first
        for key in movement_dict:
            movement_dict[key] = False
            
        if action == "walk":
            if direction == "left":
                movement_dict["left"] = True
            elif direction == "right":
                movement_dict["right"] = True
            elif direction == "up":
                movement_dict["up"] = True
            elif direction == "down":
                movement_dict["down"] = True
                
        # Set sprite state if available
        if hasattr(sprite, 'set_state'):
            sprite.set_state(action)
            print(f"Set {sprite} to state: {action}")