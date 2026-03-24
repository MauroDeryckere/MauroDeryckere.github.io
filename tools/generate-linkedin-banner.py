"""
Generates the LinkedIn banner image.
Run: python tools/generate-linkedin-banner.py
Output: assets/images/site/linkedin-banner.png
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, '..')
SITE = os.path.join(BASE, 'assets', 'images', 'site')
LOGOS = os.path.join(BASE, 'assets', 'images', 'logos')
OUTPUT = os.path.join(SITE, 'linkedin-banner.png')

# Config - edit these to update the banner
NAME = 'Mauro Deryckere'
TITLE = 'Engine & Graphics Programmer'
TAGS = ['C++', 'Vulkan', 'Game Engines', 'Graphics Programming', 'Unreal Engine', 'Godot']
LINKS = [
    ('globe', 'mauroderyckere.github.io', '#6bc5f8'),
    ('mail', 'mauro.deryckere@gmail.com', '#b4b4bf'),
    ('linkedin', 'Mauro-Deryckere', '#b4b4bf'),
    ('github', 'MauroDeryckere', '#b4b4bf'),
    ('itchio', 'mauroderyckere', '#b4b4bf'),
]

# Colors (match site palette)
BG_COLOR = '#11111b'
ACCENT_PURPLE = '#8000ff'
TEXT_WHITE = '#ffffff'
TEXT_GRAY = '#b4b4bf'
TEXT_CYAN = '#6bc5f8'
TAG_TEXT = '#cf59e6'
TAG_BG = '#1a1a2e'
TAG_BORDER = '#292929'

# Dimensions (LinkedIn banner standard)
W, H = 1584, 396
# Left offset to avoid profile photo overlap
LEFT = 300

img = Image.new('RGB', (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Background purple blob (bottom-right)
for y in range(H):
    for x in range(W):
        dx = (x - W * 0.9) / W
        dy = (y - H * 0.85) / H
        dist = (dx*dx + dy*dy) ** 0.5
        purple_amount = max(0, 1 - dist * 2.2)
        r = int(17 + purple_amount * 60)
        g = int(17 + purple_amount * 0)
        b = int(27 + purple_amount * 80)
        img.putpixel((x, y), (min(r, 255), min(g, 255), min(b, 255)))

# Fonts
try:
    title_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 56)
    subtitle_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 28)
    small_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
    link_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    bold_font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 10)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()
    link_font = ImageFont.load_default()
    bold_font = ImageFont.load_default()

# Purple accent line
draw.rectangle([(LEFT, 80), (LEFT + 4, 210)], fill=ACCENT_PURPLE)

# Name and title
draw.text((LEFT + 30, 80), NAME, fill=TEXT_WHITE, font=title_font)
draw.text((LEFT + 30, 145), TITLE, fill=TEXT_GRAY, font=subtitle_font)

# Tech tags
x_pos = LEFT + 30
for tag in TAGS:
    bbox = draw.textbbox((0, 0), tag, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle(
        [(x_pos, 200), (x_pos + tw + 20, 230)],
        radius=12, fill=TAG_BG, outline=TAG_BORDER
    )
    draw.text((x_pos + 10, 202), tag, fill=TAG_TEXT, font=small_font)
    x_pos += tw + 30

# Separator line
draw.line([(LEFT + 30, H - 60), (W - 80, H - 60)], fill=TAG_BORDER, width=1)

# Helper: create text badge icon
def make_badge(text, bg_color, size=16):
    badge = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle([(0, 0), (size-1, size-1)], radius=3, fill=bg_color)
    d.text((size//2 - 4, size//2 - 6), text, fill='#ffffff', font=bold_font)
    return badge

# Icons
# Globe (website)
globe = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
gd = ImageDraw.Draw(globe)
gd.ellipse([(1, 1), (14, 14)], outline=TEXT_CYAN, width=1)
gd.line([(8, 1), (8, 14)], fill=TEXT_CYAN, width=1)
gd.line([(1, 8), (14, 8)], fill=TEXT_CYAN, width=1)

# Envelope (email)
mail = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
md = ImageDraw.Draw(mail)
md.rounded_rectangle([(1, 3), (14, 13)], radius=2, outline=TEXT_GRAY, width=1)
md.line([(1, 3), (8, 9), (14, 3)], fill=TEXT_GRAY, width=1)

# LinkedIn badge
li_badge = make_badge('in', '#0a66c2')

# GitHub logo (from PNG)
gh_logo = Image.open(os.path.join(LOGOS, 'github.png')).convert('RGBA').resize((16, 16), Image.LANCZOS)

# itch.io badge
io_badge = make_badge('io', '#fa5c5c')

icon_map = {
    'globe': globe,
    'mail': mail,
    'linkedin': li_badge,
    'github': gh_logo,
    'itchio': io_badge,
}

# Links row
text_y = H - 42
icon_y = text_y + 1
x_pos = LEFT + 30
for icon_name, text, color in LINKS:
    icon = icon_map[icon_name]
    img.paste(icon, (x_pos, icon_y), icon)
    x_pos += 22
    draw.text((x_pos, text_y), text, fill=color, font=link_font)
    bbox = draw.textbbox((0, 0), text, font=link_font)
    tw = bbox[2] - bbox[0]
    x_pos += tw + 22

# Decorative dots (top-right)
for i in range(3):
    draw.ellipse([(W - 140 + i * 25, 30), (W - 132 + i * 25, 38)], fill=ACCENT_PURPLE)

img.save(OUTPUT, optimize=True)
size = os.path.getsize(OUTPUT)
print(f'Generated {OUTPUT} ({size} bytes)')
