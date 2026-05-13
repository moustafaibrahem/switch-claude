---
description: Switch between Claude Code account profiles
argument-hint: save <name> | use <name> | list | delete <name> | current
allowed-tools: Bash(bash:*)
---

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/claude-switch" $ARGUMENTS`

Based on the script output above:
- If the command was `use` and it succeeded, remind me to exit this session and start a new one for the switch to take effect.
- If the command failed, show the error and suggest the correct usage.
- If no arguments were provided, show the usage block from the script output.
