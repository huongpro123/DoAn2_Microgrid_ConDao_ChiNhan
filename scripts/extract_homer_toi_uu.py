# -*- coding: utf-8 -*-
"""Trich xuat toan bo ket qua mo phong thuc te tu ST_Giai_doan_3_toi_uu.homer."""
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HOMER_DIR = BASE_DIR / "homer"
HOMER_PATH = HOMER_DIR / "ST_Giai_doan_3_toi_uu.homer"
OUT_JSON = HOMER_DIR / "homer_toi_uu_results.json"


def _strip(tag: str) -> str:
    return tag.split("}")[-1]


def _get(node, path: str, default=None):
    cur = node
    for part in path.split("/"):
        nxt = next((c for c in cur if _strip(c.tag) == part), None)
        if nxt is None:
            return default
        cur = nxt
    return (cur.text or "").strip() if cur.text is not None else default


def _f(val, default=0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def parse_summary(rs) -> dict:
    prod = _f(_get(rs, "AnnualElectricProduction"))
    cons = _f(_get(rs, "AnnualElectricConsumption"))
    exc = _f(_get(rs, "ExcessElectricity"))
    unm = _f(_get(rs, "UnmetLoad"))
    exc_pct = (100.0 * exc / prod) if prod > 0 else 999.0
    unm_pct = (100.0 * unm / (cons + unm)) if (cons + unm) > 0 else 999.0

    return {
        "infeasible": _get(rs, "Infeasible") == "true",
        "controller": _get(rs, "ControllerId", ""),
        "dispatch": _get(rs, "DispatchStrategy", ""),
        "pv_kw": round(_f(_get(rs, "PVs/PvSummary/Size")), 2),
        "pv_prod": round(_f(_get(rs, "PVs/PvSummary/TotalProduction")), 1),
        "wind_qty": round(_f(_get(rs, "WindTurbines/WindTurbineSummary/Quantity")), 0),
        "wind_prod": round(_f(_get(rs, "WindTurbines/WindTurbineSummary/TotalProduction")), 1),
        "bess_qty": round(_f(_get(rs, "Storage/StorageSummary/Quantity")), 0),
        "bess_autonomy": round(_f(_get(rs, "Storage/StorageSummary/Autonomy")), 2),
        "bess_throughput": round(_f(_get(rs, "Storage/StorageSummary/AnnualThroughput")), 1),
        "conv_kw": round(_f(_get(rs, "Converter/Size")), 1),
        "gen_kw": round(_f(_get(rs, "Generators/GeneratorSummary/Size")), 1),
        "gen_prod": round(_f(_get(rs, "Generators/GeneratorSummary/ElectricalProduction")), 1),
        "gen_hours": round(_f(_get(rs, "Generators/GeneratorSummary/HoursOfOperation")), 0),
        "total_prod": round(prod, 1),
        "served": round(cons, 1),
        "unmet_kwh": round(unm, 4),
        "unmet_pct": round(unm_pct, 2),
        "excess_kwh": round(exc, 1),
        "excess_pct": round(exc_pct, 2),
        "rf_pct": round(_f(_get(rs, "RenewableFraction")), 2),
        "capex": round(_f(_get(rs, "CapitalCost")), 0),
        "npc": round(_f(_get(rs, "NetPresentCost")), 0),
        "coe": round(_f(_get(rs, "CostOfEnergy")), 4),
        "operating_cost": round(_f(_get(rs, "OperatingCost")), 1),
        "om_cost": round(_f(_get(rs, "OmCost")), 1),
        "fuel_l": round(_f(_get(rs, "TotalFuel")), 1),
        "irr": round(_f(_get(rs, "InternalRateOfReturn")), 2),
        "roi": round(_f(_get(rs, "ReturnOnInvestment")), 2),
        "simple_payback": round(_f(_get(rs, "SimplePayback")), 2),
        "discounted_payback": round(_f(_get(rs, "DiscountedPayback")), 2),
        "present_worth": round(_f(_get(rs, "PresentWorth")), 0),
        "co2_kg": round(_f(_get(rs, "Co2")), 2),
        "nox_kg": round(_f(_get(rs, "Nox")), 2),
        "so2_kg": round(_f(_get(rs, "So2")), 2),
        "co_kg": round(_f(_get(rs, "Co")), 2),
        "pm_kg": round(_f(_get(rs, "Pm")), 2),
    }


def main() -> int:
    with zipfile.ZipFile(HOMER_PATH) as z:
        root = ET.fromstring(z.read("cases/0"))

    all_rows = [parse_summary(rs) for rs in root.iter() if _strip(rs.tag) == "ResultSummary"]
    feas = sorted([r for r in all_rows if not r["infeasible"] and r["npc"] > 0], key=lambda x: x["npc"])
    gvhd_ok = [r for r in feas if r["unmet_pct"] <= 0.1 and r["excess_pct"] <= 10.0]
    base_candidates = [r for r in feas if r["pv_kw"] == 0 and r["wind_qty"] == 0]

    payload = {
        "source_file": HOMER_PATH.name,
        "summary_counts": {
            "total": len(all_rows),
            "feasible": len(feas),
            "gvhd_ok": len(gvhd_ok),
        },
        "base_case": base_candidates[0] if base_candidates else None,
        "lowest_npc_overall": feas[0] if feas else None,
        "gvhd_top5": gvhd_ok[:5],
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Wrote", OUT_JSON.name, "| counts:", payload["summary_counts"])
    print("gvhd_top5[0]:", json.dumps(payload["gvhd_top5"][0], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
