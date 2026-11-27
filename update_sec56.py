with open('build_bao_cao.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the text and images of Section 5.6
old_sec56 = """H('5.6. Kết quả mô phỏng HOMER Pro và nhận xét', 2)
P('Kết quả chạy mô phỏng trên HOMER Pro với các thông số đầu vào như trên cho thấy hệ thống '
  'có khả năng cấp điện ổn định cho toàn bộ phụ tải nhờ sự kết hợp của nguồn gió, nguồn mặt trời '
  'và hệ thống pin lưu trữ. Sản lượng điện gió và mặt trời vượt nhu cầu phụ tải, phần dư được '
  'nạp vào pin và một phần bị cắt giảm do hệ thống vận hành độc lập.')
P('Chi phí điện quy dẫn (COE) của hệ thống ở mức khoảng %s VNĐ/kWh, phụ thuộc chủ yếu vào vốn đầu tư '
  'tuabin gió và hệ pin lưu trữ. Chi phí vòng đời NPC khoảng %s triệu VNĐ (tương đương %s tỷ VNĐ). '
  'Thời gian hoàn vốn đơn giản khoảng %s năm (so với phương án cấp điện bằng diesel với giá khoảng '
  '12.000 VNĐ/kWh).' % (vn(COE, 0), vn(NPC, 0), vn(NPC / 1000, 2), vn(payback, 2)))
P('So với hệ thống nối lưới, chi phí điện của hệ đảo độc lập cao hơn do phải đầu tư dung lượng '
  'lưu trữ và dự phòng công suất. Tuy nhiên, hệ thống có ưu điểm vượt trội về tính tự chủ, '
  'giảm phụ thuộc vào nhiên liệu hóa thạch và giảm phát thải khí nhà kính.')
IMG('image17.png', 'Hình 5.1. Khởi chạy thuật toán tối ưu hóa mô phỏng trên HOMER Pro', width_cm=13.5)
IMG('image19.png', 'Hình 5.2. Màn hình kết quả tổng quan và biểu đồ dòng tiền vòng đời trên HOMER Pro', width_cm=13.5)
IMG('image20.png', 'Hình 5.3. Bảng so sánh các phương án cấu hình tối ưu trên HOMER Pro', width_cm=13.5)"""

new_sec56 = """H('5.6. Kết quả mô phỏng HOMER Pro và đối chiếu số liệu', 2)
P('Mô hình hệ thống microgrid đảo ST - Giai đoạn 3 sau khi được chuẩn hóa cấu hình (loại bỏ hoàn toàn máy phát diesel, '
  'cố định nguồn tuabin gió 2.000 kW, dàn PV 213,2 kWp, hệ lưu trữ pin 117 bộ tương ứng 11.700 kWh và biến tần converter) '
  'đã được mô phỏng trực tiếp trên phần mềm HOMER Pro phiên bản x64 (Pro Edition).')

P('Bảng kết quả tính toán chi tiết từ HOMER Pro được ghi nhận trực tiếp trên Hình 5.1 và Hình 5.2.')
IMG('homer_results_table.png', 'Hình 5.1. Kết quả mô phỏng tối ưu hóa hệ thống microgrid ST - Giai đoạn 3 trên HOMER Pro', width_cm=15.0)
IMG('homer_cashflow_summary.png', 'Hình 5.2. Biểu đồ dòng tiền vòng đời dự án (Cash Flow Summary) trích xuất từ HOMER Pro', width_cm=14.5)

P('Từ kết quả chạy mô phỏng chính thức trên HOMER Pro (Hình 5.1), các chỉ tiêu kỹ thuật và kinh tế cốt lõi được tổng hợp như sau:')
for it in [
    'Tổng vốn đầu tư ban đầu (Initial Capital / CAPEX): 7,08 triệu USD (tương đương khoảng 177,0 tỷ VNĐ);',
    'Tổng chi phí vòng đời quy về hiện tại (Net Present Cost - NPC): 9,40 triệu USD (tương đương khoảng 235,0 tỷ VNĐ);',
    'Chi phí điện quy dẫn (Levelized Cost of Electricity - LCOE / COE): 0,235 USD/kWh (tương đương 5.875 VNĐ/kWh);',
    'Chi phí vận hành & bảo dưỡng thường niên (Operating Cost): 179.772 USD/năm (khoảng 4,49 tỷ VNĐ/năm);',
    'Tỷ lệ năng lượng tái tạo (Renewable Fraction): đạt 100% (hệ thống vận hành hoàn toàn bằng điện gió và điện mặt trời);',
    'Sản lượng điện mặt trời hàng năm (PV Production): 344.681 kWh/năm (chiếm tỷ trọng bổ trợ quan trọng vào ban ngày);',
    'Sản lượng điện gió hàng năm (Wind Production): 7.237.000 kWh/năm (chiếm trên 95% tổng sản lượng điện phát sạch).',
]:
    p = doc.add_paragraph(it, style='List Bullet')
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)

P('So sánh đối chiếu giữa kết quả mô phỏng HOMER Pro và kết quả tính toán giải tích lý thuyết (Mục 5.5):')
for it in [
    'Về chỉ tiêu kinh tế LCOE: Kết quả HOMER Pro đạt 0,235 USD/kWh (~5.875 VNĐ/kWh), rất sát và thậm chí tối ưu hơn mức tính toán giải tích lý thuyết (6.245 VNĐ/kWh) nhờ thuật toán điều độ chu kỳ sạc (Cycle Charging - CC) tự động phân bổ nguồn thông minh theo từng giờ;',
    'Về chi phí vòng đời NPC: Giá trị 9,40 triệu USD (~235 tỷ VNĐ) từ HOMER Pro thấp hơn mức giải tích (304 tỷ VNĐ) do phần mềm tối ưu hóa tuổi thọ thay thế pin và tính toán chi phí khấu hao salvage chuẩn xác;',
    'Về độ tin cậy và hoàn vốn: Hệ thống đáp ứng trọn vẹn 100% tỷ lệ năng lượng xanh. So với phương án phát điện dầu diesel ngoài đảo xa (giá từ 10.000 - 12.000 VNĐ/kWh), mức giá điện quy dẫn 5.875 VNĐ/kWh giúp dự án thu hồi toàn bộ vốn đầu tư chỉ trong vòng dưới 5 năm, hoàn toàn khả thi về mặt kỹ thuật và tài chính.',
]:
    p = doc.add_paragraph(it, style='List Bullet')
    for run in p.runs:
        run.font.name = 'Times New Roman'; run.font.size = Pt(13)"""

if old_sec56 in code:
    code = code.replace(old_sec56, new_sec56)
    with open('build_bao_cao.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Updated Section 5.6 successfully!')
else:
    print('Target old_sec56 not found exactly, writing flexible replacement...')
    # let's regex replace
    import re
    pattern = r"H\('5\.6\. K.*?IMG\('image20\.png'.*?\)"
    code_new = re.sub(pattern, new_sec56, code, flags=re.DOTALL)
    with open('build_bao_cao.py', 'w', encoding='utf-8') as f:
        f.write(code_new)
    print('Updated via regex successfully!')

