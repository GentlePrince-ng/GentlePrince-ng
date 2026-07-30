"""
Generate dark-theme SVGs from the light originals.

Every colour in these diagrams lives in one of three places: the <style> block,
a marker's fill attribute, or a handful of inline fills. That makes a mapped
substitution safe — but ONLY if white is handled first, because white means
three different things in these files:

  1. the page background and the small rects that mask arrows behind labels
     -> must become the dark canvas
  2. .container / .process-light surfaces
     -> must become a dark raised surface
  3. .white-label text sitting on teal or amber
     -> must stay white, it is still legible on dark

A blanket #FFFFFF replace would turn every label invisible. So the two
class-scoped cases are rewritten first, the remaining inline fills become the
canvas, and .white-label is simply never touched.
"""

import re
import pathlib

HERE = pathlib.Path(__file__).parent
DARK = HERE / "dark"
DARK.mkdir(exist_ok=True)

CANVAS = "#0D1117"   # GitHub dark canvas, so embeds blend rather than glare
SURFACE = "#161B22"  # raised surface for data stores and outlined cards

# Applied after the white-handling above. Order matters only in that longer
# hexes never overlap shorter ones here — all keys are full 6-digit.
PALETTE = {
    "#334155": "#C9D1D9",  # body text and connectors
    "#2E8B74": "#3DA88C",  # process fill, approved paths — brightened for dark
    "#D98A2B": "#E09B3D",  # decision diamonds
    "#F1F5F9": SURFACE,    # data-store fill
    "#F8FAFC": SURFACE,    # design container / empty-state fill
    "#CBD5E1": "#30363D",  # store and container borders
    "#E2E8F0": "#30363D",  # inset border
    "#94A3B8": "#8B949E",  # muted labels, design container border
    "#B4483C": "#D9705F",  # flagged / rejected — brightened for contrast
    "#64748B": "#8B949E",  # pending / held, optional notes
    "#DDEEE9": "#1B3A33",  # highlighted grid cell
}


def to_dark(svg: str) -> str:
    # 1. Class-scoped white surfaces, before anything else touches white.
    svg = re.sub(
        r"(\.(?:container|process-light)\s*\{[^}]*?fill:\s*)#FFFFFF",
        lambda m: m.group(1) + SURFACE,
        svg,
    )

    # 1b. .held is a filled block carrying white text, so it cannot take the
    # same slate the *labels* take. #64748B lightens to #8B949E below, which is
    # right for text and lines but leaves white-on-grey at about 2.6:1 — well
    # under the 4.5:1 floor. Pin the block to a darker slate first.
    svg = re.sub(
        r"\.held\s*\{\s*fill:\s*#64748B;\s*stroke:\s*#64748B;",
        ".held           { fill: #57606A; stroke: #57606A;",
        svg,
    )

    # 2. Remaining inline white fills: page background and label masks.
    svg = svg.replace('fill="#FFFFFF"', f'fill="{CANVAS}"')

    # 3. Everything else.
    for light, dark in PALETTE.items():
        svg = svg.replace(light, dark)
        svg = svg.replace(light.lower(), dark)

    return svg


def main() -> None:
    sources = sorted(p for p in HERE.glob("*.svg"))
    if not sources:
        raise SystemExit("no source SVGs found")

    for src in sources:
        out = DARK / src.name
        out.write_text(to_dark(src.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"{src.name} -> dark/{out.name}")

    print(f"\n{len(sources)} dark variant(s) written")


if __name__ == "__main__":
    main()
