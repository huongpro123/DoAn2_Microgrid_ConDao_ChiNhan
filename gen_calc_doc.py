# -*- coding: utf-8 -*-
"""Sinh tài liệu Word: Tính toán hệ thống microgrid ST - Giai đoạn 3 (Côn Đảo)."""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ---------------------------- 1. SỐ LIỆU SƠ ĐỒ ----------------------------
Wp = 650.0
n_A, n_B, n_C = 109, 109, 110
P_pv = Wp * (n_A + n_B + n_C) / 1000.0        # 213.2 kWp
P_pvinv = 3 * 100.0                            # 300 kW
P_wind = 2000.0                                # kW
E_batt = 5800.0 + 5900.0                       # kWh
P_gfi = 2 * 1000.0                             # kW
L_ht, L_CS, L_KT = 118.1, 40.0, 625.0
P_peak = L_ht + L_CS + L_KT                    # 783.1 kW

# ---------------------------- 2. GIẢ ĐỊNH ----------------------------
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

# ---------------------------- 3. TÍNH TOÁN ----------------------------
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

# ---------------------------- 4. FORMAT ----------------------------
def vn(x, dec=2):
    s = f"{x:,.{dec}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

# ---------------------------- 5. WORD HELPERS ----------------------------
doc = Document()

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(13)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.3

for nm, sz in (('Heading 1', 15), ('Heading 2', 13)):
    st = doc.styles[nm]
    st.font.name = 'Times New Roman'
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)

TOKEN_RE = re.compile(r'(_\{[^}]*\}|\^\{[^}]*\})')

def add_runs(p, text, size=13, italic=False, bold=False, mono=False):
    """Thêm run, parse _{...} thành subscript, ^{...} thành superscript."""
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        msub = re.match(r'_\{([^}]*)\}$', tok)
        msup = re.match(r'\^\{([^}]*)\}$', tok)
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.italic = italic
        run.bold = bold
        if msub:
            run.text = msub.group(1)
            run.font.subscript = True
        elif msup:
            run.text = msup.group(1)
            run.font.superscript = True
        else:
            run.text = tok

def H(text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

def P(text, bold=False, italic=False, align=None, size=13):
    p = doc.add_paragraph()
    add_runs(p, text, size=size, italic=italic, bold=bold)
    if align is not None:
        p.alignment = align
    return p

def FORMULA(text, size=13):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    add_runs(p, text, size=size, italic=True)
    return p

def CAP(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs(p, text, size=12, italic=True)
    return p

def TBL(headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    # lap lai dong tieu de khi bang bi cat sang trang
    trPr = table.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
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
    # khong cho tach dong; giu bang lien mach
    last = len(table.rows) - 1
    for ri, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if ri < last:
            for cell in row.cells:
                for para in cell.paragraphs:
                    para.paragraph_format.keep_with_next = True
    doc.add_paragraph()
    return table

# ---------------------------- TIÊU ĐỀ ----------------------------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('TÍNH TOÁN HỆ THỐNG MICROGRID ĐẢO ST – GIAI ĐOẠN 3')
r.font.name = 'Times New Roman'; r.font.size = Pt(18); r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('(Khu vực biển Đông, gần Côn Đảo – mô phỏng bằng HOMER Pro)')
r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.italic = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Tài liệu công thức và tính toán số liệu kỹ thuật – kinh tế')
r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True
doc.add_paragraph()

P('Tài liệu trình bày hệ thống công thức và kết quả tính toán cho sơ đồ nguyên lý '
  'microgrid đảo “ST – Giai đoạn 3” được mô phỏng trên phần mềm HOMER Pro. Các thông số '
  'công suất được lấy trực tiếp từ sơ đồ; các thông số tài nguyên, hệ số tải, lãi suất và '
  'đơn giá được nêu rõ trong mục giả định để có thể thay bằng số liệu thực tế/HOMER khi nộp bài.')

# ---------------------------- 1 ----------------------------
H('1. Thông số đầu vào và sơ đồ hệ thống', 1)
H('1.1. Sơ đồ nguyên lý', 2)
P('Sơ đồ nguyên lý hệ microgrid đảo ST – Giai đoạn 3 (thanh cái hạ thế 0,4 kV) như hình dưới đây:')
try:
    doc.add_picture('st_diagram.png', width=Cm(13.0))
    CAP('Hình 1. Sơ đồ nguyên lý hệ thống microgrid ST – Giai đoạn 3')
except Exception as e:
    P('(Không chèn được hình: %s)' % e)

H('1.2. Bảng tổng hợp thông số thiết bị (theo sơ đồ)', 2)
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
    widths=[2.2, 4.3, 5.2, 2.2, 2.8])

H('1.3. Thông số kinh tế khai báo trong HOMER Pro', 2)
P('Theo màn hình HOMER Pro của nhóm, các thông số tài chính và thời gian dự án được đặt như sau:')
TBL(
    ['Thông số trong HOMER Pro', 'Giá trị', 'Ghi chú'],
    [
        ['Discount rate (danh nghĩa)', '8,00 %/năm', 'Lãi suất chiết khấu danh nghĩa'],
        ['Inflation rate', '2,00 %/năm', 'Tỷ lệ lạm phát'],
        ['Lãi suất chiết khấu thực r', '%s %%/năm' % vn(r_real * 100, 2), 'r = (1 + 0,08)/(1 + 0,02) − 1'],
        ['Annual capacity shortage', '0,00 %', 'Không cho phép thiếu hụt'],
        ['Project lifetime', '25 năm', 'Thời gian dự án'],
        ['Location (tọa độ)', '8,683°N – 106,617°E', 'Côn Đảo — cần chọn lại trong ô Location Search'],
    ],
    widths=[6.0, 4.5, 5.5])
P('Lưu ý: màn hình HOMER hiện để tọa độ 0°N 0°W (ngoài khơi châu Phi). Cần gõ “Con Dao” hoặc nhập '
  '8,683°N / 106,617°E vào ô Location Search để tải đúng dữ liệu bức xạ và gió của Côn Đảo trước khi tính.',
  italic=True)

# ---------------------------- 2 ----------------------------
H('2. Tính toán phụ tải', 1)
H('2.1. Tổng công suất phụ tải đỉnh', 2)
P('Tổng công suất đặt/đỉnh bằng tổng công suất của ba nhóm phụ tải:')
FORMULA('P_{đỉnh} = P_{hiện trạng} + P_{CS} + P_{KT}')
FORMULA('P_{đỉnh} = 118,1 + 40,0 + 625,0 = 783,1 kW')

H('2.2. Phụ tải trung bình và điện năng tiêu thụ', 2)
P('Hệ số tải (load factor) k_{tải} = 0,55 (giả định cho phụ tải đảo có tính mùa vụ):')
FORMULA('P_{tb} = k_{tải} × P_{đỉnh} = 0,55 × 783,1 = %s kW' % vn(P_avg, 1))
FORMULA('E_{ngày} = P_{tb} × 24 = %s × 24 = %s kWh/ngày' % (vn(P_avg, 1), vn(E_day, 1)))
FORMULA('E_{năm} = E_{ngày} × 365 = %s × 365 = %s kWh/năm' % (vn(E_day, 1), vn(E_load, 0)))
P('Như vậy, nhu cầu điện năng của khu vực khoảng %s GWh/năm.' % vn(E_load / 1e6, 2))

# ---------------------------- 3 ----------------------------
H('3. Tính toán hệ thống điện mặt trời (PV)', 1)
H('3.1. Công suất đỉnh lắp đặt', 2)
FORMULA('P_{PV} = N × W_{p}')
FORMULA('P_{PV} = (109 + 109 + 110) × 650 Wp = 213.200 Wp = 213,2 kWp')
P('Trong đó: N = tổng số tấm pin (328 tấm), W_{p} = công suất đỉnh một tấm (650 Wp).')

H('3.2. Sản lượng điện năm', 2)
P('Sản lượng điện của dàn PV được tính theo công thức:')
FORMULA('E_{PV} = P_{PV} × (H / 1 kW/m²) × PR')
P('Trong đó: H là tổng bức xạ năm trên mặt phẳng nghiêng (kWh/m²/năm); PR là hệ số hiệu '
  'suất tổng hợp (performance ratio), kể cả tổn thất nhiệt độ, bụi bẩn, sai lệch điểm làm '
  'việc và tổn thất dây dẫn.')
P('Với bức xạ trung bình 4,9 kWh/m²/ngày (H = %s kWh/m²/năm) và PR = 0,80:' % vn(GHI_year, 1))
FORMULA('E_{PV} = 213,2 × %s × 0,80 = %s kWh/năm' % (vn(GHI_year, 1), vn(E_pv, 0)))
P('Sản lượng trung bình ngày: E_{PV ngày} = %s / 365 = %s kWh/ngày.' % (vn(E_pv, 0), vn(E_pv_day, 1)))

H('3.3. Tỷ số công suất DC/AC của biến tần PV', 2)
FORMULA('k_{DC/AC} = P_{PV} / P_{biến tần PV}')
FORMULA('k_{DC/AC} = 213,2 / 300 = %s' % vn(k_dcac, 3))
P('Hệ số %s cho thấy công suất biến tần đang lớn hơn công suất dàn pin (khoảng 1,41 lần), '
  'phù hợp khi cần dự phòng công suất hoặc dự kiến mở rộng dàn PV sau này.' % vn(k_dcac, 3))

H('3.4. Bảng kết quả PV', 2)
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất đỉnh lắp đặt', 'P_{PV}', '213,2 kWp'],
        ['Tổng công suất biến tần PV', 'P_{inv}', '300 kW'],
        ['Tỷ số DC/AC', 'k_{DC/AC}', vn(k_dcac, 3)],
        ['Bức xạ năm (giả định)', 'H', '%s kWh/m²/năm' % vn(GHI_year, 1)],
        ['Hiệu suất tổng hợp', 'PR', '0,80'],
        ['Sản lượng điện năm', 'E_{PV}', '%s kWh/năm' % vn(E_pv, 0)],
        ['Sản lượng trung bình ngày', 'E_{PV ngày}', '%s kWh/ngày' % vn(E_pv_day, 1)],
    ],
    widths=[7.0, 3.5, 5.5])

# ---------------------------- 4 ----------------------------
H('4. Tính toán tuabin gió', 1)
H('4.1. Sản lượng điện năm', 2)
FORMULA('E_{gió} = P_{định mức} × CF × 8.760')
P('Trong đó CF là hệ số công suất của tuabin (giả định 0,38 cho điều kiện gió ngoài khơi gần '
  'Côn Đảo). Với tuabin 2.000 kW:')
FORMULA('E_{gió} = 2.000 × 0,38 × 8.760 = %s kWh/năm' % vn(E_wind, 0))
P('Số giờ làm việc hiệu dụng ở công suất định mức:')
FORMULA('h_{gió} = CF × 8.760 = 0,38 × 8.760 = %s giờ/năm' % vn(h_wind, 0))

H('4.2. Tỷ lệ thâm nhập của nguồn gió', 2)
FORMULA('Tỷ lệ thâm nhập = E_{gió} / E_{năm} = %s / %s = %s%%' % (vn(E_wind, 0), vn(E_load, 0), vn(share_wind * 100, 1)))
P('Tỷ lệ thâm nhập lớn hơn 100% cho thấy sản lượng gió đã vượt nhu cầu phụ tải; phần dư sẽ '
  'được nạp vào pin hoặc phải cắt giảm (curtailment) do hệ thống vận hành độc lập, không có '
  'lưới để bán.')

H('4.3. Bảng kết quả tuabin gió', 2)
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất định mức', 'P_{đm}', '2.000 kW'],
        ['Hệ số công suất (giả định)', 'CF', '0,38'],
        ['Sản lượng điện năm', 'E_{gió}', '%s kWh/năm' % vn(E_wind, 0)],
        ['Số giờ làm việc hiệu dụng', 'h_{gió}', '%s giờ/năm' % vn(h_wind, 0)],
        ['Tỷ lệ thâm nhập so với phụ tải', '—', '%s %%' % vn(share_wind * 100, 1)],
    ],
    widths=[7.0, 3.5, 5.5])

# ---------------------------- 5 ----------------------------
H('5. Tính toán hệ thống pin lưu trữ', 1)
H('5.1. Dung lượng khả dụng', 2)
FORMULA('E_{khả dụng} = E_{pin} × DoD')
FORMULA('E_{khả dụng} = (5.800 + 5.900) × 0,90 = 11.700 × 0,90 = %s kWh' % vn(E_batt_usable, 0))

H('5.2. Thời gian tự chủ của pin', 2)
FORMULA('t_{tự chủ} = E_{khả dụng} / P_{phụ tải}')
P('Tại phụ tải trung bình (P_{tb} = %s kW):' % vn(P_avg, 1))
FORMULA('t_{tự chủ} = %s / %s = %s giờ' % (vn(E_batt_usable, 0), vn(P_avg, 1), vn(t_aut_avg, 1)))
P('Tại phụ tải đỉnh (P_{đỉnh} = %s kW):' % vn(P_peak, 1))
FORMULA('t_{tự chủ, đỉnh} = %s / %s = %s giờ' % (vn(E_batt_usable, 0), vn(P_peak, 1), vn(t_aut_peak, 1)))

H('5.3. Tốc độ sạc/xả (C-rate)', 2)
FORMULA('C_{rate} = P_{biến tần} / E_{pin} = 2.000 / 11.700 = %s h⁻¹' % vn(c_rate, 3))
P('Tức xả hết pin ở công suất định mức của bộ biến tần tạo lưới mất khoảng %s giờ. C-rate nhỏ '
  '(≈ 0,17C) cho thấy pin vận hành nhẹ, ít suy giảm tuổi thọ.' % vn(t_discharge_rated, 2))

H('5.4. Bảng kết quả pin', 2)
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
    widths=[7.0, 3.5, 5.5])

# ---------------------------- 6 ----------------------------
H('6. Tính toán biến tần và biến tần tạo lưới', 1)
H('6.1. Biến tần PV', 2)
P('Biến tần PV phải đủ công suất để chuyển toàn bộ công suất DC của dàn pin lên thanh cái AC, '
  'có xét đến hiệu suất và hệ số dự phòng:')
FORMULA('P_{biến tần PV} ≥ P_{PV} / k_{dự phòng}')
P('Với 3 bộ biến tần 100 kW (tổng 300 kW) và P_{PV} = 213,2 kWp, hệ số dự phòng thực tế là '
  '300/213,2 ≈ 1,41 lần — đáp ứng tốt và sẵn sàng cho mở rộng.')

H('6.2. Biến tần tạo lưới (grid-forming inverter)', 2)
P('Bộ biến tần tạo lưới vừa phải cấp đủ công suất cho phụ tải đỉnh, vừa phải đủ dư để nạp pin '
  'khi có nguồn tái tạo dư. Công suất tối thiểu theo phụ tải:')
FORMULA('P_{GFL, min} ≥ P_{đỉnh} / η_{biến tần}')
FORMULA('P_{GFL, min} ≥ 783,1 / 0,95 = %s kW' % vn(P_gfi_req, 1))
P('Thực tế sơ đồ bố trí 2 bộ biến tần tạo lưới 1 MW (tổng 2.000 kW), tức dự phòng khoảng %s lần '
  'so với công suất tối thiểu, đồng thời cho phép nạp pin ở công suất lớn và duy trì cấp điện '
  'khi một bộ gặp sự cố.' % vn(ratio_gfi, 2))

H('6.3. Bảng kết quả biến tần', 2)
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Công suất biến tần PV', 'P_{inv PV}', '300 kW (3 × 100 kW)'],
        ['Công suất tạo lưới tối thiểu', 'P_{GFL,min}', '%s kW' % vn(P_gfi_req, 1)],
        ['Công suất tạo lưới lắp đặt', 'P_{GFL}', '2.000 kW (2 × 1 MW)'],
        ['Hệ số dự phòng tạo lưới', '—', '%s lần' % vn(ratio_gfi, 2)],
    ],
    widths=[7.0, 3.5, 5.5])

# ---------------------------- 7 ----------------------------
H('7. Tính toán kinh tế', 1)
H('7.1. Lãi suất chiết khấu thực (r)', 2)
P('HOMER Pro sử dụng lãi suất chiết khấu thực. Từ lãi suất danh nghĩa i và tỷ lệ lạm phát f, '
  'lãi suất thực r được xác định theo công thức Fisher:')
FORMULA('r = (1 + i) / (1 + f) − 1')
P('Với i = 8%/năm và f = 2%/năm:')
FORMULA('r = (1 + 0,08) / (1 + 0,02) − 1 = %s%%' % vn(r_real * 100, 2))

H('7.2. Hệ số thu hồi vốn (CRF)', 2)
FORMULA('CRF(r, N) = r(1 + r)^{N} / [(1 + r)^{N} − 1]')
P('Với r = %s%%/năm và thời gian dự án N = %d năm:' % (vn(r_real * 100, 2), N_years))
FORMULA('CRF = %s' % vn(CRF, 4))

H('7.3. Chi phí vòng đời quy về hiện tại (NPC)', 2)
FORMULA('NPC = C_{0} + Σ (OM_{t} + Rep_{t} − S_{t}) / (1 + r)^{t}')
P('Trong đó: C_{0} là vốn đầu tư ban đầu; OM_{t} là chi phí vận hành bảo dưỡng năm t; '
  'Rep_{t} là chi phí thay thế thiết bị năm t; S_{t} là giá trị thu hồi cuối đời; r là lãi suất '
  'chiết khấu thực; N là thời gian dự án.')

H('7.4. Chi phí điện quy dẫn (COE)', 2)
FORMULA('COE = (NPC × CRF) / E_{năm}')
P('Trong đó (NPC × CRF) là chi phí thường niên tương đương, E_{năm} là điện năng phục vụ phụ tải '
  'trong năm.')

H('7.5. Thời gian hoàn vốn', 2)
FORMULA('T_{hoàn vốn} = C_{0} / (L_{tiết kiệm/năm} − OM_{năm})')
P('Trong đó L_{tiết kiệm} là lợi ích ròng hằng năm (tiền tiết kiệm do không phải mua điện diesel '
  'hoặc tiền bán điện), đã trừ chi phí vận hành bảo dưỡng.')

H('7.6. Bảng vốn đầu tư ban đầu', 2)
TBL(
    ['Hạng mục', 'Đơn giá (triệu VNĐ)', 'Khối lượng', 'Thành tiền (triệu VNĐ)'],
    [
        ['Tấm pin PV', '62,5 /kWp', '213,2 kWp', vn(C_pv, 0)],
        ['Biến tần PV', '7,5 /kW', '300 kW', vn(C_pvinv, 0)],
        ['Tuabin gió', '50 /kW', '2.000 kW', vn(C_wind, 0)],
        ['Pin lưu trữ', '6 /kWh', '11.700 kWh', vn(C_batt, 0)],
        ['Biến tần tạo lưới', '10 /kW', '2.000 kW', vn(C_gfi, 0)],
        ['Tủ phân phối + MCCB', '—', '1 bộ', vn(p_board, 0)],
        ['Tổng vốn đầu tư C_{0}', '', '', vn(C_capex, 0)],
    ],
    widths=[6.0, 4.0, 3.0, 4.0])

H('7.7. Bảng kết quả kinh tế', 2)
TBL(
    ['Chỉ tiêu', 'Ký hiệu', 'Giá trị'],
    [
        ['Lãi suất chiết khấu thực', 'r', '%s %%' % vn(r_real * 100, 2)],
        ['Thời gian dự án', 'N', '%d năm' % N_years],
        ['Hệ số thu hồi vốn', 'CRF', vn(CRF, 4)],
        ['Vốn đầu tư ban đầu', 'C_{0}', '%s triệu VNĐ' % vn(C_capex, 0)],
        ['Chi phí vận hành bảo dưỡng năm', 'OM', '%s triệu VNĐ/năm' % vn(OM_year, 1)],
        ['Chi phí vòng đời (NPC)', 'NPC', '%s triệu VNĐ' % vn(NPC, 0)],
        ['Chi phí thường niên tương đương', 'C_{ann}', '%s triệu VNĐ/năm' % vn(C_ann, 0)],
        ['Chi phí điện quy dẫn', 'COE', '%s VNĐ/kWh' % vn(COE, 0)],
        ['Thời gian hoàn vốn đơn giản', 'T_{hv}', '%s năm' % vn(payback, 2)],
    ],
    widths=[7.0, 3.5, 5.5])

# ---------------------------- 8 ----------------------------
H('8. Bảng tổng hợp kết quả', 1)
TBL(
    ['STT', 'Chỉ tiêu', 'Giá trị'],
    [
        ['1', 'Tổng công suất phụ tải đỉnh', '%s kW' % vn(P_peak, 1)],
        ['2', 'Điện năng tiêu thụ năm', '%s kWh/năm' % vn(E_load, 0)],
        ['3', 'Công suất PV lắp đặt', '213,2 kWp'],
        ['4', 'Sản lượng PV năm', '%s kWh/năm' % vn(E_pv, 0)],
        ['5', 'Công suất tuabin gió', '2.000 kW'],
        ['6', 'Sản lượng gió năm', '%s kWh/năm' % vn(E_wind, 0)],
        ['7', 'Tổng sản lượng nguồn tái tạo', '%s kWh/năm' % vn(E_re, 0)],
        ['8', 'Tỷ lệ nguồn tái tạo so với phụ tải', '%s %%' % vn(share_re * 100, 1)],
        ['9', 'Dung lượng pin', '11.700 kWh'],
        ['10', 'Thời gian tự chủ tại tải trung bình', '%s giờ' % vn(t_aut_avg, 1)],
        ['11', 'Vốn đầu tư ban đầu', '%s triệu VNĐ (%s tỷ)' % (vn(C_capex, 0), vn(C_capex / 1000, 2))],
        ['12', 'NPC', '%s triệu VNĐ' % vn(NPC, 0)],
        ['13', 'COE', '%s VNĐ/kWh' % vn(COE, 0)],
        ['14', 'Thời gian hoàn vốn', '%s năm' % vn(payback, 2)],
    ],
    widths=[1.2, 9.0, 5.5])

# ---------------------------- 9 ----------------------------
H('9. Giả định và ghi chú khi áp dụng', 1)
P('Các kết quả trên được tính theo chuỗi công thức chuẩn, có thể dùng để đối chiếu với kết quả '
  'HOMER Pro. Khi nộp bài cần thay các giả định sau bằng số liệu thực tế của nhóm/HOMER:')
items = [
    'Bức xạ mặt trời: 4,9 kWh/m²/ngày (GHI) — lấy theo dữ liệu NASA/HOMER cho tọa độ Côn Đảo;',
    'Hệ số hiệu suất PV PR = 0,80;',
    'Hệ số công suất tuabin gió CF = 0,38 (gió ngoài khơi);',
    'Hệ số tải phụ tải k_{tải} = 0,55;',
    'Độ sâu xả pin DoD = 0,90; hiệu suất biến tần 95%;',
    'Lãi suất danh nghĩa 8%/năm, lạm phát 2%/năm → lãi suất thực r = ' + vn(r_real * 100, 2) + '%/năm;',
    'Đơn giá: PV 62,5 triệu/kWp; gió 50 triệu/kW; biến tần 7,5 triệu/kW (theo bảng giá báo cáo); '
    'pin 6 triệu/kWh và biến tần tạo lưới 10 triệu/kW (giá tham khảo);',
    'Giá điện diesel thay thế 12.000 VNĐ/kWh để tính thời gian hoàn vốn;',
    'Thời gian dự án 25 năm.',
]
for it in items:
    p = doc.add_paragraph(style='List Bullet')
    add_runs(p, it, size=13)

P('Lưu ý: sản lượng gió và PV cộng lại lớn hơn nhu cầu phụ tải (tỷ lệ thâm nhập > 100%), nên '
  'trong vận hành độc lập sẽ có phần điện dư bị cắt giảm hoặc dùng để nạp pin. Khi mô phỏng HOMER '
  'Pro, phần dư này thể hiện ở chỉ tiêu “excess electricity” và ảnh hưởng trực tiếp tới COE, NPC.',
  italic=True)

doc.save('Tinh_toan_ST_Giai_doan_3.docx')
print('SAVED')
print('P_avg=%s E_load=%s E_pv=%s E_wind=%s r=%s CRF=%s NPC=%s COE=%s payback=%s' % (
    round(P_avg, 1), round(E_load, 1), round(E_pv, 1), round(E_wind, 1),
    round(r_real, 5), round(CRF, 5), round(NPC, 1), round(COE, 1), round(payback, 2)))
