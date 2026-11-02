"""白背景のロゴPNGを透過化し、ヘッダー用（濃色文字）とフッター用（白文字）を作る。"""
import sys
from PIL import Image
src, out_dir = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
dark, light = [], []
for r, g, b, a in im.getdata():
    lum = (r * 299 + g * 587 + b * 114) / 1000
    sat = max(r, g, b) - min(r, g, b)
    if sat > 60:  # 黄色の光（ロゴマーク）はそのまま
        alpha = min(255, int(sat * 1.6))
        dark.append((r, g, b, alpha)); light.append((r, g, b, alpha))
    else:  # 白〜黒の文字部分：暗さをアルファに
        alpha = int(max(0, 255 - lum) * 255 / 255)
        dark.append((29, 39, 48, alpha)); light.append((255, 255, 255, alpha))
for name, px in (("logo-yoko.png", dark), ("logo-yoko-white.png", light)):
    o = Image.new("RGBA", im.size); o.putdata(px); o.save(f"{out_dir}/{name}", optimize=True)
print(im.size)
