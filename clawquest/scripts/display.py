#!/usr/bin/env python3
import json
import math
import sys
from pathlib import Path

STAT_NAMES = ["INT", "CHA", "WIS", "DEX", "CON", "STR"]

CLASS_NAMES = {
    "scholar": "Scholar", "artisan": "Artisan", "scout": "Scout",
    "herald": "Herald", "sage": "Sage", "guardian": "Guardian"
}
CLASS_NAMES_CN = {
    "scholar": "学者", "artisan": "工匠", "scout": "斥候",
    "herald": "使者", "sage": "贤者", "guardian": "守护者"
}
CLASS_EMOJI = {
    "scholar": "📚", "artisan": "🔨", "scout": "🔍",
    "herald": "📜", "sage": "🔮", "guardian": "🛡️"
}
QUALITY_ICONS = {
    "common": "⬜", "uncommon": "🟩", "rare": "🟦",
    "epic": "🟪", "legendary": "🟧", "mythic": "🟥"
}
TIER_NAMES = {
    (1, 10): "Apprentice", (11, 25): "Traveler", (26, 50): "Master",
    (51, 99): "Legend", (100, 100): "Myth"
}


def get_char_path():
    return Path.home() / ".openclaw" / "skills" / "clawquest" / "data" / "character.json"


def load_character():
    p = get_char_path()
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def xp_for_level(lvl):
    return math.floor(50 * (1.08 ** (lvl - 1)))


def xp_progress(char):
    level = char.get("level", 1)
    total_xp = char.get("xp", 0)
    earned = sum(xp_for_level(i) for i in range(1, level))
    current = total_xp - earned
    needed = xp_for_level(level)
    return max(0, current), needed


def get_tier(level):
    for (lo, hi), name in TIER_NAMES.items():
        if lo <= level <= hi:
            return name
    return "Myth"


def xp_bar(current, total, width=10):
    filled = round(current / total * width) if total > 0 else 0
    return "▓" * filled + "░" * (width - filled)


def stat_bar(val, width=16):
    return "█" * min(val, width)


def status_bar(char=None):
    if char is None:
        char = load_character()
    if char is None:
        return "❌ No character. Use /cq new"

    level = char.get("level", 1)
    cls = char.get("class", "scholar")
    gold = char.get("gold", 0)
    cur, needed = xp_progress(char)
    stats = char.get("stats", {})
    base = stats.get("base", {})
    bonus = stats.get("equipment_bonus", {})

    stat_parts = []
    for s in STAT_NAMES:
        b = bonus.get(s, 0)
        stat_parts.append(f"{s}{base.get(s,0)}{'(+'+str(b)+')' if b else ''}")

    return (f"⚔️ Lv.{level} {CLASS_NAMES_CN[cls]} {CLASS_NAMES[cls]} · "
            f"XP {cur}/{needed} {xp_bar(cur, needed, 8)} · "
            f"{' '.join(stat_parts)} · 💰{gold}")


def panel(char=None):
    if char is None:
        char = load_character()
    if char is None:
        return "❌ No character. Use /cq new"

    name = char.get("name", "?")
    cls = char.get("class", "scholar")
    level = char.get("level", 1)
    gold = char.get("gold", 0)
    streak = char.get("streak_days", 0)
    avail = char.get("skill_points_available", 0)
    tier = get_tier(level)
    cur, needed = xp_progress(char)

    stats = char.get("stats", {})
    base = stats.get("base", {})
    bonus = stats.get("equipment_bonus", {})

    eq = char.get("equipment", {})

    lines = []
    lines.append(f"**⚔️ {name}** · Lv.{level} {CLASS_EMOJI.get(cls,'')} {CLASS_NAMES_CN[cls]} {CLASS_NAMES[cls]} · *{tier}*")
    lines.append(f"XP {cur}/{needed}  {xp_bar(cur, needed)}  💰{gold}  🔥{streak}天连击")
    if avail:
        lines.append(f"✨ 有 **{avail}** 个属性点待分配！用 `/cq allocate <属性> <点数>`")
    lines.append("")
    lines.append("**📊 属性**")

    for s in STAT_NAMES:
        bv = base.get(s, 0)
        bon = bonus.get(s, 0)
        total = bv + bon
        bar = stat_bar(total)
        bonus_str = f"  *(+{bon} 装备)*" if bon else ""
        lines.append(f"`{s}` {bar} **{total}**{bonus_str}")

    lines.append("")
    lines.append("**🗡️ 装备**")

    slots = [("🗡️ 武器", eq.get("weapon")),
             ("🛡️ 护甲", eq.get("armor")),
             ("💎 饰品", eq.get("accessory")),
             ("🐎 坐骑", eq.get("mount"))]

    for slot_label, item in slots:
        if item:
            qi = QUALITY_ICONS.get(item.get("quality", "common"), "")
            stat_parts = []
            if item.get("prefix"):
                stat_parts.append(f"+{item['prefix']['value']} {item['prefix']['stat']}")
            if item.get("suffix"):
                stat_parts.append(f"+{item['suffix']['value']} {item['suffix']['stat']}")
            lines.append(f"{slot_label}  {qi} **{item.get('name_cn') or item.get('name','')}**  {', '.join(stat_parts)}")
        else:
            lines.append(f"{slot_label}  —")

    return "\n".join(lines)


def equipment(char=None):
    if char is None:
        char = load_character()
    if char is None:
        return "❌ No character."

    eq = char.get("equipment", {})
    lines = ["**🗡️ 装备栏**", ""]

    slots = [("🗡️ 武器", eq.get("weapon")),
             ("🛡️ 护甲", eq.get("armor")),
             ("💎 饰品", eq.get("accessory")),
             ("🐎 坐骑", eq.get("mount"))]

    for slot_label, item in slots:
        if item:
            qi = QUALITY_ICONS.get(item.get("quality", "common"), "")
            stat_parts = []
            if item.get("prefix"):
                stat_parts.append(f"+{item['prefix']['value']} {item['prefix']['stat']}")
            if item.get("suffix"):
                stat_parts.append(f"+{item['suffix']['value']} {item['suffix']['stat']}")
            lines.append(f"{slot_label}  {qi} **{item.get('name_cn') or item.get('name','')}**  {', '.join(stat_parts)}")
        else:
            lines.append(f"{slot_label}  —")

    return "\n".join(lines)


def quests(char=None):
    if char is None:
        char = load_character()
    if char is None:
        return "❌ No character."

    q = char.get("quests", {})
    disciplines = q.get("disciplines", [])
    dailies = q.get("dailies", [])
    adventures = q.get("adventures", [])

    lines = ["**📜 任务日志**", ""]

    lines.append("**📿 修炼**（可重复习惯）")
    if disciplines:
        for d in disciplines:
            lines.append(f"  `[+]` {d['name']}  ×{d.get('count_positive',0)}次  (+{d['xp']} XP/次)")
    else:
        lines.append("  *暂无修炼*")

    lines.append("")
    lines.append("**📋 日常委托**")
    if dailies:
        for d in dailies:
            done = "✅" if d.get("done_today") else "⬜"
            lines.append(f"  {done} {d['name']}  +{d['xp']} XP  ({d.get('period','daily')})")
    else:
        lines.append("  *暂无日常委托*")

    lines.append("")
    lines.append("**🗡️ 冒险任务**")
    if adventures:
        for a in adventures:
            status_map = {"active": "🔵 进行中", "pending": "⏳ 待领取", "completed": "✅ 完成"}
            st = status_map.get(a.get("status","active"), a.get("status",""))
            qi = QUALITY_ICONS.get(a.get("loot_quality",""), "")
            lines.append(f"  {st} **{a['name']}**  {a['xp']} XP + {qi}装备")
    else:
        lines.append("  *暂无冒险任务*")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 display.py <panel|status_bar|equipment|quests>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "panel":
        print(panel())
    elif cmd == "status_bar":
        print(status_bar())
    elif cmd == "equipment":
        print(equipment())
    elif cmd == "quests":
        print(quests())
    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
