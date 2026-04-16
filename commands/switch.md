---
description: Switch between Claude Code account profiles
argument-hint: <command> [name] (e.g., use work, save personal, list, delete test, current)
allowed-tools: Bash(bash:*)
---

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/claude-switch" $ARGUMENTS`

Based on the output above:
- If the command was "use" and it succeeded, remind me I need to exit this session and start a new one for the switch to take effect.
- If the command failed, show the error and suggest the correct usage.
- If no arguments were provided, show the usage block from the script output.
