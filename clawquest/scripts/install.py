#!/usr/bin/env python3
"""
ClawQuest installer: patches AGENTS.md with global XP rules.
Usage: python3 install.py [--uninstall]
"""
import sys
import os
import json
from pathlib import Path

MARKER_START = "<!-- clawquest:global-xp:start -->"
MARKER_END = "<!-- clawquest:global-xp:end -->"

GLOBAL_XP_BLOCK = f"""{MARKER_START}
## ⚔️ ClawQuest 全局经验规则

**无论在哪个群组、私聊、还是任何触发 OpenClaw 的场景，每次回复用户后都要执行：**

### 每轮自动涨经验

每次回复结束后，判断本轮交互复杂度，调用脚本奖励 XP：

```bash
# 1-3 XP：简单问候、单句回答
# 5-10 XP：普通帮助请求
# 15-30 XP：复杂任务、编码、深度解释
# 20-50 XP：长对话、研究、多轮规划
python3 ~/.openclaw/skills/clawquest/scripts/game_engine.py award_xp <amount>
```

如果是职业主属性相关行为（如学者回答知识问题），追加 `--class-bonus`。

### 处理升级

如果 `award_xp` 返回 `"leveled_up": true`，立即发送升级通知：

```
🎉 **升级！** Lv.X → Lv.Y
获得 2 属性点！用 `/cq allocate <属性> <点数>` 分配
```

### 状态栏

除非 `character.json` 中 `quiet_mode: true`，每轮回复末尾先输出 `---` 分隔线，再输出：

```bash
python3 ~/.openclaw/skills/clawquest/scripts/display.py status_bar
```

### `/cq` 命令

如果用户消息以 `/cq` 开头，优先处理游戏命令（详见 `~/.openclaw/skills/clawquest/SKILL.md`）。

### 注意

- 脚本不存在时静默跳过，不报错
- character.json 不存在时提示 `/cq new`，之后正常响应
- 状态栏只追加一次
{MARKER_END}"""


def find_agents_md():
    # 1. Prefer OPENCLAW_WORKSPACE env var
    workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace:
        p = Path(workspace) / "AGENTS.md"
        if p.parent.exists():
            return p

    # 2. Read from openclaw.json config (agents.defaults.workspace)
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            ws = config.get("agents", {}).get("defaults", {}).get("workspace")
            if ws:
                p = Path(ws) / "AGENTS.md"
                if p.parent.exists():
                    return p
        except Exception:
            pass

    # 3. Common fallback paths
    candidates = [
        Path.home() / ".openclaw" / "workspace" / "AGENTS.md",
        Path.home() / ".clawd" / "AGENTS.md",
        Path(os.getcwd()) / "AGENTS.md",
    ]
    for p in candidates:
        if p.exists():
            return p

    # 4. Default (may not exist yet — will be created)
    return Path.home() / ".openclaw" / "workspace" / "AGENTS.md"


def is_installed(content):
    return MARKER_START in content


def install(agents_path):
    if agents_path.exists():
        content = agents_path.read_text(encoding="utf-8")
    else:
        content = "# AGENTS.md\n"

    if is_installed(content):
        print(f"✅ ClawQuest global XP rules already installed in {agents_path}")
        return True

    # append after first heading or at end
    if content.strip():
        new_content = content.rstrip() + "\n\n" + GLOBAL_XP_BLOCK + "\n"
    else:
        new_content = GLOBAL_XP_BLOCK + "\n"

    agents_path.parent.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(new_content, encoding="utf-8")
    print(f"✅ ClawQuest global XP rules installed in {agents_path}")
    print("   Every conversation will now award XP automatically!")
    return True


def uninstall(agents_path):
    if not agents_path.exists():
        print("❌ AGENTS.md not found, nothing to uninstall")
        return False

    content = agents_path.read_text(encoding="utf-8")
    if not is_installed(content):
        print("ℹ️  ClawQuest rules not found in AGENTS.md, nothing to remove")
        return True

    # remove block between markers (inclusive)
    lines = content.split("\n")
    new_lines = []
    skipping = False
    for line in lines:
        if MARKER_START in line:
            skipping = True
        if not skipping:
            new_lines.append(line)
        if MARKER_END in line:
            skipping = False

    # clean up extra blank lines
    result = "\n".join(new_lines).rstrip() + "\n"
    agents_path.write_text(result, encoding="utf-8")
    print(f"✅ ClawQuest global XP rules removed from {agents_path}")
    return True


def main():
    uninstalling = "--uninstall" in sys.argv
    agents_path = find_agents_md()

    if uninstalling:
        success = uninstall(agents_path)
    else:
        success = install(agents_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
