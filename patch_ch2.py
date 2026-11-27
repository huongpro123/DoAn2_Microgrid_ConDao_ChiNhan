# -*- coding: utf-8 -*-
"""Bo sung luan giai + chu thich dai luong cho chuong 2; chen ngat trang; bo doan dau chuong 3."""
import io

P = r'D:\chinhan\build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()

NEW22 = r"""H('2.1. Tính toán phụ tải', 2)
P('Phụ tải là số liệu gốc của toàn bộ bài toán: công suất đỉnh quyết định công suất nguồn và biến tần, '
  'còn điện năng tiêu thụ quyết định sản lượng nguồn phát và dung lượng lưu trữ. Công suất đỉnh lấy bằng '
  'tổng công suất đặt của các nhóm phụ tải; điện năng ngày được suy ra từ công suất trung bình thông qua '
  'hệ số tải, đặc trưng cho mức độ sử dụng điện không đồng đều trong ngày của phụ tải đảo.')
FORMULA('P_{đỉnh} = Σ P_{i}')
FORMULA('P_{tb} = k_{tải} × P_{đỉnh}')
FORMULA('E_{ngày} = P_{tb} × 24')
FORMULA('E_{năm} = E_{ngày} × 365')
P('Trong đó: P_{đỉnh} là tổng công suất đặt của các nhóm phụ tải (kW); P_{i} là công suất đặt của nhóm '
  'phụ tải thứ i (kW); k_{tải} là hệ số tải, bằng tỷ số giữa công suất trung bình và công suất đỉnh, '
  'thường lấy 0,5–0,6 đối với phụ tải sinh hoạt và dịch vụ trên đảo; P_{tb} là công suất trung bình (kW); '
  'E_{ngày} và E_{năm} là điện năng tiêu thụ trong ngày và trong năm (kWh). Hệ số 24 và 365 tương ứng '
  'số giờ trong ngày và số ngày trong năm.')
H('2.2. Tính toán điện mặt trời', 2)
P('Công suất đỉnh của dàn pin bằng tổng công suất đỉnh của các tấm pin thành phần. Sản lượng điện năm '
  'được tính theo bức xạ tổng trên mặt phẳng nghiêng của dàn pin; để kể đến tổn thất thực tế (nhiệt độ '
  'làm việc cao, bụi bẩn, lệch điểm công suất cực đại, tổn thất dây dẫn và bộ biến đổi), người ta đưa vào '
  'hệ số hiệu suất tổng hợp PR thay vì dùng trực tiếp hiệu suất danh định của tấm pin.')
FORMULA('P_{PV} = N × W_{p}')
FORMULA('E_{PV} = P_{PV} × (H / 1 kW/m²) × PR')
FORMULA('k_{DC/AC} = P_{PV} / P_{biến tần PV}')
P('Trong đó: N là tổng số tấm pin của dàn (tấm); W_{p} là công suất đỉnh của một tấm pin (kWp); '
  'P_{PV} là công suất đỉnh lắp đặt của dàn (kWp); H là tổng bức xạ mặt trời năm trên mặt phẳng nghiêng '
  '(kWh/m²/năm), lấy theo cơ sở dữ liệu NASA cho toạ độ khảo sát; PR là hệ số hiệu suất tổng hợp của dàn '
  '(không thứ nguyên), thường 0,75–0,85; E_{PV} là sản lượng điện năm của dàn (kWh/năm); '
  'k_{DC/AC} là tỷ số công suất một chiều trên công suất xoay chiều của dàn, dùng để kiểm tra mức dự phòng '
  'của biến tần PV; P_{biến tần PV} là tổng công suất biến tần PV (kW).')
H('2.3. Tính toán tuabin gió', 2)
P('Sản lượng điện của tuabin gió phụ thuộc phân bố tốc độ gió tại vị trí đặt máy và đường cong công suất '
  'của tuabin. Vì tốc độ gió biến đổi liên tục, người ta đặc trưng mức độ khai thác bằng hệ số công suất CF '
  '— tỷ số giữa sản lượng thực tế và sản lượng lý thuyết khi tuabin chạy liên tục ở công suất định mức.')
FORMULA('E_{gió} = P_{định mức} × CF × 8.760')
FORMULA('h_{gió} = CF × 8.760')
P('Trong đó: P_{định mức} là công suất định mức của tuabin (kW); CF là hệ số công suất của tuabin (không '
  'thứ nguyên), phụ thuộc đường cong công suất và phân bố tốc độ gió, với vùng biển gần Côn Đảo thường '
  '0,35–0,45; 8.760 là số giờ trong năm; E_{gió} là sản lượng điện năm (kWh/năm); h_{gió} là số giờ làm '
  'việc hiệu dụng quy đổi về công suất định mức (giờ/năm).')
H('2.4. Tính toán hệ thống pin lưu trữ', 2)
P('Pin lưu trữ làm nhiệm vụ cân bằng công suất giữa nguồn phát và phụ tải. Dung lượng khả dụng không phải '
  'toàn bộ dung lượng danh định mà chỉ là phần cho phép xả, phụ thuộc độ sâu xả cho phép DoD; thời gian '
  'tự chủ cho biết pin có thể cấp điện liên tục cho phụ tải trong bao lâu khi không có nguồn phát. Tốc độ '
  'sạc/xả C-rate dùng để kiểm tra pin có bị làm việc quá tải hay không.')
FORMULA('E_{khả dụng} = E_{pin} × DoD')
FORMULA('t_{tự chủ} = E_{khả dụng} / P_{phụ tải}')
FORMULA('C_{rate} = P_{biến tần} / E_{pin}')
P('Trong đó: E_{pin} là tổng dung lượng danh định của hệ pin (kWh); DoD là độ sâu xả cho phép (không thứ '
  'nguyên), bằng 1 trừ đi mức SoC tối thiểu; E_{khả dụng} là dung lượng thực tế có thể sử dụng (kWh); '
  'P_{phụ tải} là công suất phụ tải đang xét (kW); t_{tự chủ} là thời gian tự chủ của pin (giờ); '
  'C_{rate} là tốc độ sạc/xả (1/giờ), bằng nghịch đảo số giờ cần thiết để xả hết dung lượng danh định ở '
  'công suất biến tần; P_{biến tần} là công suất biến tần tạo lưới nối với hệ pin (kW).')
H('2.5. Tính toán biến tần', 2)
P('Biến tần tạo lưới phải vừa cấp đủ công suất cho phụ tải đỉnh, vừa chịu được dòng nạp/xả của pin; do có '
  'tổn thất chuyển đổi nên công suất biến tần phải lớn hơn công suất phụ tải đỉnh chia cho hiệu suất biến tần.')
FORMULA('P_{GFL, min} ≥ P_{đỉnh} / η_{biến tần}')
P('Trong đó: P_{GFL, min} là công suất tối thiểu cần trang bị của bộ biến tần tạo lưới (kW); P_{đỉnh} là '
  'công suất phụ tải đỉnh (kW); η_{biến tần} là hiệu suất của bộ biến tần (không thứ nguyên), thường '
  '0,94–0,97. Công suất thực chọn còn phải làm tròn lên theo công suất thương mại của thiết bị và có dự '
  'phòng cho phụ tải phát triển.')
H('2.6. Tính toán kinh tế', 2)
P('Các chỉ tiêu kinh tế được tính theo phương pháp quy đổi dòng tiền về hiện tại, tương tự cách tính của '
  'HOMER Pro. Trước hết lãi suất danh nghĩa được chuyển thành lãi suất thực theo công thức Fisher để loại '
  'bỏ ảnh hưởng của lạm phát; sau đó dùng hệ số thu hồi vốn CRF để phân bố vốn đầu tư ban đầu thành chi phí '
  'niên đều, và quy toàn bộ chi phí trong vòng đời dự án về hiện tại để có NPC và COE.')
FORMULA('r = (1 + i) / (1 + f) − 1')
FORMULA('CRF(r, N) = r(1 + r)^{N} / [(1 + r)^{N} − 1]')
FORMULA('NPC = C_{0} + Σ (OM_{t} + Rep_{t} − S_{t}) / (1 + r)^{t}')
FORMULA('COE = (NPC × CRF) / E_{năm}')
FORMULA('T_{hoàn vốn} = C_{0} / (L_{tiết kiệm/năm} − OM_{năm})')
P('Trong đó: i là lãi suất danh nghĩa (phần trăm/năm); f là tỷ lệ lạm phát (phần trăm/năm); r là lãi suất '
  'chiết khấu thực (phần trăm/năm); N là tuổi thọ dự án (năm); CRF là hệ số thu hồi vốn; C_{0} là vốn đầu '
  'tư ban đầu (đồng); OM_{t} là chi phí vận hành và bảo dưỡng năm thứ t (đồng); Rep_{t} là chi phí thay thế '
  'thiết bị năm thứ t (đồng); S_{t} là giá trị thu hồi cuối đời của thiết bị (đồng); t là năm tính toán; '
  'NPC là tổng chi phí vòng đời quy về hiện tại (đồng); E_{năm} là điện năng phục vụ phụ tải trong năm '
  '(kWh/năm); COE là chi phí điện năng quy dẫn (đồng/kWh); T_{hoàn vốn} là thời gian hoàn vốn đơn giản '
  '(năm); L_{tiết kiệm/năm} là lợi ích ròng hằng năm so với phương án mua điện diesel (đồng/năm).')
"""

start = s.index("H('2.1. Tính toán phụ tải', 2)")
end_marker = "BREAK()\n\n# ===================== CHUONG 5"
end = s.index(end_marker)
s = s[:start] + NEW22 + s[end:]

# ngat trang truoc CHUONG 2
s = s.replace("\nH('CHƯƠNG 2: PHƯƠNG PHÁP TÍNH TOÁN CẤU HÌNH NGUỒN CUNG CẤP ĐIỆN', 1)\n",
              "\nBREAK()\n\nH('CHƯƠNG 2: PHƯƠNG PHÁP TÍNH TOÁN CẤU HÌNH NGUỒN CUNG CẤP ĐIỆN', 1)\n", 1)

# bo 2 doan dau chuong 3 (thay bang 1 doan ngan)
old_c3 = s[s.index("H('CHƯƠNG 3: TÍNH TOÁN NGUỒN CUNG CẤP ĐIỆN CHO MICROGRID ST – GIAI ĐOẠN 3', 1)"):]
old_c3 = old_c3[:old_c3.index("H('3.1. Địa điểm")]
new_c3 = ("H('CHƯƠNG 3: TÍNH TOÁN NGUỒN CUNG CẤP ĐIỆN CHO MICROGRID ST – GIAI ĐOẠN 3', 1)\n")
i0 = s.index("H('CHƯƠNG 3: TÍNH TOÁN NGUỒN CUNG CẤP ĐIỆN CHO MICROGRID ST – GIAI ĐOẠN 3', 1)")
i1 = s.index("H('3.1. Địa điểm", i0)
s = s[:i0] + new_c3 + s[i1:]

io.open(P, 'w', encoding='utf-8').write(s)
print('patched chapter 2 content, page break, chapter 3 intro')
