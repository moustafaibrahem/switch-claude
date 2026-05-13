#!/usr/bin/env bash
# Installs/refreshes the claude-switch CLI shim at ~/.local/bin/claude-switch.
# Runs on every Claude Code session start. tmp + mv keeps the install atomic
# even if two Claude sessions race. Prints status every session.
set -euo pipefail

# Guard: under `set -u`, an unset $HOME would crash with "unbound variable".
if [[ -z "${HOME:-}" ]]; then
  echo "[claude-switch] \$HOME is unset; skipping CLI install." >&2
  exit 0
fi

if [[ -z "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
  echo "[claude-switch] \$CLAUDE_PLUGIN_ROOT is unset; skipping CLI install." >&2
  exit 0
fi

SRC="${CLAUDE_PLUGIN_ROOT}/scripts/claude-switch"
BIN_DIR="$HOME/.local/bin"
DEST="$BIN_DIR/claude-switch"
TMP="$DEST.tmp.$$"

if [[ ! -f "$SRC" ]]; then
  echo "[claude-switch] Source script not found at $SRC; skipping CLI install." >&2
  exit 0
fi

mkdir -p "$BIN_DIR"
cp "$SRC" "$TMP"
chmod +x "$TMP" 2>/dev/null || true
mv -f "$TMP" "$DEST"

echo "[claude-switch] CLI ready at $DEST"

# Print PATH guidance only if ~/.local/bin is NOT on PATH.
case ":${PATH:-}:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "[claude-switch] To run 'claude-switch' from your terminal, add ~/.local/bin to PATH:"
    if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* ]]; then
      echo "  Git Bash (append to ~/.bashrc, then reopen your terminal):"
      echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
      echo "  Windows PowerShell (run once, then reopen your terminal):"
      echo "    [Environment]::SetEnvironmentVariable('PATH', \"\$env:USERPROFILE\\.local\\bin;\" + [Environment]::GetEnvironmentVariable('PATH','User'), 'User')"
    else
      echo "  bash/zsh (append to ~/.bashrc or ~/.zshrc, then reopen your terminal):"
      echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
    ;;
esac

exit 0
