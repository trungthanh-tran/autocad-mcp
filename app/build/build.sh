#!/usr/bin/env bash
# Đóng gói cho Linux (chạy trên máy Linux; PyInstaller không cross-compile).
# Cần: pip install -e ".[web,llm]" pyinstaller ; pywebview trên Linux cần GTK (python3-gi, gir1.2-webkit2-4.1) hoặc Qt.
set -e
cd "$(dirname "$0")/.."
python3 -m PyInstaller build/cadtroly.spec --noconfirm --clean --workpath build/_work --distpath dist
OUT=dist/AI-Tro-ly-AutoCAD
if [ -f build/bin/ant ]; then mkdir -p "$OUT/bin"; cp build/bin/ant "$OUT/bin/ant"; chmod +x "$OUT/bin/ant"; fi
cp build/HUONG-DAN.txt "$OUT/"; cp LICENSE "$OUT/LICENSE.txt"
echo "Xong: $OUT/AI-Tro-ly-AutoCAD  (nén cả thư mục rồi gửi đối tác)"
