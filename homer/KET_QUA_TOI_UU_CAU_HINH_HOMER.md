# Kết quả phân tích & tối ưu cấu hình Microgrid Côn Đảo (đáp ứng 0 % thiếu · ≤ 10 % dư)

> **CẬP NHẬT XÁC THỰC TRỰC TIẾP TRÊN HOMER PRO x64 v3.18.5 (`ST_Giai_doan_3_toi_uu.homer` → `homer_toi_uu_results.json`):**
> - **Tổng số tổ hợp đã chạy trên phần mềm:** `454` cấu hình (`450` khả thi, **`288` cấu hình đạt đồng thời `0,00 %` thiếu tải & `≤ 10 %` điện dư**).
> - **Cấu hình chọn dẫn đầu đạt chuẩn GVHD (Load Following):** **`1.200 kWp PV + 1 × 500 kW Windflow 45 + 60 khối BESS (6.000 kWh) + 970 kW Autosize Genset + 800 kW Converter`**
>   - **Kỹ thuật:** `Unmet = 0,00 %` (`0 kWh`), `Excess = 6,15 %` (`260.422 kWh/năm ≤ 10 %`), `RF = 78,9 %`.
>   - **Kinh tế (so với Base Case Diesel `970 kW + 20 BESS` có `NPC $19.462.122`, `LCOE $0,3990/kWh`):** `CAPEX = $5.946.500` (giảm `16,0 %` so bản `.homer` gốc `$7,08M`), `NPC = $11.544.581` (giảm `40,7 %`), `LCOE = $0,2367/kWh` (giảm `40,7 %`), `IRR = 18,9 %`, `ROI = 15,0 %`, hoàn vốn `5,02 năm`.
>   - **Môi trường:** `Fuel = 226.143 L/năm` (giảm `78,5 %` so `1.054.193 L/năm` của Base Case), `CO₂ = 592,0 tấn/năm` (tránh được **`2.167,5 tấn CO₂/năm`**).
> - **Lưu ý đối chiếu:** Phần mềm tìm được phương án NPC nhỏ nhất toàn cục (`2 × 500 kW` gió, `NPC $10.752.556`, `LCOE $0,2204/kWh`), nhưng bị dư điện tới `26,14 % > 10 %`, do đó báo cáo chọn cấu hình `1 × 500 kW` gió đạt chuẩn `6,15 % ≤ 10 %`.

---

## Ghi chú kết quả khảo sát sơ bộ trước khi chạy HOMER Pro (`phan_tich_toi_uu_homer.py`)
> Bảng gốc lấy trực tiếp từ `homer_results.json` (`05_File_Mo_Phong_HOMER_Pro.homer`);
> các kịch bản A/B/C dưới đây là bước khảo sát **8.760 giờ hiệu chuẩn trong Python** dùng để tìm vùng dải tìm kiếm đưa vào `ST_Giai_doan_3_toi_uu.homer`.

## 1. Vì sao cấu hình gốc trong `.homer` không đạt tiêu chí GVHD?
- Công suất đỉnh chuỗi tải 8.760 giờ hiệu chuẩn: **`776.0 kW`**, tổng phụ tải năm: **`3,773,005 kWh/năm`**.
- **Lỗi 1 — Nghẽn Converter `100 kW`:** Tải đỉnh `783,1 kW` nhưng bộ biến đổi DC–AC khai báo chỉ `100 kW` → thiếu **`679,837 kWh/năm` (`18,0 %`)**.
- **Lỗi 2 — Thừa công suất gió `2.000 kW`:** Riêng 1 tuabin E-82 tạo `7,237,202 kWh/năm` (gần gấp đôi nhu cầu) → dư **`4,426,778 kWh/năm` (`58,4 %` > `10 %`)**.

## 2. Kịch bản A — Nếu chỉ nâng Converter lên `1.000–2.000 kW` (giữ nguyên `1 × E-82 2.000 kW`)
| Converter (kW) | Thiếu tải (%) | Dư điện (%) | NPC (USD) | COE (USD/kWh) | Đạt tiêu chí GVHD? |
|---:|---:|---:|---:|---:|---|
| 100 | 7.62 | 53.58 | 9,041,856 | 0.2007 | KHÔNG (còn dư > 10%) |
| 500 | 5.55 | 52.32 | 9,212,769 | 0.2000 | KHÔNG (còn dư > 10%) |
| 850 | 5.53 | 52.30 | 9,362,318 | 0.2032 | KHÔNG (còn dư > 10%) |
| 1000 | 5.53 | 52.30 | 9,426,410 | 0.2046 | KHÔNG (còn dư > 10%) |
| 2000 | 5.53 | 52.30 | 9,853,692 | 0.2138 | KHÔNG (còn dư > 10%) |

## 3. Kịch bản B — 100 % Tái tạo (Hạ cỡ gió + tăng lưu trữ/PV, Converter `1.000 kW`)
- Số phương án 100 % RE đạt đồng thời `Unmet ≤ 0,1 %` và `Excess ≤ 10 %`: **`0`** *(nếu = 0: hiển thị top phương án 100 % RE có tỷ lệ dư nhỏ nhất)*.
| PV (kWp) | Gió (kW) | BESS (khối 100 kWh) | Thiếu (%) | Dư (%) | CAPEX (USD) | NPC (USD) | COE (USD/kWh) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2000 | 800 | 350 | 0.00 | 35.05 | 14,688,400 | 18,249,556 | 0.3742 |
| 2000 | 800 | 250 | 0.00 | 35.14 | 12,388,400 | 15,155,965 | 0.3107 |
| 2000 | 800 | 180 | 0.00 | 35.20 | 10,778,400 | 12,990,451 | 0.2663 |
| 2000 | 1000 | 350 | 0.00 | 42.39 | 15,073,000 | 18,733,595 | 0.3841 |
| 2000 | 1000 | 250 | 0.00 | 42.47 | 12,773,000 | 15,640,003 | 0.3207 |

## 4. Kịch bản C — Hybrid Tái tạo + Diesel dự phòng nhỏ (tối ưu chi phí & đạt chuẩn `0 % thiếu · ≤ 10 % dư`)
| PV (kWp) | Gió (kW) | BESS (khối) | Diesel (kW) | RF (%) | Thiếu (%) | Dư (%) | CAPEX (USD) | NPC (USD) | COE (USD/kWh) | CO₂ giảm (tấn/năm) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000 | 500 | 40 | 650 | 79.2 | 0.00 | 7.77 | 4,906,500 | 9,506,231 | 0.1949 | 2,210.8 |
| 1000 | 500 | 40 | 800 | 79.2 | 0.00 | 7.77 | 4,981,500 | 9,797,428 | 0.2009 | 2,210.8 |
| 800 | 600 | 60 | 650 | 78.3 | 0.00 | 9.96 | 5,078,800 | 10,025,504 | 0.2055 | 2,186.7 |
| 1000 | 500 | 60 | 650 | 79.5 | 0.00 | 7.47 | 5,366,500 | 10,074,212 | 0.2066 | 2,218.2 |
| 800 | 600 | 60 | 800 | 78.3 | 0.00 | 9.96 | 5,153,800 | 10,327,334 | 0.2117 | 2,186.7 |
| 1000 | 500 | 60 | 800 | 79.5 | 0.00 | 7.47 | 5,441,500 | 10,362,093 | 0.2124 | 2,218.2 |
| 800 | 600 | 80 | 650 | 78.4 | 0.00 | 9.90 | 5,538,800 | 10,636,734 | 0.2181 | 2,187.8 |
| 1000 | 500 | 80 | 650 | 79.5 | 0.00 | 7.39 | 5,826,500 | 10,684,120 | 0.2191 | 2,219.5 |

## 5. Hướng dẫn 5 bước bấm chạy lại trên HOMER Pro (trước Thứ Tư)
1. Mở `HO_SO_BAO_CAO_CHIEU_NAY\05_File_Mo_Phong_HOMER_Pro.homer` trên máy có bản quyền HOMER Pro còn hạn.
2. Vào mục **System Converter** → nâng giới hạn `Capacity` lên `0, 800, 1000, 1200, 2000` kW (thay vì cố định `100 kW`).
3. Đổi **Wind Turbine** từ `1 × 2.000 kW` sang dải tìm kiếm công suất nhỏ hơn (`600–1.000 kW`, hoặc bổ sung tổ máy nhỏ + **Generic PV** `400–1.200 kWp` + **Storage** `40–150` khối); nếu dùng phương án Hybrid C thì bật thêm **Generator Diesel** `400–800 kW` cho ngày lặng gió tháng 4–5.
4. Đặt **Constraints → Max annual capacity shortage = `0 %`**, bấm **Calculate** → lọc bảng **Optimization Results** lấy dòng đầu tiên có **Excess Electricity ≤ `10 %`** và **Unmet Electric Load = `0 %`**.
5. Chụp lại **Optimization Table**, **Electrical Summary** và **Cash Flow Summary** + lưu đè file `.homer` mới.
