# main.py
from scene import Scene
from story_fetcher import get_groq_story
from story_window import StoryWindow
from animation_controller import AnimationController

if __name__ == "__main__":
    # For testing, you can uncomment the hardcoded version:
    story = [
        {"narrator": "In the heart of the Whispering Woods..."},
        {"hero": "I've been searching for you, Malakai!"},
        {"villain": "Ah, Eira. The chosen one. I've been expecting you."},
        {"narrator": "Eira drew her sword, its blade shimmering with light."}
    ]
    instructions = [
        {"character": "hero", "action": "walk", "direction": "right", "duration": 2},
        {"character": "villain", "action": "idle", "duration": 1.5},
        {"character": "hero", "action": "hurt", "duration": 1},
        {"character": "villain", "action": "walk", "direction": "left", "duration": 1.5}
    ]
    
    # Or use the API version (comment out the above when using this):
    # story, instructions = get_groq_story(
    #     "Write a peaceful fantasy scene in a forest with a hero and a villain, including dialogue."
    # )
    
    print("Story:", story)
    print("Instructions:", instructions)
    
    scene = Scene(
        background_layers=[
            ":resources:/images/miami_synth_parallax/layers/back.png",
            ":resources:/images/miami_synth_parallax/layers/buildings.png",
            ":resources:/images/miami_synth_parallax/layers/palms.png",
            ":resources:/images/miami_synth_parallax/layers/highway.png"
        ],
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
    
    import arcade
    arcade.run()