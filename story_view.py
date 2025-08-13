import arcade
import arcade.future.background as background
from settings import *
from character import CharacterSprite
from scene import Scene


class StoryView(arcade.View):
    def __init__(self, scene: Scene, dialogue_lines: list):
        super().__init__()
        self.scene = scene
        self.camera = arcade.Camera2D()
        self.backgrounds = background.ParallaxGroup()

        depths = [10.0, 5.0, 3.0, 1.0]
        bg_layer_size_px = (WINDOW_WIDTH, SCALED_BG_LAYER_HEIGHT_PX)
        for path, depth in zip(scene.background_layers, depths):
            self.backgrounds.add_from_file(path, size=bg_layer_size_px, depth=depth, scale=PIXEL_SCALE)

        self.character_sprites = arcade.SpriteList()
        self.hero = CharacterSprite(scene.sprites["hero"], ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{}.png", 0.5)
        self.hero.position = 200, 150
        self.character_sprites.append(self.hero)

        self.villain = CharacterSprite(scene.sprites["villain"], ":resources:images/animated_characters/zombie/zombie_walk{}.png", 0.5)
        self.villain.position = 600, 150
        self.character_sprites.append(self.villain)

        self.hero_movement = {k: False for k in ["up","down","left","right"]}
        self.villain_movement = {k: False for k in ["up","down","left","right"]}

        self.dialogue_lines = dialogue_lines
        self.max_subtitle_lines = 2
        self.current_line_start = 0
        self.current_line_end = min(self.max_subtitle_lines, len(dialogue_lines))
        self.dialogue_alpha = 0.0
        self.fade_state = "fadein"
        self.dialogue_timer = 0

    def _draw_wrapped(self, text, x_center, y_start, width, font_size, alpha):
        arcade.draw_text(
            text,
            x_center - width // 2, y_start,
            (*arcade.color.WHITE[:3], int(alpha * 255)),
            font_size=font_size, width=width, multiline=True,
            anchor_x="left",
            anchor_y="bottom"
        )

    def wrap_text(self, text, max_width, font_size):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            approx_width = len(test_line) * font_size * 0.5  # rough width estimation
            if approx_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.backgrounds.offset = self.camera.bottom_left
            self.backgrounds.pos = self.camera.bottom_left
            with self.window.ctx.enabled(self.window.ctx.BLEND):
                self.backgrounds.draw()
            self.character_sprites.draw()

            max_width = int(WINDOW_WIDTH * 0.8)
            font_size = 18
            alpha = self.dialogue_alpha
            line_spacing = 4

            y = 56  # Start from bottom for the first subtitle block

            for idx in range(self.current_line_start, self.current_line_end):
                text = self.dialogue_lines[idx]
                # ---- WRAPPING section ----
                # Use custom wrap_text from above
                wrapped_lines = self.wrap_text(text, max_width, font_size)
                block_height = len(wrapped_lines) * (font_size + line_spacing)

                # Draw the whole paragraph block, letting Arcade handle its own wrapping
                arcade.draw_text(
                    text,
                    WINDOW_WIDTH // 2,
                    y,
                    (*arcade.color.WHITE[:3], int(alpha * 255)),
                    font_size=font_size,
                    width=max_width,
                    multiline=True,
                    anchor_x="center",
                    anchor_y="bottom"
                )
                # Advance y for the next block:
                y += block_height

    def on_update(self, dt):
        self._move_sprites(dt)
        self._fade_dialogue()

    def _move_sprites(self, dt):
        dx = (self.hero_movement["right"] - self.hero_movement["left"]) * PLAYER_SPEED * dt
        dy = (self.hero_movement["up"] - self.hero_movement["down"]) * PLAYER_SPEED * dt
        self.hero.center_x += dx
        self.hero.center_y += dy
        self.hero.update_animation(dx != 0 or dy != 0, dt)

        vdx = (self.villain_movement["right"] - self.villain_movement["left"]) * PLAYER_SPEED * dt
        vdy = (self.villain_movement["up"] - self.villain_movement["down"]) * PLAYER_SPEED * dt
        self.villain.center_x += vdx
        self.villain.center_y += vdy
        self.villain.update_animation(vdx != 0 or vdy != 0, dt)

    def _fade_dialogue(self):
        if self.fade_state == "fadein":
            self.dialogue_alpha += FADE_IN_SPEED
            if self.dialogue_alpha >= 1.0:
                self.dialogue_alpha = 1.0
                self.fade_state = "display"
                self.dialogue_timer = 0

        elif self.fade_state == "display":
            self.dialogue_timer += 1
            if self.dialogue_timer >= DIALOGUE_DISPLAY_TIME:
                self.fade_state = "fadeout"

        elif self.fade_state == "fadeout":
            self.dialogue_alpha -= FADE_OUT_SPEED
            if self.dialogue_alpha <= 0:
                self.dialogue_alpha = 0
                self.fade_state = "fadein"
                # Advance subtitle index
                self.current_line_start += self.max_subtitle_lines
                if self.current_line_start >= len(self.dialogue_lines):
                    self.current_line_start = 0
                self.current_line_end = min(self.current_line_start + self.max_subtitle_lines, len(self.dialogue_lines))


    def on_key_press(self, key, modifiers):
        mapping = {
            arcade.key.W: ("hero", "up"), arcade.key.S: ("hero", "down"),
            arcade.key.A: ("hero", "left"), arcade.key.D: ("hero", "right"),
            arcade.key.UP: ("villain", "up"), arcade.key.DOWN: ("villain", "down"),
            arcade.key.LEFT: ("villain", "left"), arcade.key.RIGHT: ("villain", "right")
        }
        if key == arcade.key.SPACE:
            self.current_line_start += self.max_subtitle_lines
            if self.current_line_start >= len(self.dialogue_lines):
                self.current_line_start = 0
            self.current_line_end = min(self.current_line_start + self.max_subtitle_lines, len(self.dialogue_lines))
            self.dialogue_alpha = 0
            self.fade_state = "fadein"
            self.dialogue_timer = 0
        if key in mapping:
            who, direction = mapping[key]
            if who == "hero":
                self.hero_movement[direction] = True
            else:
                self.villain_movement[direction] = True

    def on_key_release(self, key, modifiers):
        mapping = {
            arcade.key.W: ("hero", "up"), arcade.key.S: ("hero", "down"),
            arcade.key.A: ("hero", "left"), arcade.key.D: ("hero", "right"),
            arcade.key.UP: ("villain", "up"), arcade.key.DOWN: ("villain", "down"),
            arcade.key.LEFT: ("villain", "left"), arcade.key.RIGHT: ("villain", "right")
        }
        if key in mapping:
            who, direction = mapping[key]
            if who == "hero":
                self.hero_movement[direction] = False
            else:
                self.villain_movement[direction] = False

    def update_animations_based_on_text(self, text):
        text = text.lower()

        # Hero animation updates
        if "hero" in text:
            if any(k in text for k in ["walk", "move", "run", "forward"]):
                self.hero.set_state("walk")
            elif any(k in text for k in ["hurt", "injured", "damage"]):
                self.hero.set_state("hurt")
            else:
                self.hero.set_state("idle")
        else:
            self.hero.set_state("idle")

        # Villain animation updates
        if "villain" in text:
            if any(k in text for k in ["walk", "move", "run", "forward"]):
                self.villain.set_state("walk")
            elif any(k in text for k in ["hurt", "injured", "damage"]):
                self.villain.set_state("hurt")
            else:
                self.villain.set_state("idle")
        else:
            self.villain.set_state("idle")
