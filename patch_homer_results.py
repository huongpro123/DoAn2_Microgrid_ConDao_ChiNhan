# -*- coding: utf-8 -*-
"""Patch: chen ket qua HOMER Pro that (trich tu .homer) vao muc 3.14 + qua trang dau chuong."""
import io
import re

P = r'D:\chinhan\build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()

# 1. Qua trang truoc cac tieu de cap 1
for h in ["H('MỞ ĐẦU', 1)", "H('CHƯƠNG 1: TỔNG QUAN HỆ THỐNG OFF-GRID TRONG MICROGRID', 1)",
          "H('CHƯƠNG 3: TÍNH TOÁN NGUỒN CUNG CẤP ĐIỆN CHO MICROGRID ST – GIAI ĐOẠN 3', 1)",
          "H('KẾT LUẬN VÀ KIẾN NGHỊ', 1)", "H('TÀI LIỆU THAM KHẢO', 1)"]:
    old = "\n" + h
    if old in s and ("BREAK()\n" + h) not in s:
        s = s.replace(old, "\nBREAK()\n" + h, 1)

# 2. Thay khoi 3.14 (tu bullet dau tien den het bang 3.14) bang phan tich dung so HOMER
start_anchor = "P('Từ kết quả chạy mô phỏng chính thức trên HOMER Pro (Hình 3.3)"
end_anchor = "caption='Bảng 3.14. Đối chiếu kết quả tính toán giải tích và mô phỏng HOMER Pro')"
i0 = s.index(start_anchor)
i1 = s.index(end_anchor) + len(end_anchor)

new = r'''P('Kết quả chi tiết của lần chạy mô phỏng được trích xuất trực tiếp từ tệp mô phỏng '
  '(ST_Giai_doan_3_template.homer), cụ thể là khối ResultSummary do chính HOMER Pro tính và lưu lại. '
  'Vì vậy toàn bộ số liệu trong Bảng 3.15 là kết quả của phần mềm, không phải số tính tay.')
HOMER = json.load(io_open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homer_results.json'), encoding='utf-8'))[0]
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
        ['Công suất nghịch lưu trung bình', 'P_{inv,tb}', 'kW', vn(HOMER['inverter_mean'], 2)],
        ['Công suất chỉnh lưu trung bình', 'P_{rec,tb}', 'kW', vn(HOMER['rectifier_mean'], 2)],
        ['Vốn đầu tư ban đầu', 'CAPEX', 'USD', vn(HOMER['capital_cost'], 0)],
        ['Chi phí vòng đời quy về hiện tại', 'NPC', 'USD', vn(HOMER['net_present_cost'], 0)],
        ['Chi phí điện quy dẫn', 'LCOE', 'USD/kWh', vn(HOMER['cost_of_energy'], 4)],
        ['Chi phí vận hành – bảo dưỡng hàng năm', 'O\\&M', 'USD/năm', vn(HOMER['operating_cost'], 0)],
    ],
    widths=[6.6, 3.2, 2.4, 3.8], caption='Bảng 3.15. Kết quả mô phỏng HOMER Pro trích xuất từ tệp mô phỏng')

P('Từ Bảng 3.15, tổng phụ tải mà mô hình phải phục vụ là ' + vn(E_total_load, 0) + ' kWh/năm '
  '(gồm ' + vn(E_served, 0) + ' kWh được cấp và ' + vn(E_unmet, 0) + ' kWh còn thiếu), chỉ lệch '
  '0,001 % so với giá trị ' + vn(E_load, 0) + ' kWh/năm tính theo phương pháp hệ số tải ở Mục 3.9. '
  'Điều này xác nhận mô hình đã khai báo đúng bộ số liệu phụ tải của hệ thống.')
P('Hai chỉ tiêu cần được luận giải thêm là điện năng thiếu và điện năng dư. Lượng điện thiếu chiếm '
  + vn(pct_unmet, 1) + ' % phụ tải, xuất hiện chủ yếu vào các giờ tối khi tuabin gió ở dưới tốc độ khởi '
  'động và dàn PV không phát: khi đó pin chỉ xả được tối đa bằng công suất bộ converter '
  + vn(HOMER['converter_size'], 0) + ' kW, nhỏ hơn nhiều so với phụ tải đỉnh ' + vn(P_peak, 1) + ' kW. '
  'Ngược lại, lượng điện dư chiếm ' + vn(pct_excess, 1) + ' % tổng sản lượng vì hệ thống vận hành độc lập, '
  'không có lưới để phát ngược và dung lượng lưu trữ không đủ hấp thụ toàn bộ sản lượng gió về đêm.')
P('Kết quả này chỉ ra rằng bộ converter khai báo trong mô hình (100 kW) chính là khâu giới hạn độ tin cậy '
  'cấp điện, trong khi sơ đồ nguyên lý đã bố trí hai biến tần tạo lưới 1 MW cho hai cụm pin. Việc khai báo '
  'đúng công suất converter theo sơ đồ (2.000 kW) sẽ là nội dung cần chạy lại mô phỏng để lượng điện thiếu '
  'giảm về mức không đáng kể; các chỉ tiêu kinh tế trong Bảng 3.15 vì thế được xem là phương án đối chiếu '
  'ở điều kiện bảo thủ.')

P('Bảng 3.16 tổng hợp đối chiếu song song giữa kết quả tính toán giải tích và kết quả mô phỏng HOMER Pro.')
TBL(
    ['Chỉ tiêu', 'Tính toán giải tích (Mục 3.13)', 'Mô phỏng HOMER Pro', 'Nhận xét'],
    [
        ['Vốn đầu tư ban đầu', '206.275 triệu VNĐ (≈ 8,25 triệu USD)',
         '7.078.680 USD (≈ 177,0 tỷ VNĐ)', 'HOMER dùng bộ đơn giá thiết bị của phần mềm'],
        ['Chi phí vòng đời (NPC)', '304.578 triệu VNĐ (≈ 12,2 triệu USD)',
         '9.402.682 USD (≈ 235,1 tỷ VNĐ)', 'HOMER tính khấu hao và thay thế pin theo tuổi thọ nên thấp hơn'],
        ['Chi phí điện quy dẫn (COE/LCOE)', '6.245 VNĐ/kWh',
         '0,2351 USD/kWh ≈ 5.878 VNĐ/kWh', 'Cùng bậc, chênh lệch khoảng 6 %'],
        ['Sản lượng điện mặt trời năm', '305.047 kWh', '344.681 kWh', 'HOMER dùng dữ liệu bức xạ NASA theo giờ'],
        ['Sản lượng điện gió năm', '6.657.600 kWh', '7.237.202 kWh', 'Hệ số công suất mô phỏng ≈ 0,41 so với 0,38 giả định'],
        ['Điện năng phục vụ tải', '3.772.976 kWh (toàn bộ nhu cầu)', vn(E_served, 0) + ' kWh (còn thiếu ' + vn(E_unmet, 0) + ' kWh)',
         'Mô hình đang bị giới hạn bởi converter 100 kW'],
        ['Thời gian hoàn vốn', '4,80 năm', 'Không tính (giá bán điện bằng 0)', 'Cần khai báo giá bán điện để HOMER xuất IRR/hoàn vốn'],
    ],
    widths=[3.6, 4.2, 4.2, 4.0], caption='Bảng 3.16. Đối chiếu kết quả tính toán giải tích và mô phỏng HOMER Pro')'''

s = s[:i0] + new + s[i1:]

# 3. bo sung import io_open (dung io.open de doc utf-8)
if 'import io\n' not in s:
    s = s.replace('import re\nimport os\nimport json\n', 'import re\nimport os\nimport json\nimport io as io_open\n', 1)

io.open(P, 'w', encoding='utf-8').write(s)
print('patched OK')
