# scene.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Scene:
    background_layers: List[str]
    dialogue: List[Dict[str, str]]
    sprites: Dict[str, str]
