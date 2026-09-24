#!/usr/bin/env bash
# Put the agent-skills command on your PATH. That is all it does: no skills
# are switched on until you link them into a project.

set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd -P)
command -v git >/dev/null || { echo "Git is needed first."; exit 1; }
command -v python3 >/dev/null || echo "Note: python3 is needed for the checks (lint, catalogue), not for linking."

bin_dir=""
for dir in "$HOME/.local/bin" "$HOME/bin"; do
    case ":$PATH:" in *":$dir:"*) bin_dir="$dir"; break ;; esac
done
if [ -z "$bin_dir" ]; then
    bin_dir="$HOME/.local/bin"
    echo "Add this line to your shell profile (for example ~/.zshrc), then open a new terminal:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

mkdir -p "$bin_dir"
chmod +x "$here/bin/agent-skills"
ln -sf "$here/bin/agent-skills" "$bin_dir/agent-skills"
echo "Installed: $bin_dir/agent-skills -> $here/bin/agent-skills"
echo
echo "Next, from inside a project:"
echo "  agent-skills list          # see what is available"
echo "  agent-skills add <skill>   # link it for Claude Code and Codex"
