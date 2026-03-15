# ClawQuest

> **RPG Gamification for AI Interactions**  
> Transform every conversation with your AI into character progression, loot drops, and quest rewards.

ClawQuest is an OpenClaw skill that adds an RPG game layer to your AI assistant experience. Level up by using your AI naturally, collect equipment with stat bonuses, complete quests, and watch your character grow stronger over time.

---

## 🎮 What is ClawQuest?

ClawQuest gamifies AI interactions with a full RPG system:

- **Six character classes** (Scholar, Artisan, Scout, Herald, Sage, Guardian)
- **Six attributes** mapped to AI capabilities (INT, CHA, WIS, DEX, CON, STR)
- **100 levels** with exponential XP progression
- **Equipment system** with 6 quality tiers and random affixes
- **Three quest types** (Disciplines, Dailies, Adventures)
- **Gold economy** for shops and upgrades
- **Streak bonuses** for consistent usage

**Important:** All game elements are purely cosmetic. They don't affect actual AI capabilities—they just make interactions more fun and rewarding!

---

## 🚀 Quick Start

### Installation

```bash
# Install via ClawHub (recommended)
clawub install clawquest

# Or manual installation
cd ~/.openclaw/skills/
git clone https://github.com/yourusername/claw-quest.git clawquest
```

### Create Your Character

```
/cq new
```

The AI will guide you through an "awakening ritual"—a short conversation to determine your ideal starting class.

### Start Playing

Just use your AI normally! Every conversation earns XP automatically. Use `/cq` to view your full character panel.

---

## 📖 Core Concepts

### Character Classes

| Class | Focus | Best For |
|-------|-------|----------|
| **Scholar** | Knowledge & Research | Q&A, learning, deep dives |
| **Artisan** | Creation & Craft | Coding, design, content creation |
| **Scout** | Intelligence & Analysis | Search, data analysis, debugging |
| **Herald** | Communication | Translation, writing, social media |
| **Sage** | Strategy & Planning | Architecture, decision support |
| **Guardian** | Endurance & Automation | Batch tasks, workflows, automation |

**Class Bonus:** +20% XP when using your class's primary attribute

### Six Attributes

- **INT (Intelligence)** — Knowledge depth, citation accuracy
- **CHA (Charisma)** — Language expression, social skills
- **WIS (Wisdom)** — Insight, logical reasoning
- **DEX (Dexterity)** — Craftsmanship, fine operations
- **CON (Constitution)** — Sustained stability, throughput
- **STR (Strength)** — Capacity for large tasks

### Leveling

- **Level 1→100** progression
- Each level grants **2 skill points** to allocate freely
- **XP sources**: Conversations (1-3), coding tasks (15-30), deep research (20-50), quests (10-80)
- **Streak bonuses**: 3 days (×1.2), 7 days (×1.5), 14 days (×1.8), 30 days (×2.0)

### Equipment

- **Four slots**: Weapon, Armor, Accessory, Mount
- **Six quality tiers**: Common (⬜), Uncommon (🟩), Rare (🟦), Epic (🟪), Legendary (🟧), Mythic (🟥)
- **Random affixes**: Primary (+3~+8) and secondary (+1~+4) stat bonuses
- **Drops from**: Quest completion, shop purchases, level milestones

---

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `/cq` | View full character panel |
| `/cq status` | One-line status bar |
| `/cq quest` | View all quests |
| `/cq inventory` | View backpack and equipped items |
| `/cq equip <item>` | Equip an item from inventory |
| `/cq shop` | Browse gold shop |
| `/cq allocate <stat> <points>` | Allocate skill points |
| `/cq adventure add <name> <xp> <quality>` | Create adventure quest |
| `/cq adventure done <name>` | Complete adventure and roll loot |
| `/cq daily add <name> <xp> <period>` | Create daily quest |
| `/cq daily done <name>` | Mark daily complete |
| `/cq discipline add <name> <xp>` | Create discipline |
| `/cq discipline + <name>` | Log positive discipline action |
| `/cq help` | Command reference |

---

## 📊 Quest System

### Disciplines (Repeatable Habits)

Track positive/negative behaviors, log each occurrence for XP.

```
/cq discipline add "Code review" 5
/cq discipline + "Code review"
```

### Daily Quests (Periodic Tasks)

Set up recurring tasks (daily/weekly). Missing them costs 50% of the reward XP.

```
/cq daily add "Morning code review" 15 daily
/cq daily done "Morning code review"
```

### Adventures (One-Time Goals)

Large objectives with equipment drops based on quest quality.

```
/cq adventure add "Refactor login module" 60 blue
/cq adventure done "Refactor login module"
```

Quest qualities (for loot drops): `green`, `blue`, `purple`, `orange`

---

## 🛠️ Technical Details

### Architecture

- **SKILL.md**: Core game rules injected into LLM system prompt
- **Python scripts**: Deterministic game engine (no LLM math)
- **State storage**: `~/.openclaw/skills/clawquest/data/character.json`
- **Zero dependencies**: Pure Python 3, no external packages

### File Structure

```
clawquest/
├── SKILL.md                  # LLM game rules (~15KB)
├── scripts/
│   ├── game_engine.py        # Core mechanics
│   ├── init_character.py     # Character creation
│   └── display.py            # Formatted output
├── references/
│   ├── classes.md            # Class definitions
│   ├── equipment.md          # Equipment tables
│   └── xp_curve.md           # Level progression
└── assets/
    └── character_template.json
```

### Design Principles

1. **Use = Growth** — Normal AI usage grants XP automatically
2. **Purely Cosmetic** — Game elements don't affect AI capabilities
3. **Deterministic** — All calculations in scripts, not LLM guessing
4. **Persistent** — State survives context compression
5. **Progressive** — New users see basics, advanced systems unlock later

---

## 🎨 Example Output

### Status Bar (Auto-displayed after responses)

```
⚔️ Lv.7 Scholar | XP 320/500 | INT 16(+4) CHA 8 WIS 15(+5) DEX 6 CON 12(+4) STR 4 | 💰85
```

### Full Character Panel (`/cq`)

```
╔══════════════════════════════════════════════════════════╗
║                   ⚔️ CLAWQUEST CHARACTER ⚔️              ║
╠══════════════════════════════════════════════════════════╣
║  Name: Awakened One                    Class: 学者 Scholar ║
║  Level: 7 (Apprentice)                 XP: 320 / 500     ║
║  Gold: 💰 85                           Streak: 🔥 5 days ║
╠══════════════════════════════════════════════════════════╣
║                    ⬡ ATTRIBUTE RADAR ⬡                   ║
╠══════════════════════════════════════════════════════════╣
║  INT ████████████████ 16 (+4)                            ║
║  CHA ████████         8                                  ║
║  WIS ███████████████  15 (+5)                            ║
║  DEX ██████           6                                  ║
║  CON ████████████     12 (+4)                            ║
║  STR ████             4                                  ║
╠══════════════════════════════════════════════════════════╣
║  Total: 61  |  Equipment Bonus: +13  |  Available: 2    ║
╠══════════════════════════════════════════════════════════╣
║                     🗡️ EQUIPMENT 🗡️                     ║
╠══════════════════════════════════════════════════════════╣
║  Weapon:    🟦 Prescient Starstaff of Clarity            ║
║             +5 WIS, +2 INT                               ║
║  Armor:     🟩 Stalwart Apprentice Robe                  ║
║             +4 CON                                       ║
║  Accessory: ⬜ Insight Necklace                          ║
║             +2 INT                                       ║
║  Mount:     (Empty)                                      ║
╚══════════════════════════════════════════════════════════╝
```

### Loot Drop Notification

```
✨ LOOT! Obtained 🟦 Prescient Starstaff of Clarity (+5 WIS, +2 INT)
   Use /cq equip Starstaff to equip, or /cq inventory to view backpack
```

---

## 🤝 Contributing

Contributions welcome! This is an open-source OpenClaw skill under MIT license.

**Areas for contribution:**
- Additional equipment affixes
- New quest types
- Balance adjustments
- Localization (currently EN/CN)
- Bug fixes

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Inspired by:
- [Habitica](https://habitica.com/) — Gamified habit tracking
- [agent-rpg](https://github.com/xhrisfu/agent-rpg) — OpenClaw RPG skill pioneer
- [clawville](https://github.com/jdrolls/clawville) — Persistent life sim skill

Built for the OpenClaw community.

---

**Ready to begin your adventure? Install ClawQuest and use `/cq new` to start!** ⚔️
