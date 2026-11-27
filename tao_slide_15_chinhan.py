# -*- coding: utf-8 -*-
"""Dựng 15 slide thuyết trình Đồ án 2 (ST - Giai đoạn 3, Côn Đảo) theo chuẩn StageDeck 16:9."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"D:\Du an\code\chinhan")
PPT_TOOLS = Path(r"D:\Tai lieu\second-brain\tools\ppt")
LOGO_CTUT = Path(r"D:\Tai lieu\second-brain\templates\word\img\logo-ctut.png")
sys.path.insert(0, str(PPT_TOOLS))

from stage_builder import StageDeck  # noqa: E402

OUT_DIR = ROOT / "HO_SO_NOP_BAO_CAO_CHINH_THUC"
CHART_DIR = ROOT / "_slide_charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
OUT_PPTX = OUT_DIR / "07_Slide_Thuyet_Trinh_15_Trang_ST_Giai_Doan_3.pptx"
OUT_PPTX_ROOT = ROOT / "Slide_Thuyet_Trinh_15_Trang_ST_Giai_Doan_3.pptx"

DATA = json.loads((ROOT / "homer_toi_uu_results.json").read_text(encoding="utf-8"))
BASE = DATA["base_case"]
OPT = DATA["gvhd_top5"][0]
LOWEST = DATA["lowest_npc_overall"]

BG_HEX = "#11192D"
GRID_HEX = "#2E436C"
TXT_HEX = "#D6E0F0"
ACCENT_HEX = "#38BDF8"
OK_HEX = "#10B981"
WARN_HEX = "#F59E0B"
DANGER_HEX = "#EF4444"


def _style_ax(ax, title=""):
    ax.set_facecolor(BG_HEX)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(GRID_HEX)
    ax.tick_params(colors=TXT_HEX, labelsize=10)
    ax.grid(axis="y", color=GRID_HEX, alpha=0.35, linestyle="--")
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color="#F8FAFC", fontsize=12, fontweight="bold", pad=10)


def make_charts():
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    # 1. Chart: Chẩn đoán 4 cấu hình (Unmet % & Excess %)
    c1 = CHART_DIR / "c1_bottleneck.png"
    fig, ax = plt.subplots(figsize=(7.2, 3.85), dpi=220)
    fig.patch.set_facecolor(BG_HEX)
    labels = [
        "Cấu hình ban đầu\n(2 MW Gió, Conv 100kW)",
        "Kịch bản A\n(Conv 2 MW)",
        "NPC thấp nhất\n(2×500 kW Gió)",
        "Cấu hình CHỌN\n(1×500 kW Gió)",
    ]
    unmet = [18.0, 0.0, 0.0, 0.0]
    excess = [58.4, 52.3, 26.14, 6.15]
    x = np.arange(len(labels))
    w = 0.35
    b1 = ax.bar(x - w / 2, unmet, w, label="Thiếu tải Unmet (%)", color=DANGER_HEX)
    b2 = ax.bar(x + w / 2, excess, w, label="Điện dư Excess (%)", color=WARN_HEX)
    b2[3].set_color(OK_HEX)
    ax.axhline(10.0, color=ACCENT_HEX, linestyle="--", linewidth=1.4, label="Giới hạn điện dư ≤ 10 %")
    _style_ax(ax, "So sánh Thiếu tải & Điện dư qua các phương án tối ưu")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.8)
    ax.set_ylabel("Tỷ lệ (%)", color=TXT_HEX, fontsize=10)
    ax.set_ylim(0, 68)
    for bar in list(b1) + list(b2):
        h = bar.get_height()
        lbl = f"{h:.2f}%" if (0 < h < 10 or abs(h - 26.14) < 0.05) else f"{h:.1f}%"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 1.2,
            lbl,
            ha="center",
            va="bottom",
            color="#F8FAFC",
            fontsize=8.8,
            fontweight="bold",
        )
    ax.legend(facecolor=BG_HEX, edgecolor=GRID_HEX, labelcolor=TXT_HEX, fontsize=8.8, loc="upper right")
    fig.tight_layout()
    fig.savefig(c1, dpi=220, facecolor=BG_HEX)
    plt.close(fig)

    # 2. Chart: Cơ cấu sản lượng điện cấu hình chọn
    c2 = CHART_DIR / "c2_generation.png"
    fig, ax = plt.subplots(figsize=(7.2, 3.85), dpi=220)
    fig.patch.set_facecolor(BG_HEX)
    sources = [
        "Điện mặt trời PV\n(1.200 kWp)",
        "Tuabin gió\n(1 × 500 kW)",
        "Máy phát Diesel\n(970 kW dự phòng)",
        "Phụ tải tiêu thụ\n(Đáp ứng 100%)",
        "Điện dư cắt giảm\n(6,15 % ≤ 10 %)",
    ]
    vals = [
        OPT["pv_prod"] / 1e6,
        OPT["wind_prod"] / 1e6,
        OPT["gen_prod"] / 1e6,
        OPT["served"] / 1e6,
        OPT["excess_kwh"] / 1e6,
    ]
    cols = [WARN_HEX, ACCENT_HEX, "#64748B", OK_HEX, "#38BDF8"]
    bars = ax.barh(sources[::-1], vals[::-1], color=cols[::-1], height=0.58)
    _style_ax(ax, "Cân bằng sản lượng điện năm — Cấu hình chọn (GWh/năm)")
    ax.grid(axis="x", color=GRID_HEX, alpha=0.35, linestyle="--")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Sản lượng (GWh/năm)", color=TXT_HEX, fontsize=10)
    ax.set_xlim(0, 4.75)
    tot = OPT["total_prod"] / 1e6
    for bar, v in zip(bars, vals[::-1]):
        pct = (v / tot) * 100
        ax.text(
            v + 0.07,
            bar.get_y() + bar.get_height() / 2,
            f"{v:.2f} GWh ({pct:.1f}%)",
            va="center",
            color="#F8FAFC",
            fontsize=9.2,
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(c2, dpi=220, facecolor=BG_HEX)
    plt.close(fig)

    # 3. Chart: Hiệu quả Kinh tế (CAPEX, NPC, LCOE)
    c3 = CHART_DIR / "c3_economics.png"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.85), dpi=220, gridspec_kw={"width_ratios": [1.45, 1]})
    fig.patch.set_facecolor(BG_HEX)
    cats = ["Base Case\nDiesel", "Cấu hình\nban đầu*", "Cấu hình\nCHỌN"]
    capex = [BASE["capex"] / 1e6, 7.07868, OPT["capex"] / 1e6]
    npc = [BASE["npc"] / 1e6, 9.402682, OPT["npc"] / 1e6]
    x = np.arange(len(cats))
    w = 0.36
    r1 = ax1.bar(x - w / 2, capex, w, label="CAPEX (Triệu USD)", color=ACCENT_HEX)
    r2 = ax1.bar(x + w / 2, npc, w, label="NPC 25 năm (Triệu USD)", color=WARN_HEX)
    r2[2].set_color(OK_HEX)
    _style_ax(ax1, "Vốn đầu tư & NPC (Triệu USD)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(cats, fontsize=8.8)
    ax1.set_ylim(0, 23.0)
    for bar in list(r1) + list(r2):
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.35,
            f"${h:.2f}M",
            ha="center",
            va="bottom",
            color="#F8FAFC",
            fontsize=8.4,
            fontweight="bold",
        )
    ax1.legend(facecolor=BG_HEX, edgecolor=GRID_HEX, labelcolor=TXT_HEX, fontsize=8.2, loc="upper right")

    lcoe = [BASE["coe"], 0.2351, OPT["coe"]]
    r3 = ax2.bar(cats, lcoe, width=0.52, color=[DANGER_HEX, "#64748B", OK_HEX])
    _style_ax(ax2, "Giá điện LCOE ($/kWh)")
    ax2.set_xticks(range(len(cats)))
    ax2.set_xticklabels(cats, fontsize=8.8)
    ax2.set_ylim(0, 0.48)
    for bar in r3:
        h = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.012,
            f"${h:.4f}",
            ha="center",
            va="bottom",
            color="#F8FAFC",
            fontsize=8.8,
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(c3, dpi=220, facecolor=BG_HEX)
    plt.close(fig)

    # 4. Chart: Nhiên liệu & Phát thải CO2
    c4 = CHART_DIR / "c4_environment.png"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.85), dpi=220)
    fig.patch.set_facecolor(BG_HEX)
    f_vals = [BASE["fuel_l"] / 1000.0, OPT["fuel_l"] / 1000.0]
    f_bars = ax1.bar(["Base Case\nDiesel", "Cấu hình\nCHỌN"], f_vals, width=0.5, color=[DANGER_HEX, OK_HEX])
    _style_ax(ax1, "Dầu Diesel (Nghìn L/năm)")
    ax1.set_ylim(0, 1260)
    for bar in f_bars:
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 25,
            f"{h:,.1f}k L",
            ha="center",
            va="bottom",
            color="#F8FAFC",
            fontsize=9.8,
            fontweight="bold",
        )
    ax1.annotate(
        "-78,5 %",
        xy=(1, f_vals[1] + 35),
        xytext=(0.45, 760),
        arrowprops=dict(arrowstyle="->", color=ACCENT_HEX, lw=1.6),
        color=ACCENT_HEX,
        fontsize=11,
        fontweight="bold",
    )

    e_vals = [BASE["co2_kg"] / 1000.0, OPT["co2_kg"] / 1000.0]
    e_bars = ax2.bar(["Base Case\nDiesel", "Cấu hình\nCHỌN"], e_vals, width=0.5, color=[DANGER_HEX, OK_HEX])
    _style_ax(ax2, "Phát thải CO₂ (Tấn/năm)")
    ax2.set_ylim(0, 3260)
    for bar in e_bars:
        h = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            h + 65,
            f"{h:,.1f} t",
            ha="center",
            va="bottom",
            color="#F8FAFC",
            fontsize=9.8,
            fontweight="bold",
        )
    ax2.annotate(
        "Tránh\n2.167,5 t/năm",
        xy=(1, e_vals[1] + 80),
        xytext=(0.28, 1850),
        arrowprops=dict(arrowstyle="->", color=OK_HEX, lw=1.6),
        color=OK_HEX,
        fontsize=10.2,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(c4, dpi=220, facecolor=BG_HEX)
    plt.close(fig)

    # 5. Chart: Mùa gió & nắng bổ trợ tại vùng biển Côn Đảo
    c5 = CHART_DIR / "c5_season.png"
    fig, ax = plt.subplots(figsize=(7.2, 3.85), dpi=220)
    fig.patch.set_facecolor(BG_HEX)
    months = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]
    wind_ms = [10.9, 10.8, 7.8, 4.97, 5.1, 7.4, 8.2, 8.5, 7.6, 6.9, 8.9, 11.0]
    ax.plot(months, wind_ms, marker="o", linewidth=2.4, color=ACCENT_HEX, label="Tốc độ gió đặc trưng theo mùa (m/s)")
    ax.fill_between(months, wind_ms, color=ACCENT_HEX, alpha=0.14)
    ax.axvspan(3, 4.3, color=WARN_HEX, alpha=0.18, label="Vùng lặng gió T4–T5 (~4,97 m/s) → PV + Diesel gánh")
    ax.axvspan(10.7, 11.4, color=OK_HEX, alpha=0.16, label="Mùa gió Đông Bắc T12–T2 (~10,8–11,0 m/s)")
    ax.axvspan(-0.4, 1.3, color=OK_HEX, alpha=0.16)
    _style_ax(ax, "Tính biến động mùa gió tại Côn Đảo — Lý do cần phối hợp Hybrid")
    ax.set_ylabel("Tốc độ gió (m/s)", color=TXT_HEX, fontsize=10)
    ax.set_ylim(0, 13.2)
    ax.legend(facecolor=BG_HEX, edgecolor=GRID_HEX, labelcolor=TXT_HEX, fontsize=8.4, loc="lower left")
    fig.tight_layout()
    fig.savefig(c5, dpi=220, facecolor=BG_HEX)
    plt.close(fig)

    return c1, c2, c3, c4, c5


def add_image_and_notes(deck, kicker, title, img_path, right_title, bullets, slide_no, img_caption=None):
    s = deck._new_slide()
    deck._add_header_and_footer(s, kicker, title, slide_no)
    deck._rect(s, 0.55, 1.34, 7.55, 5.28, deck.t["panel"], border_rgb=deck.t["border"], border_pt=1.0)
    p = Path(img_path)
    if p.exists():
        with Image.open(p) as im:
            iw, ih = im.size
        box_w, box_h = 7.25, 4.68 if img_caption else 5.00
        scale = min(box_w / iw, box_h / ih)
        pw, ph = iw * scale, ih * scale
        px = 0.55 + (7.55 - pw) / 2
        py = 1.34 + ((4.88 if img_caption else 5.28) - ph) / 2
        s.shapes.add_picture(str(p), Inches(px), Inches(py), width=Inches(pw), height=Inches(ph))
    if img_caption:
        deck._text(s, 0.70, 6.24, 7.25, 0.32, img_caption, size=10.2, color=deck.t["muted"], align=PP_ALIGN.CENTER)

    deck._rect(s, 8.32, 1.34, 4.46, 5.28, deck.t["panel_hi"], border_rgb=deck.t["accent"], border_pt=1.0)
    deck._text(s, 8.54, 1.50, 4.02, 0.36, right_title.upper(), size=11.5, bold=True, color=deck.t["accent"])
    tb = s.shapes.add_textbox(Inches(8.54), Inches(1.94), Inches(4.02), Inches(4.52))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, (head, desc) in enumerate(bullets[:5]):
        par = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        par.space_after = Pt(10)
        r1 = par.add_run()
        r1.text = f"▸ {head}: "
        r1.font.name, r1.font.size, r1.font.bold, r1.font.color.rgb = deck.t["font"], Pt(12), True, deck.t["title"]
        r2 = par.add_run()
        r2.text = desc
        r2.font.name, r2.font.size, r2.font.color.rgb = deck.t["font"], Pt(11.5), deck.t["text"]
    return s


def add_ctut_cover(deck):
    """Slide 01: Slide Bìa CTUT chuẩn sân khấu 16:9 có Logo CTUT, Trường/Khoa, tên đề tài và 4 KPI."""
    s = deck._new_slide()
    # Dải nhấn trên cùng + khung header Trường/Khoa với Logo CTUT
    deck._rect(s, 0.0, 0.0, 13.333, 0.11, deck.t["accent"], rounded=False, name="!!morph_topband")
    deck._rect(s, 0.68, 0.34, 11.97, 1.18, deck.t["panel"], border_rgb=deck.t["border"], border_pt=1.0)
    # Huy hiệu nền trắng bo tròn đặt logo CTUT sắc nét trên nền tối
    deck._rect(s, 0.86, 0.44, 0.98, 0.98, RGBColor(255, 255, 255), border_rgb=deck.t["accent"], border_pt=1.4)
    if LOGO_CTUT.exists():
        s.shapes.add_picture(str(LOGO_CTUT), Inches(0.92), Inches(0.50), width=Inches(0.86), height=Inches(0.86))
    deck._text(s, 2.02, 0.48, 7.30, 0.38, "TRƯỜNG ĐẠI HỌC KỸ THUẬT – CÔNG NGHỆ CẦN THƠ",
               size=15.5, bold=True, color=deck.t["title"])
    deck._text(s, 2.02, 0.86, 7.30, 0.34, "KHOA ĐIỆN – ĐIỆN TỬ  ·  NGÀNH CÔNG NGHỆ KỸ THUẬT NĂNG LƯỢNG",
               size=12, bold=True, color=deck.t["accent"])
    # Huy hiệu bên phải header
    deck._rect(s, 9.65, 0.60, 2.78, 0.56, deck.t["panel_hi"], border_rgb=deck.t["accent"],
               border_pt=1.1, name="!!morph_kicker")
    deck._text(s, 9.73, 0.70, 2.62, 0.36, "BẢO VỆ ĐỒ ÁN 2 · K2023", size=11.5, bold=True,
               color=deck.t["accent"], align=PP_ALIGN.CENTER)

    # Khối tiêu đề chính
    deck._rect(s, 0.68, 1.82, 0.13, 2.22, deck.t["accent"], rounded=False, name="!!morph_bar")
    deck._text(s, 1.00, 1.80, 11.6, 1.38,
               "MÔ PHỎNG HỆ THỐNG MICROGRID\nĐẢO ST – GIAI ĐOẠN 3 (CÔN ĐẢO)",
               size=34, bold=True, color=deck.t["title"])
    deck._text(s, 1.00, 3.24, 11.4, 0.72,
               "Tối ưu hóa hệ thống Hybrid PV – Gió – BESS – Diesel trên HOMER Pro x64 v3.18.5\nđạt đồng thời chuẩn kỹ thuật 0,00 % thiếu tải và ≤ 10 % điện dư cắt giảm",
               size=15, color=deck.t["text"])

    # 4 thẻ KPI nổi bật
    pills = [
        ("THIẾU TẢI (UNMET)", "0,00 %", "ok"),
        ("ĐIỆN DƯ (EXCESS)", "6,15 %", "accent"),
        ("GIÁ ĐIỆN (LCOE)", "$0,2367/kWh", "warn"),
        ("GIẢM PHÁT THẢI CO₂", "-2.167,5 t/năm", "ok"),
    ]
    cw, gap = 2.81, 0.24
    for i, (lbl, val, tone) in enumerate(pills):
        cx = 0.68 + i * (cw + gap)
        col = deck.t.get(tone, deck.t["accent"])
        deck._rect(s, cx, 4.34, cw, 1.32, deck.t["panel"], border_rgb=col, border_pt=1.25, name=f"!!morph_kpi_{i}")
        deck._rect(s, cx, 4.34, cw, 0.08, col, rounded=False)
        deck._text(s, cx + 0.18, 4.50, cw - 0.36, 0.28, lbl, size=10.5, bold=True, color=deck.t["muted"])
        deck._text(s, cx + 0.18, 4.84, cw - 0.36, 0.62, val, size=22, bold=True, color=col)

    # Thanh chân bìa trang trọng
    deck._rect(s, 0.68, 6.08, 11.97, 0.92, deck.t["panel_hi"], border_rgb=deck.t["border"], border_pt=1.0)
    deck._text(s, 0.92, 6.20, 4.40, 0.32, "SINH VIÊN THỰC HIỆN", size=10, bold=True, color=deck.t["muted"])
    deck._text(s, 0.92, 6.48, 4.40, 0.38, "Đào Chí Nhân  (KTNL – K2023)", size=13.5, bold=True, color=deck.t["title"])
    deck._text(s, 5.45, 6.20, 4.20, 0.32, "GIẢNG VIÊN HƯỚNG DẪN", size=10, bold=True, color=deck.t["muted"])
    deck._text(s, 5.45, 6.48, 4.20, 0.38, "TS. Trần Hữu Tính", size=13.5, bold=True, color=deck.t["accent"])
    deck._text(s, 9.75, 6.20, 2.68, 0.32, "ĐỊA ĐIỂM & NĂM", size=10, bold=True, color=deck.t["muted"], align=PP_ALIGN.RIGHT)
    deck._text(s, 9.75, 6.48, 2.68, 0.38, "Cần Thơ, năm 2026", size=13.5, bold=True, color=deck.t["title"], align=PP_ALIGN.RIGHT)
    return s


def add_thank_you_slide(deck, slide_no=16):
    """Slide 16: Slide Chào & Cảm ơn Hội đồng trang trọng cho phần Q&A."""
    s = deck._new_slide()
    deck._rect(s, 0.0, 0.0, 13.333, 0.11, deck.t["accent"], rounded=False, name="!!morph_topband")
    deck._rect(s, 0.72, 0.48, 11.89, 5.96, deck.t["panel"], border_rgb=deck.t["border"], border_pt=1.1)
    deck._rect(s, 0.72, 0.48, 11.89, 0.09, deck.t["accent"], rounded=False)

    # Logo CTUT trung tâm trên khung nền trắng sang trọng
    deck._rect(s, 6.08, 0.84, 1.18, 1.18, RGBColor(255, 255, 255), border_rgb=deck.t["accent"], border_pt=1.5)
    if LOGO_CTUT.exists():
        s.shapes.add_picture(str(LOGO_CTUT), Inches(6.16), Inches(0.92), width=Inches(1.02), height=Inches(1.02))

    deck._text(s, 1.10, 2.20, 11.13, 0.34,
               "TRƯỜNG ĐẠI HỌC KỸ THUẬT – CÔNG NGHỆ CẦN THƠ  ·  KHOA ĐIỆN – ĐIỆN TỬ",
               size=12, bold=True, color=deck.t["accent"], align=PP_ALIGN.CENTER, name="!!morph_kicker")
    deck._text(s, 1.00, 2.62, 11.33, 1.25,
               "TRÂN TRỌNG CẢM ƠN\nQUÝ THẦY/CÔ HỘI ĐỒNG ĐÃ LẮNG NGHE!",
               size=32, bold=True, color=deck.t["title"], align=PP_ALIGN.CENTER)
    deck._text(s, 1.30, 3.96, 10.73, 0.50,
               "Kính mời Quý Thầy/Cô đặt câu hỏi và đóng góp ý kiến để đồ án được hoàn thiện hơn.",
               size=15.5, color=deck.t["text"], align=PP_ALIGN.CENTER)

    # 3 chip tóm tắt thông điệp chốt nhanh khi đứng Q&A
    chips = [
        ("CẤU HÌNH TỐI ƯU", "1.200 kWp PV · 500 kW Gió · 6 MWh BESS", "ok"),
        ("CHUẨN KỸ THUẬT", "0,00 % Thiếu tải · 6,15 % Điện dư", "accent"),
        ("HIỆU QUẢ KINH TẾ – XANH", "NPC -40,7 % · Tránh 2.167,5 t CO₂/năm", "warn"),
    ]
    cw, gap = 3.56, 0.24
    start_x = 1.06
    for i, (lbl, val, tone) in enumerate(chips):
        cx = start_x + i * (cw + gap)
        col = deck.t.get(tone, deck.t["accent"])
        deck._rect(s, cx, 4.76, cw, 1.18, deck.t["panel_hi"], border_rgb=col, border_pt=1.2, name=f"!!morph_kpi_{i}")
        deck._rect(s, cx, 4.76, 0.08, 1.18, col, rounded=False)
        deck._text(s, cx + 0.20, 4.90, cw - 0.34, 0.28, lbl, size=10.5, bold=True, color=col)
        deck._text(s, cx + 0.20, 5.22, cw - 0.34, 0.56, val, size=12.5, bold=True, color=deck.t["title"])

    # Footer riêng
    deck._text(s, 0.72, 6.70, 9.80, 0.36,
               "Đào Chí Nhân (KTNL K2023)  ·  GVHD: TS. Trần Hữu Tính  ·  Đồ án 2 – Microgrid Đảo ST",
               size=11, color=deck.t["muted"])
    deck._text(s, 11.2, 6.70, 1.40, 0.36, f"{slide_no:02d}", size=11, bold=True,
               color=deck.t["muted"], align=PP_ALIGN.RIGHT)
    return s


def build_deck():
    c1, c2, c3, c4, c5 = make_charts()
    deck = StageDeck(
        theme="dark-stage",
        footer_left="Đồ án 2 · Microgrid Đảo ST – Giai đoạn 3 (Côn Đảo) · Đào Chí Nhân",
        author="Đào Chí Nhân",
    )

    # Slide 1: Slide Bìa CTUT có Logo + Trường/Khoa + 4 KPI
    add_ctut_cover(deck)

    # Slide 2: Bối cảnh & Bài toán cấp điện đảo ST
    add_image_and_notes(
        deck,
        kicker="01 · Bối cảnh & Đặt vấn đề",
        title="Bài toán cấp điện độc lập cho khu vực đảo ST (gần Côn Đảo)",
        img_path=ROOT / "con_dao_region.png",
        right_title="Mục tiêu & Ràng buộc đề tài",
        bullets=[
            ("Đặc thù lưới đảo", "Cách xa đất liền, không nối lưới quốc gia; chạy thuần Diesel tốn >1,05 triệu L dầu/năm (LCOE $0,3990/kWh)."),
            ("Nhu cầu phụ tải năm", "3.773.005 kWh/năm (~10.337 kWh/ngày), công suất đỉnh 776,0 kW."),
            ("Ràng buộc kỹ thuật", "Đáp ứng 100 % phụ tải (Unmet = 0,00 %) và khống chế điện dư cắt giảm ≤ 10 %."),
            ("Mục tiêu 3 trụ cột", "Đánh giá toàn diện Kỹ thuật – Kinh tế (NPC/LCOE/IRR) – Môi trường (CO₂)."),
        ],
        slide_no=2,
        img_caption="Vị trí khu vực nghiên cứu đảo ST – vùng biển gần Côn Đảo",
    )

    # Slide 3: Tổng quan cấu hình Microgrid Off-grid (Chương 1)
    deck.add_cards(
        kicker="02 · Chương 1 – Tổng quan cấu hình Off-grid",
        title="So sánh 3 kiến trúc lưới điện độc lập cho hải đảo",
        cards=[
            (
                "Cấu hình 1 · Base Case",
                "Thuần Diesel dự phòng",
                [
                    "Vốn đầu tư ban đầu thấp ($1,185M).",
                    "Phụ thuộc hoàn toàn vận chuyển nhiên liệu ra đảo.",
                    "Chi phí vận hành cực cao: NPC $19,46M, LCOE $0,3990/kWh.",
                    "Phát thải lớn: 2.759,5 tấn CO₂/năm.",
                ],
                "danger",
            ),
            (
                "Cấu hình 2 · 100 % NLTT",
                "PV + Gió + BESS (Không Diesel)",
                [
                    "Phát thải tại chỗ bằng 0.",
                    "Phải thiết kế dư nguồn lớn để vượt tháng 4–5 lặng gió.",
                    "Điện dư cắt giảm tối thiểu ~35,1–58,4 % (> 10 %).",
                    "Vốn đầu tư CAPEX đội cao ($7,08M trở lên).",
                ],
                "warn",
            ),
            (
                "Cấu hình 3 · Chọn tối ưu",
                "Hybrid PV + Gió + BESS + Diesel",
                [
                    "Khai thác bổ trợ nắng – gió, tỷ lệ tái tạo đạt 78,9 %.",
                    "Diesel 970 kW chỉ chạy dự phòng 2.425 giờ/năm.",
                    "Đạt đồng thời 0,00 % thiếu tải & 6,15 % điện dư.",
                    "Giảm 40,7 % NPC/LCOE và tránh 2.167,5 tấn CO₂/năm.",
                ],
                "ok",
            ),
        ],
        slide_no=3,
    )

    # Slide 4: Đặc điểm khí tượng & tính bổ trợ mùa
    deck.add_kpi_and_chart(
        kicker="03 · Đặc trưng tài nguyên thiên nhiên",
        title="Biến động mùa gió Côn Đảo — Lý do cần phối hợp nguồn Hybrid",
        kpis=[
            ("PHỤ TẢI NĂM", "3,773 GWh", "Đỉnh 776,0 kW", "accent"),
            ("GIÓ MÙA ĐÔNG BẮC", "10,8–11,0 m/s", "Tháng 12 – Tháng 2", "ok"),
            ("MÙA LẶNG GIÓ", "4,97 m/s", "Tháng 4 – Tháng 5", "warn"),
            ("BỔ TRỢ NGUỒN", "PV + BESS", "Gánh tải mùa lặng gió", "accent"),
        ],
        chart_path=c5,
        bullets=[
            ("Phân hóa mùa mạnh", "Gió đạt đỉnh 10,8–11,0 m/s vào T12–T2 nhưng tụt xuống ~4,97 m/s vào T4–T5."),
            ("Hệ quả nếu lắp gió quá lớn", "1 tuabin 2 MW phát dư tới 58,4 % vào mùa gió mạnh nhưng vẫn thiếu khi lặng gió."),
            ("Giải pháp cân bằng", "Hạ quy mô gió về 1 × 500 kW, kết hợp 1.200 kWp PV + 6.000 kWh BESS và Diesel dự phòng."),
        ],
        slide_no=4,
    )

    # Slide 5: Sơ đồ nguyên lý & Kiến trúc hệ thống
    add_image_and_notes(
        deck,
        kicker="04 · Kiến trúc hệ thống (Bản vẽ 34-ST)",
        title="Sơ đồ nguyên lý Microgrid AC/DC Bus & Chiến lược điều độ",
        img_path=OUT_DIR / "05_Hinh_Anh_Ket_Qua_HOMER_Pro" / "st_diagram.png",
        right_title="Phân tầng thanh cái & Điều độ",
        bullets=[
            ("Thanh cái AC (AC Bus)", "Đấu nối trực tiếp phụ tải đảo ST (776 kW đỉnh), Tuabin gió 500 kW và Máy phát Diesel 970 kW."),
            ("Thanh cái DC (DC Bus)", "Đấu nối giàn pin mặt trời 1.200 kWp và hệ lưu trữ 60 khối BESS Li-ion 6.000 kWh."),
            ("Bộ biến đổi 2 chiều", "Converter 800 kW (nâng từ 100 kW gốc) — xóa hoàn toàn nghẽn công suất truyền DC ↔ AC."),
            ("Chiến lược Load Following", "Máy phát Diesel chỉ phát đúng phần thiếu tải, nhường nạp BESS cho PV và Gió."),
        ],
        slide_no=5,
        img_caption="Sơ đồ nguyên lý hệ thống Microgrid đảo ST – Giai đoạn 3 (Bản vẽ 34-ST)",
    )

    # Slide 6: Cơ sở toán học (Chương 2)
    deck.add_cards(
        kicker="05 · Chương 2 – Mô hình toán học hệ thống",
        title="Chuẩn hóa 3 nhóm công thức cốt lõi (2.1) – (2.24)",
        cards=[
            (
                "Mục 2.1 · Nguồn phát",
                "Mô hình PV, Gió & Diesel",
                [
                    "Công suất PV theo bức xạ mặt trời, hệ số suy giảm (derating) và hiệu ứng nhiệt độ cell.",
                    "Hiệu chỉnh tốc độ gió theo chiều cao trụ tuabin (hub height 47 m) và đường cong công suất.",
                    "Đường đặc tính tiêu hao nhiên liệu tuyến tính của máy phát Diesel (F₀, F₁).",
                ],
                "accent",
            ),
            (
                "Mục 2.2 · Lưu trữ & Cân bằng",
                "BESS Li-ion & Bộ biến đổi",
                [
                    "Ràng buộc trạng thái sạc SOCmin ≤ SOC(t) ≤ SOCmax, hiệu suất vòng khép kín và luân chuyển năng lượng.",
                    "Cân bằng công suất theo từng giờ (8.760 giờ/năm) qua hiệu suất Inverter/Rectifier.",
                    "Định nghĩa chặt chỉ tiêu Unmet Load (%) và Excess Electricity (%).",
                ],
                "ok",
            ),
            (
                "Mục 2.3 · Kinh tế & Môi trường",
                "NPC, LCOE, IRR & Phát thải",
                [
                    "Tổng chi phí hiện tại ròng NPC quy đổi theo vòng đời 25 năm và hệ số thu hồi vốn CRF.",
                    "Giá thành điện quy dẫn LCOE = Cann,tot / Eserved ($/kWh).",
                    "Tính toán IRR, ROI, thời gian hoàn vốn giản đơn và phát thải CO₂, NOx, SO₂, CO, PM.",
                ],
                "warn",
            ),
        ],
        slide_no=6,
    )

    # Slide 7: Chẩn đoán nút thắt cấu hình ban đầu
    deck.add_kpi_and_chart(
        kicker="06 · Chẩn đoán kỹ thuật",
        title="Vì sao cấu hình ban đầu thiếu tải 18,0 % nhưng vẫn dư điện 58,4 %?",
        kpis=[
            ("THIẾU TẢI GỐC", "18,0 %", "Do nghẽn Converter 100 kW", "danger"),
            ("ĐIỆN DƯ GỐC", "58,4 %", "Cắt giảm 4,43 GWh/năm", "warn"),
            ("PHƯƠNG ÁN 2 TUABIN", "26,14 % dư", "Vượt ngưỡng 10 %", "warn"),
            ("PHƯƠNG ÁN CHỌN", "0 % / 6,15 %", "Đạt chuẩn kỹ thuật", "ok"),
        ],
        chart_path=c1,
        bullets=[
            ("Nút thắt 1 – Converter quá nhỏ", "Converter gốc chỉ 100 kW trong khi đỉnh tải 776 kW → không kịp xả điện từ BESS/PV sang AC."),
            ("Nút thắt 2 – Tuabin quá lớn", "1 tuabin E-82 2.000 kW phát tới 7,24 GWh/năm (gấp đôi phụ tải) → dư 58,4 %."),
            ("Bẫy tối ưu thuần NPC", "Cấu hình 2 × 500 kW gió có NPC thấp nhất ($10,75M) nhưng dư tới 26,14 % > 10 % nên bị loại."),
        ],
        slide_no=7,
    )

    # Slide 8: Thiết lập không gian tìm kiếm HOMER Pro
    deck.add_table_slide(
        kicker="07 · Thiết lập mô phỏng HOMER Pro x64 v3.18.5",
        title="Không gian tìm kiếm & Lọc 454 tổ hợp theo ràng buộc kỹ thuật",
        headers=["Thành phần / Tham số", "Cấu hình ban đầu", "Dải tối ưu HOMER Pro", "Giá trị CHỌN"],
        rows=[
            ["Điện mặt trời (PV)", "Cố định nhỏ", "0 – 1.200 kWp", "1.200 kWp"],
            ["Tuabin gió (Wind)", "1 × Enercon E-82 (2.000 kW)", "0 – 2 × Windflow 45 (500 kW, 47 m)", "1 × 500 kW"],
            ["Lưu trữ pin (BESS Li-ion)", "Nhỏ, thiếu tự chủ", "20 – 117 khối (100 kWh/khối)", "60 khối (6.000 kWh)"],
            ["Bộ biến đổi (Converter)", "100 kW (nghẽn)", "0 – 1.200 kW", "800 kW"],
            ["Máy phát dự phòng (Diesel)", "Không dùng", "Autosize Generator (970 kW)", "970 kW (LF)"],
            ["Ràng buộc & Kết quả lọc", "Thiếu 18,0 % · Dư 58,4 %", "Max Capacity Shortage = 0 % · 454 tổ hợp", "288 cấu hình đạt chuẩn"],
        ],
        note="Kết quả quét thực tế trên HOMER Pro v3.18.5: 454 tổ hợp → 450 khả thi → 288 cấu hình đạt đồng thời 0,00 % thiếu tải và ≤ 10 % điện dư.",
        slide_no=8,
    )

    # Slide 9: Bằng chứng chạy thật HOMER Pro — Bảng tối ưu
    add_image_and_notes(
        deck,
        kicker="08 · Bằng chứng mô phỏng thực tế (HOMER Pro v3.18.5)",
        title="Bảng xếp hạng tối ưu hóa — Quyết định chọn phương án 1 × 500 kW gió",
        img_path=OUT_DIR / "05_Hinh_Anh_Ket_Qua_HOMER_Pro" / "homer_opt_table.png",
        right_title="Giải trình chọn phương án",
        bullets=[
            ("Dòng #1 toàn cục (2 × 500 kW)", "NPC $10,75M, LCOE $0,2204/kWh nhưng điện dư tới 26,14 % — vi phạm ràng buộc ≤ 10 %."),
            ("Phương án chọn (1 × 500 kW)", "Dẫn đầu trong nhóm 288 cấu hình đạt chuẩn kỹ thuật: Unmet 0,00 % và Excess 6,15 %."),
            ("Chi phí đánh đổi hợp lý", "LCOE chỉ nhỉnh $0,0163/kWh (+7,4 %) nhưng giảm CAPEX $961.500 và giảm 81 % lượng điện dư."),
            ("Điều độ Load Following", "Hiệu quả hơn Cycle Charging nhờ không ép máy phát chạy tải cao để nạp pin."),
        ],
        slide_no=9,
        img_caption="Ảnh chụp trực tiếp bảng Optimization Results từ HOMER Pro x64 v3.18.5",
    )

    # Slide 10: Bằng chứng chạy thật HOMER Pro — Tóm tắt cấu hình chọn
    add_image_and_notes(
        deck,
        kicker="09 · Bằng chứng mô phỏng thực tế (HOMER Pro v3.18.5)",
        title="Chi tiết cấu hình tối ưu chọn: 1.200 kWp PV · 500 kW Gió · 6 MWh BESS",
        img_path=OUT_DIR / "05_Hinh_Anh_Ket_Qua_HOMER_Pro" / "homer_opt_summary.png",
        right_title="Thông số vận hành then chốt",
        bullets=[
            ("Tổng sản lượng phát", "4.233.058 kWh/năm phục vụ 3.773.005 kWh/năm phụ tải (0 kWh thiếu)."),
            ("Hiệu quả BESS 6.000 kWh", "Thời gian tự chủ 11,14 giờ; điện năng luân chuyển 961.779 kWh/năm."),
            ("Vận hành máy phát 970 kW", "Chỉ chạy 2.425 giờ/năm (giảm 44,1 % so với 4.342 giờ của Base Case)."),
            ("Tính khả thi tài chính", "IRR = 18,9 %, ROI = 15,0 %, hoàn vốn giản đơn 5,02 năm (chiết khấu 6,28 năm)."),
        ],
        slide_no=10,
        img_caption="Ảnh chụp trực tiếp Simulation Summary của cấu hình chọn trên HOMER Pro v3.18.5",
    )

    # Slide 11: Trụ cột 1 — Kỹ thuật & Cơ cấu sản lượng
    deck.add_kpi_and_chart(
        kicker="10 · Trụ cột 1 – Đánh giá Kỹ thuật",
        title="Cân bằng năng lượng: Tái tạo chiếm 78,9 %, điện dư chỉ 6,15 %",
        kpis=[
            ("TỶ LỆ TÁI TẠO (RF)", "78,9 %", "PV 45,8 % + Gió 35,4 %", "ok"),
            ("ĐÁP ỨNG PHỤ TẢI", "100,0 %", "0 kWh thiếu tải/năm", "ok"),
            ("ĐIỆN DƯ CẮT GIẢM", "6,15 %", "260.422 kWh (≤ 10 %)", "accent"),
            ("TỰ CHỦ BESS", "11,14 giờ", "Luân chuyển 961,8 MWh", "warn"),
        ],
        chart_path=c2,
        bullets=[
            ("Đóng góp PV (1,94 GWh)", "Chiếm 45,8 % tổng phát — cung cấp nền ổn định vào ban ngày và mùa lặng gió."),
            ("Đóng góp Gió (1,50 GWh)", "Chiếm 35,4 % tổng phát — phát mạnh về đêm và mùa gió Đông Bắc."),
            ("Dự phòng Diesel (0,80 GWh)", "Chỉ chiếm 18,8 % — đảm bảo an ninh cấp điện 100 % khi âm u/lặng gió kéo dài."),
        ],
        slide_no=11,
    )

    # Slide 12: Trụ cột 2 — Kinh tế vòng đời
    deck.add_kpi_and_chart(
        kicker="11 · Trụ cột 2 – Đánh giá Kinh tế (25 năm)",
        title="Giảm 40,7 % tổng chi phí NPC và giá điện LCOE so với Base Case",
        kpis=[
            ("CAPEX ĐẦU TƯ", "$5,95M", "Giảm 16,0 % so bản đầu", "accent"),
            ("NPC 25 NĂM", "$11,54M", "Tiết kiệm $7,92M (-40,7 %)", "ok"),
            ("GIÁ ĐIỆN LCOE", "$0,2367", "Giảm từ $0,3990 (-40,7 %)", "ok"),
            ("HOÀN VỐN / IRR", "5,02 năm", "IRR 18,9 % · ROI 15,0 %", "warn"),
        ],
        chart_path=c3,
        bullets=[
            ("Vượt trội Base Case", "Tuy CAPEX cao hơn Diesel thuần ($5,95M vs $1,19M), chi phí vận hành giảm mạnh từ $1,41M xuống $0,43M/năm."),
            ("Tiết kiệm vốn hơn bản gốc", "Bỏ tuabin 2 MW dư thừa giúp giảm $1,13M vốn đầu tư ban đầu (-16,0 %)."),
            ("Giá trị hiện tại ròng", "Present Worth đạt +$6,94M sau 25 năm vận hành — dự án khả thi cao."),
        ],
        slide_no=12,
    )

    # Slide 13: Trụ cột 3 — Nhiên liệu & Môi trường
    deck.add_kpi_and_chart(
        kicker="12 · Trụ cột 3 – Đánh giá Môi trường",
        title="Cắt giảm 78,5 % dầu Diesel và tránh 2.167,5 tấn CO₂ mỗi năm",
        kpis=[
            ("TIẾT KIỆM DẦU", "828.050 L", "Mỗi năm (-78,5 %)", "ok"),
            ("TRÁNH PHÁT THẢI CO₂", "2.167,5 tấn", "2.759,5 → 592,0 t/năm", "ok"),
            ("GIẢM NOx / SO₂", "-78,5 %", "Bảo vệ hệ sinh thái đảo", "accent"),
            ("GIỜ CHẠY DIESEL", "2.425 h/năm", "Giảm 1.917 h/năm", "warn"),
        ],
        chart_path=c4,
        bullets=[
            ("Giảm rủi ro hậu cần biển", "Giảm từ 1.054.193 L xuống 226.143 L/năm, hạn chế phụ thuộc tàu chở dầu mùa biển động."),
            ("Phát thải trong 25 năm", "Tránh tích lũy hơn 54.187 tấn CO₂ trong suốt vòng đời dự án."),
            ("Giảm tiếng ồn & bảo dưỡng", "Số giờ chạy máy phát giảm 44,1 %, kéo dài tuổi thọ tổ máy phát Diesel."),
        ],
        slide_no=13,
    )

    # Slide 14: Bảng đối chiếu tổng hợp 3 trụ cột
    deck.add_table_slide(
        kicker="13 · Tổng hợp đối chiếu 3 trụ cột",
        title="Bảng so sánh toàn diện: Base Case Diesel vs Ban đầu vs Chọn tối ưu",
        headers=["Trụ cột", "Chỉ tiêu", "Base Case Diesel", "Cấu hình ban đầu", "Cấu hình CHỌN"],
        rows=[
            ["Kỹ thuật", "Thiếu tải / Đáp ứng", "0,00 % / 100 %", "18,0 % / 82,0 %", "0,00 % / 100,0 %"],
            ["Kỹ thuật", "Điện dư cắt giảm", "0,00 %", "58,4 %", "6,15 % (≤ 10 %)"],
            ["Kỹ thuật", "Tỷ lệ tái tạo (RF)", "0,0 %", "100 % (thiếu tải)", "78,9 %"],
            ["Kinh tế", "CAPEX (USD)", "$1.185.000", "$7.078.680", "$5.946.500 (-16,0 %)"],
            ["Kinh tế", "NPC 25 năm (USD)", "$19.462.122", "$9.402.682*", "$11.544.581 (-40,7 %)"],
            ["Kinh tế", "LCOE (USD/kWh)", "$0,3990", "$0,2351*", "$0,2367 (-40,7 %)"],
            ["Môi trường", "Dầu / Phát thải CO₂", "1,05M L · 2.759,5 t", "0 L · cắt 4,43 GWh", "226k L · 592,0 t (-78,5 %)"],
        ],
        note="Đã hoàn thành 6/6 góp ý của TS. Trần Hữu Tính: tách sạch Chương 1–3, công thức (2.1)–(2.24), chạy thật HOMER Pro v3.18.5, báo cáo chuẩn CTUT 100/100.",
        slide_no=14,
    )

    # Slide 15: Kết luận, Kiến nghị & Hỏi đáp Hội đồng
    deck.add_cards(
        kicker="14 · Kết luận – Kiến nghị & Q&A Hội đồng",
        title="Tổng kết đóng góp đề tài & Sẵn sàng phản biện Hội đồng",
        cards=[
            (
                "Kết luận đạt được",
                "Giải trọn bài toán 3 trụ cột",
                [
                    "Cấu hình tối ưu: 1.200 kWp PV + 500 kW Gió + 6.000 kWh BESS + 970 kW Diesel + 800 kW Converter.",
                    "Đạt 0,00 % thiếu tải, 6,15 % điện dư, RF = 78,9 %.",
                    "NPC giảm 40,7 %, LCOE $0,2367/kWh, hoàn vốn 5,02 năm, tránh 2.167,5 t CO₂/năm.",
                ],
                "ok",
            ),
            (
                "Hạn chế & Hướng mở rộng",
                "Độ nhạy & Ổn định lưới",
                [
                    "Phân tích độ nhạy theo biến động giá dầu Diesel, giá pin BESS và tăng trưởng phụ tải.",
                    "Mô phỏng quá độ tần số – điện áp (PSS/E hoặc PowerFactory) khi chuyển chế độ Diesel/BESS.",
                    "Đánh giá mặt bằng lắp đặt chống ăn mòn muối biển tại đảo ST.",
                ],
                "accent",
            ),
            (
                "Trọng tâm Q&A Hội đồng",
                "3 câu hỏi cốt lõi sẵn sàng",
                [
                    "Vì sao không chọn 2 × 500 kW gió (NPC thấp nhất)? → Vì điện dư 26,14 % > 10 %.",
                    "Vì sao không chạy 100 % tái tạo? → Mùa lặng gió T4–T5 ép điện dư ≥ 35 % và đội CAPEX.",
                    "Chiến lược Load Following: Diesel chỉ bù phần thiếu, nhường sạc BESS cho PV và Gió.",
                ],
                "warn",
            ),
        ],
        slide_no=15,
    )

    # Slide 16: Slide Chào & Cảm ơn Hội đồng
    add_thank_you_slide(deck, slide_no=16)

    deck.save(OUT_PPTX)
    deck.save(OUT_PPTX_ROOT)
    print(f"SAVED 16 SLIDES -> {OUT_PPTX}")
    print(f"SAVED COPY      -> {OUT_PPTX_ROOT}")


if __name__ == "__main__":
    build_deck()
