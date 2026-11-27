# -*- coding: utf-8 -*-
"""Sap xep lai bao cao thanh 3 chuong theo yeu cau cua thay (mot lan chay)."""
import io
import re

SRC = r'D:\chinhan\build_bao_cao.py'
src = io.open(SRC, encoding='utf-8').read()
lines = src.splitlines(True)


def idx(anchor):
    for i, ln in enumerate(lines):
        if anchor in ln:
            return i
    raise SystemExit('anchor not found: ' + anchor)


A = [idx('CHƯƠNG 1: TỔNG QUAN HỆ THỐNG ST'),
     idx("H('1.2. Sơ đồ nguyên lý hệ thống'"),
     idx("H('1.3. Thông số thiết bị của hệ thống'"),
     idx('CHƯƠNG 2: DỮ LIỆU ĐẦU VÀO'),
     idx("H('2.2. Bức xạ mặt trời'"),
     idx("H('2.4. Thông số kinh tế'"),
     idx('CHƯƠNG 3: MÔ HÌNH HỆ THỐNG TRÊN HOMER PRO'),
     idx('CHƯƠNG 4: CƠ SỞ TÍNH TOÁN VÀ CÔNG THỨC'),
     idx('CHƯƠNG 5: KẾT QUẢ TÍNH TOÁN VÀ MÔ PHỎNG'),
     idx('CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN'),
     idx("H('TÀI LIỆU THAM KHẢO', 1)")]

pre = ''.join(lines[:A[0]])
post = ''.join(lines[A[-1]:])
segs = [''.join(lines[A[i]:A[i + 1]]) for i in range(len(A) - 1)]
(CH1_LOC, CH1_SODO, DEV, LOAD, LOC_INPUT, ECON, HOMER, FORM, RES, CONC) = segs
for n, s in zip(['CH1_LOC', 'CH1_SODO', 'DEV', 'LOAD', 'LOC_INPUT', 'ECON',
                 'HOMER', 'FORM', 'RES', 'CONC'], segs):
    print(n, s.count('\n'), 'dong')


def strip_trailing_break(text):
    t = text.rstrip('\n')
    if t.endswith('BREAK()'):
        t = t[:t.rfind('BREAK()')].rstrip('\n')
    return t + '\n\n'


def renumber(text, pairs):
    """Thay the an toan (khong de thay lan nhau)."""
    tmp = []
    for i, (old, new) in enumerate(pairs):
        tok = '@@%d@@' % i
        tmp.append((tok, new))
        text = text.replace(old, tok)
    for tok, new in tmp:
        text = text.replace(tok, new)
    return text


# ---------- Chuong 1 ----------
CH1_LOC = CH1_LOC.replace(
    "H('CHƯƠNG 1: TỔNG QUAN HỆ THỐNG ST – GIAI ĐOẠN 3 VÀ LỰA CHỌN THIẾT BỊ', 1)",
    "H('1.3. Vị trí địa lý và hiện trạng hệ thống ST – Giai đoạn 3', 2)", 1)
CH1_SODO = CH1_SODO.replace("H('1.2. Sơ đồ nguyên lý hệ thống', 2)",
                            "H('1.4. Sơ đồ nguyên lý hệ thống', 2)", 1)

NEW_CH1 = r"""H('CHƯƠNG 1: TỔNG QUAN HỆ THỐNG OFF-GRID TRONG MICROGRID', 1)
H('1.1. Khái niệm microgrid và hệ thống off-grid', 2)
P('Microgrid là một hệ thống điện cỡ nhỏ gồm các nguồn phát phân tán, hệ thống lưu trữ năng lượng, các bộ '
  'biến đổi công suất và phụ tải, được quản lý bởi một bộ điều khiển trung tâm. Hệ thống có thể vận hành '
  'song song với lưới điện phân phối hoặc tách khỏi lưới để tự cấp điện cho một khu vực nhất định.')
P('Hệ thống off-grid (độc lập, không nối lưới) là trường hợp microgrid vận hành hoàn toàn tách khỏi lưới điện '
  'quốc gia. Khi đó hệ thống phải tự cân bằng công suất tại mọi thời điểm: nguồn phát đáp ứng đủ phụ tải, '
  'phần dư được nạp vào hệ lưu trữ, phần thiếu phải bù bằng nguồn dự phòng hoặc cắt giảm phụ tải. Vì vậy cấu '
  'hình nguồn cung cấp điện cho off-grid thường gồm nhiều nguồn kết hợp (gió, mặt trời, diesel, pin) để tăng '
  'độ tin cậy cấp điện.')
P('So với hệ nối lưới, hệ off-grid có ba đặc điểm kỹ thuật cần quan tâm: (i) không có lưới làm nguồn tham chiếu '
  'điện áp nên cần ít nhất một bộ biến tần tạo lưới (grid-forming) để giữ điện áp và tần số; (ii) tỷ lệ năng '
  'lượng tái tạo cao thường đi kèm nhu cầu lưu trữ và thời gian tự chủ lớn; (iii) công suất nguồn phải chọn '
  'theo công suất đỉnh và công suất đứt tải lớn nhất, không chỉ theo điện năng tiêu thụ.')
H('1.2. Các cấu hình off-grid thường dùng trong microgrid', 2)
P('Thực tế triển khai cho thấy bốn cấu hình off-grid phổ biến nhất hiện nay là: (i) điện mặt trời kết hợp pin '
  'lưu trữ, đấu ở phía DC (DC-coupled); (ii) điện mặt trời và điện gió kết hợp pin, đấu ở phía AC (AC-coupled) '
  '— cấu hình lai hybrid; (iii) điện mặt trời hoặc gió kết hợp máy phát diesel và pin để đảm bảo dự phòng; '
  '(iv) chỉ dùng máy phát diesel cho phụ tải nhỏ, ngắn hạn.')
P('Việc lựa chọn cấu hình phụ thuộc ba yếu tố đầu vào cơ bản: tiềm năng tự nhiên tại địa điểm (bức xạ, tốc độ '
  'gió), đặc tính phụ tải (công suất đỉnh, hệ số tải, mức độ ưu tiên cấp điện) và chi phí cho mỗi kWh điện năng '
  'sản xuất. Tại các khu vực đảo xa bờ có tiềm năng gió và mặt trời tốt, cấu hình lai gió – mặt trời – pin '
  'thường cho chi phí quy dẫn thấp nhất và tỷ lệ điện năng tái tạo cao nhất. Bảng 1.1 so sánh ưu, nhược điểm '
  'của bốn cấu hình nêu trên.')
TBL(['Cấu hình', 'Thành phần chính', 'Ưu điểm', 'Hạn chế', 'Mức độ phù hợp'],
    [['PV – pin (DC-coupled)', 'Dàn PV, biến tần PV, pin, bộ tạo lưới',
      'Đơn giản, hiệu suất cao, vốn đầu tư thấp', 'Không phát điện ban đêm, cần pin dung lượng lớn', 'Phụ tải nhỏ, ban ngày'],
     ['PV – gió – pin (hybrid AC-coupled)', 'Dàn PV, tuabin gió, pin, bộ tạo lưới',
      'Bù trừ thời tiết, độ tin cậy cao, nhiều điện năng tái tạo', 'Vốn đầu tư lớn, điều khiển phức tạp', 'Đảo, vùng biển có gió tốt'],
     ['PV/gió – diesel – pin', 'Nguồn tái tạo, máy phát diesel, pin',
      'Cấp điện 100 %, giảm tiêu hao nhiên liệu', 'Chi phí nhiên liệu và bảo dưỡng cao, có phát thải', 'Vùng thiếu nguồn, cần dự phòng'],
     ['Diesel đơn thuần', 'Máy phát diesel',
      'Cấu hình gọn, vốn đầu tư nhỏ', 'Chi phí điện năng cao, phụ thuộc nhiên liệu', 'Phụ tải nhỏ, ngắn hạn']],
    widths=[3.2, 3.8, 4.0, 3.6, 2.6],
    caption='Bảng 1.1. So sánh các cấu hình off-grid thường dùng trong microgrid')
P('Đối với hệ thống ST – Giai đoạn 3 đặt tại Côn Đảo, cấu hình được lựa chọn là phương án lai gồm dàn pin mặt '
  'trời, một tuabin gió 2.000 kW, hệ pin Li-ion 11.700 kWh và hai bộ biến tần tạo lưới 1 MW. Vị trí, hiện trạng '
  'phụ tải và sơ đồ nguyên lý của hệ thống được trình bày trong hai mục tiếp theo.')
"""

# ---------- Chuong 2 ----------
FORM = FORM.replace("H('CHƯƠNG 4: CƠ SỞ TÍNH TOÁN VÀ CÔNG THỨC', 1)",
                    "H('CHƯƠNG 2: PHƯƠNG PHÁP TÍNH TOÁN CẤU HÌNH NGUỒN CUNG CẤP ĐIỆN', 1)", 1)
for old, new in (('4.1. Tính toán phụ tải', '2.1. Tính toán phụ tải'),
                 ('4.2. Tính toán điện mặt trời', '2.2. Tính toán điện mặt trời'),
                 ('4.3. Tính toán tuabin gió', '2.3. Tính toán tuabin gió'),
                 ('4.4. Tính toán hệ thống pin lưu trữ', '2.4. Tính toán hệ thống pin lưu trữ'),
                 ('4.5. Tính toán biến tần', '2.5. Tính toán biến tần'),
                 ('4.6. Tính toán kinh tế', '2.6. Tính toán kinh tế')):
    FORM = FORM.replace("H('" + old + "', 2)", "H('" + new + "', 2)", 1)

HOMER = HOMER.replace("H('CHƯƠNG 3: MÔ HÌNH HỆ THỐNG TRÊN HOMER PRO', 1)",
                      "H('2.7. Phương pháp mô phỏng tối ưu bằng HOMER Pro', 2)", 1)
HOMER = HOMER.replace("H('3.1. Kiến trúc mô hình', 2)", "H('2.8. Kiến trúc mô hình trên HOMER Pro', 2)", 1)
HOMER = HOMER.replace("H('3.2. Thông số các thành phần', 2)", "H('2.9. Thông số các thành phần', 2)", 1)
HOMER = HOMER.replace("H('3.3. Chiến lược điều độ', 2)", "H('2.10. Chiến lược điều độ', 2)", 1)
HOMER = HOMER.replace("H('3.4. Ràng buộc hệ thống', 2)", "H('2.11. Ràng buộc hệ thống', 2)", 1)
HOMER = renumber(HOMER, [('Hình 3.1', 'Hình 2.1'), ('Hình 3.2', 'Hình 2.2'),
                         ('Hình 3.3', 'Hình 2.3'), ('Hình 3.4', 'Hình 2.4')])

# ---------- Chuong 3 ----------
LOC_INPUT = LOC_INPUT.replace("H('2.2. Bức xạ mặt trời', 2)",
                              "H('3.1. Địa điểm và điều kiện bức xạ – nhiệt độ', 2)", 1)
LOC_INPUT = LOC_INPUT.replace("H('2.3. Tốc độ gió', 2)",
                              "H('3.2. Điều kiện gió tại địa điểm', 2)", 1)
LOAD = LOAD.replace("H('2.1. Phụ tải', 2)", "H('3.3. Phụ tải của hệ thống', 2)", 1)
ECON = ECON.replace("H('2.4. Thông số kinh tế', 2)", "H('3.4. Thông số kinh tế của dự án', 2)", 1)

DEV = DEV.replace("H('1.3. Thông số thiết bị của hệ thống', 2)",
                  "H('3.5. Thông số thiết bị của hệ thống', 2)", 1)
DEV = DEV.replace("H('1.4. Lựa chọn tấm pin quang điện và biến tần PV', 2)",
                  "H('3.6. Lựa chọn tấm pin quang điện và biến tần PV', 2)", 1)
DEV = DEV.replace("H('1.5. Lựa chọn tuabin gió', 2)", "H('3.7. Lựa chọn tuabin gió', 2)", 1)
DEV = DEV.replace("H('1.6. Lựa chọn hệ thống pin lưu trữ', 2)",
                  "H('3.8. Lựa chọn hệ thống pin lưu trữ', 2)", 1)

RES = RES.replace("H('CHƯƠNG 5: KẾT QUẢ TÍNH TOÁN VÀ MÔ PHỎNG', 1)\n", "", 1)
RES = renumber(RES, [
    ("H('5.1. Kết quả tính toán phụ tải', 2)", "H('3.9. Kết quả tính toán phụ tải', 2)"),
    ("H('5.2. Kết quả tính toán điện mặt trời', 2)", "H('3.10. Kết quả tính toán điện mặt trời', 2)"),
    ("H('5.3. Kết quả tính toán tuabin gió', 2)", "H('3.11. Kết quả tính toán tuabin gió', 2)"),
    ("H('5.4. Kết quả tính toán hệ thống pin', 2)", "H('3.12. Kết quả tính toán hệ thống pin', 2)"),
    ("H('5.5. Kết quả tính toán kinh tế', 2)", "H('3.13. Kết quả tính toán kinh tế', 2)"),
    ("H('5.6. Kết quả mô phỏng HOMER Pro và đối chiếu số liệu', 2)",
     "H('3.14. Kết quả mô phỏng HOMER Pro và đối chiếu số liệu', 2)"),
    ('Bảng 5.1', 'Bảng 3.8'), ('Bảng 5.2', 'Bảng 3.9'), ('Bảng 5.3', 'Bảng 3.10'),
    ('Bảng 5.4', 'Bảng 3.11'), ('Bảng 5.5', 'Bảng 3.12'), ('Bảng 5.6', 'Bảng 3.13'),
    ('Bảng 5.7', 'Bảng 3.14'),
    ('Hình 5.1', 'Hình 3.3'), ('Hình 5.2', 'Hình 3.4'),
    ('Mục 5.5', 'Mục 3.13'),
])

DEV = renumber(DEV, [('Bảng 1.1', 'Bảng 3.2'), ('Bảng 1.2', 'Bảng 3.3'),
                     ('Bảng 1.3', 'Bảng 3.4'), ('Bảng 1.4', 'Bảng 3.5'),
                     ('Bảng 1.5', 'Bảng 3.6'), ('Bảng 1.6', 'Bảng 3.7')])
ECON = renumber(ECON, [('Bảng 2.1', 'Bảng 3.1')])
LOAD = renumber(LOAD, [('Hình 2.1', 'Hình 3.2')])
LOC_INPUT = renumber(LOC_INPUT, [('Hình 2.2', 'Hình 3.1'),
                                 ('mục 1.5', 'mục 3.7'),
                                 ('Bảng 1.4', 'Bảng 3.5')])

# ---------- Ket luan ----------
CONC = CONC.replace("H('CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN', 1)",
                    "H('KẾT LUẬN VÀ KIẾN NGHỊ', 1)", 1)
CONC = CONC.replace("H('6.1. Kết luận', 2)", "H('1. Kết luận', 2)", 1)
CONC = CONC.replace("H('6.2. Hướng phát triển', 2)", "H('2. Kiến nghị và hướng phát triển', 2)", 1)

post = post.replace('Chương 5', 'Chương 3')
pre = pre.replace('Chương 5', 'Chương 3')

# ---------- Ghep lai ----------
BREAK = "BREAK()\n\n"
new = (pre
       + NEW_CH1 + '\n'
       + CH1_LOC + CH1_SODO
       + strip_trailing_break(FORM) + HOMER
       + '\n' + LOC_INPUT + LOAD + ECON
       + strip_trailing_break(DEV)
       + RES + CONC + post)

io.open(SRC, 'w', encoding='utf-8').write(new)
print('restructured ->', len(new), 'chars')
for name, txt in [('Ch1', NEW_CH1), ('Ch2', FORM + HOMER), ('Ch3', LOC_INPUT + LOAD + ECON + DEV + RES)]:
    hs = re.findall(r"H\('([^']+)', 2\)", txt)
    print(name, 'H2:', hs)
