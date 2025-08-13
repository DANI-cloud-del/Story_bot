# character.py
import arcade

class CharacterSprite(arcade.Sprite):
    def __init__(self, idle_path, walk_pattern, scale=0.5):
        super().__init__(idle_path, scale=scale)
        self.idle_texture = arcade.load_texture(idle_path)
        self.walk_textures = [arcade.load_texture(walk_pattern.format(i)) for i in range(8)]
        # Add more textures for different states if available
        self.texture = self.idle_texture
        self._walk_index = 0
        self._walk_timer = 0
        self.walk_anim_speed = 0.12
        self.current_state = "idle"

    def set_state(self, state):
        self.current_state = state
        if state == "idle":
            self.texture = self.idle_texture

    def update_animation(self, moving, delta_time):
        if self.current_state == "walk" and moving:
            self._walk_timer += delta_time
            if self._walk_timer >= self.walk_anim_speed:
                self._walk_index = (self._walk_index + 1) % len(self.walk_textures)
                self.texture = self.walk_textures[self._walk_index]
                self._walk_timer = 0
        elif self.current_state == "idle":
            self.texture = self.idle_texture
            self._walk_index = 0
            self._walk_timer = 0
        # Add more animation states as needed