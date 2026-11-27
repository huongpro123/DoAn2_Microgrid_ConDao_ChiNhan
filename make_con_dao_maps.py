# -*- coding: utf-8 -*-
"""Tao 2 hinh ban do khu vuc Con Dao tu tile ve tinh (Esri World Imagery)."""
import io
import math
import urllib.request

from PIL import Image, ImageDraw, ImageFont

UA = {'User-Agent': 'Mozilla/5.0 (report-figure)'}
TILE = ('https://services.arcgisonline.com/ArcGIS/rest/services/'
        'World_Imagery/MapServer/tile/{z}/{y}/{x}')
FONT = r'C:\Windows\Fonts\arial.ttf'
FONT_B = r'C:\Windows\Fonts\arialbd.ttf'


def deg2tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_r) + 1.0 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y


def fetch(z, x, y):
    url = TILE.format(z=z, x=x, y=y)
    err = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
                return Image.open(io.BytesIO(r.read())).convert('RGB')
        except Exception as e:
            err = e
    raise RuntimeError('tile fail %s: %s' % (url, err))


def build(center, z, nx, ny, points, out, scale=1.6, size_label=34, size_city=26,
          attribution=True, crop=None):
    clat, clon = center
    fx, fy = deg2tile(clat, clon, z)
    x0 = int(fx) - nx // 2
    y0 = int(fy) - ny // 2
    img = Image.new('RGB', (256 * nx, 256 * ny), (8, 18, 36))
    for j in range(ny):
        for i in range(nx):
            img.paste(fetch(z, x0 + i, y0 + j), (256 * i, 256 * j))

    def to_px(lat, lon):
        tx, ty = deg2tile(lat, lon, z)
        return (tx - x0) * 256, (ty - y0) * 256

    d = ImageDraw.Draw(img)
    # duong noi Vung Tau - Con Dao (net dut)
    for p in points:
        if p.get('dashed_to'):
            a = to_px(*p['xy'])
            b = to_px(*p['dashed_to'])
            n = 26
            for k in range(n):
                if k % 2:
                    continue
                t1, t2 = k / n, (k + 0.6) / n
                d.line([a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1,
                        a[0] + (b[0] - a[0]) * t2, a[1] + (b[1] - a[1]) * t2],
                       fill=(255, 235, 60), width=5)

    for p in points:
        px, py = to_px(*p['xy'])
        if p.get('main'):
            r = 16
            d.ellipse([px - r, py - r, px + r, py + r], outline=(255, 40, 40), width=5)
            d.line([px, py - r - 34, px, py - r], fill=(255, 40, 40), width=5)
            f = ImageFont.truetype(FONT_B, size_label)
            label = p['label']
            tw = d.textlength(label, font=f)
            box = [px - tw / 2 - 12, py - r - 84, px + tw / 2 + 12, py - r - 34]
            d.rectangle(box, fill=(255, 255, 255), outline=(255, 40, 40), width=3)
            d.text((px - tw / 2, py - r - 79), label, font=f, fill=(190, 0, 0))
        else:
            r = 8
            d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 235, 60),
                      outline=(20, 20, 20), width=2)
            f = ImageFont.truetype(FONT, size_city)
            label = p['label']
            tw = d.textlength(label, font=f)
            d.rectangle([px + 14, py - 20, px + 24 + tw, py + 14], fill=(255, 255, 255))
            d.text((px + 19, py - 19), label, font=f, fill=(0, 0, 0))

    if attribution:
        fa = ImageFont.truetype(FONT, 16)
        txt = 'Anh ve tinh: Esri, Maxar, Earthstar Geographics'
        tw = d.textlength(txt, font=fa)
        d.rectangle([img.width - tw - 16, img.height - 26, img.width, img.height],
                    fill=(255, 255, 255))
        d.text((img.width - tw - 8, img.height - 23), txt, font=fa, fill=(0, 0, 0))

    if crop:
        img = img.crop(crop)
    if scale != 1:
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img.save(out)
    print(out, img.size)


if __name__ == '__main__':
    # Hinh 1: toan canh khu vuc
    build(
        center=(9.7, 106.5), z=8, nx=5, ny=5,
        points=[
            dict(xy=(8.683, 106.617), label='Côn Đảo', main=True,
                 dashed_to=(10.35, 107.08)),
            dict(xy=(10.35, 107.08), label='TP. Vũng Tàu'),
            dict(xy=(10.78, 106.70), label='TP. Hồ Chí Minh'),
            dict(xy=(10.03, 105.78), label='TP. Cần Thơ'),
        ],
        out=r'D:\chinhan\con_dao_region.png', scale=1.7, size_label=34, size_city=26,
        crop=(8, 150, 1272, 1075))

    # Hinh 2: can canh quan dao
    build(
        center=(8.683, 106.617), z=13, nx=3, ny=3,
        points=[dict(xy=(8.683, 106.617), label='Côn Đảo', main=True)],
        out=r'D:\chinhan\con_dao_islands.png', scale=2.7, size_label=40,
        crop=(30, 30, 740, 740))
