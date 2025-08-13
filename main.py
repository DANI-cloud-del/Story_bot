# main.py (updated)
from scene import Scene
from story_fetcher import get_groq_story
from story_window import StoryWindow
from animation_controller import AnimationController
from resource_bank import ResourceBank
import random
import arcade
import subprocess  # Added this import

def generate_scene(story, instructions):
    """Create a scene using resources from ResourceBank"""
    return Scene(
        background_layers=ResourceBank.get_background_set(),
        dialogue=story,
        sprites={
            "hero": ResourceBank.get_random_character("hero")[0],
            "villain": ResourceBank.get_random_character("villain")[0]
        }
    )

if __name__ == "__main__":
    try:
        # Check audio dependencies first
        subprocess.run(["ffplay", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: ffplay not found. Please install ffmpeg package.")
        input("Press Enter to exit...")
        exit(1)

    # Check if music files exist
    if hasattr(ResourceBank, 'MUSIC'):
        for track, path in ResourceBank.MUSIC.items():
            if not arcade.resources.resolve(path):
                print(f"Warning: Music track '{track}' not found at {path}")

    try:  # Main execution block starts here
        # Generate dynamic story and matching animations
        story, instructions, music_instructions = get_groq_story()
        
        print("Generated Story:")
        for line in story:
            print(line)
        
        print("\nAnimation Instructions:")
        for cmd in instructions:
            print(cmd)
        
        print("\nMusic Instructions:")
        for cmd in music_instructions:
            print(cmd)
        
        scene = generate_scene(story, instructions)
        window = StoryWindow(scene)
        window.animation_controller = AnimationController(window.hero, window.villain)
        window.animation_instructions = instructions
        window.music_instructions = music_instructions
        window.current_instruction_index = 0
        window.instruction_timer = 0
        
        arcade.run()
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        if 'window' in locals():
            window.cleanup()
        input("Press Enter to exit...")