# -*- coding: utf-8 -*-
"""Driver: build -> convert PDF -> map so trang, lap lai den khi on dinh."""
import subprocess
import sys

PY = sys.executable
BASE = r'D:\chinhan'
SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.exe'


def run(cmd):
    r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


for i in range(6):
    rc, o = run([PY, 'build_bao_cao.py'])
    if rc:
        print('BUILD FAIL', o[-2000:])
        sys.exit(1)
    rc, o2 = run([SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', BASE,
                  BASE + r'\Bao_cao_ST_Giai_doan_3.docx'])
    rc, o3 = run([PY, 'map_toc.py'])
    print('pass %d: %s' % (i + 1, o3.strip()))
    if i >= 2:
        break

# luot cuoi: build lai voi so trang vua map
rc, o = run([PY, 'build_bao_cao.py'])
run([SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', BASE,
     BASE + r'\Bao_cao_ST_Giai_doan_3.docx'])
rc, o3 = run([PY, 'map_toc.py'])
print('final:', o3.strip())
