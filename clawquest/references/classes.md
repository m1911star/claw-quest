# ClawQuest Classes Reference

This document provides detailed information about the six character classes in ClawQuest.

---

## 🎓 Scholar (学者)

**Archetype:** Knowledge seeker, researcher, information master

**Primary Attribute:** INT (Intelligence)  
**Secondary Attribute:** WIS (Wisdom)

**Best For:**
- Knowledge queries and research
- Q&A sessions
- Deep dives into technical topics
- Academic research and citations
- Learning new concepts

**Starting Stats:**
- INT: 8
- WIS: 6
- CHA: 4
- DEX: 4
- CON: 4
- STR: 4

**Class Bonus:** +20% XP when using research, knowledge queries, explanations

**Recommended Stat Progression:**
- Priority: INT → WIS → DEX
- Keep INT highest for knowledge depth
- Invest in WIS for better reasoning
- Some DEX helps with creative explanations

**Ideal Equipment Focus:**
- Weapon: INT-boosting staffs, tomes
- Armor: WIS/INT balanced robes
- Accessory: INT enhancement items

---

## 🔨 Artisan (工匠)

**Archetype:** Creator, craftsman, code artisan

**Primary Attribute:** DEX (Dexterity)  
**Secondary Attribute:** INT (Intelligence)

**Best For:**
- Code writing and development
- Design work (UI/UX)
- Content creation
- Crafting solutions
- Fine-detail implementations

**Starting Stats:**
- DEX: 8
- INT: 6
- WIS: 4
- CHA: 4
- CON: 4
- STR: 4

**Class Bonus:** +20% XP when coding, designing, creating content

**Recommended Stat Progression:**
- Priority: DEX → INT → CON
- Keep DEX highest for craftsmanship
- Invest in INT for better code quality
- Some CON helps with sustained coding sessions

**Ideal Equipment Focus:**
- Weapon: DEX-boosting tools, precision instruments
- Armor: CON for endurance during long builds
- Accessory: INT for clever solutions

---

## 🔍 Scout (斥候)

**Archetype:** Information gatherer, analyst, explorer

**Primary Attribute:** WIS (Wisdom)  
**Secondary Attribute:** DEX (Dexterity)

**Best For:**
- Search and intelligence gathering
- Data analysis
- Pattern recognition
- Debugging and troubleshooting
- Exploring codebases

**Starting Stats:**
- WIS: 8
- DEX: 6
- INT: 4
- CHA: 4
- CON: 4
- STR: 4

**Class Bonus:** +20% XP when searching, analyzing data, investigating

**Recommended Stat Progression:**
- Priority: WIS → DEX → INT
- Keep WIS highest for insight
- Invest in DEX for quick data parsing
- Some INT helps with complex analysis

**Ideal Equipment Focus:**
- Weapon: WIS-enhancing scopes, compasses
- Armor: DEX for quick movement
- Accessory: INT for deeper understanding

---

## 📯 Herald (使者)

**Archetype:** Communicator, translator, social expert

**Primary Attribute:** CHA (Charisma)  
**Secondary Attribute:** WIS (Wisdom)

**Best For:**
- Translation work
- Writing emails and communications
- Social media content
- Persuasive writing
- Cross-cultural communication

**Starting Stats:**
- CHA: 8
- WIS: 6
- INT: 4
- DEX: 4
- CON: 4
- STR: 4

**Class Bonus:** +20% XP when translating, writing communications, social tasks

**Recommended Stat Progression:**
- Priority: CHA → WIS → INT
- Keep CHA highest for expression
- Invest in WIS for cultural insight
- Some INT helps with complex translations

**Ideal Equipment Focus:**
- Weapon: CHA-boosting orbs, horns
- Armor: WIS for better understanding
- Accessory: CHA enhancement items

---

## 🧙 Sage (贤者)

**Archetype:** Strategist, planner, advisor

**Primary Attribute:** WIS (Wisdom)  
**Secondary Attribute:** INT (Intelligence)

**Best For:**
- Strategic planning
- Decision support
- Architecture design
- Long-term planning
- Advisory and consulting

**Starting Stats:**
- WIS: 8
- INT: 6
- CHA: 4
- DEX: 4
- CON: 4
- STR: 4

**Class Bonus:** +20% XP when planning, strategizing, advising

**Recommended Stat Progression:**
- Priority: WIS → INT → CHA
- Keep WIS highest for insight
- Invest in INT for knowledge depth
- Some CHA helps with persuasive recommendations

**Ideal Equipment Focus:**
- Weapon: WIS-enhancing crystals, orbs
- Armor: INT for knowledge retention
- Accessory: CHA for convincing strategies

---

## 🛡️ Guardian (守护者)

**Archetype:** Automator, worker, endurance specialist

**Primary Attribute:** CON (Constitution)  
**Secondary Attribute:** STR (Strength)

**Best For:**
- Automation and workflows
- Batch processing
- Repetitive tasks
- Long-running operations
- Infrastructure work

**Starting Stats:**
- CON: 8
- STR: 6
- INT: 4
- WIS: 4
- DEX: 4
- CHA: 4

**Class Bonus:** +20% XP when automating, batch processing, workflow tasks

**Recommended Stat Progression:**
- Priority: CON → STR → INT
- Keep CON highest for endurance
- Invest in STR for handling large tasks
- Some INT helps with smarter automation

**Ideal Equipment Focus:**
- Weapon: STR-boosting hammers, shields
- Armor: CON-heavy plate armor
- Accessory: INT for efficient workflows

---

## 🔄 Class Change System

**Cost:** 200 gold

**Process:**
1. User runs `/cq class` to view available classes
2. User confirms class change (costs 200 gold)
3. Primary/secondary attributes change
4. All allocated stat points remain unchanged
5. All equipment remains equipped (no penalties)

**When to Change:**
- Your usage patterns shift (e.g., from coding to research)
- You want to experiment with different playstyles
- You've accumulated enough gold and want a fresh identity

**Note:** Class is purely cosmetic and doesn't affect AI capabilities. It only changes:
- Title prefix (e.g., "Scholar" → "Artisan")
- XP bonus triggers (different actions get +20%)
- Starting equipment recommendations

---

## 📊 Class Comparison Matrix

| Class | Primary | Secondary | Best Scenarios | XP Bonus Triggers |
|-------|---------|-----------|----------------|-------------------|
| **Scholar** | INT | WIS | Research, Q&A, learning | "Explain...", "What is...", "Research..." |
| **Artisan** | DEX | INT | Coding, design, creation | "Write code...", "Design...", "Create..." |
| **Scout** | WIS | DEX | Search, analysis, debugging | "Find...", "Search...", "Analyze..." |
| **Herald** | CHA | WIS | Translation, communication | "Translate...", "Write email...", "Draft..." |
| **Sage** | WIS | INT | Planning, strategy, advice | "Plan...", "Strategy for...", "How should I..." |
| **Guardian** | CON | STR | Automation, batch tasks | "Automate...", "Batch process...", "Workflow..." |

---

## 💡 Choosing Your First Class

**During the awakening ritual (`/cq new`), the LLM will ask:**

1. "What do you usually use AI for?"
2. "Do you prefer creative tasks or analytical ones?"
3. "Quick wins or deep dives?"

**Based on answers:**

| User Pattern | Recommended Class |
|--------------|-------------------|
| Research-heavy, asking questions | **Scholar** |
| Writing code, building things | **Artisan** |
| Finding information, debugging | **Scout** |
| Writing/translating content | **Herald** |
| Planning projects, architecture | **Sage** |
| Setting up automation, scripts | **Guardian** |

**Remember:** You can always change classes later for 200 gold!
