# Chuẩn form viết báo cáo (theo mẫu của Trường/Khoa)

Nguồn chuẩn: `form_chuan/Mau_Huong_Dan_Viet_De_Cuong.docx` (mẫu hướng dẫn viết đề cương của
Trường Đại học Kỹ thuật – Công nghệ Cần Thơ, Khoa Điện – Điện tử). Logo dùng lại: `form_chuan/ctut_image1.png`.

Mọi báo cáo về sau phải bám đúng các mục dưới đây. Script `build_bao_cao.py` đã được cấu hình theo chuẩn này.

## 1. Trang và canh lề

| Thuộc tính | Giá trị |
|---|---|
| Khổ giấy | A4 (21,0 × 29,7 cm) |
| Lề trái | 3,0 cm |
| Lề phải | 2,0 cm |
| Lề trên | 2,5 cm |
| Lề dưới | 2,5 cm |

## 2. Phông chữ và đoạn văn

- Phông: **Times New Roman**, cỡ **13 pt** cho toàn bộ nội dung.
- Giãn dòng: **1,5 lines**; giãn đoạn sau 4 pt.
- Canh đều hai bên (Justify).
- **Thụt đầu dòng 1,25 cm** cho mọi đoạn thân bài.
- Tiêu đề chương: in đậm, canh giữa, 16 pt.
- Tiêu đề mục (Heading 2): in đậm, canh trái, 14 pt.
- Tiêu đề mục nhỏ (Heading 3): in đậm, 13 pt.
- Chú thích hình/bảng: 12 pt, in nghiêng, canh giữa, đặt **trên bảng** và **dưới hình**.

## 3. Thứ tự các phần đầu báo cáo

1. Bìa ngoài (có logo): TRƯỜNG – KHOA – ❖ – logo – ĐỒ ÁN – Ngành – TÊN ĐỀ TÀI – HỌ VÀ TÊN SINH VIÊN – Cần Thơ, năm …
2. Bìa trong (có logo): như bìa ngoài, phần cuối là bảng 2 cột *Giảng viên hướng dẫn* / *Sinh viên thực hiện*.
3. LỜI CAM ĐOAN
4. LỜI CẢM ƠN
5. MỤC LỤC
6. MỞ ĐẦU (1. Lý do chọn đề tài; 2. Mục tiêu nghiên cứu; 3. Đối tượng và phạm vi; 4. Phương pháp nghiên cứu)
7. Các chương nội dung, TÀI LIỆU THAM KHẢO, PHỤ LỤC.

Hai trang bìa **không đánh số trang**; số trang bắt đầu hiển thị từ phần nội dung nhưng vẫn đếm liên tục.

**Khung viền bìa:** cả hai trang bìa đều có khung viền bao quanh trang (`w:pgBorders`, `display="firstPage"`).
Mẫu gốc dùng kiểu trang trí `twistedLines1` — kiểu này chỉ hiển thị trong Microsoft Word, còn khi xuất PDF
bằng LibreOffice sẽ **mất khung**. Vì vậy báo cáo dùng khung `double` cỡ 18 (dày 2,25 pt), khoảng cách 3 pt,
hiển thị đúng ở cả Word và PDF. Muốn đổi lại đúng kiểu trang trí của mẫu thì sửa `w:val` trong hàm
`add_page_border()` của `build_bao_cao.py` thành `twistedLines1` (nhưng PDF sẽ mất khung).

## 4. Đánh số mục

- Cấp 1: `1.`, `2.`, `3.` … hoặc `CHƯƠNG 1:`, `CHƯƠNG 2:` …
- Cấp 2: `1.1.`, `1.2.`, `2.1.` …
- Cấp 3: `2.1.1.`, `2.1.2.` … (chỉ dùng khi thật cần chia nhỏ)

## 5. Quy tắc bắt buộc khi tách mục

> **Không tách một mục nhỏ ra nếu bên trong nó không có ít nhất 2 đoạn văn.**

Tức là mỗi mục cấp 2 (và cấp 3 nếu có) phải có **từ 2 đoạn văn trở lên**; không được để mục chỉ có
1 đoạn văn duy nhất rồi nhảy sang mục khác. Nếu nội dung chưa đủ 2 đoạn thì phải viết thêm phần
phân tích/nhận xét, hoặc gộp nội dung đó vào mục phía trên.

Kiểm tra tự động: `python form_chuan\check_form.py Bao_cao_ST_Giai_doan_3.docx`
( script liệt kê các mục cấp 2 đang có dưới 2 đoạn văn ).

## 6. Bảng, hình, công thức

- Bảng: kiểu Table Grid, cỡ chữ 12 pt, dòng tiêu đề in đậm và **lặp lại khi bảng sang trang**,
  không cho tách dòng giữa hai trang (`cantSplit`), chú thích bảng đặt phía trên.
- Hình: canh giữa, chú thích in nghiêng đặt phía dưới, đánh số theo chương (`Hình 1.1`, `Hình 5.2` …).
- Công thức: canh giữa, ký hiệu viết dạng chỉ số dưới/chỉ số trên (`P_{PV}`, `h⁻¹`), không viết `P_PV` thô.

## 7. Mục lục

Mục lục tĩnh 2 cấp, có dấu chấm dẫn và số trang thật (không phụ thuộc field của Word, không cần nhấn F9).
Số trang mục lục được lấy tự động sau khi xuất PDF: chạy script build 2 lần rồi lấy số trang từ PDF
(xem `build_bao_cao.py`, phần `toc_pages.json`).
