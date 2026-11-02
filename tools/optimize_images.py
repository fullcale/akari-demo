"""現行サイトの画像をWebPに変換・縮小して site/img に出力する。"""
import sys, os
from PIL import Image, ImageOps
src, dst = sys.argv[1], sys.argv[2]
# (元ファイル, 出力名, 最大幅, 正方形トリミング)
JOBS = [
    # 現行サイトで表示されている位置に合わせて使う
    ("slider-2-2023.jpg", "hero-team", 2000, False),        # トップのスライダー／法人案内
    ("hikari.png", "top-ichigu", 900, False),               # トップ「一隅を照らす」欄
    # 各業務ページ冒頭のメイン写真（トップの丸い写真と同じ写真）
    ("service-zeimu.png", "main-zeimu", 900, False),
    ("morigami_side.jpg", "main-souzoku", 1200, False),
    ("service-support.png", "main-support", 900, False),
    ("service-school.png", "main-school", 900, False),
    ("ujiie2.png", "main-roumu", 1200, False),
    ("about-cowork.png", "main-cowork", 900, False),
    # 各業務ページ下部の写真
    ("zaimu-image.png", "sub-zeimu", 1600, False),
    ("souzoku-image.jpg", "sub-souzoku", 1600, False),
    ("Support2-2023.jpg", "sub-support", 1600, False),
    ("school-image.jpg", "sub-school", 1600, False),
    ("roumu-image.jpg", "sub-roumu", 1600, False),
    ("akari-cowork.png", "cowork-diagram", 1400, False),    # 他士業との連携の図
    # お客様の声
    ("voice-kawaji.png", "voice-kawaji", 480, False),
    ("voice-enpachi.png", "voice-enpachi", 480, False),
    ("morigami_side.jpg", "staff-morigami", 900, False),
    ("logoTate.png", "logo-mark", 183, False),
]
STAFF = ["staff2","staff3","staff5","staff7","staff15","staff-kagawa","staff-fujimoto","staff9",
         "staff-mabe","staff-aihara-2","staff10","staff12","staff13"]
JOBS += [(f + ".png", "p-" + f, 480, True) for f in STAFF]
os.makedirs(dst, exist_ok=True)
for f, name, w, sq in JOBS:
    im = Image.open(os.path.join(src, f))
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGBA" if name in ("logo-mark", "cowork-diagram") else "RGB")
    if sq:
        im = ImageOps.fit(im, (w, w), centering=(0.5, 0.35))
    elif im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = os.path.join(dst, name + ".webp")
    im.save(out, "WEBP", quality=80, method=6)
    print(f"{name}.webp {im.size} {os.path.getsize(out)//1024}KB")
