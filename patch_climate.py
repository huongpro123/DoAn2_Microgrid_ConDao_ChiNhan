# -*- coding: utf-8 -*-
"""Bo sung muc 3.1 (khi tuong), 3.2 (gio theo thang), 3.3 (co cau phu tai)."""
import io

P = 'build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()

MONTHS = ['Tháng 1','Tháng 2','Tháng 3','Tháng 4','Tháng 5','Tháng 6',
          'Tháng 7','Tháng 8','Tháng 9','Tháng 10','Tháng 11','Tháng 12']
ghi = [5.02,5.96,6.37,6.65,5.59,4.99,4.83,5.05,4.90,4.80,4.66,4.40]
t2m = [25.1,25.4,26.5,28.1,28.9,28.7,28.3,28.3,28.2,27.9,27.3,26.2]
tmax= [28.1,27.7,28.9,30.0,30.8,30.7,30.3,29.6,30.1,29.7,29.0,28.4]
tmin= [22.8,23.1,23.6,25.0,25.8,26.1,25.9,26.5,25.8,25.7,25.0,23.0]
rh  = [86.1,85.1,83.6,81.1,81.2,81.9,82.3,82.6,82.0,82.5,84.8,85.3]
ws2 = [7.47,6.67,5.40,4.32,3.86,4.72,5.35,5.76,5.10,4.63,5.95,7.62]
ws50= [10.15,8.95,7.03,5.35,4.66,5.87,6.79,7.38,6.42,5.78,7.79,10.32]
ALPHA = 0.143
ws78 = [x * (78.0/50.0) ** ALPHA for x in ws50]


def v(x, d=2):
    return ('%.*f' % (d, x)).replace('.', ',')


rw = [[MONTHS[i], v(ghi[i]), v(t2m[i],1), v(tmax[i],1), v(tmin[i],1), v(rh[i],1)] for i in range(12)]
rw.append(['Trung bình năm', v(5.26), v(27.4,1), v(30.8,1), v(22.8,1), v(83.2,1)])
rn = [[MONTHS[i], v(ws2[i]), v(ws50[i]), v(ws78[i])] for i in range(12)]
rn.append(['Trung bình năm', v(5.57), v(7.20), v(7.67)])

T_WEATHER = ("TBL(\n"
             "    ['Tháng', 'Bức xạ (kWh/m²/ngày)', 'Nhiệt độ TB (°C)', 'Cao nhất (°C)', 'Thấp nhất (°C)', 'Độ ẩm (%)'],\n"
             "    " + repr(rw) + ",\n"
             "    widths=[3.0, 3.6, 3.0, 2.8, 2.8, 2.4],\n"
             "    caption='Bảng 3.1. Thông số khí tượng trung bình tháng tại Côn Đảo (NASA POWER, 2001–2025)')\n")

T_WIND = ("TBL(\n"
          "    ['Tháng', 'Gió ở 2 m (m/s)', 'Gió ở 50 m (m/s)', 'Gió ở 78 m (m/s)'],\n"
          "    " + repr(rn) + ",\n"
          "    widths=[3.2, 4.2, 4.2, 4.2],\n"
          "    caption='Bảng 3.2. Tốc độ gió trung bình tháng tại Côn Đảo (NASA POWER, 2001–2025)')\n")

T_LOAD = ("TBL(\n"
          "    ['Nhóm phụ tải', 'Công suất đặt (kW)', 'Tỷ trọng (%)', 'Đặc điểm sử dụng'],\n"
          "    [\n"
          "        ['Phụ tải hiện trạng', '118,1', '15,1', 'Khu dân cư và cơ quan hiện hữu trên đảo'],\n"
          "        ['Phụ tải CS', '40,0', '5,1', 'Hạ tầng, chiếu sáng công cộng và dịch vụ'],\n"
          "        ['Phụ tải KT', '625,0', '79,8', 'Cơ sở lưu trú, du lịch – nghỉ dưỡng'],\n"
          "        ['Tổng cộng', '783,1', '100,0', 'Công suất đặt/đỉnh của hệ thống'],\n"
          "    ],\n"
          "    widths=[4.0, 3.2, 2.8, 6.0],\n"
          "    caption='Bảng 3.3. Cơ cấu phụ tải của hệ thống ST – Giai đoạn 3')\n")

NEW_31 = (
    "P('Côn Đảo nằm ở vĩ độ thấp (khoảng 8,68° Bắc) nên có khí hậu nhiệt đới gió mùa, nhiệt độ cao và '\n"
    "  'ổn định quanh năm, độ ẩm lớn. Số liệu khí tượng trung bình nhiều năm (2001–2025) trích từ cơ sở '\n"
    "  'dữ liệu NASA POWER [3] tại tọa độ 8,68°N – 106,60°E được tổng hợp trong Bảng 3.1, gồm bức xạ tổng '\n"
    "  'trên mặt phẳng ngang, nhiệt độ không khí và độ ẩm tương đối.')\n"
    + T_WEATHER +
    "P('Về bức xạ, tổng xạ trung bình năm đạt khoảng 5,26 kWh/m²/ngày, tương đương 1.921 kWh/m²/năm; '\n"
    "  'cao nhất vào tháng 4 (6,65 kWh/m²/ngày) và thấp nhất vào tháng 12 (4,40 kWh/m²/ngày). Đây là mức '\n"
    "  'bức xạ thuận lợi cho khai thác điện mặt trời, chỉ thấp hơn khoảng 15–20 % so với khu vực Tây Nguyên '\n"
    "  'và Nam Trung Bộ. Trong tính toán giải tích của báo cáo, giá trị thiết kế được chọn thận trọng là '\n"
    "  '4,9 kWh/m²/ngày (%s kWh/m²/năm), thấp hơn khoảng 7 %% so với số liệu NASA và khoảng 15 %% so với dữ '\n"
    "  'liệu giờ mà HOMER Pro sử dụng, nhằm dự phòng suy giảm do bụi bẩn, mây mùa mưa và sai lệch giữa dữ '\n"
    "  'liệu vệ tinh với điều kiện thực tế trên đảo. Hệ số hiệu suất tổng hợp của dàn PV (PR) lấy bằng 0,80, '\n"
    "  'kể cả tổn thất nhiệt độ, bụi bẩn, sai lệch điểm làm việc và tổn thất dây dẫn [6].' % vn(GHI_year, 1))\n"
    "P('Về nhiệt độ, nhiệt độ không khí trung bình năm khoảng 27,4 °C với biên độ năm nhỏ: tháng mát nhất '\n"
    "  '(tháng 1) khoảng 25,1 °C và tháng nóng nhất (tháng 5) khoảng 28,9 °C; nhiệt độ cao nhất xấp xỉ '\n"
    "  '30,8 °C. Độ ẩm tương đối cao, trung bình 83 % và lên tới 86 % vào các tháng mùa mưa. Nhiệt độ cao '\n"
    "  'ảnh hưởng trực tiếp đến hiệu suất tấm pin: với hệ số nhiệt công suất −0,34 %/°C và nhiệt độ làm việc '\n"
    "  'của tế bào ước tính theo T_{tế bào} = T_{môi trường} + (NOCT − 20) × G/800 (NOCT ≈ 45 °C), vào buổi trưa '\n"
    "  'khi G ≈ 800 W/m² và T_{môi trường} ≈ 30 °C thì T_{tế bào} ≈ 55 °C, cao hơn 25 °C của điều kiện tiêu chuẩn '\n"
    "  'khoảng 30 °C, làm giảm công suất khoảng 10 %; phần tổn thất này đã được tính gộp trong PR = 0,80.')\n"
    "P('Mùa mưa kéo dài từ tháng 5 đến tháng 11, trùng giai đoạn bức xạ thấp hơn; mùa khô từ tháng 12 đến '\n"
    "  'tháng 4 có bức xạ cao nhất. Sự lệch pha này khiến sản lượng điện mặt trời theo tháng chênh lệch đáng '\n"
    "  'kể (tháng 4 cao hơn tháng 12 khoảng 50 %), là lý do hệ thống cần dung lượng lưu trữ đủ lớn cho các '\n"
    "  'tháng mùa mưa — nội dung phân tích tiếp ở mục 3.10 và 3.12.')\n"
)

OLD_31 = (
    "P('Dữ liệu bức xạ mặt trời được lấy theo tọa độ Côn Đảo từ nguồn NASA [3] (phù hợp với HOMER Pro), '\n"
    "  'với tổng xạ trung bình khoảng 4,9 kWh/m²/ngày, tương đương %s kWh/m²/năm. '\n"
    "  'Hệ số hiệu suất tổng hợp của dàn PV (PR) lấy bằng 0,80, kể cả tổn thất nhiệt độ, bụi bẩn, '\n"
    "  'sai lệch điểm làm việc và tổn thất dây dẫn [6].' % vn(GHI_year, 1))\n")

ANCHOR_32 = "  'này cho tốc độ gió sát với điều kiện thực tế của đảo hơn so với số liệu đo tại độ cao 10 m.')\n"

NEW_32 = ANCHOR_32 + T_WIND + (
    "P('Tốc độ gió phân hóa rõ theo mùa: mạnh nhất vào các tháng 12, 1 và 2 (10,2–10,3 m/s ở độ cao 50 m, '\n"
    "  'tương ứng khoảng 10,9–11,0 m/s ở 78 m) do ảnh hưởng của gió mùa Đông Bắc; yếu nhất vào tháng 4–5 '\n"
    "  '(5,35 m/s và 4,66 m/s ở 50 m, tức 5,70 m/s và 4,97 m/s ở 78 m). Trung bình năm đạt 7,2 m/s ở 50 m và '\n"
    "  'khoảng 7,67 m/s ở độ cao trục 78 m, xác định bằng quy luật gió mũ với hệ số mũ α = 0,143: '\n"
    "  'v_{78} = v_{50} × (78/50)^{0,143}.')\n"
    "P('Với đường cong công suất của Enercon E-82 E2 (khởi động 2–3 m/s, đạt định mức 13 m/s), tốc độ gió '\n"
    "  'trung bình tháng luôn lớn hơn tốc độ khởi động nên tuabin phát điện được cả năm; các tháng 12–2 cho '\n"
    "  'sản lượng cao nhất, tháng 4–5 thấp nhất. Chính sự bù trừ theo mùa giữa gió và bức xạ là cơ sở để chọn '\n"
    "  'cấu hình lai gió – mặt trời – pin cho hệ thống ST.')\n")

ANCHOR_33 = "  'công suất các nguồn phát và dung lượng lưu trữ.' % vn(E_load / 1e6, 2))\n"

NEW_33 = ANCHOR_33 + T_LOAD + (
    "P('Cơ cấu phụ tải cho thấy nhóm KT (cơ sở lưu trú, du lịch – nghỉ dưỡng) chiếm tới 79,8 % công suất '\n"
    "  'đặt, phụ tải hiện trạng 15,1 % và phụ tải CS 5,1 %. Đặc điểm này khiến đồ thị phụ tải có tính mùa vụ '\n"
    "  'rõ rệt theo mùa du lịch và có đỉnh buổi tối khi khách sạn, nhà hàng hoạt động mạnh — phù hợp với '\n"
    "  'dạng đồ thị phụ tải Community mà mô hình HOMER Pro sử dụng (Hình 3.2).')\n"
    "P('Do hệ số tải là giả định, báo cáo khảo sát độ nhạy của nhu cầu điện năng trong khoảng k_{tải} = '\n"
    "  '0,50–0,60: với k_{tải} = 0,50 điện năng tiêu thụ khoảng 9.397 kWh/ngày (3,43 GWh/năm); với '\n"
    "  'k_{tải} = 0,60 khoảng 11.277 kWh/ngày (4,12 GWh/năm). Giá trị chọn dùng 0,55 tương ứng 10.336,9 '\n"
    "  'kWh/ngày (3,77 GWh/năm) nằm giữa khoảng này và được dùng thống nhất cho mọi tính toán phía sau.')\n")


def apply(old, new, tag):
    global s
    assert old in s, 'MISSING: ' + tag
    s = s.replace(old, new, 1)


apply(OLD_31, NEW_31, '3.1')
apply(ANCHOR_32, NEW_32, '3.2')
apply(ANCHOR_33, NEW_33, '3.3')

io.open(P, 'w', encoding='utf-8').write(s)
print('OK: inserted 3.1 / 3.2 / 3.3 content')
