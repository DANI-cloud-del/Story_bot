# story_engine/main.py

import arcade
import arcade.future.background as background
from dataclasses import dataclass
from typing import List, Dict


# Constants for the window size and pixel scaling (matches the parallax example)
PIXEL_SCALE = 3
ORIGINAL_BG_LAYER_HEIGHT_PX = 240
SCALED_BG_LAYER_HEIGHT_PX = ORIGINAL_BG_LAYER_HEIGHT_PX * PIXEL_SCALE

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 600  # Keep a nice height for character movement

PLAYER_SPEED = 300  # Player speed in pixels per second
CAMERA_SPEED = 0.1  # Camera lerp speed

@dataclass
class Scene:
    background_layers: List[str]  # Paths for parallax layers
    dialogue: List[Dict[str, str]]
    sprites: Dict[str, str]


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


class StoryWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Story Engine with Parallax Background", resizable=True)

        # Define parallax layer paths (same as in provided parallax example)
        self.scene = Scene(
            background_layers=[
                ":resources:/images/miami_synth_parallax/layers/back.png",
                ":resources:/images/miami_synth_parallax/layers/buildings.png",
                ":resources:/images/miami_synth_parallax/layers/palms.png",
                ":resources:/images/miami_synth_parallax/layers/highway.png"
            ],
            dialogue=[
                {"hero": "Hello world!"},
                {"villain": "This is a test!"}
            ],
            sprites={
                "hero": ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                "villain": ":resources:images/animated_characters/zombie/zombie_idle.png"
            }
        )

        # Set background color to match parallax example
        self.background_color = (162, 84, 162, 255)

        # Camera for view control
        self.camera = arcade.Camera2D()

        # Setup parallax backgrounds
        self.backgrounds = background.ParallaxGroup()
        bg_layer_size_px = (WINDOW_WIDTH, SCALED_BG_LAYER_HEIGHT_PX)
        # Depths control how fast layers move relative to player: higher means farther away (slower)
        depths = [10.0, 5.0, 3.0, 1.0]

        for layer_path, depth in zip(self.scene.background_layers, depths):
            self.backgrounds.add_from_file(layer_path, size=bg_layer_size_px, depth=depth, scale=PIXEL_SCALE)

        # Setup characters
        self.character_sprites = arcade.SpriteList()

        self.hero = CharacterSprite(
            idle_path=self.scene.sprites["hero"],
            walk_pattern=":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{}.png",
            scale=0.5
        )
        self.hero.position = 200, 150
        self.character_sprites.append(self.hero)

        self.villain = CharacterSprite(
            idle_path=self.scene.sprites["villain"],
            walk_pattern=":resources:images/animated_characters/zombie/zombie_walk{}.png",
            scale=0.5
        )
        self.villain.position = 600, 150
        self.character_sprites.append(self.villain)

        self.current_line = 0

        # Movement control flags
        self.hero_movement = {"up": False, "down": False, "left": False, "right": False}
        self.villain_movement = {"up": False, "down": False, "left": False, "right": False}
        self.movement_speed = 200  # pixels per second; slower for smoother parallax

    def pan_camera_to_player(self):
        """Move the camera smoothly towards the hero's position."""
        target_x = self.hero.center_x
        target_y = self.height // 2
        self.camera.position = arcade.math.lerp_2d(self.camera.position, (target_x, target_y), CAMERA_SPEED)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            # Update parallax background offsets for depth effect
            self.backgrounds.offset = self.camera.bottom_left
            self.backgrounds.pos = self.camera.bottom_left

            with self.ctx.enabled(self.ctx.BLEND):
                self.backgrounds.draw()

            # Draw characters on top
            self.character_sprites.draw()

            # Draw dialogue (fixed to screen coords)
            arcade.draw_text(
                list(self.scene.dialogue[self.current_line].values())[0],
                self.camera.position[0], 50,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        # Calculate movement based on pressed keys

        # Hero movement
        dx = 0
        dy = 0
        if self.hero_movement["up"]:
            dy += self.movement_speed * delta_time
        if self.hero_movement["down"]:
            dy -= self.movement_speed * delta_time
        if self.hero_movement["left"]:
            dx -= self.movement_speed * delta_time
        if self.hero_movement["right"]:
            dx += self.movement_speed * delta_time

        hero_moving = dx != 0 or dy != 0
        self.hero.center_x += dx
        self.hero.center_y += dy

        # Villain movement similarly
        vdx = 0
        vdy = 0
        if self.villain_movement["up"]:
            vdy += self.movement_speed * delta_time
        if self.villain_movement["down"]:
            vdy -= self.movement_speed * delta_time
        if self.villain_movement["left"]:
            vdx -= self.movement_speed * delta_time
        if self.villain_movement["right"]:
            vdx += self.movement_speed * delta_time

        villain_moving = vdx != 0 or vdy != 0
        self.villain.center_x += vdx
        self.villain.center_y += vdy

        # Animate characters based on movement
        self.hero.update_animation(hero_moving, delta_time)
        self.villain.update_animation(villain_moving, delta_time)

        # Keep sprites inside window bounds
        for sprite in (self.hero, self.villain):
            sprite.center_x = max(sprite.width / 2, min(self.camera.position[0] + self.width / 2 - sprite.width / 2, sprite.center_x))
            sprite.center_y = max(sprite.height / 2, min(self.height - sprite.height / 2, sprite.center_y))

        # Pan the camera to the hero
        self.pan_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.current_line = (self.current_line + 1) % len(self.scene.dialogue)
        if key == arcade.key.W:
            self.hero_movement["up"] = True
        elif key == arcade.key.S:
            self.hero_movement["down"] = True
        elif key == arcade.key.A:
            self.hero_movement["left"] = True
        elif key == arcade.key.D:
            self.hero_movement["right"] = True
        elif key == arcade.key.UP:
            self.villain_movement["up"] = True
        elif key == arcade.key.DOWN:
            self.villain_movement["down"] = True
        elif key == arcade.key.LEFT:
            self.villain_movement["left"] = True
        elif key == arcade.key.RIGHT:
            self.villain_movement["right"] = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.hero_movement["up"] = False
        elif key == arcade.key.S:
            self.hero_movement["down"] = False
        elif key == arcade.key.A:
            self.hero_movement["left"] = False
        elif key == arcade.key.D:
            self.hero_movement["right"] = False
        elif key == arcade.key.UP:
            self.villain_movement["up"] = False
        elif key == arcade.key.DOWN:
            self.villain_movement["down"] = False
        elif key == arcade.key.LEFT:
            self.villain_movement["left"] = False
        elif key == arcade.key.RIGHT:
            self.villain_movement["right"] = False

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.camera.match_window()
        full_width_size = (width, SCALED_BG_LAYER_HEIGHT_PX)
        for layer, depth in self.backgrounds:
            layer.size = full_width_size


if __name__ == "__main__":
    window = StoryWindow()
    arcade.run()
