# KỊCH BẢN LỒNG TIẾNG CHI TIẾT (KHỚP VIDEO THỰC TẾ 4 PHÚT 13 GIÂY)
**Tập tin video:** [`Video_Thuyet_Trinh_HOMER_Chinh_Thuc.mp4`](file:///d:/chinhan/Video_Thuyet_Trinh_HOMER_Chinh_Thuc.mp4)

---

### [00:00 - 00:04] Slide Mở đầu
> *"Kính chào Thầy và các bạn! Em tên là Đào Chí Nhân, sinh viên lớp KTNL2311. Hôm nay em xin trình bày báo cáo đồ án: **'Mô phỏng và tối ưu hóa hệ thống Microgrid đảo ST – Giai đoạn 3 Côn Đảo trên phần mềm HOMER Pro'**, dưới sự hướng dẫn của thầy Trần Hữu Tính."*

---

### [00:04 - 00:45] Phần 1: Khởi tạo dự án & Bản đồ Côn Đảo
> *"Đầu tiên, trên giao diện chính của HOMER Pro, dự án được thiết lập tại vị trí Côn Đảo, tọa độ địa lý 8 độ 42 phút Bắc và 106 độ 36 phút Đông. Dữ liệu khí tượng gồm bức xạ mặt trời và tốc độ gió được tích hợp tự động từ chuỗi dữ liệu vệ tinh của NASA và Global Wind Atlas. Về thông số kinh tế: Lãi suất danh nghĩa 8%, tỷ lệ lạm phát 2%, tính ra lãi suất chiết khấu thực r = 5,88%/năm và thời gian dự án là 25 năm."*

---

### [00:45 - 01:25] Phần 2: Cấu hình Phụ tải (Electric Load)
> *"Tiếp theo là thiết lập thông số phụ tải điện. Hệ thống cấp điện cho 3 nhóm phụ tải gồm phụ tải hiện trạng 118,1 kW, phụ tải CS 40 kW và phụ tải KT 625 kW, cho tổng công suất đỉnh là 783,1 kW. Với hệ số tải k_tải = 0,55, điện năng tiêu thụ trung bình ngày là 10.337 kWh/ngày, tương đương khoảng 3,77 triệu kWh/năm. Đồ thị 24 giờ phản ánh đúng nhu cầu tiêu thụ thực tế của đảo."*

---

### [01:25 - 02:00] Phần 3: Cấu hình Tuabin gió & Pin mặt trời (Wind & PV)
> *"Về các nguồn phát năng lượng tái tạo:
> - Nguồn điện gió sử dụng một tuabin công nghiệp Enercon E-82 E2 công suất định mức 2.000 kW (2 MW) đặt tại độ cao trục 85 m, khai thác tiềm năng gió biển tầng cao rất dồi dào tại Côn Đảo với hệ số công suất CF đạt 0,38.
> - Nguồn pin mặt trời PV gồm 3 dàn A, B, C với tổng cộng 328 tấm pin 650 Wp, cho tổng công suất đỉnh 213,2 kWp, kết nối vào thanh cái DC với hệ số suy giảm Derating factor 80%."*

---

### [02:00 - 02:40] Phần 4: Cấu hình Pin lưu trữ & Biến tần (BESS & Converter)
> *"Để đảm bảo cấp điện liên tục khi vận hành độc lập không nối lưới:
> - Hệ thống lưu trữ sử dụng 117 bộ pin Lithium-ion 100 kWh, tổng dung lượng danh định 11.700 kWh, tương ứng hai cụm 5.800 kWh và 5.900 kWh trên bản vẽ thiết kế 34 - ST. Dung lượng này đảm bảo thời gian tự chủ cấp tải liên tục 24,4 giờ (hơn 1 ngày đêm) khi hoàn toàn không có gió và nắng.
> - Biến tần Converter đóng vai trò biến tần tạo lưới Grid-Forming đảm bảo ổn định điện áp và tần số cho lưới điện đảo 0,4 kV."*

---

### [02:40 - 03:25] Phần 5: Thiết lập ràng buộc (Constraints) & Chạy mô phỏng (Calculate)
> *"Về ràng buộc kỹ thuật, đối với hệ thống vi lưới biển đảo 100% năng lượng tái tạo không sử dụng máy phát diesel, tỷ lệ thiếu hụt công suất cho phép được đặt ở mức 20% và dự phòng quay tối ưu hóa theo đặc tính biến tần tạo lưới. Sau khi thiết lập đầy đủ thông số, ta bấm nút Calculate để HOMER Pro tiến hành mô phỏng cân bằng năng lượng theo từng giờ trong 8.760 giờ của năm."*

---

### [03:25 - 04:08] Phần 6: Phân tích kết quả mô phỏng (Tab Results & Tables)
> *"Sau khi chạy mô phỏng xong, HOMER Pro đưa ra kết quả rất tối ưu:
> - Tỷ lệ năng lượng tái tạo đạt 100%, không phát thải khí nhà kính.
> - Sản lượng điện gió đạt hơn 7,2 triệu kWh/năm (chiếm hơn 95% sản lượng phát), sản lượng điện mặt trời đạt khoảng 344.000 kWh/năm.
> - Về kinh tế: Vốn đầu tư ban đầu CAPEX là 7,08 triệu USD (~177 tỷ VNĐ), chi phí vòng đời NPC quy về hiện tại là 9,40 triệu USD (~235 tỷ VNĐ). Chi phí điện quy dẫn LCOE chỉ 0,235 USD/kWh (khoảng 5.875 đ/kWh), rẻ hơn rất nhiều so với giá chạy dầu diesel ngoài đảo (12.000 đ/kWh), mang lại thời gian hoàn vốn đầu tư chỉ khoảng 4,5 năm."*

---

### [04:08 - 04:13] Slide Kết thúc
> *"Hệ thống Microgrid đảo ST – Giai đoạn 3 chứng minh tính khả thi kỹ thuật vượt trội và hiệu quả kinh tế cao, mở ra hướng đi bền vững cho cấp điện hải đảo. Em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe bài thuyết trình của em!"*
