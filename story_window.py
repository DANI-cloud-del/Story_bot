# story_window.py
import arcade
import arcade.future.background as background
from settings import *
from character import CharacterSprite
from scene import Scene

class StoryWindow(arcade.Window):
    def __init__(self, scene: Scene):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Story Engine with Parallax", resizable=True)

        self.scene = scene
        self.background_color = (162, 84, 162, 255)
        self.camera = arcade.Camera2D()

        # Parallax backgrounds
        self.backgrounds = background.ParallaxGroup()
        bg_layer_size_px = (WINDOW_WIDTH, SCALED_BG_LAYER_HEIGHT_PX)
        depths = [10.0, 5.0, 3.0, 1.0]

        for path, depth in zip(self.scene.background_layers, depths):
            self.backgrounds.add_from_file(path, size=bg_layer_size_px, depth=depth, scale=PIXEL_SCALE)

        # Characters
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

        # Movement flags
        self.hero_movement = {"up": False, "down": False, "left": False, "right": False}
        self.villain_movement = {"up": False, "down": False, "left": False, "right": False}
        self.movement_speed = 200

        # Dialogue state
        self.current_line = 0
        self.dialogue_alpha = 0.0
        self.fade_state = "fadein"
        self.dialogue_timer = 0
        self.animation_controller = None
        self.animation_instructions = []
        self.current_instruction_index = 0
        self.instruction_timer = 0

    def pan_camera_to_player(self):
        target_x = self.hero.center_x
        target_y = self.height // 2
        self.camera.position = arcade.math.lerp_2d(self.camera.position, (target_x, target_y), CAMERA_SPEED)

    def draw_wrapped_text(self, text, center_x, start_y, max_width, font_size, alpha):
        """
        Draw text wrapped inside max_width with alpha transparency.
        It uses arcade.draw_text's built-in word wrapping (width param).
        Starts drawing from start_y and moves downward as text flows.
        """
        # arcade.draw_text automatically wraps text if given width
        arcade.draw_text(
            text,
            center_x - max_width // 2,  # correct argument: x
            start_y,                    # correct argument: y
            color=(*arcade.color.WHITE[:3], int(alpha * 255)),
            font_size=font_size,
            width=max_width,
            multiline=True,
            anchor_x="left"
        )


    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.backgrounds.offset = self.camera.bottom_left
            self.backgrounds.pos = self.camera.bottom_left

            with self.ctx.enabled(self.ctx.BLEND):
                self.backgrounds.draw()

            self.character_sprites.draw()

            # Draw wrapped dialogue text with fade alpha
            dialogue_text = list(self.scene.dialogue[self.current_line].values())[0]
            max_width = int(self.width * 0.8)
            # Start a little above bottom + font size * lines (approximate)
            start_y = 70
            self.draw_wrapped_text(dialogue_text, self.camera.position[0], start_y, max_width, 18, self.dialogue_alpha)


    def on_update(self, delta_time):
        # Movement
        self._handle_character_movement(delta_time)
        self.pan_camera_to_player()
        self._update_dialogue_fade()
        self._update_animations(delta_time)

    def _update_animations(self, delta_time):
        if not self.animation_controller or not self.animation_instructions:
            return
            
        if self.current_instruction_index >= len(self.animation_instructions):
            return
            
        current_instruction = self.animation_instructions[self.current_instruction_index]
        self.instruction_timer += delta_time
        
        if self.instruction_timer >= current_instruction.get("duration", 2):
            self.current_instruction_index += 1
            self.instruction_timer = 0
            if self.current_instruction_index < len(self.animation_instructions):
                next_instruction = self.animation_instructions[self.current_instruction_index]
                self.animation_controller.apply_instructions([next_instruction])

    def _handle_character_movement(self, dt):
        # Hero
        dx = (self.hero_movement["right"] - self.hero_movement["left"]) * self.movement_speed * dt
        dy = (self.hero_movement["up"] - self.hero_movement["down"]) * self.movement_speed * dt
        hero_moving = dx != 0 or dy != 0
        self.hero.center_x += dx
        self.hero.center_y += dy

        # Villain
        vdx = (self.villain_movement["right"] - self.villain_movement["left"]) * self.movement_speed * dt
        vdy = (self.villain_movement["up"] - self.villain_movement["down"]) * self.movement_speed * dt
        villain_moving = vdx != 0 or vdy != 0
        self.villain.center_x += vdx
        self.villain.center_y += vdy

        # Animate
        self.hero.update_animation(hero_moving, dt)
        self.villain.update_animation(villain_moving, dt)

    def _update_dialogue_fade(self):
        if self.fade_state == "fadein":
            self.dialogue_alpha += FADE_IN_SPEED
            if self.dialogue_alpha >= 1.0:
                self.fade_state = "display"
                self.dialogue_alpha = 1.0
                self.dialogue_timer = 0
        elif self.fade_state == "display":
            self.dialogue_timer += 1
            if self.dialogue_timer >= DIALOGUE_DISPLAY_TIME:
                self.fade_state = "fadeout"
        elif self.fade_state == "fadeout":
            self.dialogue_alpha -= FADE_OUT_SPEED
            if self.dialogue_alpha <= 0:
                self.fade_state = "fadein"
                self.dialogue_alpha = 0
                self.current_line = (self.current_line + 1) % len(self.scene.dialogue)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.current_line = (self.current_line + 1) % len(self.scene.dialogue)
            self.dialogue_alpha = 0.0
            self.fade_state = "fadein"
            self.dialogue_timer = 0
        if key == arcade.key.W: self.hero_movement["up"] = True
        elif key == arcade.key.S: self.hero_movement["down"] = True
        elif key == arcade.key.A: self.hero_movement["left"] = True
        elif key == arcade.key.D: self.hero_movement["right"] = True
        elif key == arcade.key.UP: self.villain_movement["up"] = True
        elif key == arcade.key.DOWN: self.villain_movement["down"] = True
        elif key == arcade.key.LEFT: self.villain_movement["left"] = True
        elif key == arcade.key.RIGHT: self.villain_movement["right"] = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W: self.hero_movement["up"] = False
        elif key == arcade.key.S: self.hero_movement["down"] = False
        elif key == arcade.key.A: self.hero_movement["left"] = False
        elif key == arcade.key.D: self.hero_movement["right"] = False
        elif key == arcade.key.UP: self.villain_movement["up"] = False
        elif key == arcade.key.DOWN: self.villain_movement["down"] = False
        elif key == arcade.key.LEFT: self.villain_movement["left"] = False
        elif key == arcade.key.RIGHT: self.villain_movement["right"] = False

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.camera.match_window()
        full_width_size = (width, SCALED_BG_LAYER_HEIGHT_PX)
        for layer, depth in self.backgrounds:
            layer.size = full_width_size
