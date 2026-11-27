# -*- coding: utf-8 -*-
"""Kiểm tra form báo cáo theo chuẩn của Trường/Khoa (xem FORM_CHUAN.md).

Cách dùng:
    python form_chuan\\check_form.py Bao_cao_ST_Giai_doan_3.docx

Kiểm tra:
  1. Mỗi mục Heading 2 phải có tối thiểu 2 đoạn văn bên trong
     (quy tắc: không tách một mục nhỏ nếu bên trong không có từ 2 đoạn trở lên).
  2. Không còn chuỗi lỗi/placeholder trong văn bản.
  3. Font chữ mặc định Times New Roman, cỡ 13, giãn dòng 1.5.
"""
import re
import sys

import docx
from docx.shared import Pt


BAD_TOKENS = ['Không chèn được hình', '%%', '_{', '^{']
BAD_RE = [r'(?<![A-Za-z])None(?![A-Za-z])', r'(?<![A-Za-z])nan(?![A-Za-z])']


def heading_level(par):
    m = re.match(r'^Heading (\d)$', par.style.name or '')
    return int(m.group(1)) if m else None


def main(path):
    doc = docx.Document(path)
    paras = doc.paragraphs
    problems = []

    # 1. Mỗi Heading 2 phải có >= 2 đoạn văn
    i = 0
    thin = []
    while i < len(paras):
        lvl = heading_level(paras[i])
        if lvl == 2:
            j = i + 1
            count = 0
            while j < len(paras) and heading_level(paras[j]) is None:
                if paras[j].text.strip():
                    count += 1
                j += 1
            if count < 2:
                thin.append((paras[i].text.strip(), count))
            i = j
            continue
        i += 1

    # 2. Chuỗi lỗi
    bad = []
    for p in paras:
        hit = [tok for tok in BAD_TOKENS if tok in p.text]
        hit += [r for r in BAD_RE if re.search(r, p.text)]
        if hit:
            bad.append((hit[0], p.text.strip()[:60]))
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                hit = [tok for tok in BAD_TOKENS if tok in cell.text]
                hit += [r for r in BAD_RE if re.search(r, cell.text)]
                if hit:
                    bad.append((hit[0], cell.text.strip()[:60]))

    # 3. Font / giãn dòng mặc định
    st = doc.styles['Normal']
    font = st.font.name
    size = st.font.size.pt if st.font.size else None
    spacing = st.paragraph_format.line_spacing

    print('File:', path)
    print('So doan:', len(paras), '| So bang:', len(doc.tables))
    print('Normal font:', font, '| size:', size, '| line spacing:', spacing)
    print('Muc Heading 2 co < 2 doan:', thin if thin else '[]')
    print('Chuoi loi/placeholder:', bad if bad else '[]')
    if font and 'Times New Roman' not in font:
        problems.append('Normal font khong phai Times New Roman')
    if size != 13:
        problems.append('Co chu Normal khac 13 pt')
    if spacing != 1.5:
        problems.append('Gian dong Normal khac 1.5')
    if thin:
        problems.append('%d muc Heading 2 co duoi 2 doan' % len(thin))
    if bad:
        problems.append('%d chuoi loi/placeholder' % len(bad))

    if problems:
        print('KET QUA: KHONG DAT ->', '; '.join(problems))
        return 1
    print('KET QUA: DAT (dung form chuan)')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
