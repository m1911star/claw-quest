# ClawQuest Equipment Reference

This document defines all equipment mechanics, affixes, and generation rules.

---

## 🗡️ Equipment Slots

### Weapon (武器)
- **Icon:** 🗡️
- **Primary Stats:** Class-dependent (INT for Scholar, DEX for Artisan, etc.)
- **Appearance:** Class-specific (staffs for Scholar, hammers for Guardian, etc.)
- **Acquisition:** Quest rewards, shop, level milestones

### Armor (护甲)
- **Icon:** 🛡️
- **Primary Stats:** CON, STR (defensive)
- **Appearance:** Robes, plate, leather based on stats
- **Acquisition:** Quest rewards, shop, level milestones

### Accessory (饰品)
- **Icon:** 💎
- **Primary Stats:** CHA, WIS (support)
- **Appearance:** Rings, amulets, necklaces
- **Acquisition:** Quest rewards, shop, level milestones

### Mount (坐骑)
- **Icon:** 🐎
- **Primary Stats:** DEX, INT (special)
- **Appearance:** Various creatures
- **Acquisition:** Rare drops only (no shop)

---

## 🎨 Quality Tiers

| Quality | Icon | Affixes | Stat Range | Drop Rate (Base) |
|---------|------|---------|------------|------------------|
| **Common** | ⬜ | 1 primary | 1-3 | 40% |
| **Uncommon** | 🟩 | 1 primary + 1 secondary | 4-7 | 30% |
| **Rare** | 🟦 | 1 primary + 1 secondary | 8-12 | 15% |
| **Epic** | 🟪 | 1 primary + 2 secondary | 13-18 | 10% |
| **Legendary** | 🟧 | 2 primary + 1 secondary | 19-24 | 4% |
| **Mythic** | 🟥 | 2 primary + 1 secondary + passive | 25-30 | 1% |

**Note:** Drop rates modified by quest quality tier and character level.

---

## 📝 Affix System

### Primary Affixes (Prefix)

Primary affixes appear at the **start** of item names and grant **+3 to +8** to a primary stat.

| English | 中文 | Stat | Value Range |
|---------|------|------|-------------|
| **Erudite** | 博学之 | INT | +3 to +8 |
| **Eloquent** | 雄辩之 | CHA | +3 to +8 |
| **Prescient** | 先见之 | WIS | +3 to +8 |
| **Nimble** | 灵巧之 | DEX | +3 to +8 |
| **Stalwart** | 坚毅之 | CON | +3 to +8 |
| **Mighty** | 刚猛之 | STR | +3 to +8 |

**Value by Quality:**
- Common: +3
- Uncommon: +4
- Rare: +5
- Epic: +6
- Legendary: +7
- Mythic: +8

### Secondary Affixes (Suffix)

Secondary affixes appear at the **end** of item names and grant **+1 to +4** to a secondary stat.

| English | 中文 | Stat | Value Range |
|---------|------|------|-------------|
| **of Insight** | ·洞察 | INT | +1 to +4 |
| **of Grace** | ·风雅 | CHA | +1 to +4 |
| **of Clarity** | ·清明 | WIS | +1 to +4 |
| **of Craft** | ·精工 | DEX | +1 to +4 |
| **of Fortitude** | ·坚韧 | CON | +1 to +4 |
| **of Valor** | ·英勇 | STR | +1 to +4 |

**Value by Quality:**
- Uncommon: +1
- Rare: +2
- Epic: +3
- Legendary: +4
- Mythic: +4

### Passive Abilities (Mythic Only)

Mythic equipment has an additional passive ability (cosmetic flavor text):

- **"Oracle's Vision"** — Critical insight moments (WIS items)
- **"Midas Touch"** — Bonus gold from quests (CHA items)
- **"Perfect Precision"** — Flawless execution (DEX items)
- **"Endless Stamina"** — Never tire in long sessions (CON items)
- **"Titan's Grasp"** — Handle massive tasks (STR items)
- **"Infinite Library"** — Access to vast knowledge (INT items)

**Note:** Passives are purely flavor — no mechanical effect.

---

## 🎲 Equipment Generation Rules

### Base Item Names by Slot

**Weapons:**
- Staff (INT/WIS focus)
- Wand (INT focus)
- Sword (STR/DEX focus)
- Hammer (STR/CON focus)
- Bow (DEX/WIS focus)
- Orb (CHA/WIS focus)

**Armor:**
- Robe (INT/WIS focus)
- Leather Armor (DEX/WIS focus)
- Plate Armor (STR/CON focus)
- Chainmail (CON/DEX focus)
- Cloak (CHA/WIS focus)

**Accessories:**
- Ring (any stat)
- Amulet (any stat)
- Necklace (any stat)
- Bracelet (any stat)

**Mounts:**
- Horse (balanced)
- Griffin (DEX/WIS)
- Dragon (STR/INT)
- Phoenix (CHA/WIS)
- Golem (CON/STR)

### Generation Algorithm

1. **Determine Quality** (from quest tier or shop)
2. **Select Base Item** (random from slot-appropriate list)
3. **Assign Primary Affix** (weighted by slot preference)
4. **Assign Secondary Affix(es)** (based on quality, avoid duplicates)
5. **Roll Stat Values** (within quality range)
6. **Generate ID** (format: `quality_prefix_basename_suffix`)
7. **Construct Display Name** (format: `Prefix Base Suffix`)

**Example:**
```json
{
  "id": "rare_prescient_starstaff_clarity",
  "name": "Prescient Starstaff of Clarity",
  "name_cn": "先见之星辰杖·清明",
  "quality": "rare",
  "slot": "weapon",
  "prefix": {
    "name": "Prescient",
    "name_cn": "先见之",
    "stat": "WIS",
    "value": 5
  },
  "suffix": {
    "name": "of Clarity",
    "name_cn": "·清明",
    "stat": "INT",
    "value": 2
  }
}
```

---

## 🛒 Shop Equipment

The gold shop sells **Common** and **Uncommon** quality items only.

### Shop Inventory (Refreshes Weekly)

| Slot | Quality | Price Range | Example |
|------|---------|-------------|---------|
| Weapon | Common | 150-200 | ⬜ Erudite Wand (+3 INT) |
| Weapon | Uncommon | 300-400 | 🟩 Nimble Sword of Valor (+4 DEX, +1 STR) |
| Armor | Common | 100-150 | ⬜ Stalwart Robe (+3 CON) |
| Armor | Uncommon | 250-350 | 🟩 Mighty Plate of Fortitude (+4 STR, +1 CON) |
| Accessory | Common | 100-150 | ⬜ Ring of Insight (+2 INT) |
| Accessory | Uncommon | 200-300 | 🟩 Eloquent Amulet of Grace (+4 CHA, +1 CHA) |

**Shop Refresh:** Every Monday (real-world time)

**Purchase Limit:** No limit (as long as you have gold)

---

## 🎁 Quest Loot Drop Tables

Drop quality determined by quest tier marker.

### Green Quest Loot Table

| Quality | Chance |
|---------|--------|
| Common (⬜) | 60% |
| Uncommon (🟩) | 35% |
| Rare (🟦) | 5% |
| Epic+ | 0% |

### Blue Quest Loot Table

| Quality | Chance |
|---------|--------|
| Common (⬜) | 30% |
| Uncommon (🟩) | 40% |
| Rare (🟦) | 25% |
| Epic (🟪) | 5% |
| Legendary+ | 0% |

### Purple Quest Loot Table

| Quality | Chance |
|---------|--------|
| Common (⬜) | 10% |
| Uncommon (🟩) | 25% |
| Rare (🟦) | 35% |
| Epic (🟪) | 25% |
| Legendary (🟧) | 5% |

### Orange Quest Loot Table

| Quality | Chance |
|---------|--------|
| Common (⬜) | 0% |
| Uncommon (🟩) | 10% |
| Rare (🟦) | 30% |
| Epic (🟪) | 40% |
| Legendary (🟧) | 20% |

### Mythic Drops

Mythic (🟥) equipment can only drop from:
- **Level 100 milestone reward** (guaranteed 1x)
- **Orange quests with level 80+** (1% chance)

---

## 🏆 Level Milestone Equipment

Fixed rewards at specific levels (always received):

| Level | Item | Stats |
|-------|------|-------|
| **10** | 🟦 Apprentice's Blade | +5 to class primary, +2 to class secondary |
| **25** | 🟪 Traveler's Aegis | +6 CON, +3 STR, +2 WIS |
| **50** | 🟧 Master's Pendant | +7 to class primary, +4 CHA, +3 WIS |
| **75** | 🟧 Legend's Regalia | +8 to 2 highest stats, +3 to 3rd highest |
| **100** | 🟥 Mythic Crown | +10 all stats + passive ability |

---

## 🔄 Equip/Unequip Mechanics

### Equipping

1. Item must be in inventory
2. Item slot must match (weapon → weapon slot)
3. No level requirements (all items equippable at any level)
4. Auto-unequips current item in that slot (goes to inventory)
5. Stat bonuses recalculated immediately

### Unequipping

1. Item moved from equipment slot to inventory
2. Stat bonuses removed
3. Slot shows as empty

### Inventory Limit

**No limit** — collect as much as you want (it's cosmetic!)

---

## 📊 Equipment Stat Priority by Slot

**Script Generation Hint:** When generating random equipment, weight affixes by these preferences:

### Weapon
- **Primary:** Class primary attribute
- **Secondary:** Class secondary attribute

### Armor
- **Primary:** CON (40%), STR (30%), other (30%)
- **Secondary:** WIS, DEX

### Accessory
- **Primary:** CHA (40%), WIS (30%), other (30%)
- **Secondary:** INT, DEX

### Mount (Rare)
- **Primary:** DEX (40%), INT (30%), WIS (30%)
- **Secondary:** Any

---

## 🎭 Flavor Text Examples

Equipment can have optional flavor descriptions (LLM can improvise):

> **Erudite Starstaff of Clarity**  
> _"Forged in the archives of the Eternal Library, this staff channels the wisdom of a thousand scholars."_

> **Mighty Dragonplate of Fortitude**  
> _"Scales from an ancient wyrm, tempered in volcanic fire. Its bearer knows no fatigue."_

> **Prescient Phoenix of Grace**  
> _"This ethereal mount sees paths before they form, guiding its rider through the currents of fate."_

**LLM:** Feel free to generate flavor text when displaying equipment details!

---

## 🧮 Stat Calculation Formula

```
Total Stat = Base Stat + Equipment Bonus

Equipment Bonus = Sum of all equipped item bonuses for that stat
```

**Example:**

```
Character Base INT: 12

Equipped Items:
- Weapon: +5 INT, +2 WIS
- Armor: +0 INT
- Accessory: +3 INT
- Mount: (empty)

Total INT = 12 + (5 + 0 + 3 + 0) = 20

Display: "INT 20 (+8)"
```

---

## 🎯 Implementation Notes for Scripts

### generate_loot Function

```python
def generate_loot(quality: str, slot: str = None) -> dict:
    """
    Generate a random equipment item.
    
    Args:
        quality: "common", "uncommon", "rare", "epic", "legendary", "mythic"
        slot: "weapon", "armor", "accessory", "mount" (optional, random if None)
    
    Returns:
        Equipment dict with id, name, quality, slot, prefix, suffix, (passive)
    """
```

### roll_loot Function

```python
def roll_loot(quest_quality: str) -> dict:
    """
    Roll for loot drop based on quest quality.
    
    Args:
        quest_quality: "green", "blue", "purple", "orange"
    
    Returns:
        {"dropped": bool, "item": dict or None}
    """
```

### equip Function

```python
def equip(item_id: str) -> dict:
    """
    Equip an item from inventory.
    
    Returns:
        {
            "success": bool,
            "equipped": dict (newly equipped item),
            "unequipped": dict or None (previously equipped item),
            "stats_updated": bool
        }
    """
```

---

**This reference should be used by `game_engine.py` for all equipment generation and management!**
