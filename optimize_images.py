from PIL import Image, ImageOps
from pathlib import Path

SRC = Path(__file__).parent / "img"
MAX_WIDTH = 1600
QUALITY = 82

total_before = 0
total_after = 0

for f in sorted(SRC.glob("*.jpg")):
    before = f.stat().st_size
    img = Image.open(f)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > MAX_WIDTH:
        new_h = round(img.height * MAX_WIDTH / img.width)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
    img.save(f, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    after = f.stat().st_size
    total_before += before
    total_after += after
    print(f"{f.name}: {before/1e6:.1f} MB -> {after/1e6:.2f} MB")

print(f"\nTOTAL: {total_before/1e6:.1f} MB -> {total_after/1e6:.2f} MB "
      f"({100*(1-total_after/total_before):.0f}% reduction)")
