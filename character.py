# character.py
import arcade

class CharacterSprite(arcade.Sprite):
    def __init__(self, idle_path, walk_pattern, scale=0.5):
        super().__init__(idle_path, scale=scale)
        self.idle_texture = arcade.load_texture(idle_path)
        self.walk_textures = [arcade.load_texture(walk_pattern.format(i)) for i in range(8)]
        self.texture = self.idle_texture
        self._walk_index = 0
        self._walk_timer = 0
        self.walk_anim_speed = 0.12

    def update_animation(self, moving, delta_time):
        if moving:
            self._walk_timer += delta_time
            if self._walk_timer >= self.walk_anim_speed:
                self._walk_index = (self._walk_index + 1) % len(self.walk_textures)
                self.texture = self.walk_textures[self._walk_index]
                self._walk_timer = 0
        else:
            self.texture = self.idle_texture
            self._walk_index = 0
            self._walk_timer = 0
