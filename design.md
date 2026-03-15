# ClawQuest Skill MVP 设计文档

> **产品定位**: OpenClaw 原生 Skill，为 AI Agent 交互注入 RPG 游戏化层  
> **技术路线**: 纯 SKILL.md + Python 脚本，零构建依赖  
> **分发方式**: ClawHub install / 文件夹拷贝  
> **预计开发周期**: 1-2 周  
> **日期**: 2026-03-15

---

## 1. 技术架构

### 1.1 OpenClaw Skill 系统概述

OpenClaw Skill 是 **Markdown 提示词注入文档**（非代码插件），通过 `SKILL.md` 文件定义，在运行时注入 LLM 系统提示词。Skill 通过指示 LLM 使用内置工具（`read`、`write`、`exec`）来完成操作。

**关键约束：**

- SKILL.md 最大 256KB
- 无运行时代码执行能力——所有逻辑通过 `exec` 调用外部脚本
- 无自定义 UI 组件——纯文字输出（Canvas 工具可渲染 HTML，但为 v2 考虑）
- 无生命周期钩子——无法自动在 session 开始/结束时触发
- LLM 依赖——游戏循环依赖 LLM 遵循指令执行

**社区先例：**

- `agent-rpg`（by xhrisfu）—— RPG 游戏大师 skill，JSON 状态文件 + Python 脚本
- `clawville`（by jdrolls）—— 持久化生活模拟游戏 skill

### 1.2 文件结构

```
clawquest/
├── SKILL.md                         # 核心：游戏规则 + 循环逻辑（~15KB）
├── scripts/
│   ├── init_character.py            # 创建新角色
│   ├── game_engine.py               # 统一引擎：XP/升级/掉落/装备/任务
│   └── display.py                   # 格式化输出角色面板、状态栏
├── references/
│   ├── classes.md                   # 6 职业详细定义与推荐加点
│   ├── equipment.md                 # 装备表（4槽×6品质）
│   └── xp_curve.md                  # 等级-XP 对照表 + 属性点分配规则
└── assets/
    └── character_template.json      # 空白角色数据模板
```

### 1.3 状态存储

**路径**: `~/.openclaw/skills/clawquest/data/character.json`

状态文件在磁盘上持久化，不受 LLM 上下文压缩影响。每次对话开始时 LLM 读取该文件，每次状态变更后写回。

---

## 2. 核心身份系统

### 2.1 角色创建——觉醒仪式

首次使用 `/cq new` 时触发。LLM 通过 3-5 句自然对话推断用户倾向，建议初始职业，用户确认或手动选择。

### 2.2 六大职业

| 职业 | 英文 | 主属性 | 副属性 | 适合场景 |
|------|------|--------|--------|----------|
| 学者 | Scholar | INT | WIS | 知识查询、研究、Q&A |
| 工匠 | Artisan | DEX | INT | 代码编写、设计、内容创作 |
| 斥候 | Scout | WIS | DEX | 搜索、情报收集、数据分析 |
| 使者 | Herald | CHA | WIS | 翻译、社交媒体、邮件沟通 |
| 贤者 | Sage | WIS | INT | 规划、策略、决策支持 |
| 守护者 | Guardian | CON | STR | 自动化、批处理、工作流 |

**职业效果：**

- 使用主属性相关功能时 XP ×1.2 加成
- 决定角色称号前缀（如 "Lv.7 学者"）
- **不影响 AI 实际能力**——纯装饰/成就

**转职**: 消耗 200 金币可重选职业，属性点保留，装备不受影响。

### 2.3 六维属性面板

| 属性 | 缩写 | AI 行为映射 | 关联场景 |
|------|------|-------------|----------|
| 智识 | INT | 知识深度、引用准确度 | 搜索、研究、问答 |
| 口才 | CHA | 语言表达、社交能力 | 翻译、写作、邮件、社媒 |
| 洞察 | WIS | 洞察力、逻辑推理 | 数据分析、策略、决策支持 |
| 创造 | DEX | 精巧创作、精细操作 | 编程、设计、原创内容 |
| 效率 | CON | 持续稳定、吞吐量 | 自动化、批处理、工作流 |
| 毅力 | STR | 承载力、攻克大任务 | 长对话、大型项目、复杂多步骤 |

**文字雷达显示格式：**

```
╔══════════════════════════════╗
║       ⬡ 角色属性雷达 ⬡       ║
╠══════════════════════════════╣
║   INT ████████████████ 16    ║
║   CHA ████████         8     ║
║   WIS ████████████     12    ║
║   DEX ██████           6     ║
║   CON ██████████       10    ║
║   STR ████             4     ║
╠══════════════════════════════╣
║   总计: 56  |  可用点数: 2   ║
╚══════════════════════════════╝
```

**属性值来源：**

- 初始值：根据职业分配（主属性 8，副属性 6，其余 4）
- 升级点数：每升 1 级获得 2 点，手动分配
- 装备加成：显示为 `基础值 (+装备加成)`

---

## 3. 等级与经验系统

### 3.1 等级阶段

| 阶段 | 等级范围 | 称号 | 解锁内容 |
|------|----------|------|----------|
| 学徒 | 1-10 | Apprentice | 基础系统 |
| 旅者 | 11-25 | Traveler | 稀有装备掉落 |
| 大师 | 26-50 | Master | 史诗装备掉落、转职折扣 |
| 传说 | 51-99 | Legend | 传说装备掉落 |
| 神话 | 100 | Myth | 神话装备、全属性+5 |

### 3.2 XP 曲线

| 等级 | 所需 XP | 累计 XP |
|------|---------|---------|
| 1→2 | 50 | 50 |
| 2→3 | 75 | 125 |
| 3→4 | 110 | 235 |
| 5→6 | 200 | 585 |
| 10→11 | 500 | 2,800 |
| 25→26 | 2,000 | 22,500 |
| 50→51 | 5,000 | 97,500 |
| 99→100 | 15,000 | 500,000 |

公式: `XP(n) = floor(50 * (1.08 ^ (n-1)))`

### 3.3 XP 获取规则

| 行为 | 基础 XP | 说明 |
|------|---------|------|
| 普通对话 | 1-3 | 每轮自动获取 |
| 完成编码任务 | 15-30 | LLM 判定"任务完成" |
| 深度研究（>10 轮） | 20-50 | 长对话加成 |
| 冒险任务完成 | 30-80 | 手动标记完成 |
| 日常委托完成 | 10-20 | 每日重置 |
| 职业相关行为 | ×1.2 | 使用主属性对应功能 |

**连击加成（Streak）：**

- 连续 3 天使用: ×1.2
- 连续 7 天: ×1.5
- 连续 14 天: ×1.8
- 连续 30 天: ×2.0

---

## 4. 任务系统

### 4.1 三层任务结构

| 层级 | 名称 | 对应 Habitica | 特点 |
|------|------|---------------|------|
| 修炼 | Disciplines | Habits | 可重复 +/- 行为，无截止 |
| 日常委托 | Daily Quests | Dailies | 周期性任务，错过扣 XP |
| 冒险任务 | Adventures | To-Dos | 一次性目标，大 XP 奖励 |

### 4.2 修炼（Disciplines）

用户自定义的可重复行为，每次执行获得少量 XP。

```
📿 修炼清单
  [+] 代码审查          已修炼 12 次  (+5 XP/次)
  [+] 写单元测试        已修炼 8 次   (+8 XP/次)
  [-] 跳过文档          已堕落 3 次   (-3 XP/次)
```

**命令**: `/cq discipline add <名称> <XP值>`, `/cq discipline + <名称>`, `/cq discipline - <名称>`

### 4.3 日常委托（Daily Quests）

周期性任务（每日/每周），错过时扣除相当于奖励 50% 的 XP。

```
📋 日常委托
  [✓] 晨间代码审查        +15 XP  (每日)
  [ ] 整理 TODO 清单      +10 XP  (每日)
  [✓] 周报撰写            +25 XP  (每周一)
```

**命令**: `/cq daily add <名称> <XP> <周期>`, `/cq daily done <名称>`

### 4.4 冒险任务（Adventures）

一次性大目标，完成后获得高 XP + 装备掉落机会。

```
🗡️ 冒险任务
  [进行中] 重构登录模块      奖励: 60 XP + 装备掉落(蓝)
  [进行中] 完成 API 文档     奖励: 40 XP + 装备掉落(绿)
  [待领取] 部署 v2.0        奖励: 80 XP + 装备掉落(紫)
```

**命令**: `/cq adventure add <名称> <XP> <品质>`, `/cq adventure done <名称>`

**装备掉落概率：**

| 任务品质标记 | 白 | 绿 | 蓝 | 紫 | 橙 |
|-------------|-----|-----|-----|-----|-----|
| 绿色任务 | 60% | 35% | 5% | 0% | 0% |
| 蓝色任务 | 30% | 40% | 25% | 5% | 0% |
| 紫色任务 | 10% | 25% | 35% | 25% | 5% |
| 橙色任务 | 0% | 10% | 30% | 40% | 20% |

---

## 5. 装备与收藏系统

### 5.1 四个装备槽

| 槽位 | 图标 | 倾向属性 | 说明 |
|------|------|----------|------|
| 武器 | 🗡️ | 职业主属性 | 职业专属外观 |
| 护甲 | 🛡️ | CON/STR | 防御系 |
| 饰品 | 💎 | CHA/WIS | 辅助系 |
| 坐骑 | 🐎 | DEX/INT | 特殊（稀有+掉落） |

### 5.2 六个品质等级

| 品质 | 颜色 | 属性词缀数 | 总属性点范围 |
|------|------|-----------|-------------|
| 普通 Common | ⬜ 白 | 1 主词缀 | 1-3 |
| 优秀 Uncommon | 🟩 绿 | 1 主 + 1 副 | 4-7 |
| 稀有 Rare | 🟦 蓝 | 1 主 + 1 副 | 8-12 |
| 史诗 Epic | 🟪 紫 | 1 主 + 2 副 | 13-18 |
| 传说 Legendary | 🟧 橙 | 2 主 + 1 副 | 19-24 |
| 神话 Mythic | 🟥 红 | 2 主 + 1 副 + 被动 | 25-30 |

### 5.3 词缀系统

**主词缀（Prefix）：** 加主属性 +3~+8

| 词缀名 | 英文 | 属性 |
|--------|------|------|
| 博学之 | Erudite | +INT |
| 雄辩之 | Eloquent | +CHA |
| 先见之 | Prescient | +WIS |
| 灵巧之 | Nimble | +DEX |
| 坚毅之 | Stalwart | +CON |
| 刚猛之 | Mighty | +STR |

**副词缀（Suffix）：** 加副属性 +1~+4

| 词缀名 | 英文 | 属性 |
|--------|------|------|
| ·洞察 | of Insight | +INT |
| ·风雅 | of Grace | +CHA |
| ·清明 | of Clarity | +WIS |
| ·精工 | of Craft | +DEX |
| ·坚韧 | of Fortitude | +CON |
| ·英勇 | of Valor | +STR |

**生成示例：**

```
🟦 先见之星辰杖·清明 (Rare)
   +5 WIS, +2 INT
   适合: 贤者 / 斥候
```

### 5.4 装备显示格式

```
╔══════════ 🗡️ 装备栏 ══════════╗
║ 武器: 🟦 先见之星辰杖·清明      ║
║       +5 WIS, +2 INT           ║
║ 护甲: 🟩 坚毅之学徒长袍        ║
║       +4 CON                    ║
║ 饰品: ⬜ 洞察项链               ║
║       +2 INT                    ║
║ 坐骑: (空)                      ║
╠════════════════════════════════╣
║ 装备属性总加成:                 ║
║ INT +4  WIS +5  CON +4         ║
╚════════════════════════════════╝
```

### 5.5 装备获取

| 途径 | 品质范围 | 说明 |
|------|----------|------|
| 冒险任务完成 | 随任务品质 | 主要获取途径 |
| 金币商店 | 白-绿 | 100-500 金 |
| 等级里程碑 | 固定 | Lv.10 蓝武器, Lv.25 紫护甲, Lv.50 橙饰品 |
| 连击奖励 | 绿-蓝 | 7天/14天/30天连击各一件 |

---

## 6. 经济系统

### 6.1 金币（唯一货币）

| 来源 | 金币 |
|------|------|
| 普通对话 | 1-2 |
| 日常委托完成 | 5-15 |
| 冒险任务完成 | 20-50 |
| 升级奖励 | 等级 × 10 |

| 用途 | 花费 |
|------|------|
| 商店购买装备（白-绿） | 100-500 |
| 转职 | 200 |
| 属性重置（respec） | 等级 × 20 |

---

## 7. 交互命令

### 7.1 命令表

| 命令 | 说明 |
|------|------|
| `/cq` | 查看完整角色面板 |
| `/cq status` | 一行简短状态 |
| `/cq quest` | 任务列表（修炼/日常/冒险） |
| `/cq inventory` | 背包与装备 |
| `/cq equip <item>` | 装备物品 |
| `/cq unequip <slot>` | 卸下装备 |
| `/cq shop` | 金币商店 |
| `/cq class` | 职业详情 |
| `/cq respec` | 重置属性点 |
| `/cq allocate <属性> <点数>` | 分配属性点 |
| `/cq discipline add/+/-` | 修炼管理 |
| `/cq daily add/done` | 日常委托管理 |
| `/cq adventure add/done` | 冒险任务管理 |
| `/cq new` | 创建新角色（觉醒仪式） |
| `/cq help` | 命令帮助 |

### 7.2 被动行为（LLM 自动执行）

- 每轮对话结束后追加状态栏（可通过 `/cq quiet` 关闭）
- 升级时显示升级通知 + 可分配点数提醒
- 日常委托到期时显示提醒
- 装备掉落时显示掉落通知

### 7.3 状态栏格式

**正常模式（每轮追加）：**

```
⚔️ Lv.7 学者 | XP 320/500 | INT 14 CHA 8 WIS 12 DEX 6 CON 10 STR 4 | 💰85
```

**升级通知：**

```
🎉 ════════════════════════════════
   等级提升！ Lv.7 → Lv.8 学者
   获得 2 属性点！使用 /cq allocate 分配
   解锁: 稀有装备掉落
   ════════════════════════════════
```

**装备掉落：**

```
✨ 战利品! 获得 🟦 先见之星辰杖·清明 (+5 WIS, +2 INT)
   使用 /cq equip 星辰杖 装备，或 /cq inventory 查看背包
```

---

## 8. 状态数据结构

### 8.1 character.json 完整 Schema

```json
{
  "version": 1,
  "name": "觉醒者",
  "class": "scholar",
  "level": 7,
  "xp": 320,
  "skill_points_available": 2,
  "stats": {
    "base": { "INT": 12, "CHA": 6, "WIS": 10, "DEX": 4, "CON": 8, "STR": 4 },
    "equipment_bonus": { "INT": 4, "CHA": 0, "WIS": 5, "DEX": 0, "CON": 4, "STR": 0 },
    "total": { "INT": 16, "CHA": 6, "WIS": 15, "DEX": 4, "CON": 12, "STR": 4 }
  },
  "equipment": {
    "weapon": {
      "id": "rare_prescient_starstaff_clarity",
      "name": "先见之星辰杖·清明",
      "quality": "rare",
      "slot": "weapon",
      "prefix": { "name": "先见之", "stat": "WIS", "value": 5 },
      "suffix": { "name": "·清明", "stat": "INT", "value": 2 }
    },
    "armor": {
      "id": "uncommon_stalwart_apprentice_robe",
      "name": "坚毅之学徒长袍",
      "quality": "uncommon",
      "slot": "armor",
      "prefix": { "name": "坚毅之", "stat": "CON", "value": 4 },
      "suffix": null
    },
    "accessory": {
      "id": "common_insight_necklace",
      "name": "洞察项链",
      "quality": "common",
      "slot": "accessory",
      "prefix": { "name": "", "stat": "INT", "value": 2 },
      "suffix": null
    },
    "mount": null
  },
  "inventory": [
    {
      "id": "uncommon_mighty_iron_sword_valor",
      "name": "刚猛之铁剑·英勇",
      "quality": "uncommon",
      "slot": "weapon",
      "prefix": { "name": "刚猛之", "stat": "STR", "value": 4 },
      "suffix": { "name": "·英勇", "stat": "STR", "value": 2 }
    }
  ],
  "quests": {
    "disciplines": [
      { "name": "代码审查", "xp": 5, "count_positive": 12, "count_negative": 0 }
    ],
    "dailies": [
      { "name": "晨间代码审查", "xp": 15, "period": "daily", "done_today": true, "streak": 5 },
      { "name": "整理 TODO", "xp": 10, "period": "daily", "done_today": false, "streak": 0 }
    ],
    "adventures": [
      { "name": "重构登录模块", "xp": 60, "loot_quality": "rare", "status": "active" },
      { "name": "部署 v2.0", "xp": 80, "loot_quality": "epic", "status": "pending" }
    ]
  },
  "gold": 85,
  "streak_days": 5,
  "last_active": "2026-03-15",
  "total_conversations": 142,
  "total_xp_earned": 2800,
  "created_at": "2026-03-01"
}
```

---

## 9. SKILL.md 核心逻辑大纲

SKILL.md 将包含以下指令模块（供 LLM 遵循）：

### 9.1 初始化检查

```
每次对话开始时：
1. 读取 ~/.openclaw/skills/clawquest/data/character.json
2. 如果文件不存在 → 提示用户 /cq new 创建角色
3. 如果存在 → 加载角色状态，检查日常委托是否过期
```

### 9.2 游戏循环

```
每次回复用户消息后：
1. 判断本次交互类型（对话/任务完成/研究/etc）
2. 调用 scripts/game_engine.py award_xp <amount> 计算 XP
3. 如果触发升级 → 显示升级通知
4. 如果匹配活跃任务 → 更新任务进度
5. 追加状态栏到回复末尾（除非 quiet 模式）
6. 写回 character.json
```

### 9.3 装备生成

```
当需要生成装备时：
1. 调用 scripts/game_engine.py generate_loot <quality>
2. 脚本根据品质随机生成词缀组合
3. 返回装备 JSON 对象
4. 加入玩家背包
```

### 9.4 确定性操作（必须走脚本）

以下操作 **必须** 通过 `exec` 调用 Python 脚本，LLM 不得自行计算：

- XP 计算与升级判定
- 装备生成（词缀随机）
- 掉落概率判定
- 属性总值计算

---

## 10. Python 脚本接口设计

### 10.1 game_engine.py 命令列表

```bash
# XP 与升级
python3 game_engine.py award_xp <amount>
# 输出: {"xp_gained": 25, "new_xp": 345, "leveled_up": false, "level": 7}

python3 game_engine.py award_xp <amount> --class-bonus
# 输出: {"xp_gained": 30, "new_xp": 375, "leveled_up": false, "level": 7, "class_bonus": true}

# 升级后分配属性
python3 game_engine.py allocate <STAT> <points>
# 输出: {"success": true, "stat": "INT", "old": 12, "new": 14, "remaining_points": 0}

# 装备生成
python3 game_engine.py generate_loot <quality>
# 输出: {"id": "rare_...", "name": "先见之星辰杖·清明", "quality": "rare", ...}

# 装备穿戴
python3 game_engine.py equip <item_id>
# 输出: {"success": true, "equipped": {...}, "unequipped": {...}, "stats_updated": true}

# 商店购买
python3 game_engine.py shop_buy <item_index>
# 输出: {"success": true, "item": {...}, "gold_remaining": 85}

# 掉落判定
python3 game_engine.py roll_loot <quality_tier>
# 输出: {"dropped": true, "item": {...}} 或 {"dropped": false}

# 日常检查（过期扣XP）
python3 game_engine.py daily_check
# 输出: {"expired": ["整理 TODO"], "xp_lost": 5, "streaks_reset": ["整理 TODO"]}

# 状态输出
python3 game_engine.py status
# 输出: 格式化的一行状态栏字符串

python3 game_engine.py full_status
# 输出: 格式化的完整角色面板字符串
```

### 10.2 init_character.py

```bash
python3 init_character.py <class> <name>
# 创建 character.json，写入默认值
# 输出: {"success": true, "character": {...}}
```

### 10.3 display.py

```bash
python3 display.py panel
# 输出: 完整角色面板（带 ASCII 框线）

python3 display.py status_bar
# 输出: 一行状态栏

python3 display.py equipment
# 输出: 装备栏面板

python3 display.py quests
# 输出: 任务列表面板
```

**所有脚本共享状态文件路径**: `~/.openclaw/skills/clawquest/data/character.json`

---

## 11. 设计原则

1. **Use = Growth** —— 正常使用 AI 即升级，无需额外"练级"操作
2. **纯装饰奖励** —— 所有游戏化元素不影响 AI 实际能力
3. **确定性优先** —— 数值计算必须走脚本，LLM 不做数学
4. **状态持久化** —— JSON 文件在磁盘上，不受上下文压缩影响
5. **渐进复杂** —— 新用户只看到 XP 和等级，高级系统逐步解锁
6. **开源友好** —— MIT 协议，ClawHub 分发

---

## 12. MVP 范围（保留 vs 延后）

### 保留

- ✅ 6 职业 + 觉醒仪式
- ✅ 6 维属性 + 手动加点
- ✅ 等级系统（1-100，5 阶段）
- ✅ 3 层任务（修炼/日常/冒险）
- ✅ 4 槽装备 + 6 品质 + 词缀系统
- ✅ 金币经济
- ✅ 连击加成
- ✅ 文字角色面板 + 状态栏

### 延后至 v2+

- ⏸️ 冒险地图 / 章节区域
- ⏸️ BOSS 战
- ⏸️ 随机事件
- ⏸️ 套装系统
- ⏸️ 强化系统
- ⏸️ 成就系统
- ⏸️ Canvas HTML UI
- ⏸️ 多币种经济（宝石/星尘）
- ⏸️ 社交/公会/排行榜
- ⏸️ 赛季/世界事件

---

## 13. 与完整设计文档的关系

本文档是 `2026-03-15-clawquest-concept-design.md`（完整产品愿景）的 **MVP 子集实现方案**。

完整设计中的所有系统在这里被裁剪为 Skill 格式可承载的范围。未来从 Skill 演进到 Plugin 或独立产品时，完整设计文档中的系统将逐步回归。

**演进路径**: Skill MVP → Skill + Canvas UI → Plugin → 独立产品
