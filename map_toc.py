# -*- coding: utf-8 -*-
"""Map heading / caption -> page number trong PDF, ghi cac file JSON so trang."""
import json
import os
import re

import pymupdf

BASE = r'D:\chinhan'
PDF = os.path.join(BASE, 'Bao_cao_ST_Giai_doan_3.pdf')


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def map_items(items, texts, skip):
    res, miss = {}, []
    for i, item in enumerate(items):
        key = norm(item if isinstance(item, str) else item[1])
        found = None
        for pi in range(len(texts)):
            t = texts[pi]
            if pi in skip and t.find(key) > 15:
                continue
            if key in t:
                found = pi + 1
                break
        res[str(i)] = str(found) if found else '00'
        if not found:
            miss.append(key)
    return res, miss


def main():
    doc = pymupdf.open(PDF)
    texts = [norm(p.get_text()) for p in doc]
    # trang muc luc / danh muc co dau cham dan
    skip = set(i for i, t in enumerate(texts) if '.....' in t)

    out = {}

    heads = json.load(open(os.path.join(BASE, 'toc_headings.json'), encoding='utf-8'))
    res, miss = map_items(heads, texts, skip)
    json.dump(res, open(os.path.join(BASE, 'toc_pages.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    out['toc'] = (len(heads), len(miss))

    for name in ('fig', 'tbl'):
        hp = os.path.join(BASE, '%s_headings.json' % name)
        if not os.path.exists(hp):
            continue
        items = json.load(open(hp, encoding='utf-8'))
        res, miss = map_items(items, texts, skip)
        json.dump(res, open(os.path.join(BASE, '%s_pages.json' % name), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        out[name] = (len(items), len(miss))
        if miss:
            print('  MISSING %s: %s' % (name, miss[:4]))

    print('pages=%d  ' % doc.page_count +
          '  '.join('%s=%d/%d miss' % (k, v[0], v[1]) for k, v in out.items()))


if __name__ == '__main__':
    main()
