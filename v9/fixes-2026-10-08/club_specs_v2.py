"""custom.club_specs_v2 on the five clubs (2026-10-08). Read ONLY by the v4.1 theme (lg-club-specs, lg-club-tech).
Facts: copy skill product-reference-guide.md; benefit lines: spec-to-benefit.md 'For the golfer' (trimmed).
Carver lines 1-3 are the approved finish-photo callouts, verbatim."""
import json
WEDGE_TECH = [
  {"stat": "1020 carbon steel", "t": "Forged", "p": "Soft on the good ones, honest on the rest"},
  {"stat": "CNC-milled grooves", "t": "Micro-grooved face", "p": "The reason it spins"},
  {"stat": "Across the whole face", "t": "Sandblasted face", "p": "Still grips when the grass is wet. Dew sweepers, you're welcome."},
  {"stat": "300 g, every loft", "t": "Same head weight", "p": "Your 50 and your 60 swing the same, so there's no new tempo to learn."},
]
WEDGE_TILES = lambda gold: [
  {"l": "Lofts", "b": "6", "vals": ["50°", "52°", "54°", "56°", "58°", "60°"]},
  ({"l": "Grinds", "b": "2", "vals": ["K · every loft", "S · 52 56 60"]} if gold else {"l": "Grind", "b": "K", "vals": ["Every loft"]}),
  {"l": "Head", "b": "1020", "em": "forged carbon steel"},
  {"l": "Head weight", "b": "300 g", "em": "every loft"},
]
def putter(name, steel, weight, grip, hand):
  return {
    "tiles": [{"l": "Fully milled", "b": steel, "em": "stainless steel"}, {"l": "Head weight", "b": f"{weight} g"},
              {"l": "Lie", "b": "72°"}, {"l": "Loft", "b": "3.5°"}],
    "rows": [["Head shape", name], ["Construction", "Fully CNC-milled"], ["Material", f"{steel} stainless steel"],
             ["Head weight", f"{weight} g"], ["Loft", "3.5 degrees"], ["Lie", "72 degrees"], ["Length", "35 inches"],
             ["Shaft", "Lucky stock steel, regular flex, mid kick point, 110 g"], ["Grip", (f"Oversized 3.0, white and gold, {grip} g" if name == "Mallet" else f"Lucky stock, {grip} g")],
             ["Finish", "Gold"], ["Hand", hand], ["Headcover", "Not included"]],
    "tech": [
      {"stat": f"{steel} stainless", "t": "Fully CNC-milled", "p": "Solid and crisp off the face, no insert, nothing to rattle. Catch one thin and you'll know exactly where, without it stinging your hands."},
      {"stat": f"{weight} g head", "t": "Weighted to stay steady", "p": ("A heavier head that holds its line through the stroke." if name == "Blade" else
                                                                       "The wide shape keeps it stable, so a putt off the toe still holds its line.")},
      {"stat": "72° lie · 3.5° loft", "t": "Set up square", "p": "Standard lie and loft at 35 inches, so it sits flat behind the ball."},
    ]}
DATA = {
  "lucky-golf-lgw02-gold": {"tiles": WEDGE_TILES(True), "tech": WEDGE_TECH, "tech_img": "11_26414fab-14b8-41ae-8ad7-a801c2f646fb.webp"},
  "lucky-golf-lgw02-black": {"tiles": WEDGE_TILES(False), "tech": WEDGE_TECH},
  "signature-gold-putters": putter("Blade", "431", 385, 75, "Right"),
  "limited-edition-mallet-putter": putter("Mallet", "304", 365, 63, "Right and left"),
  "lucky-striker-hybrid-limited-edition": {
    "tiles": [{"l": "Loft", "b": "19°"}, {"l": "Lie", "b": "59°"}, {"l": "Head weight", "b": "235 g"}, {"l": "Titanium head", "b": "Ti"}],
    "rows": [["Head", "Titanium"], ["Face", "Flex Channel"], ["Sole", "Glide Sole"], ["Loft", "19 degrees"], ["Lie", "59 degrees"],
             ["Head weight", "235 g"], ["Length", "40.5 inches"], ["Shaft", "Stiff flex, mid kick point, 68 g"], ["Grip", "58 g"],
             ["Finish", "Brushed satin gold face, mirror gold sole, gloss black crown with a gold starburst"], ["Hand", "Right and left"], ["Headcover", "Not included"]],
    "tech": [
      {"stat": "Machined channels", "t": "Flex Channel face", "p": "The face gives a little and springs back, so the ones you don't catch perfectly still go."},
      {"stat": "Shaped to slide", "t": "Glide Sole", "p": "Doesn't fight the ground. Clean contact whether it's sitting up, sitting down or buried."},
      {"stat": "Titanium head", "t": "Light and easy to launch", "p": "Speed and forgiveness from a compact head."},
    ]},
}
if __name__ == "__main__":
  json.dump(DATA, open("club_specs_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
  print({k: len(json.dumps(v)) for k, v in DATA.items()})
