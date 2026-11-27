# -*- coding: utf-8 -*-
"""Tao bao cao do an: He microgrid dao ST - Giai doan 3 (Con Dao) - HOMER Pro."""
import re
import os
import json
import io
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ===================== SO LIEU =====================
Wp = 650.0
n_A, n_B, n_C = 109, 109, 110
P_pv = Wp * (n_A + n_B + n_C) / 1000.0        # 213.2 kWp
P_pvinv = 3 * 100.0
P_wind = 2000.0
E_batt = 5800.0 + 5900.0
P_gfi = 2 * 1000.0
L_ht, L_CS, L_KT = 118.1, 40.0, 625.0
P_peak = L_ht + L_CS + L_KT                   # 783.1

GHI_day = 4.9
GHI_year = GHI_day * 365
PR = 0.80
CF_wind = 0.38
LF = 0.55
DoD = 0.90
eta_inv = 0.95
i_nom, f_infl = 0.08, 0.02
r_real = (1 + i_nom) / (1 + f_infl) - 1.0
N_years = 25

p_pv, p_wind, p_inv = 62.5, 50.0, 7.5
p_batt, p_gfi, p_board = 6.0, 10.0, 500.0
diesel_price = 12000.0

P_avg = LF * P_peak
E_day = P_avg * 24.0
E_load = E_day * 365.0
Y_pv = GHI_year * PR
E_pv = P_pv * Y_pv
E_pv_day = E_pv / 365.0
k_dcac = P_pv / P_pvinv
E_wind = P_wind * CF_wind * 8760.0
h_wind = CF_wind * 8760.0
E_re = E_pv + E_wind
share_pv = E_pv / E_load
share_wind = E_wind / E_load
share_re = E_re / E_load
E_surplus = E_re - E_load
E_batt_usable = E_batt * DoD
t_aut_avg = E_batt_usable / P_avg
t_aut_peak = E_batt_usable / P_peak
c_rate = P_gfi / E_batt
t_discharge_rated = E_batt / P_gfi
P_gfi_req = P_peak / eta_inv
ratio_gfi = P_gfi / P_gfi_req

CRF = r_real * (1 + r_real) ** N_years / ((1 + r_real) ** N_years - 1)
def PF(t):
    return 1.0 / (1 + r_real) ** t
def PA(n):
    return (1 - (1 + r_real) ** (-n)) / r_real

C_pv = P_pv * p_pv
C_pvinv = P_pvinv * p_inv
C_wind = P_wind * p_wind
C_batt = E_batt * p_batt
C_gfi = P_gfi * p_gfi
C_capex = C_pv + C_pvinv + C_wind + C_batt + C_gfi + p_board
OM_pv = P_pv * 0.25
OM_wind = P_wind * 0.5
OM_batt = 0.015 * C_batt
OM_inv = 0.01 * (C_pvinv + C_gfi)
OM_year = OM_pv + OM_wind + OM_batt + OM_inv
repl_batt = C_batt * (PF(10) + PF(20))
repl_inv = (C_pvinv + C_gfi) * PF(15)
salvage = 0.10 * (C_capex - C_batt) * PF(N_years)
NPC = C_capex + OM_year * PA(N_years) + repl_batt + repl_inv - salvage
C_ann = NPC * CRF
COE = C_ann * 1e6 / E_load
savings_year = E_load * diesel_price / 1e6
net_cash = savings_year - OM_year
payback = C_capex / net_cash

def vn(x, dec=2):
    s = f"{x:,.{dec}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

# ===================== HELPERS =====================
doc = Document()

def _force_tnr_rfonts(el):
    rPr = el.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        el.append(rPr)
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rPr.insert(0, rf)
    for k in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if qn(k) in rf.attrib:
            del rf.attrib[qn(k)]
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(k), 'Times New Roman')

_dd = doc.styles.element.find(qn('w:docDefaults'))
if _dd is not None:
    _rp = _dd.find(qn('w:rPrDefault'))
    if _rp is not None:
        _force_tnr_rfonts(_rp)

st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.font.size = Pt(13)
_force_tnr_rfonts(st.element)
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for nm, sz, al in (('Heading 1', 16, WD_ALIGN_PARAGRAPH.CENTER),
                   ('Heading 2', 14, WD_ALIGN_PARAGRAPH.LEFT),
                   ('Heading 3', 13, WD_ALIGN_PARAGRAPH.LEFT)):
    h = doc.styles[nm]
    h.paragraph_format.alignment = al
    h.paragraph_format.first_line_indent = Cm(0)
    h.font.name = 'Times New Roman'
    h.font.size = Pt(sz)
    h.font.bold = True
    h.font.color.rgb = RGBColor(0, 0, 0)
    _force_tnr_rfonts(h.element)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True

for sec in doc.sections:
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)

TOKEN_RE = re.compile(r'(_\{[^}]*\}|\^\{[^}]*\})')

def add_runs(p, text, size=13, italic=False, bold=False):
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        sub = re.match(r'_\{([^}]*)\}$', tok)
        sup = re.match(r'\^\{([^}]*)\}$', tok)
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.italic = italic
        run.bold = bold
        if sub:
            run.text = sub.group(1)
            run.font.subscript = True
        elif sup:
            run.text = sup.group(1)
            run.font.superscript = True
        else:
            run.text = tok

HEADINGS = []

FIG_CAPTIONS = []
TBL_CAPTIONS = []
_BM_ID = 100


def add_bookmark(p, name):
    global _BM_ID
    _BM_ID += 1
    bs = OxmlElement('w:bookmarkStart')
    bs.set(qn('w:id'), str(_BM_ID))
    bs.set(qn('w:name'), name)
    be = OxmlElement('w:bookmarkEnd')
    be.set(qn('w:id'), str(_BM_ID))
    p._p.insert(0, bs)
    p._p.append(be)


def H(text, level=1):
    HEADINGS.append((level, text))
    p = doc.add_heading(text, level=level)
    if level == 1:
        p.paragraph_format.page_break_before = True
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

def P(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=13):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    add_runs(p, text, size=size, italic=italic, bold=bold)
    if align is not None:
        p.alignment = align
    return p

def FORMULA(text, num=None, size=13):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(2)
    pf.space_after = Pt(2)
    if num:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.tab_stops.add_tab_stop(Cm(8.0), WD_TAB_ALIGNMENT.CENTER)
        pf.tab_stops.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT)
        p.add_run('\t')
        add_runs(p, text, size=size, italic=True)
        r = p.add_run('\t(%s)' % num)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, text, size=size, italic=True)
    return p

def CAP(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    add_runs(p, text, size=12, italic=True)
    return p

def IMG(filename, caption_text, width_cm=14.0):
    try:
        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _assets = os.path.join(_root, 'assets')
        path = filename
        for cand in [filename, os.path.join(_assets, filename), os.path.join(_root, filename)]:
            if os.path.exists(cand):
                path = cand
                break
        if os.path.exists(path):
            from PIL import Image as _PILImage
            _w, _h = _PILImage.open(path).size
            H_cm = width_cm * float(_h) / float(_w)
            if H_cm > 20.0:
                width_cm = 20.0 * float(_w) / float(_h)
            doc.add_picture(path, width=Cm(width_cm))
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.paragraphs[-1].paragraph_format.first_line_indent = Cm(0)
            idx = len(FIG_CAPTIONS)
            FIG_CAPTIONS.append(caption_text)
            cap_p = CAP(caption_text)
            add_bookmark(cap_p, '_fig_%d' % idx)
            doc.add_paragraph()
        else:
            P('(Hình ảnh tham chiếu: %s)' % caption_text, italic=True)
    except Exception as e:
        P('(Không chèn được hình: %s)' % e, italic=True)


def TBL(headers, rows, widths=None, caption=None):
    if caption:
        idx = len(TBL_CAPTIONS)
        TBL_CAPTIONS.append(caption)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        add_runs(p, caption, size=12, bold=True)
        add_bookmark(p, '_tbl_%d' % idx)
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    trPr = table.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
    hdr = table.rows[0].cells
    for j, h in enumerate(headers):
        hdr[j].text = ''
        run = hdr[j].paragraphs[0].add_run(h)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        hdr[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in rows:
        cells = table.add_row().cells
        for j, val in enumerate(row):
            cells[j].text = ''
            add_runs(cells[j].paragraphs[0], str(val), size=12)
            if j > 0:
                cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if widths:
        for j, w in enumerate(widths):
            for row in table.rows:
                row.cells[j].width = Cm(w)
    last = len(table.rows) - 1
    for ri, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
    doc.add_paragraph()
    return table

def BREAK():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def add_toc():
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    r1 = p.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = ' TOC \\o "1-3" \\h \\z \\u '
    fs = OxmlElement('w:fldChar'); fs.set(qn('w:fldCharType'), 'separate')
    r1._r.append(f1); r1._r.append(it); r1._r.append(fs)
    r_hint = p.add_run('Nhấn F9 hoặc mở bằng Microsoft Word để cập nhật mục lục tự động.')
    r_hint.font.name = 'Times New Roman'; r_hint.font.size = Pt(12); r_hint.italic = True
    r2 = p.add_run()
    fe = OxmlElement('w:fldChar'); fe.set(qn('w:fldCharType'), 'end')
    r2._r.append(fe)

def add_page_number():
    for idx, sec in enumerate(doc.sections):
        if idx < 2:
            continue
        ft = sec.footer
        ft.is_linked_to_previous = False
        p = ft.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = ' PAGE '
        f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
        run._r.append(f1); run._r.append(it); run._r.append(f2)

# ===================== BIA (theo form CTUT) =====================
LOGO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'form_chuan', 'ctut_image1.png')
TEN_DE_TAI_1 = 'MÔ PHỎNG HỆ THỐNG MICROGRID ĐẢO ST – GIAI ĐOẠN 3'
# Ban tren bia dung khoang trang khong ngat de 'GIAI ĐOẠN 3' luon nam cung mot hang
TEN_DE_TAI_COVER = 'MÔ PHỎNG HỆ THỐNG MICROGRID ĐẢO ST – GIAI\u00A0ĐOẠN\u00A03'
TEN_DE_TAI_2 = '(Khu vực biển Đông, gần Côn Đảo) trên phần mềm HOMER Pro'


def C(text, size=14, bold=True, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    return p


def SP(n=1, size=11):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(' ')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)



def add_page_border(section):
    """Khung vien trang bia theo form truong (twistedLines1)."""
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn
    sectPr = section._sectPr
    if sectPr.find(qn('w:pgBorders')) is not None:
        return
    xml = ('<w:pgBorders ' + nsdecls('w') + ' w:display="firstPage">'
           '<w:top w:val="double" w:sz="18" w:space="3" w:color="auto"/>'
           '<w:left w:val="double" w:sz="18" w:space="3" w:color="auto"/>'
           '<w:bottom w:val="double" w:sz="18" w:space="3" w:color="auto"/>'
           '<w:right w:val="double" w:sz="18" w:space="2" w:color="auto"/>'
           '</w:pgBorders>')
    el = parse_xml(xml)
    pgMar = sectPr.find(qn('w:pgMar'))
    if pgMar is not None:
        pgMar.addnext(el)
    else:
        sectPr.append(el)

def COVER_TOP():
    C('TRƯỜNG ĐẠI HỌC KỸ THUẬT – CÔNG NGHỆ CẦN THƠ', 14)
    C('KHOA ĐIỆN – ĐIỆN TỬ', 14)
    C('❖', 16)
    SP(1, 6)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(0)
    if os.path.exists(LOGO):
        p.add_run().add_picture(LOGO, width=Cm(3.6))
    SP(1, 10)
    C('ĐỒ ÁN', 16)
    C('Ngành: Công nghệ Kỹ thuật Năng lượng', 13, bold=False)
    C('Khóa: 2023', 13, bold=False)


def COVER_TITLE():
    SP(6)
    C(TEN_DE_TAI_COVER, 18)
    C(TEN_DE_TAI_2, 13, italic=True)


def COVER_SUB():
    from docx.enum.text import WD_TAB_ALIGNMENT
    SP(4)
    for htxt, vtxt in ((['Giảng viên hướng dẫn', 'Sinh viên thực hiện'],
                        ['TS. Trần Hữu Tính', 'Đào Chí Nhân'])):
        pass
    rows = [('Giảng viên hướng dẫn', 'Sinh viên thực hiện'),
            ('TS. Trần Hữu Tính', 'Đào Chí Nhân')]
    for row in rows:
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0)
        pf.right_indent = Cm(0)
        pf.space_after = Pt(2)
        pf.tab_stops.add_tab_stop(Cm(4), WD_TAB_ALIGNMENT.CENTER)
        pf.tab_stops.add_tab_stop(Cm(12), WD_TAB_ALIGNMENT.CENTER)
        r = par.add_run('\t' + row[0] + '\t' + row[1])
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True


COVER_TOP()
COVER_TITLE()
SP(6)
C('ĐÀO CHÍ NHÂN', 14)
SP(5)
C('Cần Thơ, năm 2026', 14)
doc.add_section(WD_SECTION.NEW_PAGE)

COVER_TOP()
COVER_TITLE()
COVER_SUB()
SP(2)
C('Cần Thơ, năm 2026', 14)
doc.add_section(WD_SECTION.NEW_PAGE)
for _sec in (doc.sections[0], doc.sections[1]):
    add_page_border(_sec)

# ===================== LOI CAM DOAN =====================
H('LỜI CAM ĐOAN', 1)
P('Tôi xin cam đoan đề tài “%s” là một công trình nghiên cứu độc lập, không sao chép các đề tài khác. '
  'Các số liệu, kết quả mô phỏng và tính toán trình bày trong báo cáo được thực hiện bởi chính tôi trên cơ sở '
  'sơ đồ nguyên lý “ST – Giai đoạn 3” và các tài liệu tham khảo có nguồn gốc rõ ràng.' % TEN_DE_TAI_1)
P('Đề tài là một sản phẩm do tôi nỗ lực nghiên cứu, trong bài có sự tham khảo của một số tài liệu đã được '
  'trích dẫn đầy đủ ở phần Tài liệu tham khảo. Đề tài được nghiên cứu đảm bảo đúng mục tiêu đã được thuyết minh '
  'trước Hội đồng Khoa học nhà trường. Tôi cam đoan chịu hoàn toàn trách nhiệm về bản quyền của báo cáo.')
for _ in range(2):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0)
r = p.add_run('Sinh viên thực hiện'); r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True
for _ in range(2):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0)
r = p.add_run('Đào Chí Nhân'); r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True

# ===================== LOI CAM ON =====================
H('LỜI CẢM ƠN', 1)
P('Trong thời gian thực hiện báo cáo đồ án, sinh viên thực hiện đã nhận được rất nhiều sự quan tâm, hướng dẫn '
  'và tạo điều kiện từ quý thầy cô Trường Đại học Kỹ thuật – Công nghệ Cần Thơ, đặc biệt là quý thầy cô Khoa '
  'Điện – Điện tử. Nhờ đó, đồ án “%s” đã được hoàn thành đúng tiến độ và đạt yêu cầu đề ra.' % TEN_DE_TAI_1)
P('Sinh viên xin bày tỏ lòng biết ơn sâu sắc đến TS. Trần Hữu Tính, giảng viên đã trực tiếp hướng dẫn, góp ý '
  'chặt chẽ về nội dung chuyên môn, cấu trúc báo cáo cũng như phương pháp tiếp cận bài toán mô phỏng hệ thống '
  'microgrid trên phần mềm HOMER Pro và hoàn thiện phần tính toán kỹ thuật – kinh tế – môi trường.')
P('Xin chân thành cảm ơn gia đình, bạn bè và tập thể lớp KTNL2311 đã luôn động viên, trao đổi và hỗ trợ trong '
  'suốt quá trình học tập và thực hiện đồ án. Mặc dù đã nỗ lực hoàn thiện, báo cáo khó tránh khỏi những thiếu sót, '
  'rất mong nhận được sự góp ý của quý thầy cô để nội dung nghiên cứu ngày càng hoàn chỉnh hơn.')
for _ in range(2):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0)
r = p.add_run('Đào Chí Nhân'); r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True

# ===================== MUC LUC =====================


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


def add_caption_list(headings_file, bm_prefix):
    try:
        heads = json.load(open(headings_file, encoding='utf-8'))
    except Exception:
        heads = []
    if not heads:
        P('(Danh mục sẽ được cập nhật khi chạy lại lần hai.)', italic=True)
        return
    for i, text in enumerate(heads):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.15
        pf.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = p.add_run(text + '\t')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r1 = p.add_run()
        f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = ' PAGEREF %s%d \\h ' % (bm_prefix, i)
        fs = OxmlElement('w:fldChar'); fs.set(qn('w:fldCharType'), 'separate')
        r1._r.append(f1); r1._r.append(it); r1._r.append(fs)
        rt = p.add_run('1'); rt.font.name = 'Times New Roman'; rt.font.size = Pt(11)
        r2 = p.add_run()
        fe = OxmlElement('w:fldChar'); fe.set(qn('w:fldCharType'), 'end')
        r2._r.append(fe)



H('MỤC LỤC', 1)
add_toc()

H('DANH MỤC TỪ VIẾT TẮT', 1)
add_abbr_table()

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
H('DANH MỤC HÌNH VẼ', 1)
add_caption_list(os.path.join(_ASSETS_DIR, 'fig_headings.json'), '_fig_')

H('DANH MỤC BẢNG', 1)
add_caption_list(os.path.join(_ASSETS_DIR, 'tbl_headings.json'), '_tbl_')
# ===================== MO DAU =====================
H('MỞ ĐẦU', 1)
H('1. Lý do chọn đề tài', 2)
P('Côn Đảo là quần đảo nằm ở vùng biển Đông, cách đất liền (TP. Vũng Tàu) khoảng 80 hải lý '
  '(≈ 148 km), có vị trí quan trọng về quốc phòng – an ninh và đang phát triển mạnh về du lịch – '
  'dịch vụ. Cùng với sự tăng trưởng của phụ tải dân dụng, cơ sở lưu trú và dịch vụ, nhu cầu điện '
  'năng tại đảo tăng nhanh và đòi hỏi nguồn cung ổn định, liên tục trong khi lưới điện quốc gia '
  'chưa thể vươn tới đảo [10], [11]. Vì vậy bài toán cấp điện cho đảo hiện được giải quyết bằng '
  'nguồn phát tại chỗ, chủ yếu là máy phát diesel.')
P('Phương án cấp điện bằng diesel bộc lộ nhiều hạn chế: chi phí nhiên liệu và vận chuyển cao '
  '(dầu phải chở từ đất liền ra đảo), giá thành điện năng lớn, phụ thuộc nguồn cung nhiên liệu, '
  'phát thải khí nhà kính và tiếng ồn, đồng thời không phù hợp với định hướng phát triển năng '
  'lượng tái tạo của Quy hoạch điện VIII. Trong khi đó, Côn Đảo có tiềm năng tại chỗ rất thuận lợi: '
  'bức xạ tổng trên mặt phẳng ngang khoảng 5,26 kWh/m²/ngày và tốc độ gió trung bình năm ở độ cao '
  'trục tuabin khoảng 7,7 m/s (chi tiết tại mục 3.1 và 3.2). Đây là điều kiện để thay thế một phần '
  'đáng kể nguồn diesel bằng điện mặt trời và điện gió.')
P('Hệ thống microgrid độc lập (off-grid) là phương án kỹ thuật phù hợp cho khu vực đảo: quy mô '
  'công suất nhỏ, cấu hình linh hoạt theo nguồn tại chỗ, có thể kết hợp nhiều nguồn phát và hệ '
  'thống lưu trữ để bù trừ lẫn nhau. Tuy nhiên, do không có lưới điện làm nguồn cân bằng, hệ thống '
  'phải tự cân bằng công suất tại mọi thời điểm, đòi hỏi tính toán cẩn thận về công suất nguồn, '
  'dung lượng lưu trữ và khả năng đáp ứng phụ tải đỉnh.')
P('Sơ đồ hệ thống ST – Giai đoạn 3 là phương án cấp điện cho một khu vực phụ tải hỗn hợp gồm phụ '
  'tải hiện trạng, phụ tải CS và phụ tải KT, với các nguồn điện mặt trời, một tuabin gió và hai hệ '
  'thống pin lưu trữ. Việc tính toán, mô phỏng hệ thống này trên phần mềm HOMER Pro cho phép xác '
  'định đồng thời các chỉ tiêu kỹ thuật (sản lượng, mức đáp ứng tải, độ tin cậy) và các chỉ tiêu '
  'kinh tế – môi trường (chi phí điện năng quy dẫn, thời gian hoàn vốn, lượng phát thải tránh được), '
  'làm cơ sở đánh giá tính khả thi của phương án trước khi triển khai.')

H('2. Mục tiêu của đề tài', 2)
for it in [
    'Tổng quan các mô hình cấu hình hệ thống microgrid độc lập (off-grid) và khả năng ứng dụng cho hải đảo Việt Nam;',
    'Hệ thống hóa phương pháp tính toán giải tích, các chỉ tiêu đánh giá kinh tế – kỹ thuật – môi trường và thiết lập mô hình trên HOMER Pro;',
    'Tính toán giải tích và mô phỏng hệ thống ST – Giai đoạn 3 tại Côn Đảo, đánh giá phương án hiện hành và đề xuất cấu hình '
    'hiệu chỉnh đáp ứng đồng thời chỉ tiêu không thiếu tải (0 %) và tỷ lệ điện năng dư ≤ 10 % [1], [2].',
]:
    p = doc.add_paragraph(it, style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)

H('3. Đối tượng và phạm vi nghiên cứu', 2)
P('Đối tượng nghiên cứu là hệ thống microgrid độc lập ST – Giai đoạn 3 tại khu vực Côn Đảo (tỉnh Bà Rịa – Vũng Tàu). '
  'Phạm vi nghiên cứu bao gồm hiện trạng sơ đồ nguyên lý gồm 3 dàn pin mặt trời (tổng 213,2 kWp), một tuabin gió 2.000 kW, '
  'hai bộ pin lưu trữ (tổng 11.700 kWh) và hai biến tần tạo lưới 1 MW cấp cho ba nhóm phụ tải tổng 783,1 kW, đồng thời '
  'khảo sát không gian cấu hình mở rộng nhằm bảo đảm cân bằng năng lượng theo yêu cầu kỹ thuật.')
P('Các thông số khí tượng được khai thác từ cơ sở dữ liệu NASA POWER (giai đoạn 2001–2025) kết hợp đối chiếu với mô hình '
  'chuỗi thời gian 8.760 giờ trên phần mềm mô phỏng HOMER Pro.')

H('4. Phương pháp nghiên cứu', 2)
P('Đề tài kết hợp phương pháp tính toán giải tích theo lý thuyết hệ thống điện và phân tích dòng tiền vòng đời với phương '
  'pháp mô phỏng chuỗi thời gian 8.760 giờ trên phần mềm HOMER Pro. Bộ thông số kinh tế đầu vào gồm lãi suất chiết khấu '
  'danh nghĩa 8 %/năm, lạm phát 2 %/năm và vòng đời dự án 25 năm [1].')
P('Báo cáo được bố cục thành ba chương: Chương 1 trình bày tổng quan về cấu hình hệ thống microgrid off-grid; Chương 2 '
  'hệ thống hóa phương pháp tính toán cấu hình, các chỉ tiêu đánh giá và mô hình HOMER Pro; Chương 3 tính toán, mô phỏng, '
  'đề xuất hiệu chỉnh cấu hình và đánh giá hiệu quả kỹ thuật – kinh tế – môi trường cho dự án ST – Giai đoạn 3 tại Côn Đảo.')

# ===================== CHUONG 1 =====================
H('CHƯƠNG 1: TỔNG QUAN CẤU HÌNH OFF-GRID TRONG MICROGRID', 1)
H('1.1. Khái niệm microgrid và nguyên lý vận hành hệ thống độc lập (off-grid)', 2)
P('Microgrid được hiểu là một nhóm các nguồn phát phân tán, hệ thống tích trữ năng lượng và phụ tải được kết nối '
  'trong một ranh giới điện xác định, có khả năng vận hành như một thực thể điều khiển thống nhất, hoặc song hành '
  'cùng lưới phân phối, hoặc tách khỏi lưới để tự cấp điện cho phụ tải cục bộ. Trong các công cụ mô hình hóa như '
  'HOMER, microgrid được biểu diễn dưới dạng bài toán cân bằng năng lượng theo chuỗi thời gian: tại mỗi bước thời gian '
  '(thường là một giờ), hệ phải thỏa mãn đồng thời cân bằng công suất giữa nguồn phát, phụ tải và tích trữ cùng các '
  'ràng buộc kỹ thuật của từng thiết bị [1], [2].')
P('Đặc trưng cơ bản của chế độ off-grid là hệ thống không có điểm kết nối với lưới điện quốc gia nên không nhận được '
  'tham chiếu tần số và điện áp từ lưới. Một hoặc nhiều phần tử trong hệ phải đảm nhận vai trò tạo lưới (grid-forming) '
  'để thiết lập tần số và biên độ điện áp của thanh cái chung; phần tử này thường là bộ biến đổi hai chiều của hệ thống '
  'lưu trữ BESS hoặc máy phát diesel. Nếu tổng công suất phát khả dụng nhỏ hơn phụ tải, hệ buộc phải sa thải một phần tải; '
  'nếu lớn hơn, phần dư phải được nạp vào BESS, tiêu tán qua tải giả (dump load) hoặc cắt giảm nguồn (curtailment) [6].')
P('Về mặt vật lý, công suất đầu ra của dàn pin quang điện tỷ lệ thuận với bức xạ tới mặt phẳng dàn và suy giảm khi nhiệt '
  'độ tế bào tăng, trong khi công suất tua-bin gió tỷ lệ với lập phương tốc độ gió ở vùng dưới công suất định mức [4], [7]. '
  'Do hai nguồn tái tạo này biến động mạnh theo ngày và theo mùa, vai trò của BESS hoặc máy phát điều độ dự phòng không '
  'chỉ là bổ sung công suất đỉnh mà còn duy trì cân bằng năng lượng liên tục trong thời gian dài [6], [7].')
P('Trong quá trình vận hành, hệ off-grid chuyển đổi giữa các trạng thái điển hình: nguồn tái tạo cấp phụ tải và nạp '
  'BESS khi bức xạ hoặc tốc độ gió cao; BESS xả khi nguồn tái tạo suy giảm; máy phát dự phòng khởi động khi trạng thái '
  'sạc SoC giảm tới ngưỡng tối thiểu. Đồng thời cần phân biệt rõ kết quả mô phỏng chuỗi thời gian (dựa trên dữ liệu '
  'khí tượng NASA/Global Atlas [1], [2]) với số liệu đo đạc tại hiện trường, ghi rõ mọi giả thiết và mức hiệu chỉnh mô hình.')

H('1.2. Phân loại các cấu hình off-grid điển hình', 2)
P('Các cấu hình off-grid thường được phân loại theo hai trục chính: kiến trúc thanh cái điện (quyết định đường truyền '
  'công suất và số tầng biến đổi) và tổ hợp nguồn phát (quyết định mức độ bảo đảm cân bằng năng lượng). Sự kết hợp của '
  'hai trục này tạo thành các phương án thiết kế khác nhau về vốn đầu tư, hiệu suất và độ tin cậy.')
P('Theo kiến trúc thanh cái, cấu hình DC-coupled gom dàn pin PV (qua MPPT) và BESS trên thanh cái DC chung rồi qua một '
  'nghịch lưu cấp tải AC; ưu điểm là ít tầng biến đổi trên tuyến PV–BESS nhưng bộ nghịch lưu trở thành điểm sự cố đơn '
  'lẻ và khó nối trực tiếp nguồn xoay chiều [6]. Cấu hình AC-coupled nối các nguồn và BESS lên thanh cái xoay chiều thông '
  'qua các bộ biến tần riêng, cho tính mô-đun hóa cao, dễ đấu trực tiếp tua-bin gió hoặc diesel nhưng chịu tổn thất qua '
  'nhiều tầng biến đổi hơn [6]. Cấu hình Hybrid AC/DC kết hợp hai thanh cái qua bộ biến đổi hai chiều, giảm tầng biến đổi '
  'cho phía PV–BESS đặt gần nhau đồng thời mở rộng độc lập phía gió và diesel [1], [6].')
P('Theo tổ hợp nguồn phát, các cấu hình tiêu biểu gồm: PV–BESS (đơn giản, không có phần tử quay nhưng rủi ro thiếu hụt '
  'khi nhiều ngày ít nắng), PV–Gió–BESS (tận dụng bổ trợ giữa chu kỳ ngày của nắng và chu kỳ mùa của gió, thích hợp cho '
  'hải đảo nhưng phải kiểm soát điện dư và tải bão biển [4], [5], [7], [8]), PV/Gió–Diesel–BESS (bảo đảm công suất chắc chắn '
  'nhờ máy phát dự phòng đồng thời tiết kiệm nhiên liệu [1], [2], [6]), và Diesel đơn thuần dùng làm phương án tham chiếu. '
  'Tổng hợp so sánh các cấu hình được trình bày trong Bảng 1.1.')
TBL(
    ['Nhóm', 'Cấu hình', 'Ưu điểm chính', 'Nhược điểm / hạn chế', 'Phạm vi áp dụng điển hình'],
    [
        ['Thanh cái', 'DC-coupled', 'Ít tầng biến đổi PV–BESS; chi phí đầu tư thấp với hệ nhỏ', 'Nghịch lưu là điểm sự cố đơn; khó nối trực tiếp nguồn AC', 'Phụ tải nhỏ, trạm viễn thông, đảo nhỏ [6]'],
        ['', 'AC-coupled', 'Mô-đun hóa, dễ mở rộng; đấu trực tiếp gió/diesel', 'Tổn thất nhiều tầng biến đổi; điều khiển tần số–công suất phức tạp', 'Hệ công suất vừa–lớn mở rộng nhiều giai đoạn [6]'],
        ['', 'Hybrid AC/DC', 'Kết hợp ưu điểm DC/AC; tối ưu tổn thất cho nguồn gần bus', 'Cấu trúc điều khiển phức tạp nhất, yêu cầu bảo trì cao', 'Microgrid đa nguồn phụ tải hỗn hợp [1], [6]'],
        ['Tổ hợp nguồn', 'PV–BESS', 'Vận hành êm, ít bảo dưỡng, không cần nhiên liệu', 'BESS chiếm tỷ trọng vốn lớn; thiếu điện khi mây kéo dài', 'Phụ tải nhỏ, vùng bức xạ ổn định [6]'],
        ['', 'PV–Gió–BESS', 'Bù trừ ngày–mùa, giảm dung lượng lưu trữ đơn nguồn', 'Phải khảo sát gió và kiểm soát điện dư/ăn mòn biển', 'Hải đảo có cả bức xạ và gió tốt [4], [5], [7]'],
        ['', 'PV/Gió–Diesel–BESS', 'Độ tin cậy cao, đáp ứng phụ tải liên tục kể cả lặng gió', 'Còn phát thải và hậu cần nhiên liệu khi chạy dự phòng', 'Đảo xa bờ yêu cầu thiếu tải ≈ 0 % [1], [2], [6]'],
        ['', 'Diesel đơn thuần', 'Công suất chắc chắn, đầu tư ban đầu thấp', 'Chi phí phát điện và phát thải rất cao, phụ thuộc vận chuyển dầu', 'Phụ tải nhỏ ngắn hạn hoặc làm mốc so sánh [6]'],
    ],
    widths=[2.2, 2.7, 3.9, 3.9, 3.3],
    caption='Bảng 1.1. So sánh các cấu hình off-grid điển hình trong microgrid')
P('Không tồn tại một cấu hình chung phù hợp cho mọi điều kiện; quy trình thiết kế chuẩn là mô hình hóa đồng thời nhiều '
  'tổ hợp thiết bị theo chuỗi 8.760 giờ và đối chiếu trên các chỉ tiêu kỹ thuật, chi phí quy dẫn và phát thải [1], [2].')

H('1.3. Tình hình nghiên cứu và khả năng ứng dụng cho hải đảo Việt Nam', 2)
P('Trên thế giới, nghiên cứu về microgrid off-grid đã chuyển dịch từ hệ đơn nguồn sang tối ưu hóa đồng thời tổ hợp đa '
  'nguồn tái tạo – tích trữ – dự phòng. Phần mềm HOMER [1], [2] được ứng dụng phổ biến để đánh giá 8.760 giờ vận hành '
  'theo các bộ dữ liệu bức xạ toàn cầu Global Solar Atlas [4] và bản đồ gió Global Wind Atlas [5]. Dù thuận lợi ở bước '
  'khảo sát sơ bộ, dữ liệu vệ tinh tại địa hình đảo cần được kiểm chứng cẩn trọng do hiệu ứng địa hình cục bộ.')
P('Tại Việt Nam, Quy hoạch điện VIII ban hành theo Quyết định số 500/QĐ-TTg [10] định hướng đẩy mạnh phát triển các '
  'nguồn điện tái tạo và hệ thống nguồn phân tán bảo đảm an ninh năng lượng cho khu vực biên giới, hải đảo. So với biểu '
  'giá bán lẻ điện lưới đất liền của EVN [11], việc phát điện hoàn toàn bằng diesel tại các đảo xa bờ chịu thêm chi phí '
  'vận chuyển nhiên liệu bằng tàu biển và hao hụt lưu trữ, tạo động lực kinh tế rõ rệt cho mô hình lai tái tạo.')
P('Ở cấp độ nghiên cứu trong nước, Nguyễn Hữu Hiếu và cộng sự [9] đã khảo sát mô-đun tối ưu nguồn mặt trời – gió – '
  'sinh khối cho đảo Cù Lao Chàm. Cần phân biệt rằng mô hình tại [9] xét trường hợp có cáp ngầm hòa lưới đất liền, khác '
  'với bài toán vận hành độc lập hoàn toàn (off-grid) không thể phát ngược điện dư lên lưới. Kinh nghiệm bù trừ nguồn '
  'mặt trời – gió và cách lượng hóa chi phí vòng đời từ [1], [2], [9] sẽ được hệ thống hóa công thức trong Chương 2 và '
  'áp dụng tính toán, hiệu chỉnh cho hệ thống ST – Giai đoạn 3 tại Côn Đảo ở Chương 3.')


H('CHƯƠNG 2: PHƯƠNG PHÁP TÍNH TOÁN CẤU HÌNH VÀ MÔ PHỎNG HỆ THỐNG', 1)

H('2.1. Phương pháp tính toán cấu hình nguồn phát và hệ thống lưu trữ', 2)
P('a) Tính toán phụ tải: Phụ tải là số liệu gốc quyết định công suất nguồn phát, công suất bộ biến đổi và dung '
  'lượng lưu trữ. Công suất đỉnh lấy bằng tổng công suất đặt của các nhóm phụ tải; công suất trung bình và điện '
  'năng tiêu thụ được suy ra qua hệ số tải đặc trưng cho mức độ sử dụng điện trên đảo [1]:')
FORMULA('P_{đỉnh} = Σ P_{i}', '2.1')
FORMULA('P_{tb} = k_{tải} × P_{đỉnh}', '2.2')
FORMULA('E_{ngày} = P_{tb} × 24', '2.3')
FORMULA('E_{năm} = E_{ngày} × 365', '2.4')
P('Trong đó: P_{đỉnh} là tổng công suất đặt các nhóm phụ tải (kW); P_{i} là công suất đặt nhóm phụ tải thứ i (kW); '
  'k_{tải} là hệ số tải (thường 0,50–0,60 đối với phụ tải đảo); P_{tb} là công suất trung bình (kW); E_{ngày} và E_{năm} '
  'là điện năng tiêu thụ ngày (kWh/ngày) và năm (kWh/năm).')

P('b) Tính toán điện mặt trời: Công suất đỉnh dàn PV bằng tổng công suất đỉnh các module thành phần, còn sản lượng điện '
  'năm được tính theo bức xạ năm và hệ số hiệu suất tổng hợp PR (đã kể tổn thất nhiệt độ, bụi bẩn, dây dẫn và MPPT) [6]:')
FORMULA('P_{PV} = N × W_{p}', '2.5')
FORMULA('E_{PV} = P_{PV} × (H / 1 kW/m²) × PR', '2.6')
FORMULA('k_{DC/AC} = P_{PV} / P_{biến tần PV}', '2.7')
P('Trong đó: N là số lượng tấm pin (tấm); W_{p} là công suất đỉnh một tấm (kWp); P_{PV} là công suất đỉnh lắp đặt (kWp); '
  'H là tổng bức xạ mặt trời năm trên mặt phẳng dàn (kWh/m²/năm); PR là hệ số hiệu suất tổng hợp (thường 0,75–0,85); '
  'k_{DC/AC} là tỷ số DC/AC kiểm tra dự phòng công suất biến tần PV.')

P('c) Tính toán tuabin gió: Sản lượng điện gió hằng năm phụ thuộc đường cong công suất của tuabin, quy luật biến thiên '
  'tốc độ gió theo chiều cao trục và hệ số công suất CF tại vị trí đặt máy [7], [8]:')
FORMULA('E_{gió} = P_{định mức} × CF × 8.760', '2.8')
FORMULA('h_{gió} = CF × 8.760', '2.9')
FORMULA('v_{h} = v_{ref} × (h / h_{ref})^{α}', '2.10')
P('Trong đó: P_{định mức} là công suất định mức tuabin (kW); CF là hệ số công suất (vùng biển gần Côn Đảo khoảng 0,35–0,45); '
  'h_{gió} là số giờ làm việc hiệu dụng quy đổi (giờ/năm); v_{h}, v_{ref} lần lượt là tốc độ gió tại cao trình trục h và '
  'cao trình tham chiếu h_{ref} (m/s), với hệ số nhám ven biển α ≈ 0,143 [7].')

P('d) Tính toán hệ thống pin lưu trữ và bộ biến tần tạo lưới: Dung lượng khả dụng của BESS phụ thuộc độ sâu xả DoD [1], '
  'còn công suất bộ biến tần hai chiều phải lớn hơn phụ tải đỉnh có xét hiệu suất chuyển đổi [6]:')
FORMULA('E_{khả dụng} = E_{pin} × DoD', '2.11')
FORMULA('t_{tự chủ} = E_{khả dụng} / P_{phụ tải}', '2.12')
FORMULA('C_{rate} = P_{biến tần} / E_{pin}', '2.13')
FORMULA('P_{GFI, min} ≥ P_{đỉnh} / η_{biến tần}', '2.14')
P('Trong đó: E_{pin} là dung lượng danh định của hệ pin (kWh); DoD = 1 − SoC_{min} là độ sâu xả cho phép; '
  't_{tự chủ} là thời gian cấp tải độc lập (giờ); C_{rate} là tốc độ nạp/xả (h⁻¹); P_{GFI, min} là công suất tối thiểu '
  'của bộ biến tần tạo lưới (kW) và η_{biến tần} là hiệu suất chuyển đổi (thường 0,94–0,97).')

H('2.2. Các chỉ tiêu đánh giá hiệu quả cấu hình nguồn phát', 2)
P('a) Các chỉ tiêu kinh tế: Đề tài áp dụng phương pháp quy đổi dòng tiền vòng đời tương thích với HOMER Pro [1], [2]. '
  'Từ lãi suất danh nghĩa i và tỷ lệ lạm phát f xác định lãi suất thực r, hệ số thu hồi vốn CRF, tổng chi phí quy '
  'về hiện tại NPC, chi phí điện năng quy dẫn COE và thời gian hoàn vốn đơn giản T_{hoàn vốn}:')
FORMULA('r = (1 + i) / (1 + f) − 1', '2.15')
FORMULA('CRF(r, N) = r(1 + r)^{N} / [(1 + r)^{N} − 1]', '2.16')
FORMULA('NPC = C_{0} + Σ (OM_{t} + Rep_{t} − S_{t}) / (1 + r)^{t}', '2.17')
FORMULA('COE = (NPC × CRF) / E_{năm}', '2.18')
FORMULA('T_{hoàn vốn} = C_{0} / (L_{tiết kiệm/năm} − OM_{năm})', '2.19')
P('Trong đó: N là thời gian vòng đời dự án (năm); C_{0} là vốn đầu tư ban đầu; OM_{t}, Rep_{t}, S_{t} lần lượt là chi phí '
  'vận hành bảo dưỡng, chi phí thay thế và giá trị thu hồi năm thứ t; E_{năm} là điện năng thực cấp phục vụ phụ tải trong năm.')

P('b) Các chỉ tiêu kỹ thuật: Khả năng bảo đảm cung cấp điện và mức độ tận dụng nguồn được lượng hóa qua tỷ lệ đáp ứng '
  'nhu cầu R_{đáp ứng}, tỷ lệ năng lượng tái tạo RF, tỷ lệ điện năng dư bị cắt giảm CUR và hệ số công suất CF [1], [6]:')
FORMULA('R_{đáp ứng} = E_{phục vụ} / E_{nhu cầu} = 1 − E_{thiếu} / E_{nhu cầu}', '2.20')
FORMULA('RF = E_{tái tạo} / E_{phục vụ}', '2.21')
FORMULA('CUR = E_{dư} / E_{sản xuất}', '2.22')
FORMULA('CF = E_{năm} / (P_{định mức} × 8.760)', '2.23')
P('Đối với bài toán thiết kế microgrid off-grid tại đảo, cấu hình đạt yêu cầu kỹ thuật phải bảo đảm cấp điện liên tục '
  '(E_{thiếu} ≈ 0 %, tức R_{đáp ứng} ≈ 1) đồng thời kiểm soát tỷ lệ điện dư bị cắt giảm trong ngưỡng hợp lý (CUR ≤ 10 %) [1], [2].')

P('c) Chỉ tiêu môi trường: Lượng khí nhà kính CO_{2} tránh được hằng năm khi nguồn tái tạo thay thế máy phát diesel được '
  'tính theo hướng dẫn kiểm kê phát thải của IPCC [12], kết hợp đánh giá định tính về giảm NO_{x}, SO_{2}, bụi và tiếng ồn:')
FORMULA('M_{CO2} = E_{thay thế} × EF_{diesel} / 1.000', '2.24')
P('Trong đó: M_{CO2} tính bằng tấn CO_{2}/năm; E_{thay thế} là phần điện năng tải được nguồn tái tạo cung cấp (kWh/năm); '
  'hệ số phát thải dầu diesel theo IPCC là 74,8 kg CO_{2}/GJ [12], quy đổi theo hiệu suất máy phát khoảng 35 % cho '
  'EF_{diesel} ≈ 0,74 kg CO_{2}/kWh.')

H('2.3. Tổng quan và phương pháp thiết lập mô hình trên phần mềm HOMER Pro', 2)
P('Phần mềm HOMER Pro thực hiện mô phỏng cân bằng công suất cho toàn bộ 8.760 giờ trong năm trên từng phương án cấu hình, '
  'xét đầy đủ biến thiên theo giờ của bức xạ, tốc độ gió, đặc tính suy giảm của pin lưu trữ và ràng buộc vận hành thiết bị, '
  'sau đó xếp hạng các phương án khả thi theo NPC tăng dần [1], [2]. Giao diện khởi tạo dự án được thể hiện trên Hình 2.1.')
IMG('image6.png', 'Hình 2.1. Giao diện khởi tạo dự án microgrid trên HOMER Pro', width_cm=14.0)
P('Kiến trúc mô hình hệ thống ST – Giai đoạn 3 trên HOMER Pro gồm hai thanh cái liên kết qua bộ biến đổi hai chiều:')
for it in [
    'Thanh cái AC: kết nối tuabin gió, các bộ biến tần PV, bộ biến tần tạo lưới và ba nhóm phụ tải tiêu thụ;',
    'Thanh cái DC: kết nối các dàn pin quang điện và hai cụm pin lưu trữ Li-ion LFP;',
    'Bộ biến đổi hai chiều (System Converter): thực hiện nghịch lưu DC→AC và chỉnh lưu AC→DC để nạp/xả pin;',
    'Chế độ vận hành độc lập hoàn toàn (off-grid), không kết nối phần tử lưới điện quốc gia (Grid).',
]:
    p = doc.add_paragraph(it, style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)

P('Các thành phần chính gồm dàn PV, đường cong công suất tuabin gió và bộ biến đổi công suất được khai báo chi tiết '
  'trong thư viện thiết bị của phần mềm như minh họa trên các Hình 2.2, Hình 2.3 và Hình 2.4 [1].')
IMG('image15.png', 'Hình 2.2. Cấu hình thông số dàn pin quang điện PV trên HOMER Pro', width_cm=14.0)
IMG('image28.png', 'Hình 2.3. Cấu hình đường cong công suất tuabin gió trên HOMER Pro', width_cm=14.0)
IMG('image30.png', 'Hình 2.4. Cấu hình bộ biến tần Converter trên HOMER Pro', width_cm=14.0)
P('Về chiến lược điều độ và ràng buộc hệ thống: mô hình ưu tiên dùng trực tiếp nguồn tái tạo cho phụ tải, phần dư nạp vào '
  'BESS cho tới ngưỡng đầy, phần vượt khả năng hấp thụ bị cắt giảm (curtailment); khi mở rộng sang phương án có nguồn dự phòng, '
  'máy phát diesel chỉ khởi động khi BESS chạm SoC tối thiểu. Ràng buộc chính thức đặt tỷ lệ thiếu công suất hằng năm '
  '(Max annual capacity shortage) bằng 0 % và đánh giá thêm ngưỡng cắt giảm điện dư ≤ 10 % để bảo đảm tính thực tiễn kỹ thuật [1], [2].')

# ===================== CHUONG 3 =====================
H('CHƯƠNG 3: TÍNH TOÁN, MÔ PHỎNG VÀ ĐÁNH GIÁ HỆ THỐNG ST – GIAI ĐOẠN 3 TẠI CÔN ĐẢO', 1)

H('3.1. Vị trí địa lý, điều kiện tự nhiên và sơ đồ nguyên lý', 2)
P('Khu vực nghiên cứu nằm tại quần đảo Côn Đảo (tỉnh Bà Rịa – Vũng Tàu), có tọa độ địa lý khoảng 8,68° vĩ Bắc '
  'và 106,62° kinh Đông, cách đất liền (TP. Vũng Tàu) khoảng 80 hải lý (≈ 148 km) như minh họa trên Hình 3.1 và Hình 3.2. '
  'Khoảng cách xa đất liền khiến phương án cấp điện độc lập từ nguồn năng lượng tái tạo kết hợp tích trữ có vai trò quan trọng '
  'khi chưa có tuyến cáp ngầm nối lưới [10].')
IMG('con_dao_region.png', 'Hình 3.1. Vị trí khu vực Côn Đảo trên biển Đông', width_cm=13.0)
IMG('con_dao_islands.png', 'Hình 3.2. Ảnh vệ tinh quần đảo Côn Đảo', width_cm=10.5)

P('Về địa hình và phân bố phụ tải, Côn Đảo có cấu trúc đá granit với dải đồi núi dốc ra sát biển, thuận lợi cho các '
  'hướng gió biển thổi qua quanh năm (Hình 3.3). Trong khi đó, dân cư, cơ quan, chợ trung tâm và các cơ sở lưu trú du lịch '
  'tập trung tại vùng trung tâm đảo (Hình 3.4), hình thành ba nhóm phụ tải chính của gói dự án ST – Giai đoạn 3.')
IMG('eq_con_dao_coast.jpg', 'Hình 3.3. Đường ven biển và địa hình đồi núi đặc trưng của Côn Đảo '
    '(Ảnh: Lam Tr Th, Wikimedia Commons, CC BY-SA 3.0)', width_cm=13.0)
IMG('eq_con_dao_market.jpg', 'Hình 3.4. Khu chợ trung tâm Côn Đảo – nơi tập trung phụ tải dân dụng '
    'và dịch vụ (Ảnh: Phương Huy, Wikimedia Commons, phạm vi công cộng)', width_cm=11.5)

P('Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3 được trình bày trên Hình 3.5. Hệ thống gồm ba dàn pin mặt trời '
  'tổng 213,2 kWp nối qua ba biến tần chuỗi 100 kW lên thanh cái AC 0,4 kV, một tuabin gió 2.000 kW, hai hệ thống pin '
  'lưu trữ tổng dung lượng 11.700 kWh kết nối qua hai biến tần tạo lưới (GFI) 1 MW, và tủ phân phối hạ thế 12 ngăn '
  'cấp điện cho ba nhóm phụ tải tổng công suất đặt 783,1 kW.')
IMG('st_diagram.png', 'Hình 3.5. Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3', width_cm=14.5)

H('3.2. Dữ liệu bức xạ, gió, phụ tải và thông số kinh tế – thiết bị', 2)
P('Số liệu bức xạ và nhiệt độ trung bình nhiều năm (2001–2025) trích xuất từ cơ sở dữ liệu NASA POWER [3] tại tọa độ '
  '8,68°N – 106,60°E được tổng hợp trong Bảng 3.1 và khai báo trong HOMER Pro như Hình 3.6. Tổng xạ trung bình năm '
  'đạt 5,26 kWh/m²/ngày (Bảng 3.1), cao nhất vào tháng 4 (6,65 kWh/m²/ngày) và thấp nhất vào tháng 12 (4,40 kWh/m²/ngày). '
  'Trong tính toán giải tích bảo thủ, báo cáo chọn mức thiết kế 4,9 kWh/m²/ngày (%s kWh/m²/năm) với PR = 0,80 [6].' % vn(GHI_year, 1))
TBL(
    ['Tháng', 'Bức xạ (kWh/m²)', 'Nhiệt độ TB (°C)', 'Cao nhất (°C)', 'Thấp nhất (°C)', 'Độ ẩm (%)'],
    [['Tháng 1', '5,02', '25,1', '28,1', '22,8', '86,1'], ['Tháng 2', '5,96', '25,4', '27,7', '23,1', '85,1'], ['Tháng 3', '6,37', '26,5', '28,9', '23,6', '83,6'], ['Tháng 4', '6,65', '28,1', '30,0', '25,0', '81,1'], ['Tháng 5', '5,59', '28,9', '30,8', '25,8', '81,2'], ['Tháng 6', '4,99', '28,7', '30,7', '26,1', '81,9'], ['Tháng 7', '4,83', '28,3', '30,3', '25,9', '82,3'], ['Tháng 8', '5,05', '28,3', '29,6', '26,5', '82,6'], ['Tháng 9', '4,90', '28,2', '30,1', '25,8', '82,0'], ['Tháng 10', '4,80', '27,9', '29,7', '25,7', '82,5'], ['Tháng 11', '4,66', '27,3', '29,0', '25,0', '84,8'], ['Tháng 12', '4,40', '26,2', '28,4', '23,0', '85,3'], ['Trung bình năm', '5,26', '27,4', '30,8', '22,8', '83,2']],
    widths=[2.8, 3.0, 2.8, 2.5, 2.5, 2.4],
    caption='Bảng 3.1. Thông số khí tượng trung bình tháng tại Côn Đảo (NASA POWER)')
P('Theo Bảng 3.1 và [3], nhiệt độ không khí trung bình năm tại Côn Đảo đạt 27,4 °C (dao động 25,1–28,9 °C giữa tháng 1 và '
  'tháng 5), độ ẩm trung bình 83,2 %. Vào buổi trưa bức xạ 800 W/m² và nhiệt độ môi trường 30 °C, nhiệt độ tế bào PV đạt '
  'khoảng 55 °C (NOCT ≈ 45 °C), làm suy giảm khoảng 10 % công suất so với điều kiện chuẩn [6]; tổn thất này đã được gộp trong PR = 0,80.')
IMG('homer_ghi_crop.png', 'Hình 3.6. Khai báo dữ liệu bức xạ mặt trời NASA trên HOMER Pro', width_cm=9.6)

P('Số liệu tốc độ gió từ NASA POWER [3], [5] nội suy về cao trình trục 78 m theo công thức (2.10) với α = 0,143 [7] được trình bày '
  'trong Bảng 3.2. Gió phân hóa mùa rõ rệt: mạnh nhất vào mùa gió Đông Bắc (tháng 12–2 đạt 9,54–11,00 m/s ở 78 m) và yếu '
  'nhất vào tháng 4–5 (4,97–5,70 m/s ở 78 m), trung bình năm đạt 7,67 m/s (Bảng 3.2). Sự lệch pha giữa tháng ít gió (tháng 4–5) '
  'và tháng nhiều nắng (tháng 3–4 đạt 6,37–6,65 kWh/m²/ngày, Bảng 3.1) tạo tính bổ trợ tự nhiên cho nguồn tái tạo.')
TBL(
    ['Tháng', 'Gió ở 2 m (m/s)', 'Gió ở 50 m (m/s)', 'Gió ở 78 m (m/s)'],
    [['Tháng 1', '7,47', '10,15', '10,82'], ['Tháng 2', '6,67', '8,95', '9,54'], ['Tháng 3', '5,40', '7,03', '7,49'], ['Tháng 4', '4,32', '5,35', '5,70'], ['Tháng 5', '3,86', '4,66', '4,97'], ['Tháng 6', '4,72', '5,87', '6,26'], ['Tháng 7', '5,35', '6,79', '7,24'], ['Tháng 8', '5,76', '7,38', '7,86'], ['Tháng 9', '5,10', '6,42', '6,84'], ['Tháng 10', '4,63', '5,78', '6,16'], ['Tháng 11', '5,95', '7,79', '8,30'], ['Tháng 12', '7,62', '10,32', '11,00'], ['Trung bình năm', '5,57', '7,20', '7,67']],
    widths=[3.4, 4.2, 4.2, 4.2],
    caption='Bảng 3.2. Tốc độ gió trung bình tháng tại Côn Đảo (NASA POWER)')

P('Cơ cấu phụ tải gồm ba nhóm tổng công suất đặt 783,1 kW được liệt kê trong Bảng 3.3, trong đó nhóm cơ sở lưu trú KT '
  'chiếm 79,8 % công suất đặt, nhóm hiện trạng 15,1 % và nhóm CS 5,1 % (Bảng 3.3). Trên HOMER Pro, phụ tải giờ thực tế '
  '(January Profile, Hình 3.7) được khai báo trực tiếp theo quy mô tải đảo từ 230–245 kW ban đêm đến 620–640 kW vào giờ cao điểm tối '
  'cùng nhiễu ngẫu nhiên 3 % ngày và 5 % giờ, cho sản lượng trung bình 10.337 kWh/ngày (430,71 kW), đỉnh năm 748,17 kW (≤ 783,1 kW) '
  'và hệ số tải k_{tải} = 0,58; giải tích sử dụng hệ số bảo thủ k_{tải} = 0,55 (10.336,9 kWh/ngày) với khảo sát độ nhạy k_{tải} = 0,50–0,60 '
  '(9.397–11.277 kWh/ngày). Các thông số kinh tế đầu vào của dự án cho trong Bảng 3.4 [1].')
TBL(
    ['Nhóm phụ tải', 'Công suất đặt (kW)', 'Tỷ trọng (%)', 'Đặc điểm sử dụng'],
    [
        ['Phụ tải hiện trạng', '118,1', '15,1', 'Khu dân cư và cơ quan hiện hữu trên đảo'],
        ['Phụ tải CS', '40,0', '5,1', 'Hạ tầng, chiếu sáng công cộng và dịch vụ'],
        ['Phụ tải KT', '625,0', '79,8', 'Cơ sở lưu trú, du lịch – nghỉ dưỡng'],
        ['Tổng cộng', '783,1', '100,0', 'Công suất đặt/đỉnh của hệ thống'],
    ],
    widths=[4.0, 3.2, 2.8, 6.0],
    caption='Bảng 3.3. Cơ cấu phụ tải của hệ thống ST – Giai đoạn 3')
IMG('homer_load_crop.png', 'Hình 3.7. Khai báo đồ thị phụ tải giờ (January Profile, Peak 748,17 kW) trên HOMER Pro', width_cm=15.5)
TBL(
    ['Thông số', 'Giá trị', 'Ghi chú'],
    [
        ['Discount rate (danh nghĩa)', '8,00 %/năm', 'Lãi suất chiết khấu danh nghĩa'],
        ['Inflation rate', '2,00 %/năm', 'Tỷ lệ lạm phát'],
        ['Lãi suất chiết khấu thực r', '%s %%/năm' % vn(r_real * 100, 2), 'r = (1 + 0,08)/(1 + 0,02) − 1'],
        ['Annual capacity shortage', '0,00 %', 'Không cho phép thiếu hụt'],
        ['Project lifetime', '25 năm', 'Thời gian dự án'],
        ['Location', '8,683°N – 106,617°E', 'Côn Đảo (Bà Rịa – Vũng Tàu)'],
    ],
    widths=[6.0, 4.5, 5.5], caption='Bảng 3.4. Thông số kinh tế và thời gian dự án')

P('Tổng hợp thông số thiết bị theo sơ đồ nguyên lý (Hình 3.5) trình bày trong Bảng 3.5. Hệ nguồn PV chọn tấm pin đơn '
  'tinh thể half-cut công suất 650 Wp (Bảng 3.6, Hình 3.8), gồm 328 tấm chia thành 3 dàn đấu qua 3 biến tần chuỗi 100 kW '
  '(tổng 300 kW, tỷ số DC/AC 0,711 theo công thức 2.7), đạt hiệu suất module khoảng 21,5 % và hệ số nhiệt −0,34 %/°C (Bảng 3.6).')
TBL(
    ['Nhóm', 'Thiết bị', 'Thông số định mức', 'Số lượng', 'Tổng công suất'],
    [
        ['Nguồn PV', 'Tấm pin quang điện 650 Wp', 'Dàn A: 650 Wp × 109 tấm', '1 dàn', '70,85 kWp'],
        ['', '', 'Dàn B: 650 Wp × 109 tấm', '1 dàn', '70,85 kWp'],
        ['', '', 'Dàn C: 650 Wp × 110 tấm', '1 dàn', '71,50 kWp'],
        ['', 'Biến tần PV', '100 kW', '3 bộ', '300 kW'],
        ['Nguồn gió', 'Tuabin gió', '2.000 kW', '1 bộ', '2.000 kW'],
        ['Lưu trữ', 'Battery (pin Li-ion)', '5.800 kWh', '1 bộ', '5.800 kWh'],
        ['', '', '5.900 kWh', '1 bộ', '5.900 kWh'],
        ['', 'Biến tần tạo lưới', '1 MW', '2 bộ', '2.000 kW'],
        ['Phụ tải', 'Phụ tải hiện trạng', '118,1 kW', '', '118,1 kW'],
        ['', 'Phụ tải CS', '40,0 kW', '', '40,0 kW'],
        ['', 'Phụ tải KT', '625,0 kW', '', '625,0 kW'],
        ['Hạ thế', 'Tủ phân phối hạ thế 12 ngăn', '0,4 kV', '1', '—'],
        ['', 'MCCB', '200 A / 1.000 A / 1.600 A', '', '—'],
    ],
    widths=[2.0, 4.3, 4.7, 2.0, 3.0], caption='Bảng 3.5. Tổng hợp thông số thiết bị của hệ thống')
TBL(
    ['Thông số', 'Giá trị'],
    [
        ['Công suất đỉnh (Wp)', '650 Wp'],
        ['Công nghệ', 'Đơn tinh thể (Mono) half-cut, 2 mặt kính'],
        ['Hiệu suất module', '≈ 21,5 %'],
        ['Điện áp tại điểm công suất cực đại (Vmp)', '≈ 41,5 V'],
        ['Dòng điện tại điểm công suất cực đại (Imp)', '≈ 15,7 A'],
        ['Điện áp hở mạch (Voc)', '≈ 49,5 V'],
        ['Dòng điện ngắn mạch (Isc)', '≈ 16,6 A'],
        ['Hệ số nhiệt công suất', '−0,34 %/°C'],
        ['Suy giảm công suất theo năm', '≤ 0,5 %/năm'],
        ['Tuổi thọ thiết kế', '25 năm'],
    ],
    widths=[9.0, 5.5], caption='Bảng 3.6. Thông số kỹ thuật tấm pin quang điện 650 Wp')
IMG('eq_pv_module.png', 'Hình 3.8. Tấm pin quang điện đơn tinh thể (mono) (Ảnh: Lamiot, Wikimedia Commons, CC BY-SA 3.0)', width_cm=10.5)

P('Nguồn gió trong cấu hình ban đầu là 01 tuabin Enercon E-82 E2 công suất định mức 2.000 kW, truyền động trực tiếp không '
  'hộp số, cấp chịu gió IEC IIA [8] (Bảng 3.7, Hình 3.9). Đường cong công suất khai báo trên HOMER Pro cho trong Bảng 3.8.')
TBL(
    ['Thông số', 'Giá trị'],
    [
        ['Model', 'Enercon E-82 E2'],
        ['Công suất định mức', '2.000 kW'],
        ['Số cánh / đường kính rôto', '3 cánh / 82 m'],
        ['Diện tích quét', '5.281 m²'],
        ['Chiều cao trục (hub height)', '78 m (hoặc 98 m)'],
        ['Tốc độ gió khởi động (cut-in)', '2 – 3 m/s'],
        ['Tốc độ gió định mức', '13 m/s'],
        ['Tốc độ gió dừng (cut-out)', '25 m/s'],
        ['Cấp chịu gió', 'IEC IIA'],
        ['Truyền động', 'Trực tiếp (direct drive), không hộp số'],
        ['Điều khiển', 'Tốc độ thay đổi, điều chỉnh pitch'],
        ['Hệ số công suất CF tại Côn Đảo', '0,38 (tính toán) – 0,41 (HOMER Pro)'],
        ['Tuổi thọ thiết kế', '20 năm'],
    ],
    widths=[9.0, 5.5], caption='Bảng 3.7. Thông số kỹ thuật tuabin gió Enercon E-82 E2')
TBL(
    ['Tốc độ gió (m/s)', 'Công suất phát (kW)'],
    [
        ['2', '0'], ['3', '20'], ['4', '80'], ['5', '175'], ['6', '330'],
        ['7', '560'], ['8', '870'], ['9', '1.250'], ['10', '1.650'], ['11', '1.930'],
        ['12', '2.000'], ['13 – 25', '2.000'],
    ],
    widths=[6.0, 6.0], caption='Bảng 3.8. Đường cong công suất tuabin gió Enercon E-82 E2')
for _row in doc.tables[-1].rows:
    for _c in _row.cells:
        for _p in _c.paragraphs:
            _p.alignment = WD_ALIGN_PARAGRAPH.CENTER
IMG('eq_wind_e82.jpg', 'Hình 3.9. Tuabin gió Enercon E-82 E2 tại trang trại gió Mausdorf, Đức (Ảnh: Spike, Wikimedia Commons, CC BY-SA 4.0)', width_cm=8.2)

P('Hệ lưu trữ lựa chọn pin LiFePO₄ (LFP) thay cho ắc quy chì–axit nhờ độ sâu xả đạt 80–90 % (so với 50 % của chì–axit), '
  'tuổi thọ 3.000–6.000 chu kỳ (gấp 3–5 lần) và hiệu suất vòng 90–95 % (Bảng 3.9) [6]. Cấu hình gồm 117 khối 100 kWh chia '
  'thành hai cụm 5.800 kWh và 5.900 kWh (tổng 11.700 kWh, Bảng 3.10), bố trí trong container kèm tủ biến tần tạo lưới 2 × 1 MW (Hình 3.10).')
TBL(
    ['Tiêu chí', 'Ắc quy chì–axit', 'Pin Li-ion (LFP)'],
    [
        ['Độ sâu xả cho phép (DoD)', '50 %', '80 – 90 %'],
        ['Tuổi thọ chu kỳ', '500 – 1.200 chu kỳ', '3.000 – 6.000 chu kỳ'],
        ['Hiệu suất vòng (round-trip)', '75 – 85 %', '90 – 95 %'],
        ['Mật độ năng lượng', '30 – 40 Wh/kg', '100 – 150 Wh/kg'],
        ['Chi phí đầu tư ban đầu', 'Thấp hơn', 'Cao hơn 1,5 – 2 lần'],
        ['Chi phí năng lượng quy dẫn (LCOS)', 'Cao', 'Thấp hơn nhờ tuổi thọ dài'],
        ['Bảo dưỡng', 'Thường xuyên, có khí thoát', 'Gần như không bảo dưỡng'],
        ['Mức độ phù hợp với microgrid đảo', 'Hạn chế', 'Phù hợp'],
    ],
    widths=[5.5, 5.0, 5.5], caption='Bảng 3.9. So sánh ắc quy chì–axit và pin Li-ion cho hệ lưu trữ')
TBL(
    ['Thông số', 'Giá trị'],
    [
        ['Tổng dung lượng danh định', '11.700 kWh'],
        ['Cấu hình', '2 bộ: 5.800 kWh + 5.900 kWh (117 khối × 100 kWh)'],
        ['Điện áp danh định', '600 V DC'],
        ['Dung lượng mỗi khối', '100 kWh / 167 Ah'],
        ['Hiệu suất vòng (round-trip)', '≈ 90 %'],
        ['Dải trạng thái sạc (SoC)', '10 – 100 % (DoD 90 %)'],
        ['Tuổi thọ thiết kế', '15 năm (hoặc 3.000 chu kỳ tương đương)'],
        ['Tốc độ sạc/xả vận hành (C-rate)', '≈ 0,17 h⁻¹'],
        ['Công suất biến tần tạo lưới', '2 × 1 MW'],
    ],
    widths=[9.0, 5.5], caption='Bảng 3.10. Thông số hệ thống pin lưu trữ Li-ion')
IMG('eq_bess_container.jpg', 'Hình 3.10. Hệ thống pin lưu trữ dạng container và tủ biến tần (Ảnh: Kecko, Wikimedia Commons, CC BY 2.0)', width_cm=13.0)

H('3.3. Kết quả tính toán giải tích cấu hình ban đầu', 2)
P('Áp dụng các công thức (2.1)–(2.4) ở Mục 2.1 với tổng công suất đặt 783,1 kW và k_{tải} = 0,55 thu được các thông số '
  'phụ tải tổng hợp trong Bảng 3.11:')
FORMULA('P_{đỉnh} = 118,1 + 40,0 + 625,0 = 783,1 kW')
FORMULA('P_{tb} = 0,55 × 783,1 = %s kW ;  E_{ngày} = %s kWh/ngày ;  E_{năm} = %s kWh/năm' % (vn(P_avg, 1), vn(E_day, 1), vn(E_load, 0)))
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất đỉnh', 'P_{đỉnh}', '783,1 kW'],
        ['Phụ tải trung bình', 'P_{tb}', '%s kW' % vn(P_avg, 1)],
        ['Điện năng ngày', 'E_{ngày}', '%s kWh/ngày' % vn(E_day, 1)],
        ['Điện năng năm', 'E_{năm}', '%s kWh/năm' % vn(E_load, 0)],
    ],
    widths=[7.0, 3.5, 5.5], caption='Bảng 3.11. Kết quả tính toán phụ tải')

P('Áp dụng (2.5)–(2.14) cho dàn PV 213,2 kWp (H = %s kWh/m²/năm, PR = 0,80), tuabin gió 2.000 kW (CF = 0,38) và hệ pin '
  '11.700 kWh (DoD = 0,90) thu được kết quả chi tiết trong các Bảng 3.12, Bảng 3.13 và Bảng 3.14.' % vn(GHI_year, 1))
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất đỉnh lắp đặt', 'P_{PV}', '213,2 kWp'],
        ['Tổng công suất biến tần PV', 'P_{inv}', '300 kW'],
        ['Tỷ số DC/AC', 'k_{DC/AC}', vn(k_dcac, 3)],
        ['Sản lượng điện năm', 'E_{PV}', '%s kWh/năm' % vn(E_pv, 0)],
        ['Sản lượng trung bình ngày', 'E_{PV ngày}', '%s kWh/ngày' % vn(E_pv_day, 1)],
    ],
    widths=[7.0, 3.5, 5.5], caption='Bảng 3.12. Kết quả tính toán hệ điện mặt trời')
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất định mức', 'P_{đm}', '2.000 kW'],
        ['Hệ số công suất', 'CF', '0,38'],
        ['Sản lượng điện năm', 'E_{gió}', '%s kWh/năm' % vn(E_wind, 0)],
        ['Số giờ làm việc hiệu dụng', 'h_{gió}', '%s giờ/năm' % vn(h_wind, 0)],
        ['Tỷ lệ sản lượng gió so với phụ tải', '—', '%s %%' % vn(share_wind * 100, 1)],
    ],
    widths=[7.0, 3.5, 5.5], caption='Bảng 3.13. Kết quả tính toán tuabin gió')
P('Theo Bảng 3.13, sản lượng gió đạt %s kWh/năm, tương đương %s %% tổng nhu cầu phụ tải năm (%s kWh/năm); tổng nguồn '
  'tái tạo giải tích bằng %s %% phụ tải (Bảng 3.17). Điều này báo hiệu phần điện gió sản sinh vượt xa nhu cầu phụ tải '
  'và hệ BESS 11.700 kWh (thời gian tự chủ %s giờ ở tải trung bình, Bảng 3.14) không thể hấp thụ hết phần điện dư trong hệ off-grid.' % (
      vn(E_wind, 0), vn(share_wind * 100, 1), vn(E_load, 0), vn(share_re * 100, 1), vn(t_aut_avg, 1)))
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Tổng dung lượng danh định', 'E_{pin}', '11.700 kWh'],
        ['Độ sâu xả cho phép', 'DoD', '0,90'],
        ['Dung lượng khả dụng', 'E_{khả dụng}', '%s kWh' % vn(E_batt_usable, 0)],
        ['Thời gian tự chủ tại tải trung bình', 't_{tb}', '%s giờ' % vn(t_aut_avg, 1)],
        ['Thời gian tự chủ tại tải đỉnh', 't_{đỉnh}', '%s giờ' % vn(t_aut_peak, 1)],
        ['C-rate xả cực đại', 'C', '%s h⁻¹' % vn(c_rate, 3)],
    ],
    widths=[7.0, 3.5, 5.5], caption='Bảng 3.14. Kết quả tính toán hệ thống pin lưu trữ')

P('Áp dụng (2.15)–(2.19) theo đơn giá dự toán thiết bị thu được tổng vốn đầu tư ban đầu và các chỉ tiêu tài chính giải tích '
  'tại Bảng 3.15, Bảng 3.16; toàn bộ bảng tổng hợp chỉ tiêu giải tích của cấu hình ban đầu được tập hợp trong Bảng 3.17.')
TBL(
    ['Hạng mục', 'Đơn giá (triệu VNĐ)', 'Khối lượng', 'Thành tiền (triệu VNĐ)'],
    [
        ['Tấm pin PV', '62,5 /kWp', '213,2 kWp', vn(C_pv, 0)],
        ['Biến tần PV', '7,5 /kW', '300 kW', vn(C_pvinv, 0)],
        ['Tuabin gió', '50 /kW', '2.000 kW', vn(C_wind, 0)],
        ['Pin lưu trữ', '6 /kWh', '11.700 kWh', vn(C_batt, 0)],
        ['Biến tần tạo lưới', '10 /kW', '2.000 kW', vn(C_gfi, 0)],
        ['Tủ phân phối + MCCB', '—', '1 bộ', vn(p_board, 0)],
        ['Tổng vốn đầu tư', 'C₀', '', vn(C_capex, 0)],
    ],
    widths=[5.5, 3.5, 3.0, 4.0], caption='Bảng 3.15. Vốn đầu tư ban đầu của cấu hình giải tích')
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Lãi suất chiết khấu thực', 'r', '%s %%' % vn(r_real * 100, 2)],
        ['Thời gian dự án', 'N', '25 năm'],
        ['Hệ số thu hồi vốn', 'CRF', vn(CRF, 4)],
        ['Vốn đầu tư ban đầu', 'C₀', '%s triệu VNĐ' % vn(C_capex, 0)],
        ['Chi phí vận hành bảo dưỡng năm', 'OM', '%s triệu VNĐ/năm' % vn(OM_year, 1)],
        ['Chi phí vòng đời (NPC)', 'NPC', '%s triệu VNĐ' % vn(NPC, 0)],
        ['Chi phí thường niên tương đương', 'C_{ann}', '%s triệu VNĐ/năm' % vn(C_ann, 0)],
        ['Chi phí điện quy dẫn', 'COE', '%s VNĐ/kWh' % vn(COE, 0)],
        ['Thời gian hoàn vốn đơn giản', 'T_{hv}', '%s năm' % vn(payback, 2)],
    ],
    widths=[7.0, 3.5, 5.5], caption='Bảng 3.16. Kết quả các chỉ tiêu kinh tế giải tích')
TBL(
    ['STT', 'Chỉ tiêu tổng hợp', 'Giá trị'],
    [
        ['1', 'Tổng công suất phụ tải đỉnh', '%s kW' % vn(P_peak, 1)],
        ['2', 'Điện năng tiêu thụ năm', '%s kWh/năm' % vn(E_load, 0)],
        ['3', 'Công suất PV lắp đặt / Sản lượng PV năm', '213,2 kWp / %s kWh/năm' % vn(E_pv, 0)],
        ['4', 'Công suất tuabin gió / Sản lượng gió năm', '2.000 kW / %s kWh/năm' % vn(E_wind, 0)],
        ['5', 'Tổng sản lượng nguồn tái tạo', '%s kWh/năm' % vn(E_re, 0)],
        ['6', 'Tỷ lệ sản lượng tái tạo so với nhu cầu phụ tải', '%s %%' % vn(share_re * 100, 1)],
        ['7', 'Dung lượng pin / Thời gian tự chủ tải TB', '11.700 kWh / %s giờ' % vn(t_aut_avg, 1)],
        ['8', 'Vốn đầu tư ban đầu / Chi phí vòng đời (NPC)', '%s / %s triệu VNĐ' % (vn(C_capex, 0), vn(NPC, 0))],
        ['9', 'Chi phí điện quy dẫn (COE) / Hoàn vốn', '%s VNĐ/kWh / %s năm' % (vn(COE, 0), vn(payback, 2))],
    ],
    widths=[1.5, 9.0, 5.5], caption='Bảng 3.17. Bảng tổng hợp kết quả tính toán giải tích cấu hình ban đầu')

H('3.4. Kết quả mô phỏng hiện hành và phương án hiệu chỉnh cấu hình', 2)
P('Kết quả mô phỏng cấu hình ban đầu trên phần mềm HOMER Pro được ghi nhận trên Hình 3.11, Hình 3.12 và tổng hợp trong '
  'Bảng 3.18 [1]. Đối chiếu song song giữa phương pháp giải tích và kết quả mô phỏng ban đầu trên HOMER Pro được trình bày trong Bảng 3.19.')
IMG('homer_results_table_crop.png', 'Hình 3.11. Kết quả mô phỏng cấu hình ban đầu trên phần mềm HOMER Pro', width_cm=16.0)
IMG('homer_cashflow_crop.png', 'Hình 3.12. Biểu đồ dòng tiền vòng đời (Cash Flow Summary) của cấu hình ban đầu trên HOMER Pro', width_cm=14.0)

_PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOMER = json.load(io.open(os.path.join(_PROJ_ROOT, 'homer', 'homer_results.json'), encoding='utf-8'))[0]
REAL_OPT = json.load(io.open(os.path.join(_PROJ_ROOT, 'homer', 'homer_toi_uu_results.json'), encoding='utf-8'))
E_served = HOMER['annual_consumption']
E_unmet = HOMER['unmet_load']
E_total_load = E_served + E_unmet
E_excess = HOMER['excess_electricity']
pct_unmet = 100.0 * E_unmet / E_total_load
pct_excess = 100.0 * E_excess / HOMER['annual_production']
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Đơn vị', 'Giá trị'],
    [
        ['Công suất dàn pin quang điện lắp đặt', 'P_{PV}', 'kWp', vn(HOMER['pv_size'], 1)],
        ['Sản lượng điện mặt trời hàng năm', 'E_{PV}', 'kWh/năm', vn(HOMER['pv_production'], 0)],
        ['Số lượng tuabin gió (Enercon E-82 E2)', 'n_{gió}', 'bộ', vn(HOMER['wind_quantity'], 0)],
        ['Sản lượng điện gió hàng năm', 'E_{gió}', 'kWh/năm', vn(HOMER['wind_production'], 0)],
        ['Tổng sản lượng điện phát trong năm', 'E_{phát}', 'kWh/năm', vn(HOMER['annual_production'], 0)],
        ['Điện năng phục vụ phụ tải', 'E_{phục vụ}', 'kWh/năm', vn(E_served, 0)],
        ['Điện năng dư không sử dụng được', 'E_{dư}', 'kWh/năm', vn(E_excess, 0)],
        ['Điện năng thiếu so với phụ tải', 'E_{thiếu}', 'kWh/năm', vn(E_unmet, 0)],
        ['Tỷ lệ năng lượng tái tạo', 'RF', '%', vn(HOMER['renewable_fraction'], 0)],
        ['Dung lượng pin danh định (117 bộ × 100 kWh)', 'E_{pin}', 'kWh', vn(HOMER['storage_nominal'], 0)],
        ['Dung lượng pin khả dụng theo DoD', 'E_{pin,khả dụng}', 'kWh', vn(HOMER['storage_usable'], 0)],
        ['Thời gian tự chủ của hệ pin', 't_{tự chủ}', 'giờ', vn(HOMER['storage_autonomy'], 1)],
        ['Điện năng nạp – xả qua pin trong năm', 'E_{qua pin}', 'kWh/năm', vn(HOMER['storage_throughput'], 0)],
        ['Công suất bộ biến tần (converter)', 'P_{conv}', 'kW', vn(HOMER['converter_size'], 0)],
        ['Vốn đầu tư ban đầu', 'CAPEX', 'USD', vn(HOMER['capital_cost'], 0)],
        ['Chi phí vòng đời quy về hiện tại', 'NPC', 'USD', vn(HOMER['net_present_cost'], 0)],
        ['Chi phí điện quy dẫn', 'LCOE', 'USD/kWh', vn(HOMER['cost_of_energy'], 4)],
        ['Chi phí vận hành – bảo dưỡng hàng năm', 'O\\&M', 'USD/năm', vn(HOMER['operating_cost'], 0)],
    ],
    widths=[6.6, 3.2, 2.4, 3.8], caption='Bảng 3.18. Kết quả mô phỏng cấu hình ban đầu trên phần mềm HOMER Pro')

TBL(
    ['Chỉ tiêu', 'Tính toán giải tích (Mục 3.3)', 'Mô phỏng HOMER Pro ban đầu (Bảng 3.18)', 'Nhận xét'],
    [
        ['Vốn đầu tư ban đầu', '%s triệu VNĐ' % vn(C_capex, 0), '7,08 triệu USD', 'Đơn giá tham chiếu phần mềm'],
        ['Chi phí vòng đời (NPC)', '%s triệu VNĐ' % vn(NPC, 0), '9,40 triệu USD', 'Đã tính thay thế pin'],
        ['Chi phí điện quy dẫn', '%s VNĐ/kWh' % vn(COE, 0), '0,2351 USD/kWh (≈ 5.878 VNĐ)', 'Chênh lệch ≈ 6 %'],
        ['Sản lượng điện mặt trời', '%s kWh' % vn(E_pv, 0), '344.681 kWh', 'Chuỗi bức xạ NASA theo giờ'],
        ['Sản lượng điện gió', '%s kWh' % vn(E_wind, 0), '7.237.202 kWh', 'CF thực mô phỏng 0,41'],
        ['Điện năng phục vụ tải', '%s kWh' % vn(E_load, 0), '3.093.168 kWh (thiếu 18,0 %)', 'Nghẽn tại converter 100 kW'],
        ['Tỷ lệ điện dư', 'Chưa xét theo giờ', '4.426.778 kWh (58,4 %)', 'Dư công suất gió 2.000 kW'],
    ],
    widths=[3.4, 4.2, 4.6, 3.8], caption='Bảng 3.19. Đối chiếu kết quả tính toán giải tích và mô phỏng ban đầu trên HOMER Pro')

P('Từ Bảng 3.18 và Bảng 3.19, kết quả mô phỏng cấu hình ban đầu trên HOMER Pro chưa đạt hai yêu cầu vận hành cốt lõi của đồ án: '
  '(i) tỷ lệ thiếu tải lên tới %s %% (%s kWh/năm) do bộ converter chỉ khai báo %s kW, nhỏ hơn phụ tải đỉnh 783,1 kW; và '
  '(ii) tỷ lệ điện năng dư lên tới %s %% (%s kWh/năm, vượt xa ngưỡng ≤ 10 %%) do một tuabin E-82 2.000 kW phát tới 7,24 triệu kWh/năm, '
  'gần gấp đôi nhu cầu phụ tải năm (3,77 triệu kWh/năm).' % (
      vn(pct_unmet, 1), vn(E_unmet, 0), vn(HOMER['converter_size'], 0), vn(pct_excess, 1), vn(E_excess, 0)))

_cnt = REAL_OPT['summary_counts']
_base = REAL_OPT['base_case']
_low_all = REAL_OPT['lowest_npc_overall']
_opt = REAL_OPT['gvhd_top5'][0]
_co2_saved_base = (_base['co2_kg'] - _opt['co2_kg']) / 1000.0
_fuel_cut_pct = 100.0 * (1.0 - _opt['fuel_l'] / _base['fuel_l'])
_npc_cut_pct = 100.0 * (1.0 - _opt['npc'] / _base['npc'])
_cap_cut_orig = 100.0 * (1.0 - _opt['capex'] / HOMER['capital_cost'])

P('Để khắc phục hai điểm nghẽn nêu trên, mô hình đã được hiệu chỉnh trực tiếp (kèm đồ thị phụ tải giờ 230–640 kW, đỉnh 748,17 kW ≤ 783,1 kW) '
  'và chạy tối ưu hóa trên phần mềm HOMER Pro x64 phiên bản 3.18.5 [1]: (i) đặt ràng buộc thiếu công suất hằng năm bằng 0 %; (ii) mở dải biến tần '
  'Converter 0–1.200 kW, dàn PV 0–1.600 kWp và cụm BESS 20–117 khối; (iii) thay tuabin 2.000 kW quá cỡ bằng tổ hợp 0–2 tuabin '
  'Windflow 45 [500 kW] (cao trình trục 47 m, giữ nguyên suất đầu tư 1.923 USD/kW); và (iv) bổ sung máy phát diesel dự phòng '
  'tự chọn cỡ (Autosize Genset) gánh các ngày lặng gió tháng 4–5. Kết quả chạy trên HOMER Pro v3.18.5 được thể hiện ở Hình 3.13 '
  'và Hình 3.14.')
IMG('homer_opt_table.png', 'Hình 3.13. Bảng kết quả tối ưu hóa cấu hình trên phần mềm HOMER Pro x64 v3.18.5', width_cm=15.5)
IMG('homer_opt_summary.png', 'Hình 3.14. Biểu đồ dòng tiền tích lũy 25 năm và so sánh kinh tế với Base Case trên HOMER Pro', width_cm=15.5)

P('Trong tổng số %d cấu hình khảo sát có %d phương án khả thi và %d phương án đạt đồng thời chỉ tiêu 0,00 %% thiếu tải và '
  '≤ 10 %% điện năng dư (Bảng 3.20). Cần phân biệt rõ: phương án có NPC nhỏ nhất toàn cục trong Hình 3.13 là tổ hợp %d kWp PV + '
  '%d × 500 kW gió + %d khối BESS + %d kW diesel + %d kW Converter (chiến lược LF) với NPC %s triệu USD và LCOE %s USD/kWh, '
  'nhưng vẫn phát dư tới %s %% sản lượng do dùng 2 tuabin gió [1]. Ngược lại, khi chọn phương án đứng đầu nhóm đạt chuẩn kỹ thuật '
  '(Bảng 3.20): %s kWp PV + %d × 500 kW Windflow 45 + %d khối BESS (%s kWh) + %d kW Diesel + %d kW Converter (LF), hệ thống đạt đồng thời '
  '%s %% thiếu tải và chỉ %s %% điện dư (≤ 10 %%), tỷ lệ tái tạo RF = %s %%, NPC = %s triệu USD, LCOE = %s USD/kWh với IRR = %s %% '
  'và thời gian hoàn vốn đơn giản %s năm so với phương án chạy diesel thuần túy (Base Case) [1].' % (
      _cnt['total'], _cnt['feasible'], _cnt['gvhd_ok'],
      int(_low_all['pv_kw']), int(_low_all['wind_qty']), int(_low_all['bess_qty']), int(_low_all['gen_kw']), int(_low_all['conv_kw']),
      vn(_low_all['npc'] / 1e6, 2), vn(_low_all['coe'], 4), vn(_low_all['excess_pct'], 2),
      vn(_opt['pv_kw'], 0), int(_opt['wind_qty']), int(_opt['bess_qty']), vn(_opt['bess_qty'] * 100, 0),
      int(_opt['gen_kw']), int(_opt['conv_kw']),
      vn(_opt['unmet_pct'], 2), vn(_opt['excess_pct'], 2), vn(_opt['rf_pct'], 1),
      vn(_opt['npc'] / 1e6, 2), vn(_opt['coe'], 4), vn(_opt['irr'], 1), vn(_opt['simple_payback'], 2)))

c_rows = []
for row in REAL_OPT['gvhd_top5']:
    c_rows.append([
        vn(row['pv_kw'], 0),
        '%d×500' % int(row['wind_qty']),
        '%d (%s kWh)' % (int(row['bess_qty']), vn(row['bess_qty'] * 100, 0)),
        '%d (%s)' % (int(row['gen_kw']), row['dispatch']),
        vn(row['conv_kw'], 0),
        '%s / %s / %s' % (vn(row['rf_pct'], 1), vn(row['unmet_pct'], 2), vn(row['excess_pct'], 2)),
        '%s / %s / %s' % (vn(row['capex'] / 1e6, 2), vn(row['npc'] / 1e6, 2), vn(row['coe'], 4)),
    ])
TBL(
    ['PV (kWp)', 'Gió (kW)', 'BESS (khối)', 'Diesel (kW)', 'Conv (kW)', 'RF / Thiếu / Dư (%)', 'CAPEX / NPC (M$) / COE ($/kWh)'],
    c_rows,
    widths=[1.6, 1.5, 2.2, 2.0, 1.4, 3.1, 4.2],
    caption='Bảng 3.20. Top 5 cấu hình tối ưu trên HOMER Pro v3.18.5 đạt 0,00 % thiếu tải và ≤ 10 % điện dư')

H('3.5. Đánh giá hiệu quả kỹ thuật – kinh tế – môi trường của hệ thống', 2)
P('Để đánh giá đầy đủ hiệu quả trước và sau hiệu chỉnh, Bảng 3.21 đặt song song ba phương án mô phỏng trên phần mềm HOMER Pro: '
  'phương án chạy diesel tham chiếu (Base Case), cấu hình ban đầu (Bảng 3.18) và cấu hình tối ưu sau hiệu chỉnh (Bảng 3.20).')
TBL(
    ['Trụ cột', 'Chỉ tiêu chính', 'Base Case Diesel', 'Cấu hình ban đầu (Bảng 3.18)', 'Cấu hình chọn HOMER Pro (Bảng 3.20)'],
    [
        ['Kỹ thuật', 'Cấu hình nguồn chính', '%d kW Diesel + %d BESS (%s)' % (int(_base['gen_kw']), int(_base['bess_qty']), _base['dispatch']), '213,2 kWp PV + 2 MW Gió + 117 BESS', '%s kWp PV + %d×500 kW Gió + %d BESS + %d kW Diesel (%s)' % (vn(_opt['pv_kw'], 0), int(_opt['wind_qty']), int(_opt['bess_qty']), int(_opt['gen_kw']), _opt['dispatch'])],
        ['', 'Đáp ứng / Thiếu tải', '100 % (0,00 % thiếu)', '82,0 % (thiếu 18,0 %)', '100,0 %% (%s %% thiếu)' % vn(_opt['unmet_pct'], 2)],
        ['', 'Điện dư cắt giảm (%)', '0,00 %', '58,4 % (không đạt ≤ 10 %)', '%s %% (đạt chuẩn ≤ 10 %%)' % vn(_opt['excess_pct'], 2)],
        ['', 'Tỷ lệ tái tạo (RF)', '0,0 %', '100 % (cắt giảm 4,43 GWh/năm)', '%s %% (cấp đủ 3,77 GWh/năm)' % vn(_opt['rf_pct'], 1)],
        ['Kinh tế', 'Vốn đầu tư (CAPEX)', '%s triệu USD' % vn(_base['capex'] / 1e6, 2), '7,08 triệu USD', '%s triệu USD (giảm %s %% so cấu hình ban đầu)' % (vn(_opt['capex'] / 1e6, 2), vn(_cap_cut_orig, 1))],
        ['', 'Chi phí vòng đời (NPC)', '%s triệu USD' % vn(_base['npc'] / 1e6, 2), '9,40 triệu USD (thiếu tải)', '%s triệu USD (giảm %s %% so Base Case)' % (vn(_opt['npc'] / 1e6, 2), vn(_npc_cut_pct, 1))],
        ['', 'Chi phí điện quy dẫn (COE)', '%s USD/kWh' % vn(_base['coe'], 4), '0,2351 USD/kWh', '%s USD/kWh (giảm %s %% so Base Case)' % (vn(_opt['coe'], 4), vn(_npc_cut_pct, 1))],
        ['Môi trường', 'Tiêu thụ dầu diesel', '%s L/năm' % vn(_base['fuel_l'], 0), '0 L/năm', '%s L/năm (giảm %s %% so Base Case)' % (vn(_opt['fuel_l'], 0), vn(_fuel_cut_pct, 1))],
        ['', 'Phát thải CO₂ / Giảm trừ', '%s tấn/năm' % vn(_base['co2_kg'] / 1000.0, 1), '0 tấn/năm (tránh 2.289 tấn/năm)', '%s tấn/năm (giảm %s tấn/năm) [1], [12]' % (vn(_opt['co2_kg'] / 1000.0, 1), vn(_co2_saved_base, 1))],
    ],
    widths=[2.0, 3.0, 3.3, 3.5, 4.2],
    caption='Bảng 3.21. Đánh giá tổng hợp hiệu quả Kỹ thuật – Kinh tế – Môi trường trên HOMER Pro v3.18.5')

P('Về hiệu quả kỹ thuật: cấu hình đề xuất từ HOMER Pro v3.18.5 (%s kWp PV + %d × 500 kW gió + %s kWh BESS + %d kW diesel + '
  '%d kW Converter, Bảng 3.20) loại bỏ hoàn toàn hai nhược điểm của mô hình ban đầu: nâng tỷ lệ đáp ứng từ 82,0 %% lên 100,0 %% (%s %% thiếu '
  'so với phụ tải đỉnh thực tế 748,17 kW trong dải 783,1 kW) và giảm tỷ lệ điện dư từ 58,4 %% xuống còn %s %% (%s kWh/năm, đạt ngưỡng ≤ 10 %%, Bảng 3.21). Hệ pin '
  '%d khối (%s kWh) cung cấp thời gian tự chủ %s giờ và luân chuyển %s kWh/năm, giúp san bằng dao động ngày – đêm hiệu quả [1].' % (
      vn(_opt['pv_kw'], 0), int(_opt['wind_qty']), vn(_opt['bess_qty'] * 100, 0), int(_opt['gen_kw']), int(_opt['conv_kw']),
      vn(_opt['unmet_pct'], 2), vn(_opt['excess_pct'], 2), vn(_opt['excess_kwh'], 0),
      int(_opt['bess_qty']), vn(_opt['bess_qty'] * 100, 0), vn(_opt['bess_autonomy'], 2), vn(_opt['bess_throughput'], 0)))
P('Về hiệu quả kinh tế: so với cấu hình ban đầu chưa hiệu chỉnh, vốn đầu tư ban đầu giảm %s %% từ 7,08 triệu USD xuống còn %s triệu USD '
  '(Bảng 3.21) do cắt giảm dung lượng BESS từ 117 xuống %d khối và thu gọn tuabin gió xuống 500 kW. So với Base Case chạy diesel tại đảo '
  '(NPC %s triệu USD, LCOE %s USD/kWh, chi phí vận hành %s triệu USD/năm), cấu hình Hybrid đạt NPC %s triệu USD (giảm %s %%), '
  'LCOE %s USD/kWh (≈ %s VNĐ/kWh, thấp hơn gần một nửa chi phí phát diesel tham chiếu [11]), giá trị hiện tại ròng (Present Worth) '
  '%s triệu USD, IRR %s %% và hoàn vốn giản đơn chỉ %s năm (Hình 3.14) [1].' % (
      vn(_cap_cut_orig, 1), vn(_opt['capex'] / 1e6, 2), int(_opt['bess_qty']),
      vn(_base['npc'] / 1e6, 2), vn(_base['coe'], 4), vn(_base['operating_cost'] / 1e6, 2),
      vn(_opt['npc'] / 1e6, 2), vn(_npc_cut_pct, 1), vn(_opt['coe'], 4), vn(_opt['coe'] * 25000.0, 0),
      vn(_opt['present_worth'] / 1e6, 2), vn(_opt['irr'], 1), vn(_opt['simple_payback'], 2)))
P('Về hiệu quả môi trường: kết quả tính toán từ mô-đun phát thải của phần mềm HOMER Pro cho thấy '
  'lượng dầu diesel tiêu thụ giảm %s %% từ %s L/năm xuống còn %s L/năm; tương ứng lượng CO₂ phát thải giảm từ %s tấn/năm xuống '
  'còn %s tấn/năm, tức tránh được %s tấn CO₂/năm (giảm %s %%, Bảng 3.21) [1], [12]. Đồng thời các chất ô nhiễm độc hại tại chỗ '
  'như NOₓ giảm từ %s xuống %s kg/năm, SO₂ giảm từ %s xuống %s kg/năm, CO giảm từ %s xuống %s kg/năm và '
  'bụi PM giảm từ %s xuống %s kg/năm, góp phần bảo vệ hệ sinh thái Vườn quốc gia Côn Đảo.' % (
      vn(_fuel_cut_pct, 1), vn(_base['fuel_l'], 0), vn(_opt['fuel_l'], 0),
      vn(_base['co2_kg'] / 1000.0, 1), vn(_opt['co2_kg'] / 1000.0, 1), vn(_co2_saved_base, 1), vn(_fuel_cut_pct, 1),
      vn(_base['nox_kg'], 0), vn(_opt['nox_kg'], 0),
      vn(_base['so2_kg'], 0), vn(_opt['so2_kg'], 0),
      vn(_base['co_kg'], 0), vn(_opt['co_kg'], 0),
      vn(_base['pm_kg'], 1), vn(_opt['pm_kg'], 1)))

# ===================== CHUONG 6 =====================
H('KẾT LUẬN VÀ KIẾN NGHỊ', 1)

H('1. Kết luận', 2)
P('Trên cơ sở tổng quan các mô hình cấu hình off-grid (Chương 1), hệ thống hóa công thức giải tích và tiêu chí đánh giá '
  'kinh tế – kỹ thuật – môi trường trên HOMER Pro (Chương 2), và tính toán – mô phỏng cho dự án ST – Giai đoạn 3 tại Côn Đảo '
  '(Chương 3), báo cáo rút ra ba kết luận chính sau:')
for it in [
    'Phân tích từ phần mềm HOMER Pro chỉ ra nguyên nhân cấu hình ban đầu (213,2 kWp PV + 2.000 kW gió + '
    '11.700 kWh BESS + 100 kW Converter) không đạt chuẩn vận hành: thiếu tải 18,0 % (679.837 kWh/năm) do nghẽn Converter 100 kW và '
    'dư điện tới 58,4 % (4.426.778 kWh/năm) do tuabin gió 2.000 kW vượt gấp đôi nhu cầu phụ tải 3,77 GWh/năm (Bảng 3.18);',
    'Kết quả mô phỏng tối ưu trực tiếp trên HOMER Pro x64 v3.18.5 (%d/%d phương án khả thi, Hình 3.13) chứng minh %d cấu hình đạt đồng thời '
    '0,00 %% thiếu tải và ≤ 10 %% điện dư; trong đó phương án dẫn đầu đạt chuẩn gồm %s kWp PV + %d × 500 kW Windflow 45 + %d khối BESS '
    '(%s kWh) + %d kW diesel dự phòng + %d kW Converter (%s) đạt %s %% thiếu tải, %s %% điện dư và tỷ lệ tái tạo %s %% (Bảng 3.20);' % (
        _cnt['feasible'], _cnt['total'], _cnt['gvhd_ok'],
        vn(_opt['pv_kw'], 0), int(_opt['wind_qty']), int(_opt['bess_qty']), vn(_opt['bess_qty'] * 100, 0),
        int(_opt['gen_kw']), int(_opt['conv_kw']), _opt['dispatch'],
        vn(_opt['unmet_pct'], 2), vn(_opt['excess_pct'], 2), vn(_opt['rf_pct'], 1)),
    'So với Base Case diesel (%s triệu USD, LCOE %s USD/kWh, Bảng 3.21), phương án tối ưu giảm %s %% NPC (còn %s triệu USD) và '
    'LCOE (còn %s USD/kWh), đạt IRR %s %%, hoàn vốn %s năm (Hình 3.14), cắt giảm %s %% nhiên liệu và tránh phát thải %s tấn CO₂/năm [1], [12].' % (
        vn(_base['npc'] / 1e6, 2), vn(_base['coe'], 4), vn(_npc_cut_pct, 1), vn(_opt['npc'] / 1e6, 2),
        vn(_opt['coe'], 4), vn(_opt['irr'], 1), vn(_opt['simple_payback'], 2), vn(_fuel_cut_pct, 1), vn(_co2_saved_base, 1)),
]:
    p = doc.add_paragraph(it, style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)

H('2. Kiến nghị và hướng phát triển', 2)
P('Từ các kết quả mô phỏng đã xác thực trên phần mềm HOMER Pro x64 v3.18.5, sinh viên kiến nghị bốn hướng hoàn thiện tiếp theo '
  'khi triển khai kỹ thuật tại thực địa Côn Đảo:')
for it in [
    'Đo kiểm thực địa chuỗi tốc độ gió tại cao trình lắp đặt 47 m và đồ thị phụ tải theo mùa của nhóm cơ sở lưu trú KT nhằm hiệu chỉnh sai số số liệu vệ tinh NASA;',
    'Thực hiện phân tích độ nhạy theo giá dầu diesel, suất đầu tư pin LFP và lãi suất chiết khấu thực r trong dải ±20 %% trên mô hình HOMER Pro;',
    'Khảo sát bố trí phụ tải điều độ linh hoạt (trạm khử mặn nước biển, trạm sạc xe điện) để tận dụng nốt phần điện dư %s %% (%s MWh/năm) [1];' % (vn(_opt['excess_pct'], 2), vn(_opt['excess_kwh'] / 1000.0, 1)),
    'Đánh giá chi tiết phương án chống ăn mòn muối biển và thiết kế bảo vệ rơle – tự động hóa chuyển nguồn giữa cụm BESS, PV, tuabin gió và máy phát dự phòng.',
]:
    p = doc.add_paragraph(it, style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)

# ===================== TAI LIEU =====================
H('TÀI LIỆU THAM KHẢO', 1)
refs = [
    '[1] HOMER Energy LLC, HOMER Pro User Manual, Boulder, Colorado, USA. '
    'https://homerenergy.com/products/pro/docs/latest/index.html (truy cập ngày 24/11/2026).',
    '[2] T. Lambert, P. Gilman, P. Lilienthal, Micropower System Modeling with HOMER, '
    'Chapter 15 in Integration of Alternative Sources of Energy, Wiley, 2006.',
    '[3] NASA Langley Research Center, Prediction of Worldwide Energy Resources (POWER), '
    'https://power.larc.nasa.gov (truy cập ngày 24/11/2026).',
    '[4] World Bank Group & Solargis, Global Solar Atlas 2.0 Technical Report, 2019.',
    '[5] DTU Wind and Energy Systems & World Bank Group, Global Wind Atlas 4.0, '
    'https://globalwindatlas.info (truy cập ngày 24/11/2026).',
    '[6] G. M. Masters, Renewable and Efficient Electric Power Systems, 2nd ed., '
    'John Wiley & Sons, 2013.',
    '[7] J. F. Manwell, J. G. McGowan, A. L. Rogers, Wind Energy Explained: Theory, Design '
    'and Application, 2nd ed., John Wiley & Sons, 2009.',
    '[8] International Electrotechnical Commission, IEC 61400-1:2019 – Wind energy generation '
    'systems – Part 1: Design requirements, 2019.',
    '[9] Nguyễn Hữu Hiếu, Phạm Văn Quang, Bùi Văn Ga, Tối ưu hóa mô-đun sản xuất điện tái tạo '
    'hòa lưới kết hợp mặt trời – gió – sinh khối ở đảo Cù Lao Chàm, Tạp chí Khoa học và Công nghệ '
    '– Đại học Đà Nẵng, Vol. 22, No. 11A, 2024, tr. 25–31.',
    '[10] Thủ tướng Chính phủ, Quyết định số 500/QĐ-TTg ngày 15/5/2023 phê duyệt Quy hoạch phát '
    'triển điện lực quốc gia thời kỳ 2021–2030, tầm nhìn đến năm 2050.',
    '[11] Tập đoàn Điện lực Việt Nam, Biểu giá bán lẻ điện hiện hành, '
    'https://www.evn.com.vn (truy cập ngày 24/11/2026).',
    '[12] Intergovernmental Panel on Climate Change (IPCC), 2006 IPCC Guidelines for National '
    'Greenhouse Gas Inventories, Volume 2: Energy, Chapter 1–2, 2006.',
]
for r_ in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    add_runs(p, r_, size=13)

add_page_number()
_OUT_DOCX = os.path.join(_PROJ_ROOT, 'HO_SO_NOP_BAO_CAO_CHINH_THUC', '01_Bao_Cao_Thuyet_Minh_ST_Giai_Doan_3.docx')
json.dump([e for e in HEADINGS if e[1] != 'MỤC LỤC'], open(os.path.join(_PROJ_ROOT, 'assets', 'toc_headings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(FIG_CAPTIONS, open(os.path.join(_PROJ_ROOT, 'assets', 'fig_headings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(TBL_CAPTIONS, open(os.path.join(_PROJ_ROOT, 'assets', 'tbl_headings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for _sec in doc.sections:
    _sec.page_width = Cm(21.0)
    _sec.page_height = Cm(29.7)
    _sec.top_margin = Cm(2.5)
    _sec.bottom_margin = Cm(2.5)
    _sec.left_margin = Cm(3.0)
    _sec.right_margin = Cm(2.0)
doc.save(_OUT_DOCX)
print('SAVED', _OUT_DOCX)
print('r=%s CRF=%s NPC=%s COE=%s payback=%s capex=%s' % (
    vn(r_real*100,2), vn(CRF,4), vn(NPC,0), vn(COE,0), vn(payback,2), vn(C_capex,0)))
