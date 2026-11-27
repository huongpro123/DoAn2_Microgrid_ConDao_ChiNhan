# -*- coding: utf-8 -*-
"""Patch build_bao_cao.py: them Danh muc tu viet tat, Danh muc hinh ve, Danh muc bang,
va 2 hinh ban do Con Dao trong muc 1.1."""
import io
import re

P = r'D:\chinhan\build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    assert old in s, 'ANCHOR NOT FOUND: %r' % old[:70]
    s = s.replace(old, new, count)


# 1) globals for captions
rep("def H(text, level=1):",
    "FIG_CAPTIONS = []\nTBL_CAPTIONS = []\n\n\ndef H(text, level=1):")

# 2) collect captions
rep("""        if os.path.exists(path):
            doc.add_picture(path, width=Cm(width_cm))
            CAP(caption_text)""",
    """        if os.path.exists(path):
            doc.add_picture(path, width=Cm(width_cm))
            FIG_CAPTIONS.append(caption_text)
            CAP(caption_text)""")

rep("""def TBL(headers, rows, widths=None, caption=None):
    if caption:
        p = doc.add_paragraph()""",
    """def TBL(headers, rows, widths=None, caption=None):
    if caption:
        TBL_CAPTIONS.append(caption)
        p = doc.add_paragraph()""")

# 3) helper: danh muc tu viet tat + danh muc hinh/bang
helpers = '''

ABBR = [
    ('AC', 'Dòng điện xoay chiều (Alternating Current)'),
    ('CAPEX', 'Chi phí đầu tư ban đầu (Capital Expenditure)'),
    ('CF', 'Hệ số công suất của tuabin gió (Capacity Factor)'),
    ('COE', 'Chi phí điện năng quy dẫn (Cost of Electricity)'),
    ('CRF', 'Hệ số thu hồi vốn (Capital Recovery Factor)'),
    ('DC', 'Dòng điện một chiều (Direct Current)'),
    ('DoD', 'Độ sâu xả cho phép của pin (Depth of Discharge)'),
    ('GHI', 'Tổng bức xạ mặt trời trên mặt phẳng ngang (Global Horizontal Irradiance)'),
    ('GFI', 'Bộ biến tần tạo lưới (Grid-Forming Inverter)'),
    ('HOMER', 'Hybrid Optimization Model for Electric Renewables'),
    ('IEC', 'Ủy ban Kỹ thuật Điện Quốc tế (International Electrotechnical Commission)'),
    ('IRR', 'Tỷ suất hoàn vốn nội bộ (Internal Rate of Return)'),
    ('LCOE', 'Chi phí điện năng quy dẫn (Levelized Cost of Electricity)'),
    ('LFP', 'Pin lithium sắt phosphat (LiFePO4)'),
    ('MCCB', 'Áptômát khối (Molded Case Circuit Breaker)'),
    ('MPPT', 'Bám điểm công suất cực đại (Maximum Power Point Tracking)'),
    ('NPC', 'Tổng chi phí quy về hiện tại (Net Present Cost)'),
    ('O&M', 'Vận hành và bảo dưỡng (Operation and Maintenance)'),
    ('PR', 'Hệ số hiệu suất của dàn pin quang điện (Performance Ratio)'),
    ('PV', 'Điện mặt trời (Photovoltaic)'),
    ('RE', 'Năng lượng tái tạo (Renewable Energy)'),
    ('ROI', 'Tỷ suất sinh lời trên vốn đầu tư (Return on Investment)'),
    ('SoC', 'Trạng thái nạp của pin (State of Charge)'),
    ('ST', 'Tên gói dự án khảo sát: ST – Giai đoạn 3'),
]


def add_abbr_table():
    rows = [['Từ viết tắt', 'Diễn giải']] + [[a, b] for a, b in ABBR]
    t = doc.add_table(rows=len(rows), cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader')
    th.set(qn('w:val'), 'true')
    trPr.append(th)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.width = Cm(4.0) if j == 0 else Cm(12.0)
            par = cell.paragraphs[0]
            par.paragraph_format.first_line_indent = Cm(0)
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.15
            if j == 0:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = par.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = (i == 0)


def add_caption_list(headings_file, pages_file):
    try:
        heads = json.load(open(headings_file, encoding='utf-8'))
    except Exception:
        heads = []
    try:
        pages = json.load(open(pages_file, encoding='utf-8'))
    except Exception:
        pages = {}
    if not heads:
        P('(Danh mục sẽ được cập nhật sau khi hoàn tất bản thảo.)', italic=True)
        return
    for i, text in enumerate(heads):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.15
        pf.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        pg = pages.get(str(i), '..')
        r = p.add_run(text + '\\t' + str(pg))
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)


'''
rep("\nH('MỤC LỤC', 1)", helpers + "\nH('MỤC LỤC', 1)")

# 4) chen cac muc moi sau muc luc
rep("""H('MỤC LỤC', 1)
add_toc()
BREAK()
""",
    """H('MỤC LỤC', 1)
add_toc()
BREAK()

H('DANH MỤC TỪ VIẾT TẮT', 1)
add_abbr_table()
BREAK()

H('DANH MỤC HÌNH VẼ', 1)
add_caption_list('fig_headings.json', 'fig_pages.json')
BREAK()

H('DANH MỤC BẢNG', 1)
add_caption_list('tbl_headings.json', 'tbl_pages.json')
BREAK()
""")

# 5) hinh ban do trong muc 1.1
rep("""  'Do vận hành độc lập, yêu cầu về độ tin cậy cấp điện và dung lượng lưu trữ được đặc biệt chú trọng.')
""",
    """  'Do vận hành độc lập, yêu cầu về độ tin cậy cấp điện và dung lượng lưu trữ được đặc biệt chú trọng.')
P('Vị trí tương quan giữa quần đảo Côn Đảo với đất liền (TP. Hồ Chí Minh, TP. Vũng Tàu, '
  'TP. Cần Thơ) được thể hiện trên Hình 1.1; ảnh vệ tinh cận cảnh quần đảo – nơi đặt hệ thống '
  'ST – Giai đoạn 3 – được thể hiện trên Hình 1.2. Khoảng cách từ Côn Đảo tới TP. Vũng Tàu '
  'khoảng 80 hải lý (≈ 148 km), là khoảng cách quá lớn để kéo đường dây cấp điện từ đất liền.')
IMG('con_dao_region.png', 'Hình 1.1. Vị trí khu vực Côn Đảo trên biển Đông', width_cm=13.5)
IMG('con_dao_islands.png', 'Hình 1.2. Ảnh vệ tinh quần đảo Côn Đảo', width_cm=11.5)
""")

# 6) doi so hinh so do nguyen ly thanh 1.3
rep("""P('Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3 được trình bày trên Hình 1.1. '""",
    """P('Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3 được trình bày trên Hình 1.3. '""")
rep("""    CAP('Hình 1.1. Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3')""",
    """    CAP('Hình 1.3. Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3')""")

# 7) dump danh sach caption cuoi file
rep("""json.dump([e for e in HEADINGS if e[1] != 'MỤC LỤC'], open('toc_headings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)""",
    """json.dump([e for e in HEADINGS if e[1] != 'MỤC LỤC'], open('toc_headings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(FIG_CAPTIONS, open('fig_headings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(TBL_CAPTIONS, open('tbl_headings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)""")

io.open(P, 'w', encoding='utf-8').write(s)
print('patched build_bao_cao.py OK')
