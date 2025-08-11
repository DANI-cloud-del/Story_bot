#!/usr/bin/env python3
import argparse
import os
import sys
import textwrap
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SceneConfig:
    characters: Dict[str, str]  # character_name: sprite_path
    background: str
    dialogue: List[Dict]  # List of {character: text} pairs

def parse_args():
    p = argparse.ArgumentParser(
        description="Story scene player engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--scene", type=str, required=True, help="Scene JSON file to load")
    p.add_argument("--out-dir", type=str, default="output", help="Output directory")
    p.add_argument("--visual", action="store_true", help="Enable visual rendering")
    p.add_argument("--fps", type=int, default=30, help="Frame rate for animation")
    return p.parse_args()

def load_scene_config(scene_path: str) -> SceneConfig:
    """Load and validate scene configuration"""
    try:
        with open(scene_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation
        required_keys = {'characters', 'background', 'dialogue'}
        if not all(k in data for k in required_keys):
            raise ValueError(f"Missing required keys in scene file: {required_keys - data.keys()}")
        
        return SceneConfig(
            characters=data['characters'],
            background=data['background'],
            dialogue=data['dialogue']
        )
    except Exception as e:
        logger.error(f"Failed to load scene: {str(e)}")
        raise

def render_scene_text(scene: SceneConfig):
    """Text-only scene rendering"""
    print("\n=== SCENE ===")
    for line in scene.dialogue:
        for character, text in line.items():
            print(f"\n{character.upper()}:")
            print(textwrap.fill(text, width=70))
    print("\n[Scene end]")

def ensure_outdir(path: str):
    """Ensure output directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def main():
    args = parse_args()
    
    try:
        # Load scene configuration
        scene = load_scene_config(args.scene)
        
        # Prepare output
        ensure_outdir(args.out_dir)
        
        # Simple text rendering
        render_scene_text(scene)
        
        # Optional visual rendering
        if args.visual:
            try:
                import arcade
                from visual_renderer import render_scene_visual
                render_scene_visual(scene, args.out_dir, args.fps)
            except ImportError:
                logger.warning("Arcade not available - skipping visual rendering")
        
        logger.info(f"Scene processing complete. Output in {args.out_dir}")
        
    except Exception as e:
        logger.error(f"Error processing scene: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()