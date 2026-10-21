#!/usr/bin/env bash
# AI Trợ lý AutoCAD - chạy giao diện (Linux/macOS). Lần đầu: pip install -e ".[web,llm]"
cd "$(dirname "$0")"
[ -d "$HOME/CAD-kho" ] || python3 -m cadtroly.cli init
python3 -m cadtroly.cli ui "$@"
