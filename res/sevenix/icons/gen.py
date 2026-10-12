import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

font_path, out = sys.argv[1], sys.argv[2]
f = TTFont(font_path)
f = instantiateVariableFont(f, {"wght": 600})
gname = f.getBestCmap()[ord("7")]
gs = f.getGlyphSet()
upm = f["head"].unitsPerEm
adv = f["hmtx"][gname][0]
# Same placement as branding/favicon.svg: font-size 22, centered on x=16, baseline y=26.
s = 22 / upm
pen = SVGPathPen(gs)
gs[gname].draw(TransformPen(pen, (s, 0, 0, -s, 16 - adv * s / 2, 26)))
seven = pen.getCommands()

DARK, GREEN = "#0a0c10", "#00b87a"
def glyph(color):
    return (f'<rect x="6" y="5" width="20" height="2.5" rx="1.25" fill="{color}"/>'
            f'<path d="{seven}" fill="{color}"/>')
def svg(body, vb="0 0 32 32"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>\n'

files = {
    "square.svg": svg(f'<rect width="32" height="32" rx="7" fill="{DARK}"/>' + glyph(GREEN)),
    "round.svg": svg(f'<circle cx="16" cy="16" r="16" fill="{DARK}"/>' + glyph(GREEN)),
    # macOS: Big Sur grid, 824/1024 tile centered.
    "mac.svg": svg(f'<g transform="translate(3.125 3.125) scale(0.8047)"><rect width="32" height="32" rx="7" fill="{DARK}"/>{glyph(GREEN)}</g>'),
    # Android adaptive foreground: 108dp canvas, keep the mark inside the 66dp safe zone.
    "foreground.svg": svg(f'<g transform="translate(18.8 19.9) scale(2.2)">{glyph(GREEN)}</g>', "0 0 108 108"),
    "white.svg": svg(glyph("#ffffff"), "4 3 24 24"),
    "black.svg": svg(glyph("#000000"), "4 3 24 24"),
}
for name, data in files.items():
    open(f"{out}/{name}", "w").write(data)
