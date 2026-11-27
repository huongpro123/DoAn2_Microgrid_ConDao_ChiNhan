# Tóm tắt kết quả tối ưu & Checklist bảo vệ — Đề tài ST – Giai đoạn 3 (Côn Đảo)

- **Sinh viên thực hiện:** Đào Chí Nhân
- **GVHD:** TS. Trần Hữu Tính (ĐH Kỹ thuật – Công nghệ Cần Thơ)
- **Phần mềm mô phỏng:** HOMER Pro x64 v3.18.5 (`03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`)

---

## 1. Cấu hình chọn đạt chuẩn kỹ thuật (`0,00 % thiếu · ≤ 10 % dư`)
Trong `454` tổ hợp khảo sát (`450` khả thi), **`288` cấu hình** đạt đồng thời `Unmet load = 0,00 %` và `Excess electricity ≤ 10 %`. Cấu hình dẫn đầu theo chi phí vòng đời (chiến lược điều độ **Load Following**):

- **Nguồn & thiết bị:** `1.200 kWp PV` + `1 × 500 kW Windflow 45` (cao trình trục `47 m`) + `60 khối BESS Li-ion 100 kWh` (`6.000 kWh`) + `970 kW Autosize Diesel` + `800 kW Converter`.
- **Chỉ tiêu kỹ thuật:** `Unmet = 0,00 %` (`0 kWh/năm`) · `Excess = 6,15 %` (`260.422 kWh/năm ≤ 10 %`) · `RF = 78,9 %` · BESS tự chủ `11,14 giờ`, luân chuyển `961.779 kWh/năm`.
- **Chỉ tiêu kinh tế:** `CAPEX = 5.946.500 USD` · `NPC = 11.544.581 USD` · `LCOE = 0,2367 USD/kWh` · `IRR = 18,9 %` · `ROI = 15,0 %` · hoàn vốn giản đơn `5,02 năm`.
- **Chỉ tiêu môi trường:** tiêu thụ dầu giảm `78,5 %` (`1.054.193 → 226.143 L/năm`), phát thải `CO₂` giảm từ `2.759,5 → 592,0 tấn/năm` (**tránh `2.167,5 tấn CO₂/năm`**).

---

## 2. Đối chiếu 3 trụ cột (HOMER Pro v3.18.5)

| Trụ cột | Chỉ tiêu | Base Case Diesel | Cấu hình ban đầu | Cấu hình chọn sau tối ưu |
|---|---|---:|---:|---:|
| **Kỹ thuật** | Thiếu tải / Đáp ứng | 0,00 % / 100 % | 18,0 % / 82,0 % | **0,00 % / 100,0 %** |
| | Điện dư cắt giảm | 0,00 % | 58,4 % | **6,15 %** (`≤ 10 %`) |
| | Tỷ lệ tái tạo (RF) | 0,0 % | 100 % | **78,9 %** |
| **Kinh tế** | CAPEX (USD) | $1.185.000 | $7.078.680 | **$5.946.500** (`-16,0 %` so bản đầu) |
| | NPC (USD) | $19.462.122 | $9.402.682 *(thiếu tải)* | **$11.544.581** (`-40,7 %` so Base Case) |
| | LCOE (USD/kWh) | $0,3990 | $0,2351 | **$0,2367** (`-40,7 %` so Base Case) |
| **Môi trường** | Nhiên liệu (L/năm) | 1.054.193 | 0 | **226.143** (`-78,5 %` so Base Case) |
| | Phát thải CO₂ (tấn/năm) | 2.759,5 | 0 *(cắt 4,43 GWh)* | **592,0** *(tránh 2.167,5 tấn/năm)* |

*(Lưu ý khi hội đồng hỏi: phương án NPC nhỏ nhất toàn cục trên ảnh bảng kết quả dùng `2 × 500 kW` gió đạt `$10,75M / $0,2204/kWh` nhưng dư điện tới `26,14 % > 10 %`, nên báo cáo chọn phương án `1 × 500 kW` gió đạt chuẩn `6,15 % ≤ 10 %`.)*

---

## 3. Checklist đã xử lý đủ 6 góp ý của TS. Trần Hữu Tính
1. **Chương 1:** Chỉ giữ tổng quan cấu hình Off-grid (`1.1–1.3`, `Bảng 1.1`); chuyển toàn bộ địa lý/Côn Đảo/sơ đồ nguyên lý sang đầu Chương 3 (`3.1`).
2. **Chương 2:** Rút gọn 13 mục thành **3 mục (`2.1`, `2.2`, `2.3`)**, đưa toàn bộ công thức lên đánh số `(2.1)–(2.24)`.
3. **Chương 3:** Bổ sung số liệu & ảnh chạy thật HOMER Pro v3.18.5 (`Bảng 3.20–3.21`, `Hình 3.13–3.14`), kéo bảng tổng hợp giải tích lên `Bảng 3.17`, đánh giá đủ **Kỹ thuật – Kinh tế – Môi trường**.
4. **Kết luận:** Viết khớp 100 % Chương 1–3, bỏ số liệu cũ mâu thuẫn.
5. **TLTK & Bỏ Phụ lục A/B:** Đã xóa Phụ lục A/B thừa, thêm ngày truy cập `24/11/2026` cho `[1]`, `[3]`, `[5]`, `[11]`.
6. **Hình thức & Văn phong:** Times New Roman, căn đều `Justify`, mục lục `TOC` + danh mục `PAGEREF` tự động, đánh số trang thật (`50` trang), không lộ tên tệp nội bộ (`100/100` cả 2 bộ kiểm tra).
