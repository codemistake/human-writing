#!/usr/bin/env python3
"""Собирает assets/social-preview.png (1280x640) из assets/header.png.

GitHub требует для social preview соотношение 2:1, а шапка репозитория — 3:1.
Шапка растягивается на всю ширину, а поля сверху и снизу добираются
растяжением её крайних строк пикселей: так фон продолжается без шва.
Генерации нет, кредиты не тратятся: запускать можно сколько угодно.

    python tools/gen-social.py
"""
from pathlib import Path

from PIL import Image

W, H = 1280, 640
ROOT = Path(__file__).resolve().parent.parent


def main() -> Path:
    header = Image.open(ROOT / "assets" / "header.png").convert("RGB")
    header = header.resize((W, round(header.height * W / header.width)), Image.LANCZOS)
    top = (H - header.height) // 2

    canvas = Image.new("RGB", (W, H))
    canvas.paste(header.crop((0, 0, W, 1)).resize((W, top)), (0, 0))
    canvas.paste(header, (0, top))
    bottom = H - top - header.height
    canvas.paste(header.crop((0, header.height - 1, W, header.height)).resize((W, bottom)),
                 (0, top + header.height))

    out = ROOT / "assets" / "social-preview.png"
    canvas.save(out)
    print(f"{out} {canvas.size}")
    return out


if __name__ == "__main__":
    main()
