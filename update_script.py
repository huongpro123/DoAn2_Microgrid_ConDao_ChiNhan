import re
import os

with open('build_bao_cao.py.bak', 'r', encoding='utf-8') as f:
    content = f.read()

# Add helper IMG
img_helper = '''
def IMG(filename, caption_text, width_cm=14.0):
    try:
        path = filename
        if not os.path.exists(path) and os.path.exists(os.path.join('homer_sample', filename)):
            path = os.path.join('homer_sample', filename)
        if os.path.exists(path):
            doc.add_picture(path, width=Cm(width_cm))
            CAP(caption_text)
            doc.add_paragraph()
        else:
            P('(H\u00ecnh \u1ea3nh tham chi\u1ebfu: %s)' % caption_text, italic=True)
    except Exception as e:
        P('(Kh\u00f4ng ch\u00e8n \u0111\u01b0\u1ee3c h\u00ecnh: %s)' % e, italic=True)
'''

# insert img_helper right after def CAP
content = content.replace('def CAP(text):\n    p = doc.add_paragraph()\n    p.alignment = WD_ALIGN_PARAGRAPH.CENTER\n    add_runs(p, text, size=12, italic=True)\n    return p',
                          'def CAP(text):\n    p = doc.add_paragraph()\n    p.alignment = WD_ALIGN_PARAGRAPH.CENTER\n    add_runs(p, text, size=12, italic=True)\n    return p\n' + img_helper)

# 1. In Chapter 2:
# In 2.1 Load: add IMG('image13.png', 'H\u00ecnh 2.1. Nh\u1eadp d\u1eef li\u1ec7u v\u00e0 \u0111\u1ed3 th\u1ecb ph\u1ee5 t\u1ea3i 24 gi\u1edd tr\u00ean HOMER Pro')
ch2_target = "P('K\u1ebft qu\u1ea3 cho th\u1ea5y nhu c\u1ea7u \u0111i\u1ec7n n\u0103ng c\u1ee7a khu v\u1ef1c kho\u1ea3ng %s GWh/n\u0103m, l\u00e0 c\u01a1 s\u1edf \u0111\u1ec3 thi\u1ebft k\u1ebf '\n  'c\u00f4ng su\u1ea5t c\u00e1c ngu\u1ed3n ph\u00e1t v\u00e0 dung l\u01b0\u1ee3ng l\u01b0u tr\u1eef.' % vn(E_load / 1e6, 2))"
ch2_replace = ch2_target + "\nIMG('image13.png', 'H\u00ecnh 2.1. Nh\u1eadp d\u1eef li\u1ec7u v\u00e0 \u0111\u1ed3 th\u1ecb ph\u1ee5 t\u1ea3i 24 gi\u1edd tr\u00ean HOMER Pro', width_cm=13.5)"
content = content.replace(ch2_target, ch2_replace)

# In 2.2 Solar: add IMG('image16.png', 'H\u00ecnh 2.2. Nh\u1eadp d\u1eef li\u1ec7u t\u00e0i nguy\u00ean b\u1ee9c x\u1ea1 m\u1eb7t tr\u1eddi NASA v\u00e0 ch\u1ec9 s\u1ed1 clearness tr\u00ean HOMER Pro')
ch2_solar_target = "P('D\u1eef li\u1ec7u b\u1ee9c x\u1ea1 m\u1eb7t tr\u1eddi \u0111\u01b0\u1ee3c l\u1ea5y theo t\u1ecda \u0111\u1ed9 C\u00f4n \u0110\u1ea3o t\u1eeb ngu\u1ed3n NASA (ph\u00f9 h\u1ee3p v\u1edbi HOMER Pro), '\n  'v\u1edbi t\u1ed5ng x\u1ea1 trung b\u00ecnh kho\u1ea3ng 4,9 kWh/m\u00b2/ng\u00e0y, t\u01b0\u01a1ng \u0111\u01b0\u01a1ng %s kWh/m\u00b2/n\u0103m. '\n  'H\u1ec7 s\u1ed1 hi\u1ec7u su\u1ea5t t\u1ed5ng h\u1ee3p c\u1ee7a d\u00e0n PV (PR) l\u1ea5y b\u1eb1ng 0,80, k\u1ec3 c\u1ea3 t\u1ed5n th\u1ea5t nhi\u1ec7t \u0111\u1ed9, b\u1ee5i b\u1ea9n, '\n  'sai l\u1ec7ch \u0111i\u1ec3m l\u00e0m vi\u1ec7c v\u00e0 t\u1ed5n th\u1ea5t d\u00e2y d\u1eabn.' % vn(GHI_year, 1))"
ch2_solar_replace = ch2_solar_target + "\nIMG('image16.png', 'H\u00ecnh 2.2. Khai b\u00e1o d\u1eef li\u1ec7u b\u1ee9c x\u1ea1 m\u1eb7t tr\u1eddi NASA tr\u00ean HOMER Pro', width_cm=13.5)"
content = content.replace(ch2_solar_target, ch2_solar_replace)

# 2. In Chapter 3:
# In 3.1: add IMG('image6.png', 'H\u00ecnh 3.1. Giao di\u1ec7n kh\u1edfi t\u1ea1o d\u1ef1 \u00e1n microgrid tr\u00ean HOMER Pro')
ch3_1_target = "H('3.1. Ki\u1ebfn tr\u00fac m\u00f4 h\u00ecnh', 2)"
ch3_1_replace = ch3_1_target + "\nIMG('image6.png', 'H\u00ecnh 3.1. Giao di\u1ec7n kh\u1edfi t\u1ea1o d\u1ef1 \u00e1n microgrid tr\u00ean HOMER Pro', width_cm=13.5)"
content = content.replace(ch3_1_target, ch3_1_replace)

# In 3.2: add IMG('image15.png', 'H\u00ecnh 3.2. C\u1ea5u h\u00ecnh th\u00f4ng s\u1ed1 d\u00e0n pin quang \u0111i\u1ec7n PV tr\u00ean HOMER Pro')
# and IMG('image28.png', 'H\u00ecnh 3.3. C\u1ea5u h\u00ecnh v\u00e0 \u0111\u01b0\u1eddng cong c\u00f4ng su\u1ea5t tuabin gi\u00f3 tr\u00ean HOMER Pro')
# and IMG('image30.png', 'H\u00ecnh 3.4. C\u1ea5u h\u00ecnh b\u1ed9 bi\u1ebfn t\u1ea7n (Converter) tr\u00ean HOMER Pro')
ch3_2_target = "P('C\u00e1c th\u00e0nh ph\u1ea7n \u0111\u01b0\u1ee3c khai b\u00e1o v\u1edbi c\u00f4ng su\u1ea5t \u0111\u1ecbnh m\u1ee9c l\u1ea5y t\u1eeb s\u01a1 \u0111\u1ed3: d\u00e0n PV t\u1ed5ng 213,2 kWp, '\n  'tuabin gi\u00f3 2.000 kW, pin l\u01b0u tr\u1eef 11.700 kWh v\u00e0 bi\u1ebfn t\u1ea7n t\u1ea1o l\u01b0\u1edbi t\u1ed5ng 2.000 kW. '\n  'HOMER Pro s\u1ebd m\u00f4 ph\u1ecfng v\u1eadn h\u00e0nh theo t\u1eebng gi\u1edd trong 8.760 gi\u1edd c\u1ee7a n\u0103m, tr\u00ean c\u01a1 s\u1edf \u0111\u00f3 t\u1ed5ng h\u1ee3p '\n  's\u1ea3n l\u01b0\u1ee3ng, chi ph\u00ed v\u00e0 c\u00e1c ch\u1ec9 ti\u00eau kinh t\u1ebf.')"
ch3_2_replace = ch3_2_target + "\nIMG('image15.png', 'H\u00ecnh 3.2. C\u1ea5u h\u00ecnh th\u00f4ng s\u1ed1 d\u00e0n pin quang \u0111i\u1ec7n PV tr\u00ean HOMER Pro', width_cm=13.0)\nIMG('image28.png', 'H\u00ecnh 3.3. C\u1ea5u h\u00ecnh \u0111\u01b0\u1eddng cong c\u00f4ng su\u1ea5t tuabin gi\u00f3 tr\u00ean HOMER Pro', width_cm=13.0)\nIMG('image30.png', 'H\u00ecnh 3.4. C\u1ea5u h\u00ecnh b\u1ed9 bi\u1ebfn t\u1ea7n Converter tr\u00ean HOMER Pro', width_cm=13.0)"
content = content.replace(ch3_2_target, ch3_2_replace)

# 3. In Chapter 5.6:
# add IMG('image17.png', 'H\u00ecnh 5.1. Kh\u1edfi ch\u1ea1y thu\u1eadt to\u00e1n t\u1ed1i \u01b0u h\u00f3a m\u00f4 ph\u1ecfng tr\u00ean HOMER Pro')
# and IMG('image19.png', 'H\u00ecnh 5.2. M\u00e0n h\u00ecnh k\u1ebft qu\u1ea3 t\u1ed5ng quan v\u00e0 bi\u1ec3u \u0111\u1ed3 d\u00f2ng ti\u1ec1n v\u00f2ng \u0111\u1eddi tr\u00ean HOMER Pro')
# and IMG('image20.png', 'H\u00ecnh 5.3. B\u1ea3ng so s\u00e1nh c\u00e1c ph\u01b0\u01a1ng \u00e1n c\u1ea5u h\u00ecnh t\u1ed1i \u01b0u tr\u00ean HOMER Pro')
ch5_6_target = "P('So v\u1edbi h\u1ec7 th\u1ed1ng n\u1ed1i l\u01b0\u1edbi, chi ph\u00ed \u0111i\u1ec7n c\u1ee7a h\u1ec7 \u0111\u1ea3o \u0111\u1ed9c l\u1eadp cao h\u01a1n do ph\u1ea3i \u0111\u1ea7u t\u01b0 dung l\u01b0\u1ee3ng '\n  'l\u01b0u tr\u1eef v\u00e0 d\u1ef1 ph\u00f2ng c\u00f4ng su\u1ea5t. Tuy nhi\u00ean, h\u1ec7 th\u1ed1ng c\u00f3 \u01b0u \u0111i\u1ec3m v\u01b0\u1ee3t tr\u1ed9i v\u1ec1 t\u00ednh t\u1ef1 ch\u1ee7, '\n  'gi\u1ea3m ph\u1ee5 thu\u1ed9c v\u00e0o nhi\u00ean li\u1ec7u h\u00f3a th\u1ea1ch v\u00e0 gi\u1ea3m ph\u00e1t th\u1ea3i kh\u00ed nh\u00e0 k\u00ednh.')"
ch5_6_replace = ch5_6_target + "\nIMG('image17.png', 'H\u00ecnh 5.1. Kh\u1edfi ch\u1ea1y thu\u1eadt to\u00e1n t\u1ed1i \u01b0u h\u00f3a m\u00f4 ph\u1ecfng tr\u00ean HOMER Pro', width_cm=13.5)\nIMG('image19.png', 'H\u00ecnh 5.2. M\u00e0n h\u00ecnh k\u1ebft qu\u1ea3 t\u1ed5ng quan v\u00e0 bi\u1ec3u \u0111\u1ed3 d\u00f2ng ti\u1ec1n v\u00f2ng \u0111\u1eddi tr\u00ean HOMER Pro', width_cm=13.5)\nIMG('image20.png', 'H\u00ecnh 5.3. B\u1ea3ng so s\u00e1nh c\u00e1c ph\u01b0\u01a1ng \u00e1n c\u1ea5u h\u00ecnh t\u1ed1i \u01b0u tr\u00ean HOMER Pro', width_cm=13.5)"
content = content.replace(ch5_6_target, ch5_6_replace)

with open('build_bao_cao.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated build_bao_cao.py successfully')

