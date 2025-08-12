# story_engine/main.py
import arcade
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Scene:
    background: str
    dialogue: List[Dict[str, str]]
    sprites: Dict[str, str]


class CharacterSprite(arcade.Sprite):
    def __init__(self, idle_path, walk_pattern, scale=0.5):
        super().__init__(idle_path, scale=scale)
        # Load idle texture
        self.idle_texture = arcade.load_texture(idle_path)
        # Load walk textures as a list (assuming 8 walk frames: walk0.png ... walk7.png)
        self.walk_textures = [
            arcade.load_texture(walk_pattern.format(i)) for i in range(8)
        ]
        self.texture = self.idle_texture
        self._walk_index = 0
        self._walk_timer = 0
        self.walk_anim_speed = 0.12  # seconds per frame

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
        super().__init__(800, 600, "Story Engine Demo", resizable=True)

        # Create a simple test scene
        self.scene = Scene(
            background=":resources:images/backgrounds/abstract_1.jpg",
            dialogue=[
                {"hero": "Hello world!"},
                {"villain": "This is a test!"}
            ],
            sprites={
                "hero": ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                "villain": ":resources:images/animated_characters/zombie/zombie_idle.png"
            }
        )

        # Setup sprites as animated characters
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
        self.movement_speed = 5

    def setup_scene(self):
        # Set background to a solid color; see below for custom background images
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        # Optionally draw a background image (comment out if not needed)
        # arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, arcade.load_texture(self.scene.background))
        self.character_sprites.draw()

        # Draw dialogue
        current_text = list(self.scene.dialogue[self.current_line].values())[0]
        arcade.draw_text(
            current_text,
            self.width // 2, 50,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        # Draw controls hint
        arcade.draw_text(
            "WASD: Move Hero | Arrows: Move Villain | SPACE: Next Dialogue",
            10, 10,
            arcade.color.WHITE,
            12
        )

    def on_update(self, delta_time):
        """ Move sprites and animate based on key presses """
        # Hero movement (WASD)
        hero_moving = False
        if self.hero_movement["up"]:
            self.hero.center_y += self.movement_speed
            hero_moving = True
        if self.hero_movement["down"]:
            self.hero.center_y -= self.movement_speed
            hero_moving = True
        if self.hero_movement["left"]:
            self.hero.center_x -= self.movement_speed
            hero_moving = True
        if self.hero_movement["right"]:
            self.hero.center_x += self.movement_speed
            hero_moving = True

        # Villain movement (Arrow keys)
        villain_moving = False
        if self.villain_movement["up"]:
            self.villain.center_y += self.movement_speed
            villain_moving = True
        if self.villain_movement["down"]:
            self.villain.center_y -= self.movement_speed
            villain_moving = True
        if self.villain_movement["left"]:
            self.villain.center_x -= self.movement_speed
            villain_moving = True
        if self.villain_movement["right"]:
            self.villain.center_x += self.movement_speed
            villain_moving = True

        # Animate!
        self.hero.update_animation(hero_moving, delta_time)
        self.villain.update_animation(villain_moving, delta_time)

        # Keep sprites on screen
        for sprite in [self.hero, self.villain]:
            sprite.center_x = max(sprite.width / 2, min(self.width - sprite.width / 2, sprite.center_x))
            sprite.center_y = max(sprite.height / 2, min(self.height - sprite.height / 2, sprite.center_y))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.current_line = (self.current_line + 1) % len(self.scene.dialogue)
        # Hero controls (WASD)
        if key == arcade.key.W:
            self.hero_movement["up"] = True
        elif key == arcade.key.S:
            self.hero_movement["down"] = True
        elif key == arcade.key.A:
            self.hero_movement["left"] = True
        elif key == arcade.key.D:
            self.hero_movement["right"] = True
        # Villain controls (Arrow keys)
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

if __name__ == "__main__":
    window = StoryWindow()
    arcade.run()
