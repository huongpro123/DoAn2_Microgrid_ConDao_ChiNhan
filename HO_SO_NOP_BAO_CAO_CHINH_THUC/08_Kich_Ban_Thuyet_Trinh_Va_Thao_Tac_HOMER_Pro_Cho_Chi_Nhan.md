# KỊCH BẢN THUYẾT TRÌNH 15 SLIDE & HƯỚNG DẪN THAO TÁC HOMER PRO TỪ A–Z

- **Sinh viên thực hiện:** Đào Chí Nhân — Ngành Công nghệ Kỹ thuật Năng lượng (Khóa 2023), Trường ĐH Kỹ thuật – Công nghệ Cần Thơ
- **Giảng viên hướng dẫn:** TS. Trần Hữu Tính (Khoa Điện – Điện tử)
- **Đề tài:** Mô phỏng hệ thống Microgrid đảo ST – Giai đoạn 3 (Khu vực biển Đông, gần Côn Đảo) trên phần mềm HOMER Pro
- **Mốc kết quả mô phỏng (`HOMER Pro x64 v3.18.5`):** Toàn bộ số liệu trong tài liệu được trích nguyên văn từ file `03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer` (`454` tổ hợp → `450` khả thi → `288` cấu hình đạt chuẩn `0,00 %` thiếu tải & `≤ 10 %` điện dư).

---

# PHẦN 1: CHECKLIST CHUẨN BỊ TRƯỚC GIỜ BẢO VỆ 30 PHÚT

## 1.1. Ba nhóm file bắt buộc mở sẵn trước khi bước lên bảng
1. **Slide trình chiếu chính:** Mở `07_Slide_Thuyet_Trinh_15_Trang_ST_Giai_Doan_3.pptx` bằng PowerPoint. Bấm **`F5`** (nếu dùng máy chiếu ghép màn hình giống nhau) hoặc **`Alt + F5`** (**Presenter View** — màn hình laptop hiện Slide + Ghi chú nhỏ, màn hình chiếu chỉ hiện Slide lớn cho Hội đồng). Bấm lướt kiểm nhanh **Slide 01, 09, 10, 14** để chắc chắn không lỗi font, không vỡ khung hình.
2. **Phần mềm mô phỏng thật:** Mở sẵn **`03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`** bằng **`HOMER Pro x64 v3.18.5`**. *Lưu ý:* kết quả mô phỏng đã được lưu sẵn trong file, **chưa cần bấm `Calculate` ngay** để tránh tốn thời gian.
3. **Bộ ảnh & PDF dự phòng (phòng khi máy trường không cài HOMER Pro hoặc hết trial):** Mở sẵn thư mục `05_Hinh_Anh_Ket_Qua_HOMER_Pro\` (gồm `homer_opt_table.png`, `homer_opt_summary.png`, `st_diagram.png`), file `07_Slide_Thuyet_Trinh_15_Trang_ST_Giai_Doan_3.pdf` và `02_Bao_Cao_Thuyet_Minh_ST_Giai_Doan_3.pdf`.

## 1.2. Mốc kiểm tra nhanh & phong thái trình bày
| Mốc trước giờ G | Việc cần làm |
|---|---|
| Trước 30 phút | Cắm sạc laptop (chọn chế độ *Best Performance*), tắt thông báo Zalo/Windows (*Do Not Disturb*), tắt chế độ tự tắt màn hình. |
| Trước 15 phút | Mở sẵn đúng 3 nhóm file trên, thu gọn cửa sổ dưới thanh taskbar theo thứ tự: `1. PowerPoint` → `2. HOMER Pro` → `3. Ảnh/PDF dự phòng`. |
| Trước 5 phút | Hít thở đều, nhớ nhịp **10–12 phút cho 15 slide** (trung bình ~45 giây/slide; dồn thời gian vào **Slide 07, 09, 10, 12**). |
| Khi nói | Mắt nhìn Hội đồng khi mở ý, quay sang chỉ đúng con số/biểu đồ trên màn hình rồi quay lại nhìn Hội đồng kết câu — **không đọc thuộc lòng như đọc văn bản**. |

---

# PHẦN 2: KỊCH BẢN LỜI THOẠI CHI TIẾT 15 SLIDE (10–12 PHÚT)

### Slide 01 – Trang bìa + 4 KPI chốt (Thời lượng: 40 giây)
- **Động tác & chỉ chuột:** Đứng thẳng, cúi chào Hội đồng; chỉ lần lượt 4 ô KPI ở nửa dưới màn hình: `0,00 %` → `6,15 %` → `$0,2367/kWh` → `-2.167,5 t/năm`.
- **Lời thuyết trình chuẩn:**  
  "Kính thưa Quý Thầy/Cô trong Hội đồng chấm Đồ án Khoa Điện – Điện tử. Em tên là **Đào Chí Nhân**, sinh viên ngành Công nghệ Kỹ thuật Năng lượng khóa 2023. Hôm nay em xin phép trình bày Đồ án 2 với đề tài: **Mô phỏng hệ thống Microgrid đảo ST – Giai đoạn 3 (khu vực gần Côn Đảo) trên phần mềm HOMER Pro**, dưới sự hướng dẫn của **TS. Trần Hữu Tính**.  
  Bốn kết quả trọng tâm mà mô hình đạt được sau tối ưu là: **0,00 % thiếu tải**, **6,15 % điện dư** (đạt ngưỡng dưới 10 %), giá thành điện **LCOE $0,2367/kWh**, và cắt giảm **2.167,5 tấn CO₂ mỗi năm**. Sau đây em xin trình bày chi tiết từng phần."
- **Lưu ý nhấn mạnh:** Nhấn mạnh cặp tiêu chuẩn **0,00 % thiếu tải** và **6,15 % điện dư (≤ 10 %)** vì đây là điều kiện tiên quyết của đề tài.

---

### Slide 02 – Bối cảnh & Bài toán cấp điện đảo ST (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Chỉ vào bản đồ vị trí Côn Đảo bên trái, rồi lia chuột qua 4 gạch đầu dòng bên phải (chỉ thẳng số `3.773.005 kWh/năm`, `776,0 kW`, `>1,05 triệu L dầu/năm`).
- **Lời thuyết trình chuẩn:**  
  "Thưa Quý Thầy/Cô, đảo ST nằm ngoài khơi vùng biển gần Côn Đảo, chưa nối lưới điện quốc gia. Hiện phụ tải điện của đảo là **3.773.005 kWh/năm** (khoảng **10.337 kWh/ngày**), công suất đỉnh **776,0 kW**.  
  Nếu chỉ dùng máy phát Diesel thuần túy (Base Case), mỗi năm phải vận chuyển hơn **1,05 triệu lít dầu** ra đảo, đẩy giá điện lên rất cao tới **$0,3990/kWh**. Vì vậy, mục tiêu đề tài đặt ra là thiết kế hệ Microgrid Hybrid đáp ứng **100 % phụ tải (0 % thiếu tải)**, khống chế điện dư cắt giảm **≤ 10 %**, và đánh giá đồng thời ba trụ cột Kỹ thuật – Kinh tế – Môi trường."
- **Lưu ý nhấn mạnh:** Đọc rõ con số đỉnh tải **776,0 kW** (để lát giải thích vì sao Converter 100 kW bị nghẽn).

---

### Slide 03 – Chương 1: So sánh 3 kiến trúc lưới điện độc lập (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Chỉ từ trái sang phải qua 3 cột: *Cấu hình 1 (đỏ)* → *Cấu hình 2 (vàng)* → dừng lại lâu hơn ở *Cấu hình 3 (xanh lá)*.
- **Lời thuyết trình chuẩn:**  
  "Ở Chương 1, em tổng quan và đối chiếu ba kiến trúc Microgrid độc lập cho hải đảo:  
  - Thứ nhất là **thuần Diesel**: vốn đầu tư thấp ($1,185 triệu), nhưng chi phí vận hành vòng đời lên tới **$19,46 triệu** và phát thải **2.759,5 tấn CO₂/năm**.  
  - Thứ hai là **100 % năng lượng tái tạo (không Diesel)**: dù sạch tại chỗ, nhưng để gánh tải qua mùa lặng gió, hệ thống phải lắp dư nguồn lớn khiến điện dư lên tới **35,1–58,4 %** và đội vốn đầu tư.  
  - Thứ ba là **cấu hình Hybrid chọn (PV + Gió + BESS + Diesel dự phòng)**: đạt tỷ lệ tái tạo **78,9 %**, đáp ứng 100 % phụ tải và giữ điện dư chỉ **6,15 %**."
- **Lưu ý nhấn mạnh:** Nói dứt khoát tại sao không bỏ hẳn Diesel: vì mùa lặng gió ép điện dư của phương án 100 % tái tạo vượt xa mức 10 %.

---

### Slide 04 – Đặc trưng mùa gió Côn Đảo & tính bổ trợ Hybrid (Thời lượng: 40 giây)
- **Động tác & chỉ chuột:** Chỉ tay theo đường cong gió trên biểu đồ: nhấn mạnh vùng xanh tháng 12–2 (`10,8–11,0 m/s`) và vùng vàng tháng 4–5 (`~4,97 m/s`).
- **Lời thuyết trình chuẩn:**  
  "Sở dĩ cần phối hợp đa nguồn là do biến động gió tại vùng biển Côn Đảo phân hóa hai mùa rất rõ rệt. Từ tháng 12 đến tháng 2, gió Đông Bắc mạnh đạt **10,8–11,0 m/s**; nhưng sang **tháng 4–5**, gió yếu hẳn xuống chỉ còn khoảng **4,97 m/s**.  
  Nếu lắp tuabin gió quá lớn để chạy mùa lặng gió thì sang mùa gió mạnh lại dư điện tràn lan. Do đó, phương án hợp lý nhất là chọn quy mô gió vừa phải **1 × 500 kW**, để **1.200 kWp PV**, **6.000 kWh BESS** và **Diesel 970 kW** bổ trợ vào thời điểm lặng gió."
- **Lưu ý nhấn mạnh:** Cặp số gió **10,8–11,0 m/s** (mùa mạnh) vs **4,97 m/s** (mùa lặng).

---

### Slide 05 – Sơ đồ nguyên lý 34-ST & Chiến lược điều độ (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Chỉ lên ảnh sơ đồ `st_diagram.png` bên trái: chỉ cụm Tuabin gió + Diesel (AC), cụm PV + BESS (DC), và điểm nối Converter ở giữa.
- **Lời thuyết trình chuẩn:**  
  "Đây là sơ đồ nguyên lý hệ thống 34-ST. Trên thanh cái **AC Bus** đấu nối phụ tải đảo đỉnh 776 kW, Tuabin gió 500 kW và Máy phát Diesel 970 kW. Trên thanh cái **DC Bus** đấu nối giàn pin mặt trời 1.200 kWp và 60 khối pin Li-ion tổng dung lượng 6.000 kWh.  
  Ở giữa là bộ biến đổi 2 chiều **Converter nâng lên 800 kW** để xóa nghẽn truyền công suất giữa hai thanh cái. Hệ thống chạy theo chiến lược **Load Following**: Diesel chỉ phát đúng phần phụ tải còn thiếu, nhường quyền sạc pin cho năng lượng mặt trời và gió."
- **Lưu ý nhấn mạnh:** Khác biệt mấu chốt giữa **Load Following** và Cycle Charging.

---

### Slide 06 – Chương 2: Mô hình toán học hệ thống `(2.1)–(2.24)` (Thời lượng: 35 giây)
- **Động tác & chỉ chuột:** Chỉ lướt 3 cột (Mục 2.1 → Mục 2.2 → Mục 2.3), không cần đọc từng công thức dài dòng.
- **Lời thuyết trình chuẩn:**  
  "Ở Chương 2, theo góp ý của Thầy hướng dẫn, em đã chuẩn hóa toàn bộ cơ sở toán học thành ba nhóm với 24 phương trình đánh số từ **(2.1) đến (2.24)**:  
  - Nhóm 2.1 mô hình hóa công suất phát PV theo bức xạ – nhiệt độ, hiệu chỉnh tốc độ gió theo cao trình trục 47 m và suất tiêu hao nhiên liệu Diesel;  
  - Nhóm 2.2 mô tả trạng thái sạc BESS và cân bằng công suất từng giờ trong **8.760 giờ/năm** để định nghĩa chỉ số `Unmet` và `Excess`;  
  - Nhóm 2.3 tính toán **NPC, LCOE, IRR, hoàn vốn** và lượng phát thải khí nhà kính."
- **Lưu ý nhấn mạnh:** Toàn bộ bài mô phỏng giải cân bằng liên tục theo **8.760 giờ/năm**.

---

### Slide 07 – Chẩn đoán 2 nút thắt cấu hình ban đầu (Thời lượng: 55 giây)
- **Động tác & chỉ chuột:** Chỉ vào cột đỏ cao `18,0 %` (cấu hình ban đầu) → cột vàng `58,4 %` → cột vàng `26,14 %` (2 tuabin) → cột xanh lá `6,15 %` (phương án chọn).
- **Lời thuyết trình chuẩn:**  
  "Khi kiểm tra cấu hình ban đầu trong file mẫu cũ, em phát hiện một nghịch lý: hệ thống vừa **thiếu tải 18,0 %**, vừa **dư điện cắt bỏ tới 58,4 % (4,43 GWh/năm)**. Nguyên nhân gồm hai nút thắt:  
  Thứ nhất, **Converter gốc chỉ có 100 kW**, nhỏ hơn rất nhiều so với đỉnh tải 776 kW nên không đẩy kịp điện từ phía DC sang nuôi tải. Thứ hai, lắp 1 tuabin E-82 công suất tới **2.000 kW** là quá dư so với tải đảo.  
  Ngoài ra, khi quét tối ưu còn xuất hiện 'bẫy NPC thấp nhất': cấu hình **2 × 500 kW gió** có NPC nhỏ nhất ($10,75 triệu), nhưng điện dư lên tới **26,14 % > 10 %**, nên phải loại để giữ đúng tiêu chuẩn kỹ thuật."
- **Lưu ý nhấn mạnh:** Đây là slide ăn điểm phân tích kỹ thuật — nhớ chắc 3 con số: **18,0 %**, **58,4 %** và **26,14 %**.

---

### Slide 08 – Thiết lập không gian tìm kiếm HOMER Pro v3.18.5 (Thời lượng: 40 giây)
- **Động tác & chỉ chuột:** Chỉ theo cột "Dải tối ưu HOMER Pro" và cột "Giá trị CHỌN" bên phải, chốt ở dòng cuối màu xanh lá.
- **Lời thuyết trình chuẩn:**  
  "Để tìm cấu hình tối ưu trên **HOMER Pro x64 v3.18.5**, em mở dải tìm kiếm cho 5 thành phần: PV từ **0 đến 1.200 kWp**; Tuabin gió **0 đến 2 bộ Windflow 45 (500 kW, cao 47 m)**; pin lưu trữ **20 đến 117 khối** (loại 100 kWh/khối); Converter **0 đến 1.200 kW**; kết hợp máy phát **Autosize Diesel 970 kW** và khóa cứng ràng buộc **thiếu tải tối đa bằng 0 %**.  
  Tổng cộng phần mềm quét **454 tổ hợp**, cho **450 tổ hợp khả thi**, và lọc ra đúng **288 cấu hình** đạt đồng thời 0,00 % thiếu tải và ≤ 10 % điện dư."
- **Lưu ý nhấn mạnh:** Bộ lọc **454 → 450 → 288** từ file chạy thật.

---

### Slide 09 – Bằng chứng HOMER Pro: Bảng xếp hạng tối ưu (Thời lượng: 55 giây)
- **Động tác & chỉ chuột:** Chỉ vào dòng trên cùng trên ảnh `homer_opt_table.png` (2 tuabin gió, `$10.8M / $0.220`), rồi chỉ xuống phần giải trình bên phải.
- **Lời thuyết trình chuẩn:**  
  "Đây là ảnh chụp trực tiếp bảng **Optimization Results** sau khi chạy thật trên HOMER Pro v3.18.5. Như Quý Thầy/Cô thấy, dòng xếp đầu theo NPC dùng **2 tuabin gió** đạt NPC $10,75 triệu và LCOE $0,2204/kWh, nhưng cột điện dư lên tới **26,14 %** — vi phạm ràng buộc ≤ 10 %.  
  Vì vậy trong nhóm **288 phương án đạt chuẩn**, em chọn phương án dẫn đầu dùng **1 × 500 kW gió**: chỉ đánh đổi giá điện tăng nhẹ **$0,0163/kWh**, nhưng giảm được ngay **$961.500 vốn đầu tư ban đầu** và kéo điện dư tụt xuống chỉ còn **6,15 %**."
- **Lưu ý nhấn mạnh:** Nói rõ mức đánh đổi chỉ **+$0,0163/kWh** nhưng giảm được tới **81 % lượng điện dư**.

---

### Slide 10 – Bằng chứng HOMER Pro: Chi tiết cấu hình chọn (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Chỉ vào ảnh `homer_opt_summary.png` bên trái và đọc nhanh 4 ý bên phải.
- **Lời thuyết trình chuẩn:**  
  "Hình này là bảng **Simulation Summary** của cấu hình tối ưu đã chọn: **1.200 kWp PV + 1 × 500 kW Windflow 45 + 60 khối BESS (6.000 kWh) + 970 kW Diesel + 800 kW Converter**.  
  Tổng sản lượng phát đạt **4.233.058 kWh/năm**, phục vụ đủ **3.773.005 kWh** phụ tải với 0 kWh thiếu. Hệ BESS 6.000 kWh đạt thời gian tự chủ **11,14 giờ** và luân chuyển **961.779 kWh/năm**. Máy phát Diesel chỉ còn chạy **2.425 giờ/năm**, giảm **44,1 %** so với **4.342 giờ/năm** ở Base Case."
- **Lưu ý nhấn mạnh:** Tự chủ BESS **11,14 giờ** và giảm giờ chạy Diesel từ **4.342 → 2.425 giờ/năm**.

---

### Slide 11 – Trụ cột 1: Đánh giá Kỹ thuật & Cơ cấu sản lượng (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Chỉ 3 thanh sản lượng trên cùng của biểu đồ ngang (PV vàng, Gió xanh dương, Diesel xám) và thanh Phụ tải xanh lá.
- **Lời thuyết trình chuẩn:**  
  "Đi vào trụ cột thứ nhất — **Kỹ thuật**: Trong tổng **4,23 GWh/năm** phát ra, năng lượng mặt trời PV đóng góp **1,94 GWh (45,8 %)**, tuabin gió đóng góp **1,50 GWh (35,4 %)**, còn Diesel dự phòng chỉ đóng góp **0,80 GWh (18,8 %)**.  
  Tỷ lệ năng lượng tái tạo (**RF**) đạt **78,9 %**. Hệ thống đáp ứng **100,0 %** phụ tải, và lượng điện dư cắt giảm chỉ ở mức **260.422 kWh/năm**, tương ứng **6,15 %**, hoàn toàn nằm trong giới hạn cho phép ≤ 10 %."
- **Lưu ý nhấn mạnh:** **RF = 78,9 %** và **Excess = 6,15 %**.

---

### Slide 12 – Trụ cột 2: Đánh giá Kinh tế vòng đời 25 năm (Thời lượng: 50 giây)
- **Động tác & chỉ chuột:** Chỉ so sánh hai cột NPC (Base Case `$19,46M` vs Chọn `$11,54M`) và hai cột LCOE bên phải (`$0,3990` vs `$0,2367`).
- **Lời thuyết trình chuẩn:**  
  "Về trụ cột thứ hai — **Kinh tế trên vòng đời 25 năm**: Tuy vốn đầu tư ban đầu CAPEX của cấu hình chọn là **$5.946.500** (nhưng đã **giảm 16,0 %** so với $7,08 triệu ở cấu hình ban đầu), chi phí vận hành hàng năm giảm mạnh từ $1,41 triệu xuống còn **$433.036/năm**.  
  Nhờ đó tổng chi phí hiện tại ròng **NPC giảm tới 40,7 %** (từ $19,46 triệu xuống còn **$11,54 triệu**), kéo theo giá điện **LCOE giảm 40,7 %** từ **$0,3990 xuống $0,2367/kWh**. Dự án đạt **IRR 18,9 %**, **ROI 15,0 %**, hoàn vốn giản đơn **5,02 năm** (chiết khấu **6,28 năm**) và giá trị hiện tại ròng **+$6,94 triệu**."
- **Lưu ý nhấn mạnh:** Giảm **40,7 %** cả NPC lẫn LCOE và hoàn vốn sau **5,02 năm**.

---

### Slide 13 – Trụ cột 3: Đánh giá Nhiên liệu & Môi trường (Thời lượng: 40 giây)
- **Động tác & chỉ chuột:** Chỉ hai mũi tên đi xuống trên biểu đồ Dầu Diesel và biểu đồ Phát thải CO₂.
- **Lời thuyết trình chuẩn:**  
  "Về trụ cột thứ ba — **Nhiên liệu và Môi trường**: So với Base Case thuần Diesel tiêu thụ **1.054.193 lít dầu/năm**, cấu hình tối ưu chỉ dùng **226.143 lít/năm**, tiết kiệm **828.050 lít dầu mỗi năm (giảm 78,5 %)**, giúp giảm mạnh rủi ro phụ thuộc tàu chở dầu khi biển động.  
  Đồng thời phát thải CO₂ giảm từ **2.759,5 tấn xuống còn 592,0 tấn/năm**, tức là **tránh được 2.167,5 tấn CO₂ mỗi năm** — tương đương hơn **54.187 tấn CO₂** trong 25 năm vận hành, cùng mức giảm **78,5 %** khí thải NOx và SO₂."
- **Lưu ý nhấn mạnh:** **Tiết kiệm 78,5 % dầu (828.050 L/năm)** và **tránh 2.167,5 tấn CO₂/năm**.

---

### Slide 14 – Bảng đối chiếu tổng hợp 3 trụ cột & Hoàn thành 6 góp ý GVHD (Thời lượng: 45 giây)
- **Động tác & chỉ chuột:** Rê chuột dọc cột "Cấu hình CHỌN" ở bên phải bảng, sau đó chỉ xuống thanh xanh lá ở dưới cùng.
- **Lời thuyết trình chuẩn:**  
  "Slide này tổng hợp trực diện cả ba phương án qua 7 chỉ tiêu kỹ thuật – kinh tế – môi trường. Cấu hình chọn dung hòa trọn vẹn các mục tiêu: không mất điện như bản đầu, không xả dư 26–58 %, giá điện giảm hơn 40 % và phát thải giảm gần 80 % so với chạy Diesel.  
  Bên dưới bảng cũng xác nhận đồ án đã hoàn thiện đầy đủ **6/6 góp ý chuyên môn của TS. Trần Hữu Tính**: tách sạch Chương 1–3, chuẩn hóa 24 công thức, mô phỏng thật trên HOMER Pro v3.18.5 và hoàn chỉnh văn bản chuẩn QĐ 345/2025 của Trường."
- **Lưu ý nhấn mạnh:** Khẳng định đã khắc phục trọn vẹn 6/6 góp ý của Thầy hướng dẫn.

---

### Slide 15 – Kết luận, Kiến nghị & Sẵn sàng Hỏi đáp (Thời lượng: 40 giây)
- **Động tác & chỉ chuột:** Chỉ lướt 3 cột (Kết luận → Hạn chế/Mở rộng → Trạm Q&A), sau đó đặt tay nghỉ, mắt nhìn thẳng Hội đồng mỉm cười chào kết.
- **Lời thuyết trình chuẩn:**  
  "Tóm lại, đề tài đã thiết kế thành công cấu hình Hybrid **1.200 kWp PV + 500 kW Gió + 6.000 kWh BESS + 970 kW Diesel + 800 kW Converter** cho đảo ST.  
  Về hướng phát triển tiếp theo, mô hình cần bổ sung **phân tích độ nhạy** theo biến động giá dầu/pin, **mô phỏng quá độ ổn định tần số – điện áp** trên phần mềm lưới điện chuyên dụng (như PSS/E hoặc PowerFactory) và tính toán chống ăn mòn muối biển khi lắp đặt thực tế.  
  Phần trình bày của em đến đây là kết thúc. Em xin chân thành cảm ơn Quý Thầy/Cô đã lắng nghe và rất mong nhận được ý kiến góp ý của Hội đồng ạ!"

---

# PHẦN 3: HƯỚNG DẪN THAO TÁC TỪNG CÚ CLICK TRONG HOMER PRO x64 v3.18.5
*(Dành riêng cho Chí Nhân — làm đúng từng bước dưới đây là thao tác trôi chảy dù chưa từng dùng phần mềm)*

## Bước 1: Mở đúng file mô phỏng
1. Bật phần mềm **HOMER Pro**.
2. Góc trên cùng bên trái bấm **File** → **Open** → tìm đúng thư mục `HO_SO_NOP_BAO_CAO_CHINH_THUC` → chọn file **`03_File_Mo_Phong_HOMER_Pro_Toi_Uu.homer`** → bấm **Open**.
3. Nhìn dải menu ngang ở trên cùng sẽ thấy các thẻ chính: **`Home`**, **`Design`**, **`Demand`**, **`Resources`**, **`Components`**, **`Project`**, **`Results`**.

## Bước 2: Giải thích sơ đồ 1 sợi (`Schematic`) khi Hội đồng xem màn hình chính
- Nếu chưa hiện sơ đồ, bấm thẻ **`Design`** → bấm **`Schematic`** ở góc trái.
- Dùng chuột chỉ cho Thầy/Cô thấy 2 thanh cái và 6 khối thiết bị:
  - **Thanh cái bên trái (`AC`):** `Electric Load` (phụ tải 10.337 kWh/ngày, đỉnh 776,0 kW), `Windflow 45 [500kW]`, `Autosize Genset [970kW]`.
  - **Ở giữa nối AC ↔ DC:** `System Converter` (800 kW).
  - **Thanh cái bên phải (`DC`):** `Generic flat plate PV` (1.200 kWp), `100kWh Li-Ion [60 chuỗi = 6.000 kWh]`.

## Bước 3: Thao tác khi Thầy/Cô hỏi "Mở lại thông số đầu vào kiểm tra thử"
- **Xem phụ tải:** Bấm thẻ **`Demand`** → bấm **`Electric Load #1`**. Chỉ vào ô `Scaled Annual Average` (**10.337 kWh/ngày**, tổng **3.773.005 kWh/năm**) và `Peak` (**776,0 kW**).
- **Xem dữ liệu Nắng & Gió:** Bấm thẻ **`Resources`** → bấm **`Solar GHI`** (nắng) hoặc **`Wind`** (gió — chỉ vào biểu đồ thấy tháng 12–2 gió mạnh **10,8–11,0 m/s**, tháng 4–5 lặng gió **~4,97 m/s**).
- **Xem ràng buộc 0 % thiếu tải:** Bấm thẻ **`Project`** → bấm mục **`Constraints`** → chỉ ngay dòng **`Maximum annual capacity shortage`** đang đặt bằng **`0 %`**.
- **Xem dải tìm kiếm (`Search Space`):** Click đúp vào từng biểu tượng thiết bị trên sơ đồ (ví dụ `PV` hay `Windflow 45`) → nhìn góc dưới/bên phải bấm nút **`Search Space`** → cho thấy dải `0–1.200 kWp` (PV), `0–2` (tuabin gió), `20–117` (pin BESS), `0–1.200 kW` (Converter).

## Bước 4: Xem kết quả trong bảng `Results` (KHÔNG cần chạy lại trừ khi Thầy bảo)
1. Bấm thẳng vào thẻ **`Results`** trên thanh menu ngang *(kết quả đã chạy sẵn và lưu trong file `.homer`)*.
2. **Chỉ khi Thầy yêu cầu "Em bấm chạy lại cho Thầy xem":**
   - Nhìn góc trên cùng bên phải, bấm nút **`Calculate`** (biểu tượng máy tính lớn màu xanh).
   - Ngồi đợi khoảng **10–20 giây** thanh tiến trình chạy xong (`454` trường hợp khảo sát, `450` khả thi).
3. **Cách chuyển bảng để chỉ cấu hình chọn:**
   - Góc trên bên phải bảng `Optimization Results` có 2 nút tròn chọn: **`Categorized`** *(xếp mỗi loại cấu hình lấy 1 dòng tốt nhất)* và **`Overall`** *(liệt kê toàn bộ mọi tổ hợp từ NPC thấp nhất trở đi)*.
   - Bấm **`Overall`**: chỉ dòng **#1** là `2 tuabin gió` (`NPC $10.8M`, `COE $0.220`, kéo thanh cuộn sang phải thấy `Excess = 26.14%`), sau đó chỉ xuống dòng cấu hình chọn có **`1 tuabin gió`** (`PV 1,200`, `WF45 = 1`, `Gen 970`, `BESS 60`, `Conv 800`, `Dispatch = LF`, `NPC = $11.5M`, `COE = $0.237`, `Ren Frac = 78.9%`).

## Bước 5: Mở cửa sổ `Simulation Results` xem 5 tab chi tiết (nháy đúp)
1. **Nháy đúp chuột trái (double-click)** trực tiếp vào dòng cấu hình chọn (`1 tuabin gió · 1.200 PV · 60 BESS · LF`) → hiện ra cửa sổ mới **`Simulation Results`**.
2. Thầy hỏi mục nào thì bấm đúng tab đó ở hàng trên của cửa sổ này:
   - **Tab 1 – `Cost Summary`:** xem vốn đầu tư `CAPEX = $5.946.500`, tổng chi phí quy đổi `NPC = $11.544.581`, chi phí thay thế, O&M và nhiên liệu của từng thiết bị.
   - **Tab 2 – `Electrical`:** nhìn 2 bảng chính:
     - Bảng trên (`Production`): PV `1.940.043 kWh/yr (45,8 %)`, Wind `1.497.991 kWh/yr (35,4 %)`, Diesel `795.025 kWh/yr (18,8 %)`, tổng **`4.233.058 kWh/yr`**.
     - Bảng dưới (`Excess and Unmet`): `Excess Electricity = 260.422 kWh/yr (6,15 %)`, `Unmet Electric Load = 0 kWh/yr (0,00 %)`.
   - **Tab 3 – `Compare Economics` *(hoặc phần Economics cạnh Cost Summary)*:** xem các chỉ số tài chính khi so với Base Case Diesel: `IRR = 18,9 %`, `ROI = 15,0 %`, `Simple Payback = 5,02 yr`, `Discounted Payback = 6,28 yr`, `Present Worth = $6.942.548`.
   - **Tab 4 – `Emissions`:** xem lượng phát thải CO₂ chỉ còn **`591.956 kg/yr` (592,0 tấn/năm)** kèm NOx, SO₂, CO, PM.
   - **Tab 5 – `Time Series Plot`:** bấm vào đây nếu Thầy hỏi biểu đồ vận hành theo từng giờ trong năm (`8.760 giờ`) — chọn tháng 4–5 (lặng gió, PV + Diesel gánh) hoặc tháng 12–1 (gió mạnh, BESS sạc đầy).

## Bước 6: Xử lý sự cố khẩn cấp tại phòng bảo vệ
- **Nếu mở file bị báo hết hạn dùng thử / lỗi license / máy phòng không có HOMER Pro:** Giữ bình tĩnh, nói *"Dạ thưa Thầy/Cô, máy phòng chiếu hiện không chạy được phần mềm nên em xin phép mở ảnh kết quả chụp trực tiếp từ bản chạy HOMER Pro x64 v3.18.5 của em ạ"*, rồi mở ngay `homer_opt_table.png` và `homer_opt_summary.png` trong `05_Hinh_Anh_Ket_Qua_HOMER_Pro\`.

---

# PHẦN 4: BỘ 6 CÂU HỎI TỦ HỘI ĐỒNG & MẪU TRẢ LỜI TRÚNG SỐ LIỆU

### Câu 1: Vì sao trong bảng `Overall` phương án `2 × 500 kW` gió có NPC thấp hơn ($10,75 triệu vs $11,54 triệu) mà em lại không chọn?
- **Trả lời mẫu:**  
  "Dạ thưa Thầy/Cô, phương án `2 × 500 kW` gió tuy có NPC thấp nhất ($10,75 triệu, LCOE $0,2204/kWh), nhưng lượng điện dư cắt bỏ lên tới **26,14 %**, vi phạm ràng buộc kỹ thuật đề tài đặt ra là **≤ 10 %**. Khi chọn phương án **1 × 500 kW gió**, giá điện chỉ tăng nhẹ **$0,0163/kWh** nhưng điện dư giảm mạnh xuống còn **6,15 %** và tiết kiệm được **$961.500** vốn đầu tư ban đầu ạ."

### Câu 2: Vì sao không thiết kế 100 % năng lượng tái tạo (bỏ hẳn máy phát Diesel) để không phát thải CO₂?
- **Trả lời mẫu:**  
  "Dạ thưa Thầy/Cô, qua phân tích khí tượng vùng biển Côn Đảo, giai đoạn **tháng 4–5 lặng gió (~4,97 m/s)** kéo dài khiến phương án 100 % tái tạo buộc phải lắp dư công suất nguồn rất lớn. Kết quả chạy kiểm chứng cho thấy dù tối ưu cỡ nào thì phương án 100 % tái tạo vẫn có điện dư cắt bỏ tối thiểu **~35,1 % trở lên** (vượt xa ngưỡng 10 %) và CAPEX bị đội lên cao. Giữ lại máy phát Diesel 970 kW chỉ chạy dự phòng **2.425 giờ/năm** giúp đảm bảo 100 % an ninh cấp điện mà vẫn đạt **78,9 % tái tạo** và giảm **78,5 % CO₂** ạ."

### Câu 3: Vì sao cấu hình ban đầu có tuabin tới 2.000 kW mà vẫn thiếu tải 18,0 % đồng thời lại dư điện tới 58,4 %?
- **Trả lời mẫu:**  
  "Dạ đó là do hai lỗi mất cân đối đồng thời ạ: Thứ nhất, **Converter gốc chỉ có 100 kW** trong khi phụ tải đỉnh là **776,0 kW**, tạo nút thắt cổ chai không xả kịp điện từ PV và BESS phía DC sang phụ tải phía AC, gây thiếu tải **18,0 %**. Thứ hai, tuabin Enercon E-82 công suất **2.000 kW** tự nó đã phát **7,24 GWh/năm** — gần gấp đôi nhu cầu đảo (**3,77 GWh/năm**) nên gây dư điện cắt bỏ tới **58,4 %** ạ."

### Câu 4: Chiến lược điều độ `Load Following (LF)` khác gì `Cycle Charging (CC)` và vì sao ở đây chọn `LF`?
- **Trả lời mẫu:**  
  "Dạ ở chiến lược **Cycle Charging (CC)**, hễ máy phát Diesel bật lên là chạy gần đầy tải để vừa cấp cho phụ tải vừa sạc cho BESS, nên tốn thêm nhiên liệu dầu. Còn **Load Following (LF)** chỉ cho máy phát phát đúng phần công suất còn thiếu của phụ tải, nhường hoàn toàn việc sạc BESS cho điện mặt trời và gió. Nhờ vậy phương án chọn chạy `LF` tiết kiệm dầu và đạt NPC thấp hơn hẳn ạ."

### Câu 5: Hệ pin lưu trữ `60 khối BESS (6.000 kWh)` giữ điện cho đảo được bao lâu nếu mất nắng và lặng gió cùng lúc?
- **Trả lời mẫu:**  
  "Dạ theo kết quả từ HOMER Pro, 60 khối BESS Li-ion (tổng dung lượng danh định 6.000 kWh) có thời gian tự chủ (**Autonomy**) đạt **11,14 giờ** ở mức phụ tải trung bình, với sản lượng luân chuyển qua pin đạt **961.779 kWh/năm**, đủ san phẳng dao động ngày–đêm trước khi cần khởi động máy phát Diesel dự phòng ạ."

### Câu 6: Nếu giá dầu Diesel tăng mạnh hoặc phụ tải đảo tăng trong tương lai thì mô hình này có đứng vững không?
- **Trả lời mẫu:**  
  "Dạ với phụ tải hiện tại, vì tỷ lệ tái tạo đã đạt **78,9 %** (chỉ phụ thuộc **226.143 lít dầu/năm**, giảm 78,5 % so với Base Case), nên khi giá dầu tăng thì lợi thế kinh tế của hệ Hybrid so với chạy Diesel càng nới rộng hơn nữa. Trong hướng phát triển tiếp theo, em kiến nghị bổ sung **phân tích độ nhạy (Sensitivity Analysis)** theo giá dầu và tốc độ tăng phụ tải để lên lộ trình nâng cấp công suất theo giai đoạn ạ."
