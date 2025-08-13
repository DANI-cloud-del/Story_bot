import arcade
import random

class ResourceBank:
    # Character sprites
    CHARACTERS = {
        "hero": [
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{}.png"
        ],
        "villain": [
            ":resources:images/animated_characters/zombie/zombie_idle.png",
            ":resources:images/animated_characters/zombie/zombie_walk{}.png"
        ],
        "male_hero": [
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png",
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk{}.png"
        ],
        "robot": [
            ":resources:images/animated_characters/robot/robot_idle.png",
            ":resources:images/animated_characters/robot/robot_walk{}.png"
        ]
    }

    # Background sets
    BACKGROUND_SETS = {
        "abstract": [
            ":resources:images/backgrounds/abstract_1.jpg",
            ":resources:images/backgrounds/abstract_2.jpg"
        ],
        "space": [
            ":resources:images/backgrounds/stars.png"
        ],
        "cybercity": [
            ":resources:images/cybercity_background/far-buildings.png",
            ":resources:images/cybercity_background/back-buildings.png"
        ]
    }

    # Scene objects and tiles
    OBJECTS = {
        "tree": ":resources:images/tiles/treeGreen_large.png",
        "rock": ":resources:images/tiles/rock.png",
        "chest": ":resources:images/tiles/boxCrate_double.png",
        "sign": ":resources:images/tiles/signExit.png",
        "fountain": ":resources:images/tiles/water.png",
        "torch": ":resources:images/tiles/torch1.png",
        "bush": ":resources:images/tiles/bush.png",
        "ladder": ":resources:images/tiles/ladderMid.png",
        "coin_bronze": ":resources:images/items/coinBronze.png",
        "flag_green": ":resources:images/items/flagGreen1.png",
        "gem_blue": ":resources:images/items/gemBlue.png",
        "key_blue": ":resources:images/items/keyBlue.png",
        "switch_green": ":resources:images/tiles/switchGreen.png",
        "bomb": ":resources:images/tiles/bomb.png",
        "crate": ":resources:images/tiles/boxCrate.png",
        "bridge": ":resources:images/tiles/bridgeA.png",
        "cactus": ":resources:images/tiles/cactus.png",
        "mushroom": ":resources:images/tiles/mushroomRed.png"
    }

    # Sound effects
    SOUNDS = {
        "coin1": ":resources:sounds/coin1.wav",
        "explosion1": ":resources:sounds/explosion1.wav",
        "jump1": ":resources:sounds/jump1.wav",
        "hit1": ":resources:sounds/hit1.wav",
        "gameover1": ":resources:sounds/gameover1.wav",
        "laser1": ":resources:sounds/laser1.wav",
        "upgrade1": ":resources:sounds/upgrade1.wav",
        "error1": ":resources:sounds/error1.wav",
        "secret2": ":resources:sounds/secret2.wav",
        "fall1": ":resources:sounds/fall1.wav",
        "hurt1": ":resources:sounds/hurt1.wav",
        "lose1": ":resources:sounds/lose1.wav"
    }

    # Music tracks
    MUSIC = {
        "adventure": ":resources:music/1918.mp3",
        "scifi": ":resources:music/funkyrobot.mp3"
    }

    @classmethod
    def get_random_character(cls, role="hero"):
        """Get a random character for the specified role"""
        if role == "villain":
            options = ["villain", "robot"]
        else:
            options = ["hero", "male_hero"]
        
        char_type = random.choice(options)
        return cls.CHARACTERS.get(char_type, cls.CHARACTERS["hero"])

    @classmethod
    def get_random_objects(cls, count=3):
        """Get random scene objects"""
        return random.sample(list(cls.OBJECTS.items()), min(count, len(cls.OBJECTS)))

    @classmethod
    def get_background_set(cls, theme=None):
        """Get background layers for a theme"""
        if not theme or theme not in cls.BACKGROUND_SETS:
            theme = random.choice(list(cls.BACKGROUND_SETS.keys()))
        return cls.BACKGROUND_SETS.get(theme, cls.BACKGROUND_SETS["abstract"])

    @classmethod
    def get_random_sound(cls, category=None):
        """Get a random sound effect"""
        if category:
            sounds = {k:v for k,v in cls.SOUNDS.items() if category in k}
            if sounds:
                return random.choice(list(sounds.values()))
        return random.choice(list(cls.SOUNDS.values()))

    @classmethod
    def get_random_music(cls):
        """Get a random music track"""
        return random.choice(list(cls.MUSIC.values()))