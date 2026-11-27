# -*- coding: utf-8 -*-
"""Soan noi dung chuan bi hoi dap voi giang vien (theo tin nhan hen gap sang thu 6)."""
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn

OUT = r'D:\chinhan\Chuan_bi_hoi_dap_bao_cao_ST.docx'

doc = docx.Document()

# ---------- page setup ----------
for s in doc.sections:
    s.page_width = Cm(21.0); s.page_height = Cm(29.7)
    s.left_margin = Cm(3.0); s.right_margin = Cm(2.0)
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)

st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.font.size = Pt(13)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for name, size, align in (('Heading 1', 16, WD_ALIGN_PARAGRAPH.CENTER),
                          ('Heading 2', 14, WD_ALIGN_PARAGRAPH.LEFT),
                          ('Heading 3', 13, WD_ALIGN_PARAGRAPH.LEFT)):
    h = doc.styles[name]
    h.font.name = 'Times New Roman'; h.font.size = Pt(size); h.font.bold = True
    h.font.color.rgb = RGBColor(0, 0, 0)
    h.paragraph_format.alignment = align
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.first_line_indent = Cm(0)
    h.paragraph_format.keep_with_next = True


def H(text, level=1):
    p = doc.add_heading(text, level=level)
    for r in p.runs:
        r.font.name = 'Times New Roman'
    return p


def P(text, italic=False, bold=False, indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25) if indent else Cm(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'; r.font.size = Pt(13)
    r.italic = italic; r.bold = bold
    return p


def B(items):
    for it in items:
        p = doc.add_paragraph(it, style='List Bullet')
        p.paragraph_format.first_line_indent = Cm(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'; r.font.size = Pt(13)


# ================= NOI DUNG =================
H('CHUẨN BỊ HỎI – ĐÁP VỚI GIẢNG VIÊN', 1)
P('Tài liệu dùng cho buổi gặp Thầy (sáng thứ 6): phần 1 là đoạn văn mở đầu để trình bày khi vào gặp; '
  'phần 2 là các câu hỏi Thầy thường đặt ra kèm câu trả lời ngắn, có số liệu lấy đúng từ báo cáo; '
  'phần 3 là những điểm nên chủ động nêu trước (hạn chế và hướng khắc phục).', italic=True)

# ---------- Phan 1 ----------
H('1. Đoạn văn mở đầu (nói khi bắt đầu buổi gặp)', 2)
P('Kính thưa Thầy, em xin báo cáo tóm tắt phần đã chỉnh sửa theo các góp ý của Thầy. Về bố cục, em đã '
  'xếp lại báo cáo thành đúng ba chương: Chương 1 tổng quan hệ thống off-grid trong microgrid; Chương 2 '
  'phương pháp tính toán cấu hình nguồn cung cấp điện, trong đó mỗi công thức đều được luận giải và '
  'chú thích đầy đủ các đại lượng, bổ sung thêm hai mục chỉ tiêu đánh giá kỹ thuật và chỉ tiêu đánh giá '
  'môi trường; Chương 3 tính toán cho hệ thống ST – Giai đoạn 3 tại Côn Đảo, gồm điều kiện bức xạ – nhiệt '
  'độ, điều kiện gió, phụ tải, thông số kinh tế, lựa chọn thiết bị và toàn bộ kết quả tính toán, mô phỏng. '
  'Về nội dung, em đã bổ sung số liệu khí tượng thật của NASA POWER theo 12 tháng, làm rõ lựa chọn tấm pin '
  '650 Wp, tuabin gió Enercon E-82 E2 2.000 kW và pin Li-ion LFP 11.700 kWh, đồng thời trích dẫn 12 tài '
  'liệu tham khảo ngay trong thân bài. Về hình thức, em đã chuẩn hoá khổ A4 theo mẫu của Khoa, canh đều các '
  'đoạn, thống nhất kích thước hình, khắc phục các trang trống và chi tiết hoá kết quả mô phỏng HOMER Pro '
  'thành bảng số liệu cụ thể. Kết quả chính: với phụ tải đỉnh 783,1 kW và điện năng tiêu thụ 3.772.976 '
  'kWh/năm, cấu hình mặt trời – gió – pin cho sản lượng nguồn tái tạo 7.581.882 kWh/năm (tỷ lệ năng '
  'lượng tái tạo 100 %), chi phí điện năng quy dẫn 0,2351 USD/kWh (khoảng 5.878 đồng/kWh), thấp hơn khoảng '
  '51 % so với phương án phát điện diesel và tránh được khoảng 2.289 tấn CO₂ mỗi năm. Điểm hạn chế hiện còn '
  'là bộ biến tần 100 kW do phần mềm tự tối ưu, nên trong báo cáo em đã nêu rõ nguyên nhân và khuyến nghị '
  'chạy lại mô hình với 2.000 kW theo sơ đồ nguyên lý; đây là nội dung em xin ý kiến Thầy để hoàn thiện.')

# ---------- Phan 2 ----------
H('2. Các câu hỏi thường gặp và câu trả lời ngắn', 2)

QA = [
    ('Vì sao chọn cấu hình lai mặt trời – gió – pin mà không dùng diesel?',
     'Ba lý do: (i) nguồn tại chỗ của Côn Đảo thuận lợi, bức xạ trung bình 5,26 kWh/m²/ngày và gió '
     'trung bình 7,67 m/s ở độ cao 78 m; (ii) gió và bức xạ lệch pha theo mùa nên bù trừ cho nhau, '
     'giảm dung lượng lưu trữ; (iii) chi phí điện quy dẫn của phương án tái tạo là 0,2351 USD/kWh, '
     'thấp hơn khoảng 51 % so với diesel 10.000–12.000 đồng/kWh và không phát thải tại chỗ.'),

    ('Hai bộ số (tính tay và HOMER) khác nhau, con số nào là đúng?',
     'Cả hai đều có cơ sở, dùng để đối chiếu chứ không thay thế nhau. Tính giải tích cho COE 6.245 '
     'đồng/kWh, HOMER cho 0,2351 USD/kWh ≈ 5.878 đồng/kWh, lệch khoảng 6 % — chênh lệch chủ yếu do '
     'HOMER tính bức xạ theo giờ cao hơn 4,9 kWh/m²/ngày và có xét khấu hao, thay thế pin. Kết quả '
     'HOMER được xem là kết quả mô phỏng chính thức.'),

    ('Bức xạ dùng để tính là 4,9 hay 5,26 kWh/m²/ngày?',
     'Số liệu NASA 2001–2025 là 5,26 kWh/m²/ngày, nhưng khi tính giải tích em chọn 4,9 để dự phòng '
     'suy giảm do bụi, mây mùa mưa và sai lệch dữ liệu — thấp hơn khoảng 7 % so với NASA và 15 % so '
     'với dữ liệu giờ HOMER dùng. Điều này đã ghi rõ trong mục 3.1 để người đọc hiểu vì sao sản lượng '
     'PV của HOMER (344.681 kWh) cao hơn tính tay (305.047 kWh).'),

    ('Vì sao phụ tải thiếu 18 %? Có cấp điện 24/24 giờ được không?',
     'Chưa đạt 24/24 với cấu hình mô phỏng hiện tại. Điện năng thiếu là 679.837 kWh/năm trên tổng nhu '
     'cầu 3.772.976 kWh/năm, tức tỷ lệ đáp ứng 82,0 %. Nguyên nhân không phải thiếu nguồn (sản lượng '
     'nguồn gấp 2,01 lần nhu cầu) mà do bộ biến tần trong phương án tối ưu chỉ 100 kW, nhỏ hơn phụ tải '
     'đỉnh 783,1 kW. Khi triển khai theo sơ đồ nguyên lý với 2 biến tần tạo lưới 1 MW thì giới hạn này '
     'được loại bỏ; em đã ghi khuyến nghị chạy lại mô hình với 2.000 kW.'),

    ('Vì sao HOMER chọn converter 100 kW trong khi sơ đồ là 2 × 1 MW?',
     'HOMER tối ưu theo chi phí vòng đời nên với phụ tải trung bình 430,7 kW và nguồn gió rất lớn, phần '
     'lớn thời gian pin chỉ cần trao đổi công suất nhỏ; bộ converter 100 kW đủ để giữ chi phí thấp. Tuy '
     'nhiên khi xét phụ tải đỉnh và yêu cầu cấp điện liên tục thì cần 2.000 kW như sơ đồ. Đây là điểm '
     'em đã nêu rõ trong mục 3.14, 3.15 và phần kiến nghị.'),

    ('Vì sao chọn pin Li-ion LFP mà không dùng ắc quy chì–axit?',
     'LFP có ưu thế về độ sâu xả (80–90 % so với 50 %), tuổi thọ chu kỳ (3.000–6.000 so với '
     '500–1.200), hiệu suất vòng 90–95 % và gần như không cần bảo dưỡng — phù hợp với microgrid đảo, '
     'nơi chi phí bảo dưỡng và vận chuyển cao. Hệ thống dùng 117 khối × 100 kWh = 11.700 kWh, '
     'C-rate vận hành khoảng 0,17 h⁻¹ nên pin làm việc nhẹ, ít suy giảm tuổi thọ.'),

    ('Vì sao chọn tuabin Enercon E-82 E2?',
     'Ba lý do: đường cong công suất phù hợp dải gió tại Côn Đảo, cho hệ số công suất 0,38–0,41; '
     'truyền động trực tiếp không hộp số nên giảm bảo dưỡng và tăng độ tin cậy khi vận hành trên đảo; '
     'thiết bị thương mại phổ biến và có trong thư viện HOMER Pro. Tuabin thuộc cấp chịu gió IEC IIA, '
     'phù hợp điều kiện gió ngoài khơi gần đảo.'),

    ('Điện dư 58,4 % có lãng phí không, xử lý thế nào?',
     'Có, đây là đặc điểm của hệ off-grid khi nguồn gió lớn hơn phụ tải nhiều lần và không có lưới để '
     'phát ngược: 4.426.778 kWh/năm bị cắt giảm. Ba hướng xử lý đã nêu trong kiến nghị: giảm công suất '
     'gió hoặc số giờ khai thác, tăng dung lượng lưu trữ nếu cần cấp điện liên tục, hoặc bổ sung phụ tải '
     'có thể điều tiết (điện nước, sạc xe, trạm bơm) để hấp thụ phần dư.'),

    ('Hiệu quả môi trường tính thế nào?',
     'Theo mục 2.8: M_CO₂ = E_thay thế × EF_diesel, với hệ số phát thải của máy phát diesel khoảng '
     '0,74 kg CO₂/kWh (suy ra từ 74,8 kg CO₂/GJ của IPCC và hiệu suất 35 %). Với lượng điện thực cấp '
     '3.093.168 kWh/năm, lượng CO₂ tránh được khoảng 2.289 tấn/năm; nếu đáp ứng đủ 3.772.976 kWh/năm '
     'thì khoảng 2.792 tấn/năm; kèm theo là loại bỏ NOₓ, SO₂, bụi, tiếng ồn và rủi ro tràn dầu.'),

    ('Tính khả thi kinh tế của phương án?',
     'Vốn đầu tư ban đầu theo HOMER là 7,08 triệu USD (≈ 177 tỷ đồng), tổng chi phí vòng đời NPC '
     '9,40 triệu USD (≈ 235 tỷ đồng), chi phí vận hành bảo dưỡng 179.772 USD/năm. So với phương án '
     'diesel, mức tiết kiệm ước tính khoảng 18,9 tỷ đồng/năm (tương ứng với lượng điện thực cấp), '
     'nên thời gian hoàn vốn tính theo phương pháp giải tích khoảng 4,8 năm.'),

    ('Hạn chế của báo cáo là gì?',
     'Ba hạn chế chính, đều đã ghi trong báo cáo: (i) số liệu khí tượng lấy từ NASA POWER và dữ liệu '
     'giờ của HOMER, chưa có số liệu đo trực tiếp tại đảo; (ii) bộ biến tần do phần mềm tối ưu theo '
     'chi phí nên chưa phản ánh đúng sơ đồ nguyên lý, cần chạy lại với 2.000 kW; (iii) chưa thực hiện '
     'phân tích vòng đời (LCA) đầy đủ và chưa tính chi phí san lấp, vận chuyển thiết bị ra đảo — đây là '
     'các hướng phát triển tiếp theo.'),

    ('Nếu gió thấp hơn dự kiến thì sao?',
     'Tháng 4–5 là thời kỳ gió yếu nhất (5,70 và 4,97 m/s ở 78 m) nhưng cũng là tháng bức xạ cao nhất '
     '(6,65 và 5,59 kWh/m²/ngày), nên sản lượng PV bù được phần thiếu hụt gió. Đây chính là cơ sở để '
     'chọn cấu hình lai thay vì chỉ dùng một nguồn; phần điện dư của gió trong các tháng còn lại đủ bù '
     'cho các tháng thấp điểm.'),

    ('Báo cáo đã sửa theo những góp ý nào?',
     'Em đã sửa đủ 10 nội dung góp ý trong file nhận xét: tên ngành và khóa trên bìa; tách dòng tiêu đề '
     'đề tài; viết lại Lý do chọn đề tài; bỏ hai mục không phải mục tiêu; bổ sung chỉ tiêu kỹ thuật và '
     'môi trường ở Chương 2; thống nhất kích thước hình và xử lý các trang trống; canh giữa Bảng 3.8; '
     'crop lại Hình 3.7 chỉ lấy đồ thị; và thêm mục 3.15 thảo luận kết quả với số liệu cụ thể.'),
]

for i, (q, a) in enumerate(QA, 1):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run('Câu %d. %s' % (i, q))
    r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True
    P(a)

# ---------- Phan 3 ----------
H('3. Ba điểm nên chủ động nêu trước khi Thầy hỏi', 2)
B([
    'Thứ nhất, về bộ biến tần: em đã phát hiện và ghi rõ nguyên nhân thiếu 18 % điện năng là do converter '
    '100 kW trong phương án tối ưu, và đề xuất chạy lại với 2.000 kW theo sơ đồ — đây là việc em xin '
    'phép làm sau buổi gặp và xin ý kiến Thầy về thời gian hoàn thành.',
    'Thứ hai, về chênh lệch giữa tính tay và mô phỏng: em giữ cả hai bộ số và giải thích nguyên nhân '
    'lệch thay vì chỉnh cho khớp, để người đọc thấy rõ bản chất của từng phương pháp.',
    'Thứ ba, về dữ liệu: em không tự đặt số liệu, mọi số liệu khí tượng đều lấy từ NASA POWER và mọi số '
    'liệu mô phỏng đều trích xuất từ khối kết quả của chính HOMER Pro trong tệp .homer, không phải số '
    'tính lại bằng tay.',
])

H('4. Kế hoạch sau buổi gặp', 2)
B([
    'Chạy lại HOMER Pro với converter 2.000 kW, ghi nhận lượng điện thiếu và thời gian cấp điện liên tục.',
    'Bổ sung bảng/biểu đồ sản lượng theo tháng và trạng thái sạc pin nếu Thầy yêu cầu (cần xuất từ phần '
    'mềm vì tệp mô phỏng hiện tại chỉ lưu kết quả tổng hợp năm).',
    'Hoàn thiện phần phân tích vòng đời và chi phí lắp đặt thực tế nếu Thầy định hướng mở rộng đề tài.',
])

doc.save(OUT)
print('saved', OUT)
