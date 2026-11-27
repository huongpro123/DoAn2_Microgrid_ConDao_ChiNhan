#!/usr/bin/env python3
"""Phan tich file .homer (Con Dao ST - Giai doan 3) va quet cau hinh toi uu
theo dung 2 tieu chi GVHD: cap du phu tai (Unmet = 0 %) va khong du qua 10 % nguon phat.

Chu y: ket qua quet Python 8.760 gio la so lieu tien dinh co hieu chuan theo
homer_results.json; truoc khi nop thu Tu can bam chay lai tren phan mem HOMER Pro
co ban quyen de xuat bang/do thi chinh thuc.
"""
from __future__ import annotations

import json
import math
import random
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HOMER_FILE = BASE_DIR / "HO_SO_BAO_CAO_CHIEU_NAY" / "05_File_Mo_Phong_HOMER_Pro.homer"
HOMER_JSON = BASE_DIR / "homer_results.json"

MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _strip(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def extract_homer_inputs() -> dict:
    with zipfile.ZipFile(HOMER_FILE) as z:
        root = ET.fromstring(z.read("problem"))

    wind_node = next(c for c in root if _strip(c.tag) == "WindResources")
    wind_monthly = [
        float(x.text)
        for e in wind_node.iter()
        if _strip(e.tag) == "MonthlyAverage"
        for x in e
        if x.text
    ][:12]

    sol_node = next(c for c in root if _strip(c.tag) == "SolarResources")
    sol_monthly = [
        float(x.text)
        for e in sol_node.iter()
        if _strip(e.tag) == "MonthlyAverage"
        for x in e
        if x.text
    ][:12]

    lf_node = next(c for c in root if _strip(c.tag) == "LoadFancy")
    wd_node = next(e for e in lf_node.iter() if _strip(e.tag) == "Weekdays")
    we_node = next(e for e in lf_node.iter() if _strip(e.tag) == "Weekends")
    wd_vals = [float(x.text) for x in wd_node if x.text][:288]
    we_vals = [float(x.text) for x in we_node if x.text][:288]

    wt_node = next(c for c in root if _strip(c.tag) == "WindTurbines")
    pc_node = next(e for e in wt_node.iter() if _strip(e.tag) == "PowerCurve")
    power_curve: list[tuple[float, float]] = [(0.0, 0.0)]
    for pt in pc_node:
        ws = next((float(c.text) for c in pt if _strip(c.tag) == "WindSpeed" and c.text), 0.0)
        po = next((float(c.text) for c in pt if _strip(c.tag) == "PowerOutput" and c.text), 0.0)
        power_curve.append((ws, po))
    power_curve.sort(key=lambda x: x[0])

    return {
        "wind_monthly_50m": wind_monthly,
        "solar_monthly_kwh_m2_d": sol_monthly,
        "load_wd_288": wd_vals,
        "load_we_288": we_vals,
        "power_curve_2mw": power_curve,
    }


def _interp_curve(v: float, curve: list[tuple[float, float]]) -> float:
    if v < curve[1][0]:
        return 0.0
    if v > curve[-1][0]:
        return 0.0
    for i in range(len(curve) - 1):
        v0, p0 = curve[i]
        v1, p1 = curve[i + 1]
        if v0 <= v <= v1:
            if v1 == v0:
                return p0
            return p0 + (p1 - p0) * (v - v0) / (v1 - v0)
    return 0.0


def build_calibrated_hourly_series(inp: dict, baseline: dict) -> dict:
    """Tao chuoi 8.760 gio Load, Solar CF (kW/kWp), Wind CF (kW/kW_dm) tu du lieu .homer
    va hieu chuan dung tong san luong nam theo homer_results.json."""
    rng = random.Random(20261124)

    # 1. Load 8760h
    load_raw: list[float] = []
    hour_idx = 0
    for m_idx, days in enumerate(MONTH_DAYS):
        wd_24 = inp["load_wd_288"][m_idx * 24:(m_idx + 1) * 24]
        we_24 = inp["load_we_288"][m_idx * 24:(m_idx + 1) * 24]
        for d in range(days):
            day_of_week = (hour_idx // 24) % 7
            prof = we_24 if day_of_week in (5, 6) else wd_24
            daily_factor = max(0.7, min(1.3, 1.0 + rng.gauss(0.0, 0.06)))
            for h in range(24):
                step_factor = max(0.6, min(1.4, 1.0 + rng.gauss(0.0, 0.10)))
                load_raw.append(max(0.1, prof[h] * daily_factor * step_factor))
                hour_idx += 1

    target_load_total = float(baseline["annual_consumption"]) + float(baseline["unmet_load"])
    load_scale = target_load_total / sum(load_raw)
    load_h = [v * load_scale for v in load_raw]

    # 2. Solar 8760h (per 1 kWp AC, calibrated to baseline pv_production / pv_size)
    sol_raw: list[float] = []
    for m_idx, days in enumerate(MONTH_DAYS):
        ghi_d = inp["solar_monthly_kwh_m2_d"][m_idx]
        for d in range(days):
            day_k = max(0.45, min(1.35, 1.0 + rng.gauss(0.0, 0.14)))
            day_shape = []
            for h in range(24):
                if 6 <= h <= 17:
                    # sinusoid around solar noon 12h
                    ang = math.pi * (h - 5.5) / 12.5
                    s = max(0.0, math.sin(ang)) ** 1.15
                else:
                    s = 0.0
                day_shape.append(s)
            s_sum = sum(day_shape) or 1.0
            for val in day_shape:
                sol_raw.append((val / s_sum) * ghi_d * day_k)
    target_pv_per_kw = float(baseline["pv_production"]) / float(baseline["pv_size"])
    pv_scale = target_pv_per_kw / (sum(sol_raw) / 1.0)
    pv_unit_h = [v * pv_scale for v in sol_raw]

    # 3. Wind speed 8760h (Rayleigh/Weibull k=2 with autocorrelation + diurnal pattern, calibrated to baseline wind_production)
    curve = inp["power_curve_2mw"]
    raw_ws: list[float] = []
    prev_noise = 0.0
    for m_idx, days in enumerate(MONTH_DAYS):
        v_mean_50 = inp["wind_monthly_50m"][m_idx]
        # Rayleigh scale factor so mean = v_mean_50 * hub_factor
        v_hub = v_mean_50 * ((78.0 / 50.0) ** 0.143)
        for d in range(days):
            for h in range(24):
                diurnal = 1.0 + 0.10 * math.cos(2.0 * math.pi * (h - 15) / 24.0)
                u = min(0.9999, max(0.0001, rng.random()))
                # Weibull(k=2) quantile scaled to mean=1
                w = math.sqrt(-math.log(1.0 - u)) / 0.886227
                prev_noise = 0.72 * prev_noise + 0.28 * w
                ws = max(0.0, v_hub * diurnal * (0.35 + 0.65 * prev_noise))
                raw_ws.append(ws)

    # Calibrate hub multiplier so 1 x E-82 produces exact baseline wind_production
    lo, hi = 0.7, 1.35
    target_wind = float(baseline["wind_production"])
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        prod = sum(_interp_curve(w * mid, curve) for w in raw_ws)
        if prod < target_wind:
            lo = mid
        else:
            hi = mid
    hub_mult = 0.5 * (lo + hi)
    wind_unit_h = [_interp_curve(w * hub_mult, curve) / 2000.0 for w in raw_ws]

    return {
        "load_h": load_h,
        "pv_unit_h": pv_unit_h,
        "wind_unit_h": wind_unit_h,
        "peak_load_kw": max(load_h),
        "total_load_kwh": sum(load_h),
    }


def simulate_system(
    series: dict,
    pv_kw: float,
    wind_kw: float,
    bess_strings: int,
    conv_kw: float,
    diesel_kw: float = 0.0,
) -> dict:
    """Mo phong can bang nang luong 8.760 gio va tinh kinh te 25 nam theo don gia .homer."""
    load_h = series["load_h"]
    pv_h = series["pv_unit_h"]
    wind_h = series["wind_unit_h"]

    bess_nom_kwh = bess_strings * 100.0
    soc_min = 0.20 * bess_nom_kwh
    soc_max = 1.00 * bess_nom_kwh
    soc = 0.50 * bess_nom_kwh
    eta_inv = 0.95
    eta_rec = 0.95
    eta_bess_rt = 0.90
    eta_c = math.sqrt(eta_bess_rt)
    eta_d = math.sqrt(eta_bess_rt)
    max_bess_chg_kw = bess_strings * 100.0 * 1.0   # 1C max charge from .homer (166.7A*600V)
    max_bess_dis_kw = bess_strings * 100.0 * 3.0   # 500A*600V = 300kW/string

    pv_prod = 0.0
    wind_prod = 0.0
    diesel_prod = 0.0
    diesel_hours = 0
    excess_kwh = 0.0
    unmet_kwh = 0.0
    served_kwh = 0.0
    bess_throughput = 0.0
    inv_sum = 0.0
    rec_sum = 0.0

    for t in range(8760):
        l_t = load_h[t]
        p_pv = pv_kw * pv_h[t]
        p_w = wind_kw * wind_h[t]
        pv_prod += p_pv
        wind_prod += p_w
        re_t = p_pv + p_w
        net = re_t - l_t

        if net >= 0.0:
            # Du RE -> sac vao pin qua rectifier
            served_kwh += l_t
            if bess_nom_kwh > 0 and conv_kw > 0:
                ac_to_rec = min(net, conv_kw)
                dc_avail = ac_to_rec * eta_rec
                room_dc = max(0.0, soc_max - soc)
                dc_in = min(dc_avail, max_bess_chg_kw, room_dc / eta_c if eta_c > 0 else 0.0)
                soc += dc_in * eta_c
                ac_used_for_chg = dc_in / eta_rec if eta_rec > 0 else 0.0
                rec_sum += ac_used_for_chg
                bess_throughput += dc_in * eta_c
                excess_kwh += max(0.0, net - ac_used_for_chg)
            else:
                excess_kwh += net
        else:
            deficit = -net
            discharged_ac = 0.0
            if bess_nom_kwh > 0 and conv_kw > 0:
                avail_dc = max(0.0, soc - soc_min)
                max_ac_from_soc = avail_dc * eta_d * eta_inv
                max_ac_from_rate = min(conv_kw, max_bess_dis_kw * eta_inv)
                discharged_ac = min(deficit, max_ac_from_soc, max_ac_from_rate)
                if discharged_ac > 0:
                    dc_from_bus = discharged_ac / eta_inv
                    soc_drop = dc_from_bus / eta_d
                    soc -= soc_drop
                    inv_sum += discharged_ac
                    bess_throughput += soc_drop

            rem = deficit - discharged_ac
            if rem > 1e-6 and diesel_kw > 0:
                gen = min(rem, diesel_kw)
                diesel_prod += gen
                if gen > 0.1:
                    diesel_hours += 1
                rem -= gen
                # Optional cycle charging surplus skipped in LF mode

            if rem > 1e-6:
                unmet_kwh += rem
            served_kwh += (l_t - rem)

    total_prod = pv_prod + wind_prod + diesel_prod
    total_load = series["total_load_kwh"]
    excess_pct = 100.0 * excess_kwh / total_prod if total_prod > 0 else 0.0
    unmet_pct = 100.0 * unmet_kwh / total_load if total_load > 0 else 0.0
    rf_pct = 100.0 * (1.0 - diesel_prod / served_kwh) if served_kwh > 0 else 0.0

    # Economics matching .homer rates (r_real = 5.88235%, N = 25 yrs)
    r = (1.08 / 1.02) - 1.0
    n_yrs = 25
    crf = r * ((1 + r) ** n_yrs) / (((1 + r) ** n_yrs) - 1.0)
    pv_factor = lambda y: 1.0 / ((1 + r) ** y)
    pa_25 = (1.0 - (1 + r) ** (-n_yrs)) / r

    capex = (
        pv_kw * 2400.0
        + wind_kw * 1923.0
        + bess_strings * 23000.0
        + conv_kw * 300.0
        + diesel_kw * 500.0
    )
    fuel_l = diesel_prod * 0.28  # ~0.28 L/kWh
    om_yr = (
        pv_kw * 10.0
        + wind_kw * 38.46
        + bess_strings * 10.0
        + diesel_kw * diesel_hours * 0.03
        + fuel_l * 1.00
    )
    rep_pv = (
        bess_strings * 18400.0 * pv_factor(15)
        + conv_kw * 300.0 * pv_factor(15)
        + (diesel_kw * 500.0 * pv_factor(12) if diesel_kw > 0 else 0.0)
    )
    npc = capex + om_yr * pa_25 + rep_pv
    coe = (npc * crf) / served_kwh if served_kwh > 0 else 999.0
    co2_saved_t = (served_kwh - diesel_prod) * 0.74 / 1000.0

    return {
        "pv_kw": pv_kw,
        "wind_kw": wind_kw,
        "bess_strings": bess_strings,
        "bess_kwh": bess_nom_kwh,
        "conv_kw": conv_kw,
        "diesel_kw": diesel_kw,
        "total_prod_kwh": round(total_prod, 1),
        "pv_prod_kwh": round(pv_prod, 1),
        "wind_prod_kwh": round(wind_prod, 1),
        "diesel_prod_kwh": round(diesel_prod, 1),
        "served_kwh": round(served_kwh, 1),
        "excess_kwh": round(excess_kwh, 1),
        "excess_pct": round(excess_pct, 2),
        "unmet_kwh": round(unmet_kwh, 1),
        "unmet_pct": round(unmet_pct, 2),
        "rf_pct": round(rf_pct, 2),
        "capex_usd": round(capex, 0),
        "npc_usd": round(npc, 0),
        "coe_usd": round(coe, 4),
        "om_yr_usd": round(om_yr, 0),
        "co2_saved_t": round(co2_saved_t, 1),
    }


def main() -> int:
    baseline_list = json.loads(HOMER_JSON.read_text(encoding="utf-8"))
    baseline = baseline_list[0]
    inp = extract_homer_inputs()
    series = build_calibrated_hourly_series(inp, baseline)

    # 1. Baseline check
    sim_base = simulate_system(series, pv_kw=213.2, wind_kw=2000.0, bess_strings=117, conv_kw=100.0)
    print(f"Load peak={series['peak_load_kw']:.1f} kW total={series['total_load_kwh']:.1f} kWh/yr")
    print(f"Baseline HOMER: served={baseline['annual_consumption']:.0f}, unmet={baseline['unmet_load']:.0f}, excess={baseline['excess_electricity']:.0f}")
    print(f"Baseline Python: served={sim_base['served_kwh']:.0f}, unmet={sim_base['unmet_kwh']:.0f} ({sim_base['unmet_pct']}%), excess={sim_base['excess_kwh']:.0f} ({sim_base['excess_pct']}%)")

    # 2. Scenario A: Keep 1 x 2000 kW E-82, raise Converter (100 -> 1000, 2000 kW)
    scen_a = [
        simulate_system(series, 213.2, 2000.0, 117, c)
        for c in (100.0, 500.0, 850.0, 1000.0, 2000.0)
    ]

    # 3. Scenario B: 100% RE downsizing wind + tuning PV/BESS (Converter >= peak load)
    scen_b_all = []
    scen_b_near = []
    for wind_kw in (500.0, 600.0, 800.0, 1000.0, 1200.0):
        for pv_kw in (400.0, 800.0, 1200.0, 1600.0, 2000.0):
            for bess in (80, 120, 180, 250, 350):
                res = simulate_system(series, pv_kw, wind_kw, bess, 1000.0)
                scen_b_near.append(res)
                if res["unmet_pct"] <= 0.1:
                    scen_b_all.append(res)
    scen_b_feasible = sorted([r for r in scen_b_all if r["excess_pct"] <= 10.0], key=lambda x: x["npc_usd"])
    if scen_b_all:
        scen_b_min_excess = sorted(scen_b_all, key=lambda x: (x["excess_pct"], x["npc_usd"]))[:5]
    else:
        scen_b_min_excess = sorted(scen_b_near, key=lambda x: (x["unmet_pct"], x["excess_pct"], x["npc_usd"]))[:5]

    # 4. Scenario C: Hybrid RE + Backup Diesel (unmet == 0 AND excess <= 10%)
    scen_c_all = []
    for wind_kw in (400.0, 500.0, 600.0, 700.0, 800.0):
        for pv_kw in (200.0, 400.0, 600.0, 800.0, 1000.0):
            for bess in (20, 40, 60, 80, 100):
                for diesel_kw in (500.0, 650.0, 800.0):
                    res = simulate_system(series, pv_kw, wind_kw, bess, 1000.0, diesel_kw=diesel_kw)
                    if res["unmet_pct"] <= 0.01 and res["excess_pct"] <= 10.0 and res["rf_pct"] >= 75.0:
                        scen_c_all.append(res)
    scen_c_top = sorted(scen_c_all, key=lambda x: x["npc_usd"])[:8]

    out_data = {
        "homer_baseline_json": {
            "pv_kw": baseline["pv_size"],
            "wind_kw": 2000.0,
            "bess_strings": baseline["storage_quantity"],
            "conv_kw": baseline["converter_size"],
            "annual_production_kwh": round(baseline["annual_production"], 1),
            "served_kwh": round(baseline["annual_consumption"], 1),
            "unmet_kwh": round(baseline["unmet_load"], 1),
            "unmet_pct": round(100.0 * baseline["unmet_load"] / (baseline["annual_consumption"] + baseline["unmet_load"]), 2),
            "excess_kwh": round(baseline["excess_electricity"], 1),
            "excess_pct": round(100.0 * baseline["excess_electricity"] / baseline["annual_production"], 2),
            "npc_usd": round(baseline["net_present_cost"], 0),
            "coe_usd": round(baseline["cost_of_energy"], 4),
        },
        "python_baseline_calibrated": sim_base,
        "scenario_a_raise_converter": scen_a,
        "scenario_b_100pct_re_excess_le_10": scen_b_feasible[:5],
        "scenario_b_100pct_re_min_excess": scen_b_min_excess,
        "scenario_c_hybrid_diesel_top": scen_c_top,
    }
    (BASE_DIR / "ket_qua_toi_uu_homer.json").write_text(
        json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Kết quả phân tích & tối ưu cấu hình Microgrid Côn Đảo (đáp ứng 0 % thiếu · ≤ 10 % dư)",
        "",
        "> **Phân biệt nguồn số liệu:** Bảng gốc lấy trực tiếp từ `homer_results.json` (`05_File_Mo_Phong_HOMER_Pro.homer`);",
        "> các kịch bản A/B/C tính bằng bộ mô phỏng cân bằng năng lượng **8.760 giờ hiệu chuẩn trong Python** từ đúng chuỗi NASA/tải của file `.homer`.",
        "> Trước khi nộp Thứ Tư, cần bấm chạy lại phương án chọn trên phần mềm **HOMER Pro** bản hoạt động để lấy bảng/đồ thị gốc.",
        "",
        "## 1. Vì sao cấu hình gốc trong `.homer` không đạt tiêu chí GVHD?",
        f"- Công suất đỉnh chuỗi tải 8.760 giờ hiệu chuẩn: **`{series['peak_load_kw']:.1f} kW`**, tổng phụ tải năm: **`{series['total_load_kwh']:,.0f} kWh/năm`**.",
        f"- **Lỗi 1 — Nghẽn Converter `100 kW`:** Tải đỉnh `783,1 kW` nhưng bộ biến đổi DC–AC khai báo chỉ `100 kW` → thiếu **`{baseline['unmet_load']:,.0f} kWh/năm` (`18,0 %`)**.",
        f"- **Lỗi 2 — Thừa công suất gió `2.000 kW`:** Riêng 1 tuabin E-82 tạo `{baseline['wind_production']:,.0f} kWh/năm` (gần gấp đôi nhu cầu) → dư **`{baseline['excess_electricity']:,.0f} kWh/năm` (`58,4 %` > `10 %`)**.",
        "",
        "## 2. Kịch bản A — Nếu chỉ nâng Converter lên `1.000–2.000 kW` (giữ nguyên `1 × E-82 2.000 kW`)",
        "| Converter (kW) | Thiếu tải (%) | Dư điện (%) | NPC (USD) | COE (USD/kWh) | Đạt tiêu chí GVHD? |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for r in scen_a:
        ok = "ĐẠT" if (r["unmet_pct"] <= 0.1 and r["excess_pct"] <= 10.0) else "KHÔNG (còn dư > 10%)"
        lines.append(f"| {r['conv_kw']:.0f} | {r['unmet_pct']:.2f} | {r['excess_pct']:.2f} | {r['npc_usd']:,.0f} | {r['coe_usd']:.4f} | {ok} |")

    lines += [
        "",
        "## 3. Kịch bản B — 100 % Tái tạo (Hạ cỡ gió + tăng lưu trữ/PV, Converter `1.000 kW`)",
        f"- Số phương án 100 % RE đạt đồng thời `Unmet ≤ 0,1 %` và `Excess ≤ 10 %`: **`{len(scen_b_feasible)}`** *(nếu = 0: hiển thị top phương án 100 % RE có tỷ lệ dư nhỏ nhất)*.",
        "| PV (kWp) | Gió (kW) | BESS (khối 100 kWh) | Thiếu (%) | Dư (%) | CAPEX (USD) | NPC (USD) | COE (USD/kWh) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    rows_b = scen_b_feasible[:5] if scen_b_feasible else scen_b_min_excess
    for r in rows_b:
        lines.append(
            f"| {r['pv_kw']:.0f} | {r['wind_kw']:.0f} | {r['bess_strings']} | {r['unmet_pct']:.2f} | {r['excess_pct']:.2f} | "
            f"{r['capex_usd']:,.0f} | {r['npc_usd']:,.0f} | {r['coe_usd']:.4f} |"
        )

    lines += [
        "",
        "## 4. Kịch bản C — Hybrid Tái tạo + Diesel dự phòng nhỏ (tối ưu chi phí & đạt chuẩn `0 % thiếu · ≤ 10 % dư`)",
        "| PV (kWp) | Gió (kW) | BESS (khối) | Diesel (kW) | RF (%) | Thiếu (%) | Dư (%) | CAPEX (USD) | NPC (USD) | COE (USD/kWh) | CO₂ giảm (tấn/năm) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in scen_c_top:
        lines.append(
            f"| {r['pv_kw']:.0f} | {r['wind_kw']:.0f} | {r['bess_strings']} | {r['diesel_kw']:.0f} | {r['rf_pct']:.1f} | "
            f"{r['unmet_pct']:.2f} | {r['excess_pct']:.2f} | {r['capex_usd']:,.0f} | {r['npc_usd']:,.0f} | {r['coe_usd']:.4f} | {r['co2_saved_t']:,.1f} |"
        )

    lines += [
        "",
        "## 5. Hướng dẫn 5 bước bấm chạy lại trên HOMER Pro (trước Thứ Tư)",
        "1. Mở `HO_SO_BAO_CAO_CHIEU_NAY\\05_File_Mo_Phong_HOMER_Pro.homer` trên máy có bản quyền HOMER Pro còn hạn.",
        "2. Vào mục **System Converter** → nâng giới hạn `Capacity` lên `0, 800, 1000, 1200, 2000` kW (thay vì cố định `100 kW`).",
        "3. Đổi **Wind Turbine** từ `1 × 2.000 kW` sang dải tìm kiếm công suất nhỏ hơn (`600–1.000 kW`, hoặc bổ sung tổ máy nhỏ + **Generic PV** `400–1.200 kWp` + **Storage** `40–150` khối); nếu dùng phương án Hybrid C thì bật thêm **Generator Diesel** `400–800 kW` cho ngày lặng gió tháng 4–5.",
        "4. Đặt **Constraints → Max annual capacity shortage = `0 %`**, bấm **Calculate** → lọc bảng **Optimization Results** lấy dòng đầu tiên có **Excess Electricity ≤ `10 %`** và **Unmet Electric Load = `0 %`**.",
        "5. Chụp lại **Optimization Table**, **Electrical Summary** và **Cash Flow Summary** + lưu đè file `.homer` mới.",
    ]
    (BASE_DIR / "KET_QUA_TOI_UU_CAU_HINH_HOMER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote ket_qua_toi_uu_homer.json & KET_QUA_TOI_UU_CAU_HINH_HOMER.md (B_feasible={len(scen_b_feasible)}, C_top={len(scen_c_top)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
