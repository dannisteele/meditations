"""Generate site/icon-180.png: a calm serif 'M' on a warm stone background."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 180 * 4
img = Image.new("RGB", (S, S), (58, 52, 46))
d = ImageDraw.Draw(img)
d.ellipse((S * .14, S * .14, S * .86, S * .86), outline=(201, 169, 110), width=10)
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", int(S * .42))
d.text((S / 2, S / 2 + S * .02), "M", font=font, fill=(240, 232, 218), anchor="mm")
out = Path(__file__).resolve().parent.parent / "site" / "icon-180.png"
img.resize((180, 180), Image.LANCZOS).save(out, optimize=True)
print(out)
