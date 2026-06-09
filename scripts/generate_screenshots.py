"""Gera evidencias visuais a partir da execucao real do programa."""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def capture(scenario: str, use_ai: bool = False) -> str:
    command = [
        sys.executable,
        str(ROOT / "mission_control.py"),
        "--scenario",
        scenario,
    ]
    if not use_ai:
        command.append("--no-ai")
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return result.stdout.rstrip()


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/cour.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def render(text: str, destination: Path, title: str) -> None:
    font = load_font(22)
    title_font = load_font(24)
    lines: list[str] = []
    for line in text.splitlines():
        if len(line) <= 84:
            lines.append(line)
            continue
        indentation = len(line) - len(line.lstrip())
        lines.extend(
            textwrap.wrap(
                line,
                width=84,
                subsequent_indent=" " * indentation,
                replace_whitespace=False,
            )
        )
    line_height = 31
    width = 1180
    height = 90 + (len(lines) * line_height) + 40
    image = Image.new("RGB", (width, height), "#07111f")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 64), fill="#10243e")
    draw.text((28, 18), title, fill="#7dd3fc", font=title_font)

    y = 86
    for line in lines:
        color = "#e2e8f0"
        if "CRITICO" in line:
            color = "#fb7185"
        elif "ATENCAO" in line:
            color = "#fbbf24"
        elif "NORMAL" in line:
            color = "#4ade80"
        elif line.startswith("ALERTAS") or line.startswith("ACOES"):
            color = "#7dd3fc"
        draw.text((28, y), line, fill=color, font=font)
        y += line_height
    image.save(destination)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    scenarios = {
        "normal": "01_cenario_normal.png",
        "attention": "02_cenario_atencao.png",
        "critical": "03_cenario_critico.png",
    }
    for scenario, filename in scenarios.items():
        render(
            capture(scenario),
            ASSETS / filename,
            f"Execucao real - cenario {scenario}",
        )

    render(
        capture("critical", use_ai=True),
        ASSETS / "04_analise_ia.png",
        "Execucao real - analise gerada pelo Llama",
    )


if __name__ == "__main__":
    main()
