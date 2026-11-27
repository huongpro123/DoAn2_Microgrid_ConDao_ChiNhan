import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Directory for video frames
frames_dir = 'video_frames'
os.makedirs(frames_dir, exist_ok=True)

# Resolution 1920x1080
W, H = 1920, 1080

def create_base(color=(245, 247, 250)):
    return Image.new('RGB', (W, H), color)

# List of scenes with duration in seconds
scenes = [
    {
        'title': 'BÁO CÁO ĐỒ ÁN TỐT NGHIỆP',
        'subtitle': 'MÔ PHỎNG VÀ TỐI ƯU HÓA HỆ THỐNG MICROGRID ĐẢO ST - GIAI ĐOẠN 3 (CÔN ĐẢO)\nTRÊN PHẦN MỀM HOMER PRO',
        'info': 'Sinh viên: Đào Chí Nhân | Lớp: KTNL2311\nGVHD: ThS. Trần Hữu Tính',
        'image': None,
        'duration': 5
    },
    {
        'title': '1. SƠ ĐỒ NGUYÊN LÝ HỆ THỐNG (BẢN VẼ 34 - ST)',
        'subtitle': 'Hệ thống Microgrid độc lập 100% NLTT (Zero-carbon): PV 213,2 kWp | Wind 2 MW | BESS 11.700 kWh',
        'info': 'Thanh cái AC 0,4 kV kết nối Tuabin gió và Tủ hạ thế 12 ngăn. Thanh cái DC kết nối dàn PV và Pin BESS.',
        'image': 'diagram_34_st.png',
        'duration': 6
    },
    {
        'title': '2. KHỞI TẠO DỰ ÁN & VỊ TRÍ ĐỊA LÝ (CÔN ĐẢO)',
        'subtitle': 'Tọa độ: 8°42\'N - 106°36\'E | Dữ liệu NASA & Global Wind Atlas | r = 5,88%/năm | Vòng đời 25 năm',
        'info': 'Khai báo lãi suất danh nghĩa 8%, lạm phát 2% -> Lãi suất thực tế r = 5,88%. Không sử dụng máy phát diesel.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793460150004_1505f0d5.jpg',
        'duration': 6
    },
    {
        'title': '3. CẤU HÌNH THÔNG SỐ PHỤ TẢI (ELECTRIC LOAD)',
        'subtitle': 'P_đỉnh = 783,1 kW | Điện năng tiêu thụ ngày = 10.337 kWh/ngày (~3,77 triệu kWh/năm)',
        'info': 'Phụ tải hỗn hợp gồm 3 nhóm: Hiện trạng (118,1 kW), CS (40 kW), KT (625 kW). Hệ số tải k_tải = 0,55.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793460800077_6205ad80.jpg',
        'duration': 6
    },
    {
        'title': '4. CẤU HÌNH NGUỒN TUABIN GIÓ (WIND TURBINE)',
        'subtitle': 'Công suất định mức: 2.000 kW (2 MW) | Độ cao trục tuabin Hub Height: 85 mét',
        'info': 'Sử dụng tuabin gió Enercon E-82 E2 2 MW công nghiệp, tận dụng tiềm năng gió biển dồi dào ngoài khơi Côn Đảo.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793460885052_d3f1b2e5.jpg',
        'duration': 6
    },
    {
        'title': '5. CẤU HÌNH HỆ PIN MẶT TRỜI (SOLAR PV)',
        'subtitle': 'Công suất đặt: 213,2 kWp | Hệ số suy giảm PR (Derating Factor): 80% | DC Bus',
        'info': 'Gồm 3 dàn A, B, C (328 tấm pin 650 Wp) kết nối vào thanh cái DC, hỗ trợ cấp điện quan trọng vào ban ngày.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793460948127_6a293b2e.jpg',
        'duration': 6
    },
    {
        'title': '6. CẤU HÌNH HỆ LƯU TRỮ PIN (BESS - STORAGE)',
        'subtitle': 'Dung lượng: 11.700 kWh (117 bộ Generic 100kWh Li-ion) | Điện áp danh định: 600V',
        'info': 'Tương ứng 2 cụm pin 5.800 kWh + 5.900 kWh trên bản vẽ 34 - ST. Đảm bảo thời gian tự chủ cấp tải liên tục 24,4 giờ.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793461007130_2a97e78d.jpg',
        'duration': 6
    },
    {
        'title': '7. THIẾT LẬP RÀNG BUỘC KỸ THUẬT (CONSTRAINTS)',
        'subtitle': 'Maximum Annual Capacity Shortage: 20% | Operating Reserve: 0% (Hệ biến tần tạo lưới Grid-forming)',
        'info': 'Ràng buộc được tối ưu hóa cho hệ thống vi lưới độc lập biển đảo 100% NLTT, đảm bảo thuật toán hội tụ tối ưu.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793461387216_8343f2e4.png',
        'duration': 5
    },
    {
        'title': '8. KẾT QUẢ MÔ PHỎNG TỔNG THỂ & DÒNG TIỀN VÒNG ĐỜI (CASH FLOW)',
        'subtitle': 'Thuật toán Cycle Charging (CC) | 100% Năng lượng tái tạo sạch (Renewable Fraction: 100%)',
        'info': 'Biểu đồ dòng tiền 25 năm thể hiện rõ vốn đầu tư ban đầu CAPEX, chi phí thay thế pin năm thứ 10 và giá trị thu hồi cuối kỳ.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793461424332_f7bc97bc.jpg',
        'duration': 7
    },
    {
        'title': '9. BẢNG CHỈ TIÊU KINH TẾ KỸ THUẬT HOMER PRO',
        'subtitle': 'NPC: 9,40 triệu USD (~235 tỷ VNĐ) | LCOE: 0,235 USD/kWh (~5.875 đ/kWh) | CAPEX: 7,08 triệu USD (~177 tỷ VNĐ)',
        'info': 'Sản lượng gió: 7.237.000 kWh/năm | Sản lượng PV: 344.681 kWh/năm. Hoàn vốn nhanh ~4,5 năm so với chạy dầu diesel.',
        'image': r'C:\Users\behuo\.gemini\antigravity\brain\6c1d5399-30a4-4975-bbbd-0280d08423e8\.user_uploaded\media_1793461618843_36459a42.png',
        'duration': 8
    },
    {
        'title': 'KẾT LUẬN & HƯỚNG PHÁT TRIỂN',
        'subtitle': 'Hệ thống Microgrid đảo ST - Giai đoạn 3 hoàn toàn khả thi về kỹ thuật và tối ưu kinh tế',
        'info': 'Đảm bảo tự chủ an ninh năng lượng xanh ngoài đảo xa, giảm triệt để phát thải CO2.\nXin chân thành cảm ơn Thầy và các bạn đã theo dõi!',
        'image': None,
        'duration': 5
    }
]

# Create slide images
slide_files = []
for i, s in enumerate(scenes):
    im = create_base()
    draw = ImageDraw.Draw(im)

    # Header bar
    draw.rectangle([0, 0, W, 100], fill=(24, 43, 73))
    # Title text
    draw.text((60, 30), s['title'], fill=(255, 255, 255))

    # Subtitle
    draw.rectangle([0, 100, W, 170], fill=(235, 240, 248))
    draw.text((60, 120), s['subtitle'], fill=(18, 52, 102))

    # Content
    if s['image'] and os.path.exists(s['image']):
        try:
            content_img = Image.open(s['image'])
            # resize maintaining aspect ratio to fit inside (1800, 780)
            target_w, target_h = 1800, 780
            content_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            # paste centered
            pos_x = (W - content_img.width) // 2
            pos_y = 180 + (target_h - content_img.height) // 2
            # shadow box
            draw.rectangle([pos_x - 5, pos_y - 5, pos_x + content_img.width + 5, pos_y + content_img.height + 5], fill=(200, 210, 225))
            im.paste(content_img, (pos_x, pos_y))
        except Exception as e:
            print('Error loading image:', e)
    else:
        # Title slide / Conclusion slide text
        draw.text((120, 350), s['subtitle'], fill=(20, 35, 60))
        draw.text((120, 520), s['info'], fill=(60, 80, 110))

    # Footer bar
    draw.rectangle([0, H - 90, W, H], fill=(24, 43, 73))
    draw.text((60, H - 65), s['info'].split('\n')[0], fill=(210, 225, 245))
    draw.text((W - 350, H - 65), f'Phần {i+1} / {len(scenes)}', fill=(255, 255, 255))

    slide_path = os.path.join(frames_dir, f'slide_{i:02d}.png')
    im.save(slide_path)
    slide_files.append((slide_path, s['duration']))

print(f'Created {len(slide_files)} slide images.')

# Build concat file for ffmpeg
with open('concat_slides.txt', 'w', encoding='utf-8') as f:
    for path, dur in slide_files:
        p = path.replace('\\', '/')
        f.write(f"file '{p}'\n")
        f.write(f"duration {dur}\n")
    # last frame repeat
    f.write(f"file '{slide_files[-1][0].replace('\\', '/')}'\n")

print('Wrote concat_slides.txt')

