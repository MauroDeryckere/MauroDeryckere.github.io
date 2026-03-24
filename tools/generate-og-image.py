"""
Generates the OG (Open Graph) preview card image for social sharing.
Run: python tools/generate-og-image.py
Output: assets/images/site/og-preview.png
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, '..')
SITE = os.path.join(BASE, 'assets', 'images', 'site')
LOGOS = os.path.join(BASE, 'assets', 'images', 'logos')
OUTPUT = os.path.join(SITE, 'og-preview.png')

# Config - edit these to update the card
NAME = 'Mauro Deryckere'
TITLE = 'Engine & Graphics Programmer'
TAGS = ['C++', 'Vulkan', 'Game Engines', 'Graphics Programming']

# Colors (match site palette)
BG_COLOR = '#11111b'
ACCENT_PURPLE = '#8000ff'
TEXT_WHITE = '#ffffff'
TEXT_GRAY = '#b4b4bf'
TEXT_CYAN = '#6bc5f8'
TAG_TEXT = '#cf59e6'
TAG_BG = '#1a1a2e'
TAG_BORDER = '#292929'

# Dimensions (OG standard)
W, H = 1200, 630

img = Image.new('RGB', (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Background purple blob (bottom-right)
for y in range(H):
    for x in range(W):
        dx = (x - W * 0.85) / W
        dy = (y - H * 0.9) / H
        dist = (dx*dx + dy*dy) ** 0.5
        purple_amount = max(0, 1 - dist * 2.5)
        r = int(17 + purple_amount * 60)
        g = int(17 + purple_amount * 0)
        b = int(27 + purple_amount * 80)
        img.putpixel((x, y), (min(r, 255), min(g, 255), min(b, 255)))

# Fonts
try:
    title_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 64)
    subtitle_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 32)
    small_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 24)
    link_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    bold_font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()
    link_font = ImageFont.load_default()
    bold_font = ImageFont.load_default()

# Purple accent line
draw.rectangle([(80, 170), (84, 320)], fill=ACCENT_PURPLE)

# Name and title
draw.text((110, 170), NAME, fill=TEXT_WHITE, font=title_font)
draw.text((110, 250), TITLE, fill=TEXT_GRAY, font=subtitle_font)

# Tech tags
x_pos = 110
for tag in TAGS:
    bbox = draw.textbbox((0, 0), tag, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle(
        [(x_pos, 315), (x_pos + tw + 24, 350)],
        radius=15, fill=TAG_BG, outline=TAG_BORDER
    )
    draw.text((x_pos + 12, 318), tag, fill=TAG_TEXT, font=small_font)
    x_pos += tw + 40

# Separator line
draw.line([(110, H - 85), (W - 110, H - 85)], fill=TAG_BORDER, width=1)

# Helper: create text badge icon
def make_badge(text, bg_color, size=20):
    badge = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle([(0, 0), (size-1, size-1)], radius=4, fill=bg_color)
    d.text((size//2 - 5, size//2 - 7), text, fill='#ffffff', font=bold_font)
    return badge

# Icons
# Globe (website)
globe = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
gd = ImageDraw.Draw(globe)
gd.ellipse([(2, 2), (17, 17)], outline=TEXT_CYAN, width=1)
gd.line([(10, 2), (10, 17)], fill=TEXT_CYAN, width=1)
gd.line([(2, 10), (17, 10)], fill=TEXT_CYAN, width=1)
gd.arc([(5, 2), (14, 17)], 0, 360, fill=TEXT_CYAN, width=1)

# Envelope (email)
mail = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
md = ImageDraw.Draw(mail)
md.rounded_rectangle([(1, 4), (18, 16)], radius=2, outline=TEXT_GRAY, width=1)
md.line([(1, 4), (10, 11), (18, 4)], fill=TEXT_GRAY, width=1)

# LinkedIn badge
li_badge = make_badge('in', '#0a66c2')

# GitHub logo (from PNG)
gh_logo = Image.open(os.path.join(LOGOS, 'github.png')).convert('RGBA').resize((20, 20), Image.LANCZOS)

# itch.io badge
io_badge = make_badge('io', '#fa5c5c')

# Links row
items = [
    (globe, 'mauroderyckere.github.io', TEXT_CYAN),
    (mail, 'mauro.deryckere@gmail.com', TEXT_GRAY),
    (li_badge, 'Mauro-Deryckere', TEXT_GRAY),
    (gh_logo, 'MauroDeryckere', TEXT_GRAY),
    (io_badge, 'mauroderyckere', TEXT_GRAY),
]

x_pos = 65
text_y = H - 65
icon_y = text_y + 1
for icon, text, color in items:
    img.paste(icon, (x_pos, icon_y), icon)
    x_pos += 26
    draw.text((x_pos, text_y), text, fill=color, font=link_font)
    bbox = draw.textbbox((0, 0), text, font=link_font)
    tw = bbox[2] - bbox[0]
    x_pos += tw + 25

# Decorative dots (top-right)
for i in range(3):
    draw.ellipse([(W - 160 + i * 30, 40), (W - 150 + i * 30, 50)], fill=ACCENT_PURPLE)

img.save(OUTPUT, optimize=True)
size = os.path.getsize(OUTPUT)
print(f'Generated {OUTPUT} ({size} bytes)')
