#!/usr/bin/env python3
"""
ClawQuest Character Initialization

Creates a new character with starting class and name.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


CLASS_PRIMARY = {
    "scholar": "INT",
    "artisan": "DEX",
    "scout": "WIS",
    "herald": "CHA",
    "sage": "WIS",
    "guardian": "CON"
}

CLASS_SECONDARY = {
    "scholar": "WIS",
    "artisan": "INT",
    "scout": "DEX",
    "herald": "WIS",
    "sage": "INT",
    "guardian": "STR"
}

VALID_CLASSES = list(CLASS_PRIMARY.keys())


def get_character_path():
    home = Path.home()
    return home / ".openclaw" / "skills" / "clawquest" / "data" / "character.json"


def create_character(class_name, character_name):
    if class_name not in VALID_CLASSES:
        return {
            "error": f"Invalid class: {class_name}. Must be one of {VALID_CLASSES}"
        }
    
    primary_stat = CLASS_PRIMARY[class_name]
    secondary_stat = CLASS_SECONDARY[class_name]
    
    base_stats = {
        "INT": 4,
        "CHA": 4,
        "WIS": 4,
        "DEX": 4,
        "CON": 4,
        "STR": 4
    }
    
    base_stats[primary_stat] = 8
    base_stats[secondary_stat] = 6
    
    character = {
        "version": 1,
        "name": character_name,
        "class": class_name,
        "level": 1,
        "xp": 0,
        "skill_points_available": 0,
        "stats": {
            "base": base_stats,
            "equipment_bonus": {
                "INT": 0,
                "CHA": 0,
                "WIS": 0,
                "DEX": 0,
                "CON": 0,
                "STR": 0
            },
            "total": base_stats.copy()
        },
        "equipment": {
            "weapon": None,
            "armor": None,
            "accessory": None,
            "mount": None
        },
        "inventory": [],
        "quests": {
            "disciplines": [],
            "dailies": [],
            "adventures": []
        },
        "gold": 0,
        "streak_days": 0,
        "last_active": datetime.now().isoformat()[:10],
        "total_conversations": 0,
        "total_xp_earned": 0,
        "created_at": datetime.now().isoformat()[:10],
        "quiet_mode": False
    }
    
    char_path = get_character_path()
    char_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(char_path, 'w', encoding='utf-8') as f:
            json.dump(character, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "character": character,
            "path": str(char_path)
        }
    
    except Exception as e:
        return {
            "error": f"Failed to create character: {e}"
        }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python3 init_character.py <class> <name>",
            "valid_classes": VALID_CLASSES
        }))
        sys.exit(1)
    
    class_name = sys.argv[1].lower()
    character_name = " ".join(sys.argv[2:])
    
    result = create_character(class_name, character_name)
    print(json.dumps(result, indent=2))
    
    if result.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
