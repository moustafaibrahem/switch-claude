#!/usr/bin/env python3
"""claude-switch: swap between saved Claude Code account profiles."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
CRED_FILE = CLAUDE_DIR / ".credentials.json"
CLAUDE_JSON = HOME / ".claude.json"
PROFILE_MARKER = CLAUDE_DIR / ".current-profile"
NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def usage() -> None:
    print("Usage: claude-switch <command> [name]")
    print()
    print("Commands:")
    print("  save <name>     Save current credentials as a named profile")
    print("  use <name>      Switch to a saved profile")
    print("  list            List all saved profiles")
    print("  delete <name>   Delete a saved profile")
    print("  current         Show current account (runs claude auth status)")
    print()
    print("Example workflow:")
    print("  claude auth login          # Log in as account A")
    print("  claude-switch save work")
    print("  claude auth login          # Log in as account B")
    print("  claude-switch save personal")
    print("  claude-switch use work")


def die(msg: str, code: int = 1) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def validate_name(name: str) -> None:
    if not NAME_RE.match(name):
        die("Profile name must be alphanumeric (a-z, 0-9, dash, underscore).")


def profile_path(name: str) -> Path:
    return CLAUDE_DIR / f".credentials.{name}.json"


def clear_oauth_cache() -> None:
    if not CLAUDE_JSON.exists():
        return
    try:
        data = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Could not clear OAuth cache: {e}", file=sys.stderr)
        return
    if "oauthAccount" not in data:
        return
    data.pop("oauthAccount", None)
    try:
        CLAUDE_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not clear OAuth cache: {e}", file=sys.stderr)


def cmd_save(args: list[str]) -> None:
    if not args:
        die("Missing profile name. Usage: claude-switch save <name>")
    name = args[0]
    validate_name(name)
    if not CRED_FILE.exists():
        die("Not logged in. Run 'claude auth login' first.")
    shutil.copyfile(CRED_FILE, profile_path(name))
    PROFILE_MARKER.write_text(name, encoding="utf-8")
    print(f"Profile '{name}' saved.")


def cmd_use(args: list[str]) -> None:
    if not args:
        die("Missing profile name. Usage: claude-switch use <name>")
    name = args[0]
    validate_name(name)
    pfile = profile_path(name)
    if not pfile.exists():
        die(
            f"Profile '{name}' not found. "
            "Run 'claude-switch list' to see available profiles."
        )
    if PROFILE_MARKER.exists() and CRED_FILE.exists():
        current = PROFILE_MARKER.read_text(encoding="utf-8").strip()
        if current and current != name:
            shutil.copyfile(CRED_FILE, profile_path(current))
            print(f"Auto-saved current profile '{current}'.")
    shutil.copyfile(pfile, CRED_FILE)
    clear_oauth_cache()
    PROFILE_MARKER.write_text(name, encoding="utf-8")
    print(f"Switched to profile '{name}'. Start a new claude session to use it.")


def cmd_list(_args: list[str]) -> None:
    profiles = sorted(CLAUDE_DIR.glob(".credentials.*.json"))
    if not profiles:
        print("No saved profiles.")
        return
    for f in profiles:
        name = f.name[len(".credentials."): -len(".json")]
        print(f"  {name}")


def cmd_delete(args: list[str]) -> None:
    if not args:
        die("Missing profile name. Usage: claude-switch delete <name>")
    name = args[0]
    validate_name(name)
    pfile = profile_path(name)
    if not pfile.exists():
        die(f"Profile '{name}' not found.")
    pfile.unlink()
    print(f"Profile '{name}' deleted.")


def cmd_current(_args: list[str]) -> None:
    sys.exit(subprocess.run(["claude", "auth", "status"]).returncode)


COMMANDS = {
    "save": cmd_save,
    "use": cmd_use,
    "list": cmd_list,
    "delete": cmd_delete,
    "current": cmd_current,
}


def main(argv: list[str]) -> None:
    if not argv:
        usage()
        return
    handler = COMMANDS.get(argv[0])
    if handler is None:
        usage()
        return
    handler(argv[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
