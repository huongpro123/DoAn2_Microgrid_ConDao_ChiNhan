# Tóm tắt kết quả tối ưu & Checklist bảo vệ — Đề tài ST – Giai đoạn 3 (Côn Đảo)

- **Sinh viên thực hiện:** Đào Chí Nhân
- **GVHD:** TS. Trần Hữu Tính (ĐH Kỹ thuật – Công nghệ Cần Thơ)
- **Phần mềm mô phỏng:** HOMER Pro x64 v3.18.5 (`03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`)

---

## 1. Cấu hình chọn đạt chuẩn kỹ thuật (`0,00 % thiếu · ≤ 10 % dư`)
Với đồ thị phụ tải giờ thực tế phù hợp tổng công suất đặt **`783,1 kW`** (`230–640 kW`, nhiễu `3 % / 5 %`, đỉnh thực tế **`748,17 kW`**, trung bình **`10.337 kWh/ngày`**, hệ số tải **`0,58`**), trong `634` tổ hợp khảo sát (`630` khả thi), **`348` cấu hình** đạt đồng thời `Unmet load = 0,00 %` và `Excess electricity ≤ 10 %`. Cấu hình dẫn đầu theo chi phí vòng đời (chiến lược điều độ **Load Following**):

- **Nguồn & thiết bị:** `1.400 kWp PV` + `1 × 500 kW Windflow 45` (cao trình trục `47 m`) + `60 khối BESS Li-ion 100 kWh` (`6.000 kWh`) + `750 kW Autosize Diesel` + `800 kW Converter`.
- **Chỉ tiêu kỹ thuật:** `Unmet = 0,00 %` (`0 kWh/năm`) · `Excess = 9,30 %` (`407.745 kWh/năm ≤ 10 %`) · `RF = 83,5 %` · BESS tự chủ `11,14 giờ`, luân chuyển `977.229 kWh/năm`.
- **Chỉ tiêu kinh tế:** `CAPEX = 6.316.500 USD` (`-10,8 %` so bản đầu) · `NPC = 10.763.995 USD` (`-41,4 %` so Base Case) · `LCOE = 0,2207 USD/kWh` (`-41,4 %`) · `IRR = 19,6 %` · `ROI = 15,8 %` · hoàn vốn giản đơn `5,02 năm` (chiết khấu `5,84 năm`).
- **Chỉ tiêu môi trường:** tiêu thụ dầu giảm `82,7 %` (`1.013.464 → 174.855 L/năm`, tiết kiệm `838.609 L/năm`), phát thải `CO₂` giảm từ `2.652,9 → 457,7 tấn/năm` (**tránh `2.195,2 tấn CO₂/năm`**).

---

## 2. Đối chiếu 3 trụ cột (HOMER Pro v3.18.5)

| Trụ cột | Chỉ tiêu | Base Case Diesel | Cấu hình ban đầu | Cấu hình chọn sau tối ưu |
|---|---|---:|---:|---:|
| **Kỹ thuật** | Thiếu tải / Đáp ứng | 0,00 % / 100 % | 18,0 % / 82,0 % | **0,00 % / 100,0 %** |
| | Điện dư cắt giảm | 0,00 % | 58,4 % | **9,30 %** (`≤ 10 %`) |
| | Tỷ lệ tái tạo (RF) | 0,0 % | 100 % | **83,5 %** |
| **Kinh tế** | CAPEX (USD) | $1.535.000 | $7.078.680 | **$6.316.500** (`-10,8 %` so bản đầu) |
| | NPC (USD) | $18.356.222 | $9.402.682 *(thiếu tải)* | **$10.763.995** (`-41,4 %` so Base Case) |
| | LCOE (USD/kWh) | $0,3763 | $0,2351 | **$0,2207** (`-41,4 %` so Base Case) |
| **Môi trường** | Nhiên liệu (L/năm) | 1.013.464 | 0 | **174.855** (`-82,7 %` so Base Case) |
| | Phát thải CO₂ (tấn/năm) | 2.652,9 | 0 *(cắt 4,43 GWh)* | **457,7** *(tránh 2.195,2 tấn/năm)* |

*(Lưu ý khi hội đồng hỏi: phương án NPC nhỏ nhất toàn cục trên bảng kết quả dùng `1.200 kWp PV + 2 × 500 kW` gió đạt `$10,40M / $0,2133/kWh` nhưng dư điện tới `26,12 % > 10 %`, nên báo cáo chọn phương án `1.400 kWp PV + 1 × 500 kW` gió đạt chuẩn `9,30 % ≤ 10 %`.)*
