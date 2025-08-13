# main.py
from scene import Scene
from story_fetcher import get_groq_story
from story_window import StoryWindow
from animation_controller import AnimationController

if __name__ == "__main__":
    story, instructions = get_groq_story(
        "Write a peaceful fantasy scene in a forest with a hero and a villain, including dialogue."
    )
    
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