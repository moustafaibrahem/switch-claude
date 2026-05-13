# claude-switch

A Claude Code plugin that adds `/switch` for swapping between saved account profiles — no more `claude auth logout` / `claude auth login` every time. Works on macOS, Linux, and Windows. Single pure-bash script, no Python rewrite.

## Commands

| Command | Effect |
|---|---|
| `/switch save <name>`    | Save the current credentials as a named profile. |
| `/switch use <name>`     | Swap to a saved profile (auto-saves the outgoing one first). |
| `/switch list`           | List all saved profiles. |
| `/switch delete <name>`  | Delete a saved profile (and clears the active-profile marker if it was the one in use). |
| `/switch current`        | Show which account is active (`claude auth status`). |
| `/switch`                | Print usage. |

After `/switch use <name>`, **exit Claude Code and start a fresh `claude` session** — credentials are read once at startup.

## Requirements

- **Python 3** on `PATH` — used only to clear the OAuth identity cache when you switch. Tested with both `python3` and `python`.
- **Claude Code's Bash tool** — already required for slash commands. On Windows that means Git for Windows or WSL (Claude Code uses Git Bash for the Bash tool).

## Install (2 commands)

In Claude Code:

```
/plugin marketplace add moustafaibrahem/switch-claude
/plugin install claude-switch@switch-claude
```

That's it. The first command registers this repo as a one-plugin marketplace; the second installs the plugin.

### What happens next

On the next Claude Code session start, a SessionStart hook auto-installs the `claude-switch` CLI to `~/.local/bin/claude-switch` so you can use it from any terminal too. You'll see:

```
[claude-switch] CLI ready at /home/you/.local/bin/claude-switch
```

If `~/.local/bin` isn't on your shell PATH, the hook will print the exact command to add it. Run it once and reopen your terminal.

## Use it

**Inside Claude Code (slash command, works immediately):**

```
/switch list                 # show saved profiles
/switch save work            # save current creds as 'work'
/switch use personal         # swap to 'personal' (auto-saves current first)
/switch current              # show active account
```

After `/switch use <name>`, restart Claude Code.

**Outside Claude Code (terminal CLI, works after SessionStart hook runs at least once):**

```bash
claude-switch list
claude-switch save work
claude-switch use personal
claude-switch current
```

Both paths run the same script (`scripts/claude-switch` in the plugin); the slash command invokes it via `${CLAUDE_PLUGIN_ROOT}`, the CLI invokes it via the copy at `~/.local/bin/claude-switch`.

## How it works

`claude auth login` writes credentials to `~/.claude/.credentials.json`. This tool keeps per-profile copies and swaps the active one.

| Path | Role |
|---|---|
| `~/.claude/.credentials.json` | Active credentials. Overwritten by `use`. |
| `~/.claude/.credentials.<name>.json` | One per saved profile. |
| `~/.claude/.current-profile` | Marker of the currently active profile. Cleared by `delete` when you delete the active profile. |
| `~/.claude.json` | Only its `oauthAccount` key is cleared on `use`; everything else is preserved. |

Only credentials are swapped — project history under `~/.claude/projects/` is shared across profiles. Profile names are validated against `^[A-Za-z0-9_-]+$`.

## Troubleshooting

**`/switch` says "command not found".** Make sure the plugin actually installed: `/plugin` should list `claude-switch` as enabled. If not, run `/plugin install claude-switch@switch-claude` again.

**`claude-switch` not found in my terminal.** The SessionStart hook installs the CLI on the next Claude Code session. If you've started a Claude session and still can't run `claude-switch`, the hook printed PATH instructions on the previous session start — re-open Claude Code and copy that line. Or use the slash command `/switch` instead, which always works.

**Switched, but Claude Code still shows the old account.** You need to exit the current Claude Code session and start a fresh one — credentials are read at startup.

**`python` / `python3` not found.** Install Python 3 and ensure it's on `PATH`. On Windows, re-run the installer with "Add python.exe to PATH" checked. The script tries `python3` first, then falls back to `python`.

## Uninstall

```
/plugin uninstall claude-switch
```

This removes the plugin from `~/.claude/plugins/cache/`. The CLI shim at `~/.local/bin/claude-switch` is **not** removed automatically (it's outside the plugin root — this matches every other plugin's behavior). Remove it manually if you want:

```bash
# POSIX / Git Bash
rm ~/.local/bin/claude-switch

# Windows PowerShell
Remove-Item "$env:USERPROFILE\.local\bin\claude-switch"
```

To also wipe all saved profiles:

```bash
rm ~/.claude/.credentials.*.json ~/.claude/.current-profile
```

(PowerShell: `Remove-Item "$env:USERPROFILE\.claude\.credentials.*.json"`, `Remove-Item "$env:USERPROFILE\.claude\.current-profile"`)

<details>
<summary><b>Manual install (no plugin system)</b></summary>

If you don't want the Claude Code plugin system, you can install `claude-switch` directly. The script is self-contained — just put it on `PATH` and create a user-level slash command if you want `/switch`.

**1. Copy the script to `~/.local/bin/`:**

```bash
# POSIX / Git Bash
mkdir -p ~/.local/bin
cp scripts/claude-switch ~/.local/bin/
chmod +x ~/.local/bin/claude-switch
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item scripts\claude-switch "$env:USERPROFILE\.local\bin\"
```

**2. Add `~/.local/bin` to PATH** (if not already):

```bash
# bash/zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

```powershell
# Windows PowerShell (run once, then restart your terminal)
[Environment]::SetEnvironmentVariable('PATH', "$env:USERPROFILE\.local\bin;" + [Environment]::GetEnvironmentVariable('PATH','User'), 'User')
```

**3. (Optional) Create a user-level slash command** at `~/.claude/commands/switch.md` (Windows: `%USERPROFILE%\.claude\commands\switch.md`):

```markdown
---
description: Switch between Claude Code account profiles
argument-hint: <command> [name]
allowed-tools: [Bash(claude-switch:*)]
---

Run the following command in bash and show me the output:

claude-switch $ARGUMENTS

Notes:
- If the command was `use`, remind me to exit and start a new Claude session for the switch to take effect.
- If no arguments were given, run `claude-switch` with no args to print the usage.
```

Restart Claude Code and `/switch` will work.

</details>

## License

MIT.
