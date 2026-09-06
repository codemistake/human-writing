#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-opencode}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_to() {
  local dir="$1"
  mkdir -p "$dir/human-writing"
  cp "$SCRIPT_DIR/SKILL.md" "$dir/human-writing/SKILL.md"
  cp "$SCRIPT_DIR/GLOBAL_RULES.md" "$dir/human-writing/GLOBAL_RULES.md"
  cp "$SCRIPT_DIR/SOURCES.md" "$dir/human-writing/SOURCES.md"
  cp "$SCRIPT_DIR/THIRD_PARTY_LICENSES.md" "$dir/human-writing/THIRD_PARTY_LICENSES.md"
  cp "$SCRIPT_DIR/LICENSE" "$dir/human-writing/LICENSE"
  echo "Installed human-writing -> $dir/human-writing"
}

case "$TARGET" in
  opencode) install_to "$HOME/.config/opencode/skills" ;;
  claude)   install_to "$HOME/.claude/skills" ;;
  codex)    install_to "$HOME/.codex/skills" ;;
  cursor)   install_to "$HOME/.cursor/skills" ;;
  all)
    install_to "$HOME/.config/opencode/skills"
    install_to "$HOME/.claude/skills"
    install_to "$HOME/.codex/skills"
    install_to "$HOME/.cursor/skills"
    ;;
  *)
    echo "Usage: $0 {opencode|claude|codex|cursor|all}" >&2
    exit 2
    ;;
esac

echo "Global rules were NOT modified. Merge GLOBAL_RULES.md into your AGENTS.md/CLAUDE.md manually."
