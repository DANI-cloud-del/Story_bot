# main.py
from scene import Scene
from story_fetcher import get_groq_story
from story_window import StoryWindow
from animation_controller import AnimationController
import random
import arcade

def generate_valid_backgrounds():
    """Returns only background paths that exist in arcade resources"""
    options = [
        [  # Miami theme
            ":resources:/images/miami_synth_parallax/layers/back.png",
            ":resources:/images/miami_synth_parallax/layers/buildings.png",
            ":resources:/images/miami_synth_parallax/layers/palms.png"
        ],
        [  # Simple color backgrounds
            ":resources:/images/blue_square.png",
            ":resources:/images/green_square.png"
        ]
    ]
    return random.choice(options)

if __name__ == "__main__":
    try:
        # Generate dynamic story and matching animations
        story, instructions = get_groq_story()
        
        print("Generated Story:")
        for line in story:
            print(line)
        
        print("\nAnimation Instructions:")
        for cmd in instructions:
            print(cmd)
        
        scene = Scene(
            background_layers=generate_valid_backgrounds(),
            dialogue=story,
            sprites={
                "hero": ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                "villain": ":resources:images/animated_characters/zombie/zombie_idle.png"
            }
        )

        window = StoryWindow(scene)
        window.animation_controller = AnimationController(window.hero, window.villain)
        window.animation_instructions = instructions
        window.current_instruction_index = 0
        window.instruction_timer = 0
        
        arcade.run()
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        input("Press Enter to exit...")