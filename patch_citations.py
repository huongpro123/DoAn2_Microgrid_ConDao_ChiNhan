# -*- coding: utf-8 -*-
"""Them trich dan [n] trong than bai va cap nhat danh muc tai lieu tham khao."""
import io

P = r'D:\chinhan\build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()

# ---------- 1. Danh muc tai lieu tham khao ----------
old_refs_start = s.index("refs = [")
old_refs_end = s.index("]", s.index("'[7] Nguyễn Hữu Hiếu")) + 1
new_refs = """refs = [
    '[1] HOMER Energy LLC, HOMER Pro User Manual, Boulder, Colorado, USA. '
    'https://homerenergy.com/products/pro/docs/latest/index.html',
    '[2] T. Lambert, P. Gilman, P. Lilienthal, Micropower System Modeling with HOMER, '
    'Chapter 15 in Integration of Alternative Sources of Energy, Wiley, 2006.',
    '[3] NASA Langley Research Center, Prediction of Worldwide Energy Resources (POWER), '
    'https://power.larc.nasa.gov',
    '[4] World Bank Group & Solargis, Global Solar Atlas 2.0 Technical Report, 2019.',
    '[5] DTU Wind and Energy Systems & World Bank Group, Global Wind Atlas 4.0, '
    'https://globalwindatlas.info',
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
    '[11] Tập đoàn Điện lực Việt Nam, Biểu giá bán lẻ điện hiện hành, https://www.evn.com.vn.',
]"""
s = s[:old_refs_start] + new_refs + s[old_refs_end:]

# ---------- 2. Trich dan trong than bai ----------
pairs = [
    # (chuoi goc, chuoi thay the) - chen [n] truoc dau cham cuoi cau
    ('quản lý bởi một bộ điều khiển trung tâm.',
     'quản lý bởi một bộ điều khiển trung tâm [1], [2].'),
    ('bốn cấu hình off-grid phổ biến nhất hiện nay là:',
     'bốn cấu hình off-grid phổ biến nhất hiện nay [1], [9] là:'),
    ('nguồn gió khá dồi dào,',
     'nguồn gió khá dồi dào [4], [5],'),
    ('và tổn thất dây dẫn.',
     'và tổn thất dây dẫn [6].'),
    ('phân bố tốc độ gió tại vị trí đặt máy',
     'phân bố tốc độ gió tại vị trí đặt máy [7], [8]'),
    ('thuộc cấp chịu gió IEC IIA',
     'thuộc cấp chịu gió IEC IIA [8]'),
    ('Dữ liệu bức xạ mặt trời được lấy theo tọa độ Côn Đảo từ nguồn NASA',
     'Dữ liệu bức xạ mặt trời được lấy theo tọa độ Côn Đảo từ nguồn NASA [3]'),
    ('Dữ liệu gió được HOMER Pro lấy từ cơ sở dữ liệu NASA theo tọa độ Côn Đảo',
     'Dữ liệu gió được HOMER Pro lấy từ cơ sở dữ liệu NASA theo tọa độ Côn Đảo [3], [5]'),
    ('Các thông số kinh tế được thiết lập thống nhất trong HOMER Pro như Bảng 3.1.',
     'Các thông số kinh tế được thiết lập thống nhất trong HOMER Pro như Bảng 3.1 [1].'),
    ('đã được mô phỏng trực tiếp trên phần mềm HOMER Pro phiên bản x64 (Pro Edition).',
     'đã được mô phỏng trực tiếp trên phần mềm HOMER Pro phiên bản x64 (Pro Edition) [1].'),
    ('hướng đi phù hợp và bền vững.',
     'hướng đi phù hợp và bền vững [10], [11].'),
]
applied = 0
for a, b in pairs:
    if a in s:
        s = s.replace(a, b, 1)
        applied += 1
    else:
        print('KHONG TIM THAY:', a[:50])

# bo sung trich dan cho muc 2.6 (kinh te) va 2.7 (HOMER)
pairs2 = [
    ("'CRF là hệ số thu hồi vốn", None),
]
io.open(P, 'w', encoding='utf-8').write(s)
print('refs + citations applied:', applied)
