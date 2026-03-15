#!/usr/bin/env python3
"""
ClawQuest Display Module

Formats and renders character panels, status bars, equipment displays, and quest lists.
All output is UTF-8 formatted text with box-drawing characters.
"""

import json
import os
from pathlib import Path


# Constants
STAT_NAMES = ["INT", "CHA", "WIS", "DEX", "CON", "STR"]
STAT_NAMES_CN = {
    "INT": "智识",
    "CHA": "口才",
    "WIS": "洞察",
    "DEX": "创造",
    "CON": "效率",
    "STR": "毅力"
}

CLASS_NAMES = {
    "scholar": "Scholar",
    "artisan": "Artisan",
    "scout": "Scout",
    "herald": "Herald",
    "sage": "Sage",
    "guardian": "Guardian"
}

CLASS_NAMES_CN = {
    "scholar": "学者",
    "artisan": "工匠",
    "scout": "斥候",
    "herald": "使者",
    "sage": "贤者",
    "guardian": "守护者"
}

QUALITY_ICONS = {
    "common": "⬜",
    "uncommon": "🟩",
    "rare": "🟦",
    "epic": "🟪",
    "legendary": "🟧",
    "mythic": "🟥"
}


def get_character_path():
    """Get path to character.json file."""
    home = Path.home()
    return home / ".openclaw" / "skills" / "clawquest" / "data" / "character.json"


def load_character():
    """Load character data from JSON file."""
    char_path = get_character_path()
    if not char_path.exists():
        return None
    
    try:
        with open(char_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading character: {e}")
        return None


def render_stat_bar(stat_value, max_value=30):
    """Render a stat as a bar (each █ = 1 point)."""
    filled = "█" * stat_value
    return filled.ljust(max_value)[:max_value]


def status_bar(char=None):
    """
    Render one-line status bar.
    
    Format: ⚔️ Lv.7 Scholar | XP 320/500 | INT 16(+4) CHA 8 WIS 15(+5) DEX 6 CON 12(+4) STR 4 | 💰85
    """
    if char is None:
        char = load_character()
    
    if char is None:
        return "❌ No character found. Use /cq new to create one."
    
    # Calculate XP to next level
    import math
    def xp_for_level(level):
        return math.floor(50 * (1.08 ** (level - 1)))
    
    def cumulative_xp(level):
        return sum(xp_for_level(i) for i in range(1, level))
    
    current_xp = char.get("xp", 0)
    level = char.get("level", 1)
    next_level_total = cumulative_xp(level + 1)
    xp_needed = next_level_total - current_xp
    xp_for_this_level = xp_for_level(level)
    xp_progress = xp_for_this_level - xp_needed
    
    # Class name
    class_key = char.get("class", "scholar")
    class_name = CLASS_NAMES.get(class_key, "Unknown")
    
    # Stats with bonuses
    stats = char.get("stats", {})
    base_stats = stats.get("base", {})
    bonus_stats = stats.get("equipment_bonus", {})
    
    stat_parts = []
    for stat in STAT_NAMES:
        base_val = base_stats.get(stat, 0)
        bonus_val = bonus_stats.get(stat, 0)
        if bonus_val > 0:
            stat_parts.append(f"{stat} {base_val}(+{bonus_val})")
        else:
            stat_parts.append(f"{stat} {base_val}")
    
    stats_str = " ".join(stat_parts)
    
    gold = char.get("gold", 0)
    
    return f"⚔️ Lv.{level} {class_name} | XP {xp_progress}/{xp_for_this_level} | {stats_str} | 💰{gold}"


def panel(char=None):
    """
    Render full character panel with stats, equipment, and radar.
    """
    if char is None:
        char = load_character()
    
    if char is None:
        return "❌ No character found. Use /cq new to create one."
    
    # Header
    name = char.get("name", "Unknown")
    class_key = char.get("class", "scholar")
    class_name = CLASS_NAMES.get(class_key, "Unknown")
    class_name_cn = CLASS_NAMES_CN.get(class_key, "")
    level = char.get("level", 1)
    xp = char.get("xp", 0)
    gold = char.get("gold", 0)
    streak = char.get("streak_days", 0)
    
    # Calculate XP progress
    import math
    def xp_for_level(lvl):
        return math.floor(50 * (1.08 ** (lvl - 1)))
    
    def cumulative_xp(lvl):
        return sum(xp_for_level(i) for i in range(1, lvl))
    
    next_level_total = cumulative_xp(level + 1)
    xp_needed = next_level_total - xp
    xp_for_this_level = xp_for_level(level)
    xp_progress = xp_for_this_level - xp_needed
    
    # Tier
    if level <= 10:
        tier = "Apprentice"
    elif level <= 25:
        tier = "Traveler"
    elif level <= 50:
        tier = "Master"
    elif level <= 99:
        tier = "Legend"
    else:
        tier = "Myth"
    
    # Stats
    stats = char.get("stats", {})
    base_stats = stats.get("base", {})
    bonus_stats = stats.get("equipment_bonus", {})
    total_stats = stats.get("total", {})
    available_points = char.get("skill_points_available", 0)
    
    # Equipment
    equipment = char.get("equipment", {})
    weapon = equipment.get("weapon")
    armor = equipment.get("armor")
    accessory = equipment.get("accessory")
    mount = equipment.get("mount")
    
    # Build panel
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║                   ⚔️ CLAWQUEST CHARACTER ⚔️              ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    lines.append(f"║  Name: {name:<30} Class: {class_name_cn} {class_name:<8} ║")
    lines.append(f"║  Level: {level} ({tier}){' ' * (30 - len(str(level)) - len(tier))} XP: {xp_progress} / {xp_for_this_level}{' ' * (5 - len(str(xp_for_this_level)))} ║")
    lines.append(f"║  Gold: 💰 {gold:<28} Streak: 🔥 {streak} days{' ' * (5 - len(str(streak)))} ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    lines.append("║                    ⬡ ATTRIBUTE RADAR ⬡                   ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    for stat in STAT_NAMES:
        base_val = base_stats.get(stat, 0)
        bonus_val = bonus_stats.get(stat, 0)
        total_val = total_stats.get(stat, 0)
        bar = render_stat_bar(total_val)
        
        if bonus_val > 0:
            stat_display = f"{stat} {bar} {total_val} (+{bonus_val})"
        else:
            stat_display = f"{stat} {bar} {total_val}"
        
        lines.append(f"║  {stat_display:<56} ║")
    
    total_base = sum(base_stats.values())
    total_bonus = sum(bonus_stats.values())
    
    lines.append("╠══════════════════════════════════════════════════════════╣")
    lines.append(f"║  Total: {total_base}  |  Equipment Bonus: +{total_bonus}  |  Available: {available_points}{' ' * (4 - len(str(available_points)))} ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    lines.append("║                     🗡️ EQUIPMENT 🗡️                     ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    # Weapon
    if weapon:
        quality_icon = QUALITY_ICONS.get(weapon.get("quality", "common"), "")
        weapon_name = weapon.get("name", "Unknown")
        weapon_stats = []
        if weapon.get("prefix"):
            weapon_stats.append(f"+{weapon['prefix']['value']} {weapon['prefix']['stat']}")
        if weapon.get("suffix"):
            weapon_stats.append(f"+{weapon['suffix']['value']} {weapon['suffix']['stat']}")
        weapon_stats_str = ", ".join(weapon_stats)
        lines.append(f"║  Weapon:    {quality_icon} {weapon_name:<44} ║")
        lines.append(f"║             {weapon_stats_str:<44} ║")
    else:
        lines.append("║  Weapon:    (Empty)                                      ║")
    
    # Armor
    if armor:
        quality_icon = QUALITY_ICONS.get(armor.get("quality", "common"), "")
        armor_name = armor.get("name", "Unknown")
        armor_stats = []
        if armor.get("prefix"):
            armor_stats.append(f"+{armor['prefix']['value']} {armor['prefix']['stat']}")
        if armor.get("suffix"):
            armor_stats.append(f"+{armor['suffix']['value']} {armor['suffix']['stat']}")
        armor_stats_str = ", ".join(armor_stats)
        lines.append(f"║  Armor:     {quality_icon} {armor_name:<44} ║")
        lines.append(f"║             {armor_stats_str:<44} ║")
    else:
        lines.append("║  Armor:     (Empty)                                      ║")
    
    # Accessory
    if accessory:
        quality_icon = QUALITY_ICONS.get(accessory.get("quality", "common"), "")
        acc_name = accessory.get("name", "Unknown")
        acc_stats = []
        if accessory.get("prefix"):
            acc_stats.append(f"+{accessory['prefix']['value']} {accessory['prefix']['stat']}")
        if accessory.get("suffix"):
            acc_stats.append(f"+{accessory['suffix']['value']} {accessory['suffix']['stat']}")
        acc_stats_str = ", ".join(acc_stats)
        lines.append(f"║  Accessory: {quality_icon} {acc_name:<44} ║")
        lines.append(f"║             {acc_stats_str:<44} ║")
    else:
        lines.append("║  Accessory: (Empty)                                      ║")
    
    # Mount
    if mount:
        quality_icon = QUALITY_ICONS.get(mount.get("quality", "common"), "")
        mount_name = mount.get("name", "Unknown")
        mount_stats = []
        if mount.get("prefix"):
            mount_stats.append(f"+{mount['prefix']['value']} {mount['prefix']['stat']}")
        if mount.get("suffix"):
            mount_stats.append(f"+{mount['suffix']['value']} {mount['suffix']['stat']}")
        mount_stats_str = ", ".join(mount_stats)
        lines.append(f"║  Mount:     {quality_icon} {mount_name:<44} ║")
        lines.append(f"║             {mount_stats_str:<44} ║")
    else:
        lines.append("║  Mount:     (Empty)                                      ║")
    
    lines.append("╚══════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


def equipment(char=None):
    """Render equipment panel only."""
    if char is None:
        char = load_character()
    
    if char is None:
        return "❌ No character found."
    
    equipment_data = char.get("equipment", {})
    weapon = equipment_data.get("weapon")
    armor = equipment_data.get("armor")
    accessory = equipment_data.get("accessory")
    mount = equipment_data.get("mount")
    
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║                     🗡️ EQUIPMENT 🗡️                     ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    for slot_name, item in [("Weapon", weapon), ("Armor", armor), ("Accessory", accessory), ("Mount", mount)]:
        if item:
            quality_icon = QUALITY_ICONS.get(item.get("quality", "common"), "")
            item_name = item.get("name", "Unknown")
            item_stats = []
            if item.get("prefix"):
                item_stats.append(f"+{item['prefix']['value']} {item['prefix']['stat']}")
            if item.get("suffix"):
                item_stats.append(f"+{item['suffix']['value']} {item['suffix']['stat']}")
            item_stats_str = ", ".join(item_stats)
            lines.append(f"║  {slot_name:<11} {quality_icon} {item_name:<40} ║")
            lines.append(f"║             {item_stats_str:<44} ║")
        else:
            lines.append(f"║  {slot_name:<11} (Empty){' ' * 40} ║")
    
    lines.append("╚══════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


def quests(char=None):
    """Render quest log (disciplines, dailies, adventures)."""
    if char is None:
        char = load_character()
    
    if char is None:
        return "❌ No character found."
    
    quests_data = char.get("quests", {})
    disciplines = quests_data.get("disciplines", [])
    dailies = quests_data.get("dailies", [])
    adventures = quests_data.get("adventures", [])
    
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║                      📜 QUEST LOG 📜                      ║")
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    # Disciplines
    lines.append("║  📿 DISCIPLINES (Repeatable Habits)                      ║")
    if disciplines:
        for disc in disciplines:
            name = disc.get("name", "Unknown")
            xp = disc.get("xp", 0)
            count_pos = disc.get("count_positive", 0)
            count_neg = disc.get("count_negative", 0)
            if count_neg > 0:
                lines.append(f"║    [+/-] {name:<35} {count_pos}/{count_neg} times  ║")
            else:
                lines.append(f"║    [+] {name:<38} {count_pos} times  (+{xp} XP) ║")
    else:
        lines.append("║    (No disciplines yet)                                  ║")
    
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    # Dailies
    lines.append("║  📋 DAILY QUESTS (Periodic)                              ║")
    if dailies:
        for daily in dailies:
            name = daily.get("name", "Unknown")
            xp = daily.get("xp", 0)
            period = daily.get("period", "daily")
            done = daily.get("done_today", False)
            streak = daily.get("streak", 0)
            status = "✓" if done else " "
            lines.append(f"║    [{status}] {name:<35} +{xp} XP ({period}) ║")
    else:
        lines.append("║    (No daily quests yet)                                 ║")
    
    lines.append("╠══════════════════════════════════════════════════════════╣")
    
    # Adventures
    lines.append("║  🗡️ ADVENTURES (One-Time Goals)                         ║")
    if adventures:
        for adv in adventures:
            name = adv.get("name", "Unknown")
            xp = adv.get("xp", 0)
            quality = adv.get("loot_quality", "green")
            status = adv.get("status", "active")
            status_label = status.capitalize()
            lines.append(f"║    [{status_label:<8}] {name:<30} {xp} XP + {quality} loot ║")
    else:
        lines.append("║    (No adventures yet)                                   ║")
    
    lines.append("╚══════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


def main():
    """Command-line interface for display module."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 display.py <command>")
        print("Commands: panel, status_bar, equipment, quests")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "panel":
        print(panel())
    elif command == "status_bar":
        print(status_bar())
    elif command == "equipment":
        print(equipment())
    elif command == "quests":
        print(quests())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
