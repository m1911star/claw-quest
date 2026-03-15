#!/usr/bin/env python3
"""
ClawQuest Game Engine

Core mechanics: XP calculation, leveling, equipment generation, loot drops, stat management, quests.
All game logic runs through this deterministic engine to ensure consistency.
"""

import json
import os
import random
import math
from datetime import datetime, timedelta
from pathlib import Path


STAT_NAMES = ["INT", "CHA", "WIS", "DEX", "CON", "STR"]

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

QUALITY_TIERS = ["common", "uncommon", "rare", "epic", "legendary", "mythic"]

PREFIX_AFFIXES = {
    "INT": ("Erudite", "博学之"),
    "CHA": ("Eloquent", "雄辩之"),
    "WIS": ("Prescient", "先见之"),
    "DEX": ("Nimble", "灵巧之"),
    "CON": ("Stalwart", "坚毅之"),
    "STR": ("Mighty", "刚猛之")
}

SUFFIX_AFFIXES = {
    "INT": ("of Insight", "·洞察"),
    "CHA": ("of Grace", "·风雅"),
    "WIS": ("of Clarity", "·清明"),
    "DEX": ("of Craft", "·精工"),
    "CON": ("of Fortitude", "·坚韧"),
    "STR": ("of Valor", "·英勇")
}

BASE_ITEMS = {
    "weapon": ["Staff", "Wand", "Sword", "Hammer", "Bow", "Orb"],
    "armor": ["Robe", "Leather Armor", "Plate Armor", "Chainmail", "Cloak"],
    "accessory": ["Ring", "Amulet", "Necklace", "Bracelet"],
    "mount": ["Horse", "Griffin", "Dragon", "Phoenix", "Golem"]
}

QUEST_LOOT_DROP_RATES = {
    "green": {
        "common": 0.60,
        "uncommon": 0.35,
        "rare": 0.05,
        "epic": 0.00,
        "legendary": 0.00,
        "mythic": 0.00
    },
    "blue": {
        "common": 0.30,
        "uncommon": 0.40,
        "rare": 0.25,
        "epic": 0.05,
        "legendary": 0.00,
        "mythic": 0.00
    },
    "purple": {
        "common": 0.10,
        "uncommon": 0.25,
        "rare": 0.35,
        "epic": 0.25,
        "legendary": 0.05,
        "mythic": 0.00
    },
    "orange": {
        "common": 0.00,
        "uncommon": 0.10,
        "rare": 0.30,
        "epic": 0.40,
        "legendary": 0.20,
        "mythic": 0.00
    }
}


def get_character_path():
    home = Path.home()
    return home / ".openclaw" / "skills" / "clawquest" / "data" / "character.json"


def load_character():
    char_path = get_character_path()
    if not char_path.exists():
        return None
    
    try:
        with open(char_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Failed to load character: {e}"}))
        return None


def save_character(char):
    char_path = get_character_path()
    char_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(char_path, 'w', encoding='utf-8') as f:
            json.dump(char, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(json.dumps({"error": f"Failed to save character: {e}"}))
        return False


def xp_for_level(level):
    return math.floor(50 * (1.08 ** (level - 1)))


def cumulative_xp_for_level(level):
    return sum(xp_for_level(i) for i in range(1, level))


def calculate_level_from_xp(total_xp):
    level = 1
    while cumulative_xp_for_level(level + 1) <= total_xp:
        level += 1
    return level


def award_xp(amount, class_bonus=False):
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    old_xp = char.get("xp", 0)
    old_level = char.get("level", 1)
    
    if class_bonus:
        amount = int(amount * 1.2)
    
    streak_days = char.get("streak_days", 0)
    if streak_days >= 30:
        amount = int(amount * 2.0)
    elif streak_days >= 14:
        amount = int(amount * 1.8)
    elif streak_days >= 7:
        amount = int(amount * 1.5)
    elif streak_days >= 3:
        amount = int(amount * 1.2)
    
    new_xp = old_xp + amount
    char["xp"] = new_xp
    char["total_xp_earned"] = char.get("total_xp_earned", 0) + amount
    
    new_level = calculate_level_from_xp(new_xp)
    leveled_up = new_level > old_level
    
    skill_points_gained = 0
    gold_gained = 0
    
    if leveled_up:
        char["level"] = new_level
        levels_gained = new_level - old_level
        skill_points_gained = levels_gained * 2
        char["skill_points_available"] = char.get("skill_points_available", 0) + skill_points_gained
        
        gold_gained = new_level * 10
        char["gold"] = char.get("gold", 0) + gold_gained
    
    char["last_active"] = datetime.now().isoformat()[:10]
    char["total_conversations"] = char.get("total_conversations", 0) + 1
    
    save_character(char)
    
    result = {
        "xp_gained": amount,
        "old_xp": old_xp,
        "new_xp": new_xp,
        "leveled_up": leveled_up,
        "old_level": old_level,
        "new_level": new_level,
        "class_bonus_applied": class_bonus
    }
    
    if leveled_up:
        result["skill_points_gained"] = skill_points_gained
        result["gold_gained"] = gold_gained
    
    return result


def allocate(stat, points):
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    stat = stat.upper()
    if stat not in STAT_NAMES:
        return {"error": f"Invalid stat: {stat}. Must be one of {STAT_NAMES}"}
    
    try:
        points = int(points)
    except ValueError:
        return {"error": "Points must be a number"}
    
    available = char.get("skill_points_available", 0)
    if points > available:
        return {"error": f"Not enough skill points. Available: {available}, requested: {points}"}
    
    if points < 0:
        return {"error": "Cannot allocate negative points"}
    
    old_value = char["stats"]["base"].get(stat, 0)
    new_value = old_value + points
    
    char["stats"]["base"][stat] = new_value
    char["skill_points_available"] -= points
    
    recalculate_total_stats(char)
    
    save_character(char)
    
    return {
        "success": True,
        "stat": stat,
        "old_value": old_value,
        "new_value": new_value,
        "points_allocated": points,
        "remaining_points": char["skill_points_available"]
    }


def recalculate_total_stats(char):
    base_stats = char["stats"]["base"]
    bonus_stats = char["stats"]["equipment_bonus"]
    
    total_stats = {}
    for stat in STAT_NAMES:
        total_stats[stat] = base_stats.get(stat, 0) + bonus_stats.get(stat, 0)
    
    char["stats"]["total"] = total_stats


def generate_loot(quality, slot=None):
    if slot is None:
        slot = random.choice(["weapon", "armor", "accessory", "mount"])
    
    if slot not in BASE_ITEMS:
        return {"error": f"Invalid slot: {slot}"}
    
    if quality not in QUALITY_TIERS:
        return {"error": f"Invalid quality: {quality}"}
    
    base_name = random.choice(BASE_ITEMS[slot])
    
    quality_values = {
        "common": {"primary": 3, "secondary": 0},
        "uncommon": {"primary": 4, "secondary": 1},
        "rare": {"primary": 5, "secondary": 2},
        "epic": {"primary": 6, "secondary": 3},
        "legendary": {"primary": 7, "secondary": 4},
        "mythic": {"primary": 8, "secondary": 4}
    }
    
    values = quality_values[quality]
    
    primary_stat = random.choice(STAT_NAMES)
    prefix_en, prefix_cn = PREFIX_AFFIXES[primary_stat]
    
    prefix = {
        "name": prefix_en,
        "name_cn": prefix_cn,
        "stat": primary_stat,
        "value": values["primary"]
    }
    
    suffix = None
    suffix_en = ""
    suffix_cn = ""
    
    if quality != "common":
        secondary_stat = random.choice([s for s in STAT_NAMES if s != primary_stat])
        suffix_en, suffix_cn = SUFFIX_AFFIXES[secondary_stat]
        
        suffix = {
            "name": suffix_en,
            "name_cn": suffix_cn,
            "stat": secondary_stat,
            "value": values["secondary"]
        }
    
    if suffix:
        name = f"{prefix_en} {base_name} {suffix_en}"
        name_cn = f"{prefix_cn}{base_name}{suffix_cn}"
    else:
        name = f"{prefix_en} {base_name}"
        name_cn = f"{prefix_cn}{base_name}"
    
    item_id = f"{quality}_{prefix_en.lower().replace(' ', '_')}_{base_name.lower().replace(' ', '_')}"
    if suffix:
        item_id += f"_{suffix_en.lower().replace(' ', '_').replace('of_', '')}"
    
    item = {
        "id": item_id,
        "name": name,
        "name_cn": name_cn,
        "quality": quality,
        "slot": slot,
        "prefix": prefix,
        "suffix": suffix
    }
    
    return item


def equip(item_id):
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    inventory = char.get("inventory", [])
    item_to_equip = None
    item_index = None
    
    for i, item in enumerate(inventory):
        if item.get("id") == item_id or item.get("name") == item_id or item.get("name").lower().find(item_id.lower()) >= 0:
            item_to_equip = item
            item_index = i
            break
    
    if not item_to_equip:
        return {"error": f"Item not found in inventory: {item_id}"}
    
    slot = item_to_equip.get("slot")
    equipment = char.get("equipment", {})
    
    unequipped_item = equipment.get(slot)
    
    equipment[slot] = item_to_equip
    char["equipment"] = equipment
    
    inventory.pop(item_index)
    
    if unequipped_item:
        inventory.append(unequipped_item)
    
    char["inventory"] = inventory
    
    recalculate_equipment_bonuses(char)
    recalculate_total_stats(char)
    
    save_character(char)
    
    return {
        "success": True,
        "equipped": item_to_equip,
        "unequipped": unequipped_item,
        "stats_updated": True
    }


def unequip(slot):
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    equipment = char.get("equipment", {})
    item = equipment.get(slot)
    
    if not item:
        return {"error": f"No item equipped in slot: {slot}"}
    
    equipment[slot] = None
    char["equipment"] = equipment
    
    inventory = char.get("inventory", [])
    inventory.append(item)
    char["inventory"] = inventory
    
    recalculate_equipment_bonuses(char)
    recalculate_total_stats(char)
    
    save_character(char)
    
    return {
        "success": True,
        "unequipped": item,
        "stats_updated": True
    }


def recalculate_equipment_bonuses(char):
    equipment = char.get("equipment", {})
    bonus_stats = {stat: 0 for stat in STAT_NAMES}
    
    for slot in ["weapon", "armor", "accessory", "mount"]:
        item = equipment.get(slot)
        if item:
            prefix = item.get("prefix")
            if prefix:
                stat = prefix.get("stat")
                value = prefix.get("value", 0)
                bonus_stats[stat] += value
            
            suffix = item.get("suffix")
            if suffix:
                stat = suffix.get("stat")
                value = suffix.get("value", 0)
                bonus_stats[stat] += value
    
    char["stats"]["equipment_bonus"] = bonus_stats


def roll_loot(quest_quality):
    if quest_quality not in QUEST_LOOT_DROP_RATES:
        return {"error": f"Invalid quest quality: {quest_quality}"}
    
    rates = QUEST_LOOT_DROP_RATES[quest_quality]
    
    roll = random.random()
    cumulative = 0.0
    
    for quality in QUALITY_TIERS:
        cumulative += rates.get(quality, 0.0)
        if roll <= cumulative:
            item = generate_loot(quality)
            return {"dropped": True, "item": item, "quality_rolled": quality}
    
    return {"dropped": False}


def daily_check():
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    last_active = char.get("last_active", "")
    today = datetime.now().date()
    
    if last_active:
        last_date = datetime.fromisoformat(last_active).date()
        days_diff = (today - last_date).days
        
        if days_diff == 1:
            char["streak_days"] = char.get("streak_days", 0) + 1
        elif days_diff > 1:
            char["streak_days"] = 0
    
    dailies = char.get("quests", {}).get("dailies", [])
    expired = []
    xp_lost = 0
    
    for daily in dailies:
        if daily.get("done_today", False):
            daily["done_today"] = False
        else:
            penalty = int(daily.get("xp", 0) * 0.5)
            xp_lost += penalty
            expired.append(daily.get("name", "Unknown"))
            daily["streak"] = 0
    
    if xp_lost > 0:
        char["xp"] = max(0, char.get("xp", 0) - xp_lost)
    
    char["last_active"] = today.isoformat()
    
    save_character(char)
    
    return {
        "expired": expired,
        "xp_lost": xp_lost,
        "streak_days": char.get("streak_days", 0)
    }


def shop_buy(item_index):
    char = load_character()
    if not char:
        return {"error": "No character found"}
    
    shop_items = [
        {"quality": "common", "slot": "weapon", "price": 150},
        {"quality": "uncommon", "slot": "weapon", "price": 350},
        {"quality": "common", "slot": "armor", "price": 120},
        {"quality": "uncommon", "slot": "armor", "price": 300},
        {"quality": "common", "slot": "accessory", "price": 100},
        {"quality": "uncommon", "slot": "accessory", "price": 250}
    ]
    
    try:
        idx = int(item_index)
        if idx < 0 or idx >= len(shop_items):
            return {"error": f"Invalid item index: {idx}. Must be 0-{len(shop_items)-1}"}
    except ValueError:
        return {"error": "Item index must be a number"}
    
    shop_item = shop_items[idx]
    price = shop_item["price"]
    
    gold = char.get("gold", 0)
    if gold < price:
        return {"error": f"Not enough gold. Need {price}, have {gold}"}
    
    item = generate_loot(shop_item["quality"], shop_item["slot"])
    
    char["gold"] -= price
    char["inventory"].append(item)
    
    save_character(char)
    
    return {
        "success": True,
        "item": item,
        "price": price,
        "gold_remaining": char["gold"]
    }


def status():
    char = load_character()
    if not char:
        return "❌ No character found"
    
    from display import status_bar
    return status_bar(char)


def full_status():
    char = load_character()
    if not char:
        return "❌ No character found"
    
    from display import panel
    return panel(char)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 game_engine.py <command> [args...]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "award_xp":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: award_xp <amount> [--class-bonus]"}))
            sys.exit(1)
        amount = int(sys.argv[2])
        class_bonus = "--class-bonus" in sys.argv
        result = award_xp(amount, class_bonus)
        print(json.dumps(result))
    
    elif command == "allocate":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: allocate <STAT> <points>"}))
            sys.exit(1)
        stat = sys.argv[2]
        points = sys.argv[3]
        result = allocate(stat, points)
        print(json.dumps(result))
    
    elif command == "generate_loot":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: generate_loot <quality> [slot]"}))
            sys.exit(1)
        quality = sys.argv[2]
        slot = sys.argv[3] if len(sys.argv) > 3 else None
        result = generate_loot(quality, slot)
        print(json.dumps(result))
    
    elif command == "equip":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: equip <item_id>"}))
            sys.exit(1)
        item_id = sys.argv[2]
        result = equip(item_id)
        print(json.dumps(result))
    
    elif command == "unequip":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: unequip <slot>"}))
            sys.exit(1)
        slot = sys.argv[2]
        result = unequip(slot)
        print(json.dumps(result))
    
    elif command == "shop_buy":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: shop_buy <item_index>"}))
            sys.exit(1)
        item_index = sys.argv[2]
        result = shop_buy(item_index)
        print(json.dumps(result))
    
    elif command == "roll_loot":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: roll_loot <quest_quality>"}))
            sys.exit(1)
        quest_quality = sys.argv[2]
        result = roll_loot(quest_quality)
        print(json.dumps(result))
    
    elif command == "daily_check":
        result = daily_check()
        print(json.dumps(result))
    
    elif command == "status":
        print(status())
    
    elif command == "full_status":
        print(full_status())
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
