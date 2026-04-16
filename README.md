# claude-switch

A Claude Code plugin that adds `/switch` for swapping between saved account profiles — no more `claude auth logout` / `claude auth login` every time. Works on Windows, macOS, Linux. Core is pure Python 3.

## Commands

| | |
|---|---|
| `/switch save <name>` | Save current credentials as a named profile. |
| `/switch use <name>`  | Swap to a saved profile (auto-saves the current one first). |
| `/switch list`        | List all saved profiles. |
| `/switch delete <name>` | Delete a saved profile. |
| `/switch current`     | Show which account is active (`claude auth status`). |
| `/switch`             | Print usage. |

After `/switch use <name>`, **exit and restart Claude Code** — credentials are read at startup.

## Install

Requires **Python 3** on `PATH` (`python3 --version` on mac/Linux, `python --version` on Windows).

### Option A — plugin sideload

From Claude Code:

```
/plugin marketplace add /absolute/path/to/switch-claude
/plugin install claude-switch
```

On Windows, the slash command runs through Git Bash under the hood, so install Git for Windows or use WSL. If you only have cmd/PowerShell, use Option B instead.

### Option B — manual install (no plugin system)

**1. Put the script + a launcher on `PATH`.** Pick whichever matches your shell; the other launcher is optional.

```bash
# POSIX / Git Bash
mkdir -p ~/.local/bin
cp scripts/claude_switch.py scripts/claude-switch ~/.local/bin/
chmod +x ~/.local/bin/claude-switch
# Ensure ~/.local/bin is on PATH (add to ~/.bashrc or ~/.zshrc if not):
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

```powershell
# Windows (cmd or PowerShell — this block is PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item scripts\claude_switch.py, scripts\claude-switch.cmd "$env:USERPROFILE\.local\bin\"
[Environment]::SetEnvironmentVariable("PATH",
  "$env:USERPROFILE\.local\bin;" + [Environment]::GetEnvironmentVariable("PATH","User"), "User")
```

Open a new terminal and run `claude-switch list` to verify.

**2. Create the user-level slash command** at `~/.claude/commands/switch.md` (Windows: `%USERPROFILE%\.claude\commands\switch.md`) with this exact content:

````markdown
---
description: Switch between Claude Code account profiles
argument-hint: <command> [name] (e.g., use work, save personal, list, delete test, current)
allowed-tools: [Bash(claude-switch:*)]
---

Run the following command in bash and show me the output:

claude-switch $ARGUMENTS

Important behavior:
- If the command was "use", remind me that I need to exit this session and start a new one for the switch to take effect.
- If the command fails, show the error and suggest the correct usage.
- If no arguments were provided, run `claude-switch` with no args to show the help/usage.
````

**3. Restart Claude Code** and run `/switch` to verify.

## How it works

`claude auth login` stores credentials in `~/.claude/.credentials.json`. This tool keeps per-profile copies and swaps the active one.

| Path | Role |
|---|---|
| `~/.claude/.credentials.json` | Active credentials. Overwritten by `use`. |
| `~/.claude/.credentials.<name>.json` | One per saved profile. |
| `~/.claude/.current-profile` | Marker of the currently active profile. |
| `~/.claude.json` | Only its `oauthAccount` key is cleared — the rest is preserved. |

Only credentials are swapped — project history under `~/.claude/projects/` is shared across profiles. Profile names are validated `[A-Za-z0-9_-]+`.

## Troubleshooting

**`python` / `python3` not found.** Install Python 3 and ensure it's on `PATH`. On Windows, re-run the installer with "Add python.exe to PATH" checked.

**`bash: command not found` on Windows when `/switch` runs.** Claude Code's Bash tool needs a POSIX shell. Install Git for Windows or enable WSL and restart Claude Code. The script still runs from cmd/PowerShell directly — see Option B.

**Switched, but Claude Code still shows the old account.** Exit the session and start a new `claude` — credentials are read at startup.

## Uninstall

Plugin install: `/plugin uninstall claude-switch`.
Manual install: delete `~/.claude/commands/switch.md` and the launcher/script from `~/.local/bin/`.

To also wipe saved profiles:

```bash
rm ~/.claude/.credentials.*.json ~/.claude/.current-profile
```

(On Windows use `Remove-Item "$env:USERPROFILE\.claude\.credentials.*.json"` etc.)

## License

MIT
