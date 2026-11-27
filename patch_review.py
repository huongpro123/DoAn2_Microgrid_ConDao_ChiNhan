# -*- coding: utf-8 -*-
"""Sua bao cao theo nhan xet cua giang vien (file Bao_cao_ST_Giai_doan_3_v1.pdf)."""
import io

P = r'D:\chinhan\build_bao_cao.py'
s = io.open(P, encoding='utf-8').read()
orig = s

# ---------- 1. Ten nganh + khoa tren bia ----------
s = s.replace(
    "    C('Ngành: Kỹ thuật Điện – Điện tử', 13, bold=False)",
    "    C('Ngành: Công nghệ Kỹ thuật Năng lượng', 13, bold=False)\n"
    "    C('Khóa: 2023', 13, bold=False)", 1)

# ---------- 2. Tieu de bia: khong tach 'GIAI DOAN 3' ----------
s = s.replace(
    "TEN_DE_TAI_1 = 'MÔ PHỎNG HỆ THỐNG MICROGRID ĐẢO ST – GIAI ĐOẠN 3'",
    "TEN_DE_TAI_1 = 'MÔ PHỎNG HỆ THỐNG MICROGRID ĐẢO ST – GIAI ĐOẠN 3'\n"
    "# Ban tren bia dung khoang trang khong ngat de 'GIAI ĐOẠN 3' luon nam cung mot hang\n"
    "TEN_DE_TAI_COVER = 'MÔ PHỎNG HỆ THỐNG MICROGRID ĐẢO ST – GIAI\\u00A0ĐOẠN\\u00A03'", 1)
s = s.replace("    C(TEN_DE_TAI_1, 18)", "    C(TEN_DE_TAI_COVER, 18)", 1)

# ---------- 3. Muc 1. Ly do chon de tai: viet day du hon ----------
old_lydo = """P('Khu vực biển Đông gần Côn Đảo có vị trí quan trọng về quốc phòng – kinh tế, '
  'nhưng việc cấp điện cho các phụ tải trên đảo và vùng biển lân cận gặp nhiều khó khăn do '
  'khoảng cách xa đất liền, chi phí kéo lưới cao và nguồn nhiên liệu hóa thạch tại chỗ hạn chế. '
  'Việc xây dựng hệ thống microgrid độc lập, tận dụng nguồn năng lượng tái tạo tại chỗ '
  '(mặt trời, gió) kết hợp lưu trữ năng lượng là hướng đi phù hợp và bền vững [10], [11].')
P('Sơ đồ hệ thống ST – Giai đoạn 3 là phương án cấp điện cho một khu vực phụ tải hỗn hợp '
  'gồm phụ tải hiện trạng, phụ tải CS và phụ tải KT, với các nguồn điện mặt trời, tuabin gió '
  'và hai hệ thống pin lưu trữ. Đề tài tập trung mô phỏng hệ thống này trên phần mềm HOMER Pro '
  'nhằm tính toán các chỉ tiêu kỹ thuật – kinh tế.')"""

new_lydo = """P('Côn Đảo là quần đảo nằm ở vùng biển Đông, cách đất liền (TP. Vũng Tàu) khoảng 80 hải lý '
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
  'làm cơ sở đánh giá tính khả thi của phương án trước khi triển khai.')"""

assert old_lydo in s
s = s.replace(old_lydo, new_lydo, 1)

# ---------- 4. Bo 2 muc khong phai muc tieu ----------
s = s.replace("    'Trình bày hệ thống công thức tính toán làm cơ sở cho việc thiết lập thông số đầu vào;',\n", "", 1)
s = s.replace("    'Đánh giá kết quả và đề xuất hướng phát triển.',\n", "", 1)

# ---------- 5. Them 2.7 (chi tieu ky thuat) va 2.8 (chi tieu moi truong) ----------
anchor27 = """# ===================== CHUONG 5 =====================

H('2.7. Phương pháp mô phỏng tối ưu bằng HOMER Pro', 2)"""

new27 = """H('2.7. Các chỉ tiêu đánh giá kỹ thuật', 2)
P('Ngoài công suất và sản lượng của từng thành phần, một cấu hình nguồn còn được đánh giá bằng các '
  'chỉ tiêu tổng hợp phản ánh mức độ đáp ứng phụ tải và mức khai thác nguồn. Bốn chỉ tiêu được sử '
  'dụng trong báo cáo gồm tỷ lệ đáp ứng nhu cầu, tỷ lệ năng lượng tái tạo, tỷ lệ điện năng bị cắt '
  'giảm và hệ số công suất của nguồn phát.')
FORMULA('R_{đáp ứng} = E_{phục vụ} / E_{nhu cầu}')
FORMULA('RF = E_{tái tạo} / E_{phục vụ}')
FORMULA('CUR = E_{dư} / E_{sản xuất}')
FORMULA('CF = E_{năm} / (P_{định mức} × 8.760)')
P('Trong đó: E_{phục vụ} là điện năng thực tế cấp được cho phụ tải trong năm (kWh/năm); E_{nhu cầu} '
  'là điện năng tiêu thụ theo tính toán phụ tải (kWh/năm); R_{đáp ứng} là tỷ lệ đáp ứng nhu cầu '
  '(không thứ nguyên), bằng 1 khi hệ thống cấp đủ điện; E_{tái tạo} là điện năng do các nguồn tái '
  'tạo cung cấp (kWh/năm); RF là tỷ lệ năng lượng tái tạo (Renewable Fraction); E_{dư} là điện năng '
  'dư không hấp thụ được (kWh/năm); E_{sản xuất} là tổng điện năng các nguồn phát (kWh/năm); CUR là '
  'tỷ lệ điện năng bị cắt giảm (curtailment ratio); CF là hệ số công suất của nguồn phát; '
  'P_{định mức} là công suất định mức của nguồn (kW) và 8.760 là số giờ trong năm (giờ). '
  'Chỉ tiêu R_{đáp ứng} cho biết hệ có cấp điện liên tục hay không: R_{đáp ứng} = 1 tương ứng cấp '
  'điện 24/24 giờ, R_{đáp ứng} < 1 nghĩa là còn thời đoạn thiếu hụt và cần bổ sung nguồn hoặc '
  'tăng công suất bộ biến đổi.')

H('2.8. Các chỉ tiêu đánh giá môi trường', 2)
P('Hệ thống cấp điện bằng diesel phát thải trực tiếp khí nhà kính tại chỗ; khi thay thế bằng nguồn '
  'tái tạo, lượng phát thải đó được tránh. Lượng CO_{2} tránh được trong một năm xác định từ điện '
  'năng được thay thế và hệ số phát thải của máy phát diesel.')
FORMULA('M_{CO2} = E_{thay thế} × EF_{diesel} / 1.000')
P('Trong đó: M_{CO2} là khối lượng CO_{2} tránh được trong năm (tấn CO_{2}/năm); E_{thay thế} là '
  'điện năng do nguồn tái tạo cung cấp thay cho diesel (kWh/năm); EF_{diesel} là hệ số phát thải '
  'của máy phát diesel (kg CO_{2}/kWh); hệ số 1.000 dùng để đổi từ kg sang tấn. Theo hướng dẫn '
  'kiểm kê khí nhà kính của IPCC, hệ số phát thải của dầu diesel là 74,8 kg CO_{2}/GJ [12]; với '
  'hiệu suất máy phát diesel cỡ 35 %, hệ số phát thải tính theo điện năng xấp xỉ '
  '0,74 kg CO_{2}/kWh — phù hợp với dải 0,6–0,8 kg CO_{2}/kWh thường ghi nhận cho máy phát diesel '
  'cỡ nhỏ và vừa.')
P('Ngoài CO_{2}, việc thay thế diesel còn loại bỏ các phát thải tại chỗ khác như NO_{x}, SO_{2}, '
  'bụi mịn và tiếng ồn — những tác nhân ảnh hưởng trực tiếp đến chất lượng không khí và đời sống '
  'cư dân trên đảo, đồng thời giảm rủi ro tràn dầu khi vận chuyển và lưu trữ nhiên liệu trong khu '
  'vực Vườn quốc gia Côn Đảo. Các tác động này được đánh giá định tính, còn lượng CO_{2} tránh '
  'được tính định lượng theo công thức trên.')

""" + anchor27
assert anchor27 in s
s = s.replace(anchor27, new27, 1)

# ---------- 6. Doi so 2.7..2.11 -> 2.9..2.13 ----------
pairs = [("H('2.11. Ràng buộc hệ thống', 2)", "H('2.13. Ràng buộc hệ thống', 2)"),
         ("H('2.10. Chiến lược điều độ', 2)", "H('2.12. Chiến lược điều độ', 2)"),
         ("H('2.9. Thông số các thành phần', 2)", "H('2.11. Thông số các thành phần', 2)"),
         ("H('2.8. Kiến trúc mô hình trên HOMER Pro', 2)", "H('2.10. Kiến trúc mô hình trên HOMER Pro', 2)"),
         ("H('2.7. Phương pháp mô phỏng tối ưu bằng HOMER Pro', 2)", "H('2.9. Phương pháp mô phỏng tối ưu bằng HOMER Pro', 2)")]
for a, b in pairs:
    assert a in s, a
    s = s.replace(a, b, 1)

# ---------- 7. Chuan hoa kich thuoc anh chup HOMER ----------
for old, new in [("'Hình 2.1. Giao diện khởi tạo dự án microgrid trên HOMER Pro', width_cm=13.5)",
                  "'Hình 2.1. Giao diện khởi tạo dự án microgrid trên HOMER Pro', width_cm=14.0)"),
                 ("'Hình 2.2. Cấu hình thông số dàn pin quang điện PV trên HOMER Pro', width_cm=13.0)",
                  "'Hình 2.2. Cấu hình thông số dàn pin quang điện PV trên HOMER Pro', width_cm=14.0)"),
                 ("'Hình 2.3. Cấu hình đường cong công suất tuabin gió trên HOMER Pro', width_cm=13.0)",
                  "'Hình 2.3. Cấu hình đường cong công suất tuabin gió trên HOMER Pro', width_cm=14.0)"),
                 ("'Hình 2.4. Cấu hình bộ biến tần Converter trên HOMER Pro', width_cm=13.0)",
                  "'Hình 2.4. Cấu hình bộ biến tần Converter trên HOMER Pro', width_cm=14.0)"),
                 ("'Hình 3.1. Khai báo dữ liệu bức xạ mặt trời NASA trên HOMER Pro', width_cm=13.5)",
                  "'Hình 3.1. Khai báo dữ liệu bức xạ mặt trời NASA trên HOMER Pro', width_cm=14.0)"),
                 ("'Hình 3.2. Nhập dữ liệu và đồ thị phụ tải 24 giờ trên HOMER Pro', width_cm=13.5)",
                  "'Hình 3.2. Nhập dữ liệu và đồ thị phụ tải 24 giờ trên HOMER Pro', width_cm=14.0)")]:
    assert old in s, old
    s = s.replace(old, new, 1)

# ---------- 8. Hinh 3.7: chi lay do thi ----------
s = s.replace("IMG('homer_cashflow.png'", "IMG('homer_cashflow_crop.png'", 1)
s = s.replace("'Hình 3.7. Biểu đồ dòng tiền vòng đời dự án (Cash Flow Summary) trích xuất từ HOMER Pro', width_cm=14.5)",
              "'Hình 3.7. Biểu đồ dòng tiền vòng đời dự án (Cash Flow Summary) trích xuất từ HOMER Pro', width_cm=14.0)", 1)

# ---------- 9. Bang 3.8: canh giua cac o ----------
old_b38 = "    widths=[6.0, 6.0], caption='Bảng 3.8. Đường cong công suất tuabin gió Enercon E-82 E2')"
new_b38 = """    widths=[6.0, 6.0], caption='Bảng 3.8. Đường cong công suất tuabin gió Enercon E-82 E2')
for _row in doc.tables[-1].rows:
    for _c in _row.cells:
        for _p in _c.paragraphs:
            _p.alignment = WD_ALIGN_PARAGRAPH.CENTER"""
assert old_b38 in s
s = s.replace(old_b38, new_b38, 1)

# ---------- 10. Muc 3.15: thao luan ket qua ----------
anchor315 = "# ===================== CHUONG 6 =====================\nH('KẾT LUẬN VÀ KIẾN NGHỊ', 1)"
new315 = """H('3.15. Thảo luận kết quả: khả năng đáp ứng tải và hiệu quả kỹ thuật – kinh tế – môi trường', 2)
P('Từ các kết quả ở Bảng 3.17 và Bảng 3.18 có thể đánh giá phương án theo ba khía cạnh: khả năng đáp '
  'ứng tải, hiệu quả kỹ thuật và hiệu quả kinh tế – môi trường.')
P('Về khả năng đáp ứng tải: tổng nhu cầu tính theo hệ số tải là 3.772.976 kWh/năm, trong khi mô phỏng '
  'chỉ cấp được 3.093.168 kWh/năm, tương ứng tỷ lệ đáp ứng R_{đáp ứng} = 3.093.168 / 3.772.976 = '
  '0,820 hay 82,0 %; phần thiếu là 679.837 kWh/năm (khoảng 1.862 kWh/ngày). Nguyên nhân trực tiếp '
  'được chỉ ra từ Bảng 3.17: bộ biến tần (converter) trong phương án tối ưu chỉ có 100 kW, nhỏ hơn '
  'nhiều so với phụ tải đỉnh 783,1 kW, nên không thể truyền hết công suất từ cụm pin ra thanh cái AC '
  'vào các giờ cao điểm. Như vậy với cấu hình này hệ thống chưa đảm bảo cấp điện liên tục 24/24 giờ; '
  'đây là giới hạn của bộ biến đổi chứ không phải của nguồn phát, vì sản lượng nguồn tái tạo vượt xa '
  'nhu cầu. Khi triển khai theo sơ đồ nguyên lý với 2 biến tần tạo lưới 1 MW (tổng 2.000 kW), giới '
  'hạn này được loại bỏ và cần chạy lại mô hình để xác nhận lượng điện thiếu giảm về 0.')
P('Về hiệu quả kỹ thuật: tổng sản lượng các nguồn phát là 7.581.882 kWh/năm, gấp 2,01 lần nhu cầu '
  'phụ tải (7.581.882 / 3.772.976). Tỷ lệ năng lượng tái tạo đạt 100 %, nghĩa là toàn bộ điện năng '
  'phục vụ tải đến từ mặt trời và gió, không dùng nhiên liệu hóa thạch. Trong đó dàn PV 213,2 kWp '
  'cho 344.681 kWh/năm (hệ số công suất 0,185) và tuabin gió 2.000 kW cho 7.237.202 kWh/năm (hệ số '
  'công suất 0,41). Điện năng dư 4.426.778 kWh/năm chiếm 58,4 % sản lượng — hệ quả tất yếu của hệ '
  'off-grid có nguồn gió lớn hơn phụ tải nhiều lần và không có lưới để phát ngược; phần dư này bị cắt '
  'giảm (CUR = 0,584). Hệ pin 11.700 kWh cho thời gian tự chủ 21,7 giờ và chỉ luân chuyển 297.312 '
  'kWh/năm (khoảng 2,5 % sản lượng), tức pin làm việc ở chế độ nhẹ, ít suy giảm tuổi thọ.')
P('Về hiệu quả kinh tế: chi phí điện năng quy dẫn của phương án là 0,2351 USD/kWh, tương đương '
  'khoảng 5.878 VNĐ/kWh, thấp hơn khoảng 51 % so với chi phí phát điện diesel tại đảo (giả định '
  '10.000–12.000 VNĐ/kWh). Với mức chênh lệch 12.000 − 5.878 = 6.122 VNĐ/kWh và lượng điện thực '
  'cấp 3.093.168 kWh/năm, lợi ích tiết kiệm ước tính khoảng 18.930 triệu VNĐ/năm (≈ 18,9 tỷ '
  'đồng/năm); nếu hệ thống cấp đủ nhu cầu 3.772.976 kWh/năm thì mức tiết kiệm tương ứng khoảng '
  '23.100 triệu VNĐ/năm. Vốn đầu tư ban đầu 7,08 triệu USD (≈ 177 tỷ đồng) và tổng chi phí vòng đời '
  'NPC 9,40 triệu USD (≈ 235 tỷ đồng); chi phí vận hành bảo dưỡng hằng năm 179.772 USD.')
P('Về hiệu quả môi trường: áp dụng công thức ở mục 2.8 với hệ số phát thải của máy phát diesel '
  '0,74 kg CO_{2}/kWh, lượng CO_{2} tránh được tương ứng với lượng điện thực cấp là '
  'M_{CO2} = 3.093.168 × 0,74 / 1.000 ≈ 2.289 tấn CO_{2}/năm; nếu đáp ứng đủ nhu cầu '
  '3.772.976 kWh/năm thì lượng tránh được khoảng 2.792 tấn CO_{2}/năm. Ngoài ra hệ thống không phát '
  'thải NO_{x}, SO_{2}, bụi và tiếng ồn tại chỗ, đồng thời loại bỏ nhu cầu vận chuyển và lưu trữ dầu '
  'diesel trên đảo — yếu tố có ý nghĩa với khu vực Vườn quốc gia Côn Đảo.')
P('Tổng hợp lại, cấu hình lai mặt trời – gió – pin đáp ứng tốt yêu cầu về nguồn và có hiệu quả rõ rệt '
  'về kinh tế và môi trường so với phương án diesel; ràng buộc duy nhất còn lại là công suất bộ biến '
  'đổi, cần được thiết kế theo phụ tải đỉnh (2.000 kW theo sơ đồ nguyên lý) thay vì để phần mềm tự '
  'tối ưu theo chi phí.')

""" + anchor315
assert anchor315 in s
s = s.replace(anchor315, new315, 1)

# ---------- 11. Bo sung tai lieu tham khao [12] ----------
old_ref = "'[11] Tập đoàn Điện lực Việt Nam, Biểu giá bán lẻ điện hiện hành, https://www.evn.com.vn.',"
new_ref = (old_ref + "\n"
           "    '[12] Intergovernmental Panel on Climate Change (IPCC), 2006 IPCC Guidelines for National '\n"
           "    'Greenhouse Gas Inventories, Volume 2: Energy, Chapter 1–2, 2006.',")
assert old_ref in s
s = s.replace(old_ref, new_ref, 1)

io.open(P, 'w', encoding='utf-8').write(s)
print('patched OK, delta len =', len(s) - len(orig))
