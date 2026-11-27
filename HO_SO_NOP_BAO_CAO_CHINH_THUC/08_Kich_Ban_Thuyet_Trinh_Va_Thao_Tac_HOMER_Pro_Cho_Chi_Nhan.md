# KỊCH BẢN THUYẾT TRÌNH 16 SLIDE & HƯỚNG DẪN THAO TÁC HOMER PRO TỪ A–Z

- **Sinh viên thực hiện:** Đào Chí Nhân — Ngành Công nghệ Kỹ thuật Năng lượng (Khóa 2023), Trường ĐH Kỹ thuật – Công nghệ Cần Thơ
- **Giảng viên hướng dẫn:** TS. Trần Hữu Tính (Khoa Điện – Điện tử)
- **Đề tài:** Mô phỏng hệ thống Microgrid đảo ST – Giai đoạn 3 (Khu vực biển Đông, gần Côn Đảo) trên phần mềm HOMER Pro
- **Mốc kết quả mô phỏng (`HOMER Pro x64 v3.18.5`):** Toàn bộ số liệu được trích nguyên văn từ file `03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer` (`634` tổ hợp → `630` khả thi → `348` cấu hình đạt chuẩn `0,00 %` thiếu tải & `≤ 10 %` điện dư; đồ thị phụ tải giờ `230–640 kW`, đỉnh `748,17 kW ≤ 783,1 kW`, trung bình `10.337 kWh/ngày`, `k_tải = 0,58`).

---

# PHẦN 1: CHECKLIST CHUẨN BỊ TRƯỚC GIỜ BẢO VỆ 30 PHÚT

1. **Slide trình chiếu chính:** Mở `07_Slide_Thuyet_Trinh_15_Trang_ST_Giai_Doan_3.pptx` (gồm **16 slide**, có Slide Bìa CTUT & Slide 16 Chào Cảm ơn riêng). Bấm **`F5`** (hoặc **`Alt + F5`** Presenter View), lướt nhanh **Slide 01, 09, 10, 14, 16**.
2. **Phần mềm mô phỏng thật:** Mở sẵn **`03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`** bằng **`HOMER Pro x64 v3.18.5`** (kết quả đã chạy và lưu sẵn bên trong).
3. **Bộ ảnh & PDF dự phòng:** Mở sẵn `05_Hinh_Anh_Ket_Qua_HOMER_Pro\` (`homer_load_783kW.png`, `homer_opt_table.png`, `homer_opt_summary.png`, `st_diagram.png`) và `02_Bao_Cao_Thuyet_Minh_ST_Giai_Doan_3.pdf`.
4. **Nhịp trình bày:** Tổng thời lượng **10–12 phút** (~40–50 giây/slide), mắt nhìn Hội đồng khi mở và kết ý, chỉ chuột trực tiếp vào con số cần nhấn mạnh.

---

# PHẦN 2: KỊCH BẢN LỜI THOẠI CHI TIẾT 16 SLIDE (10–12 PHÚT)

### Slide 01 – Trang bìa CTUT + 4 KPI chốt (40 giây)
- **Chỉ chuột:** Lần lượt 4 thẻ KPI: `0,00 %` → `9,30 %` → `$0,2207/kWh` → `-2.195,2 t/năm`.
- **Lời nói:** "Kính thưa Quý Thầy/Cô Hội đồng Khoa Điện – Điện tử. Em tên là **Đào Chí Nhân**, sinh viên ngành Công nghệ Kỹ thuật Năng lượng K2023. Em xin trình bày Đồ án 2: **Mô phỏng hệ thống Microgrid đảo ST – Giai đoạn 3 (Côn Đảo) trên HOMER Pro**, dưới sự hướng dẫn của **TS. Trần Hữu Tính**. Bốn kết quả trọng tâm đạt được gồm: **0,00 % thiếu tải**, **9,30 % điện dư** (dưới ngưỡng 10 %), giá điện **LCOE $0,2207/kWh**, và cắt giảm **2.195,2 tấn CO₂/năm**."

### Slide 02 – Bối cảnh & Bài toán cấp điện đảo ST (45 giây)
- **Chỉ chuột:** Bản đồ Côn Đảo → thông số tải `3.773.005 kWh/năm`, công suất đặt `783,1 kW` (`Peak 748,17 kW`).
- **Lời nói:** "Đảo ST chưa nối lưới quốc gia, tổng công suất phụ tải đặt là **783,1 kW**, điện năng tiêu thụ **3.773.005 kWh/năm** (**10.337 kWh/ngày**, đỉnh thực tế **748,17 kW**). Nếu chạy thuần Diesel (Base Case) sẽ tiêu tốn hơn **1,01 triệu lít dầu/năm** với giá điện **$0,3763/kWh**. Bài toán đặt hai ràng buộc cứng: **0,00 % thiếu tải** và **≤ 10 % điện dư**."

### Slide 03 – Chương 1: So sánh 3 kiến trúc lưới điện độc lập (45 giây)
- **Lời nói:** "Chương 1 đối chiếu ba kiến trúc: thuần Diesel (vốn thấp $1,54M nhưng NPC tới **$18,36M**, phát thải **2.652,9 tấn CO₂/năm**); 100 % năng lượng tái tạo (vướng mùa lặng gió nên điện dư lên tới 35,1–58,4 %); và cấu hình **Hybrid chọn** kết hợp PV – Gió – BESS – Diesel đạt **83,5 % tái tạo**, giữ điện dư **9,30 %** và giảm **41,4 %** NPC/LCOE."

### Slide 04 – Đặc trưng mùa gió Côn Đảo (40 giây)
- **Lời nói:** "Gió Côn Đảo phân hóa hai mùa rõ rệt: tháng 12–2 gió Đông Bắc mạnh **10,8–11,0 m/s**, nhưng tháng 4–5 lặng gió chỉ còn khoảng **4,97 m/s**. Do đó không thể lắp tuabin quá lớn mà cần chọn **1 × 500 kW**, phối hợp **1.400 kWp PV**, **6.000 kWh BESS** và **Diesel 750 kW** bổ trợ cho mùa lặng gió."

### Slide 05 – Sơ đồ nguyên lý 34-ST & Chiến lược điều độ (45 giây)
- **Lời nói:** "Trên sơ đồ nguyên lý 34-ST: **AC Bus** nối phụ tải đảo (783,1 kW), tuabin gió 500 kW và Diesel 750 kW; **DC Bus** nối giàn pin **1.400 kWp PV** và **60 khối BESS (6.000 kWh)** qua bộ **Converter 800 kW**. Hệ thống vận hành theo chiến lược **Load Following**: Diesel chỉ phát phần thiếu tải, nhường sạc BESS cho PV và Gió."

### Slide 06 – Chương 2: Mô hình toán học `(2.1)–(2.24)` (35 giây)
- **Lời nói:** "Chương 2 hệ thống hóa 24 công thức `(2.1)–(2.24)` thành 3 nhóm: mô hình nguồn phát PV/Gió/Diesel; cân bằng năng lượng theo **8.760 giờ/năm** cùng trạng thái sạc BESS; và công thức kinh tế **NPC, LCOE, IRR, hoàn vốn** kèm phát thải khí nhà kính."

### Slide 07 – Chẩn đoán 2 nút thắt cấu hình ban đầu (50 giây)
- **Lời nói:** "Cấu hình ban đầu vừa **thiếu tải 18,0 %** do **Converter chỉ 100 kW** (quá nhỏ so với đỉnh tải `748,17 kW`), vừa **dư điện tới 58,4 % (4,43 GWh/năm)** do lắp 1 tuabin E-82 2.000 kW quá cỡ. Ngoài ra, cấu hình NPC thấp nhất toàn cục (`2 × 500 kW` gió, NPC $10,40M) lại dư tới **26,12 % > 10 %** nên vẫn bị loại."

### Slide 08 – Không gian tìm kiếm HOMER Pro v3.18.5 (40 giây)
- **Lời nói:** "Em nhập lại phụ tải giờ thực tế `230–640 kW` (nhiễu `3 % / 5 %`, đỉnh `748,17 kW ≤ 783,1 kW`), mở dải PV `0–1.600 kWp`, gió `0–2 × 500 kW`, BESS `20–117 khối`, Converter `0–1.200 kW` và Diesel tự chọn cỡ `750 kW` với ràng buộc `0 % thiếu tải`. Phần mềm quét **634 tổ hợp**, cho **630 khả thi** và lọc được **348 cấu hình** đạt chuẩn."

### Slide 09 – Bằng chứng HOMER Pro: Bảng tối ưu (55 giây)
- **Lời nói:** "Trên bảng `Optimization Results`, dòng #1 toàn cục dùng `2 × 500 kW` gió có NPC $10,40M và LCOE $0,2133/kWh nhưng dư tới **26,12 %**. Vì vậy em chọn phương án dẫn đầu trong nhóm đạt chuẩn: **1.400 kWp PV + 1 × 500 kW gió** — LCOE chỉ nhỉnh **$0,0074/kWh (+3,5 %)** nhưng giảm được **$481.500 CAPEX** và giảm **70,8 % lượng điện dư** xuống chỉ còn **9,30 %**."

### Slide 10 – Bằng chứng HOMER Pro: Chi tiết cấu hình chọn (45 giây)
- **Lời nói:** "Cấu hình tối ưu chọn phát tổng **4.383.818 kWh/năm**, phục vụ trọn **3.773.005 kWh/năm** (`0 kWh` thiếu). Hệ BESS 6.000 kWh tự chủ **11,14 giờ** và luân chuyển **977.229 kWh/năm**. Diesel 750 kW chỉ chạy **2.201 giờ/năm**, giảm **59,2 %** so với **5.400 giờ/năm** ở Base Case; đạt **IRR 19,6 %**, **ROI 15,8 %**, hoàn vốn **5,02 năm**."

### Slide 11 – Trụ cột 1: Kỹ thuật & Cơ cấu sản lượng (45 giây)
- **Lời nói:** "Trong tổng phát **4,38 GWh/năm**: PV đóng góp **2,26 GWh (51,6 %)**, Gió **1,50 GWh (34,2 %)**, Diesel dự phòng chỉ **0,62 GWh (14,2 %)**. Tỷ lệ tái tạo đạt **83,5 %**, đáp ứng **100 % tải**, điện dư **407.745 kWh (9,30 % ≤ 10 %)**."

### Slide 12 – Trụ cột 2: Kinh tế vòng đời 25 năm (45 giây)
- **Lời nói:** "CAPEX cấu hình chọn là **$6,32 triệu** (giảm **10,8 %** so với $7,08M bản ban đầu), chi phí vận hành giảm từ $1,30M xuống **$0,34M/năm**. Tổng **NPC giảm 41,4 %** (từ $18,36M xuống **$10,76M**), **LCOE giảm 41,4 %** (từ $0,3763 xuống **$0,2207/kWh**), Present Worth đạt **+$7,48 triệu**."

### Slide 13 – Trụ cột 3: Nhiên liệu & Môi trường (40 giây)
- **Lời nói:** "Tiêu thụ dầu giảm **82,7 %** từ **1.013.464 L** xuống còn **174.855 L/năm**, tiết kiệm **838.609 lít dầu/năm**. Phát thải CO₂ giảm từ **2.652,9** xuống **457,7 tấn/năm** — **tránh 2.195,2 tấn CO₂/năm** (hơn 54.880 tấn trong 25 năm) và giảm 82,7 % NOx, SO₂."

### Slide 14 – Tổng hợp đối chiếu 3 trụ cột (40 giây)
- **Lời nói:** "Bảng tổng hợp đối chiếu trực diện 3 phương án xác nhận cấu hình chọn thỏa mãn cả ba trụ cột kỹ thuật – kinh tế – môi trường, đồng thời hoàn tất chỉnh sửa đồ thị phụ tải `783,1 kW` (`Peak 748,17 kW`) theo góp ý mới nhất của Thầy hướng dẫn."

### Slide 15 – Kết luận, Kiến nghị & Trọng tâm Q&A (35 giây)
- **Lời nói:** "Tóm lại, cấu hình **1.400 kWp PV + 500 kW Gió + 6.000 kWh BESS + 750 kW Diesel + 800 kW Converter** là phương án tối ưu nhất cho đảo ST. Hướng mở rộng tiếp theo là phân tích độ nhạy giá dầu/pin, mô phỏng quá độ lưới điện và tận dụng nốt 9,30 % điện dư cho trạm khử mặn/sạc xe."

### Slide 16 – Slide Chào & Cảm ơn Hội đồng (10 giây + giữ suốt phần Q&A)
- **Lời nói:** "Phần trình bày của em đến đây là kết thúc. Em xin trân trọng cảm ơn Quý Thầy/Cô Hội đồng đã lắng nghe, rất mong nhận được câu hỏi và góp ý của Quý Thầy/Cô ạ!"

---

# PHẦN 3: HƯỚNG DẪN THAO TÁC TỪNG CÚ CLICK TRONG HOMER PRO x64 v3.18.5

1. **Mở file:** `File → Open → 03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`.
2. **Xem phụ tải giờ thực tế (khi Thầy kiểm tra):** Bấm `Design → Electric Load` (`Electric #1`) → chỉ bảng `January Profile` (`245, 235, 230... 640 kW`), ô `Daily Noise = 3 %`, `Time Step = 5 %`, bảng `Metric` ghi rõ **`Average = 10,337 kWh/day`**, **`Peak = 748.17 kW`** (`≤ 783,1 kW`), **`Load factor = .58`**.
3. **Xem Schematic & Ràng buộc:** Bấm `Design → Schematic` chỉ 6 khối; bấm `Project → Constraints` chỉ `Maximum annual capacity shortage = 0 %`; click `PV → Search Space` thấy dải `0–1.600 kWp`.
4. **Xem kết quả:** Bấm thẻ `Results` *(không cần bấm `Calculate` trừ khi Thầy bảo chạy lại; nếu chạy lại đợi ~15 giây)*. Bấm **`Overall`** ở góc phải bảng `Optimization Results` để chỉ rõ dòng #1 (`1.200 PV + 2×500 WF45`, NPC `$10.4M`, Excess `26.12%`) và dòng chọn (`1.400 PV + 1×500 WF45 + 60 BESS + 750 Gen + 800 Conv, LF`, NPC `$10.8M`, COE `$0.221`, RF `83.5%`, Excess `9.30%`, Unmet `0%`).
5. **Nháy đúp (`double-click`)** vào dòng chọn để mở cửa sổ `Simulation Results` với 5 tab: `Cost Summary` ($6.316.500 / $10.763.995), `Electrical` (PV 51,6 % · Wind 34,2 % · Diesel 14,2 % · Excess 9,30 % · Unmet 0,00 %), `Compare Economics` (IRR 19,6 % · ROI 15,8 % · Payback 5,02 yr), `Emissions` (CO₂ 457,7 t/năm), `Time Series Plot` (vận hành 8.760 giờ).

---

# PHẦN 4: BỘ 6 CÂU HỎI TỦ HỘI ĐỒNG & TRẢ LỜI NHANH

1. **Vì sao không chọn `2 × 500 kW` gió (NPC thấp nhất $10,40M)?** → Vì lượng điện dư lên tới **26,12 % (> 10 %)**. Chọn `1.400 kWp PV + 1 × 500 kW` gió chỉ tăng giá điện **+$0,0074/kWh (+3,5 %)** nhưng giảm CAPEX **$481.500** và kéo điện dư xuống **9,30 % (≤ 10 %)**.
2. **Vì sao không chạy 100 % năng lượng tái tạo (bỏ Diesel)?** → Vì tháng 4–5 lặng gió (~4,97 m/s) buộc hệ 100 % NLTT phải lắp dư lớn, điện dư ≥ 35 % (> 10 %). Giữ Diesel 750 kW chạy dự phòng **2.201 giờ/năm** giúp đạt **83,5 % tái tạo**, không thiếu tải và giảm **82,7 % CO₂**.
3. **Vì sao bản đầu thiếu tải 18,0 % nhưng vẫn dư 58,4 %?** → Do Converter gốc chỉ `100 kW` (nghẽn dưới đỉnh tải `748,17 kW`) và tuabin E-82 `2.000 kW` phát gấp đôi nhu cầu (`7,24 vs 3,77 GWh/năm`).
4. **Vì sao phụ tải giờ có `Peak 748,17 kW` trong khi tổng công suất đặt `Bảng 3.3` là `783,1 kW`?** → Vì `783,1 kW` là tổng công suất đặt danh định của 3 nhóm phụ tải cộng lại; khi tính đồng thời theo đồ thị 24 giờ và nhiễu thực tế `3 % / 5 %`, công suất đỉnh thực tế toàn đảo đạt `748,17 kW` (hệ số tải `0,58`), nằm trong giới hạn vật lý `≤ 783,1 kW`.
5. **Khác biệt `Load Following (LF)` vs `Cycle Charging (CC)`?** → `LF` chỉ cho Diesel bù đúng phần thiếu tải, nhường nạp BESS cho PV/Gió nên tiết kiệm dầu hơn hẳn `CC`.
6. **BESS 60 khối (6.000 kWh) tự chủ được bao lâu?** → **11,14 giờ** ở tải trung bình, luân chuyển **977.229 kWh/năm**, đủ san phẳng dao động ngày–đêm trước khi gọi Diesel dự phòng.
