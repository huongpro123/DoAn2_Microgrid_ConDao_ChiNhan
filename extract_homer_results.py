# -*- coding: utf-8 -*-
"""Trich xuat ket qua mo phong HOMER Pro tu tep .homer (khong bia so).

HOMER luu ket qua tinh toan trong entry `cases/0` cua tep .homer duoi dang XML
(ResultSummary). Script nay doc XML do va ghi ra JSON de dung cho bao cao.
"""
import json
import sys
import zipfile
import xml.etree.ElementTree as ET


def strip(tag):
    return tag.split('}')[-1]


def get(root, path, default=None):
    """Lay gia tri theo duong dan ten the, bo qua namespace."""
    node = root
    for part in path.split('/'):
        nxt = None
        for ch in node:
            if strip(ch.tag) == part:
                nxt = ch
                break
        if nxt is None:
            return default
        node = nxt
    return (node.text or '').strip() if node.text is not None else default


def num(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def parse(homer_path):
    z = zipfile.ZipFile(homer_path)
    root = ET.fromstring(z.read('cases/0'))
    cases = []
    for case in root:
        if strip(case.tag) != 'Cases':
            continue
        for oc in case:
            if strip(oc.tag) != 'OptimizationCase':
                continue
            for rs in oc:
                if strip(rs.tag) != 'ResultSummary':
                    continue
                r = {}
                r['controller'] = get(rs, 'ControllerId')
                r['dispatch'] = get(rs, 'DispatchStrategy')
                r['capital_cost'] = num(get(rs, 'CapitalCost'))
                r['net_present_cost'] = num(get(rs, 'NetPresentCost'))
                r['cost_of_energy'] = num(get(rs, 'CostOfEnergy'))
                r['operating_cost'] = num(get(rs, 'OperatingCost'))
                r['om_cost'] = num(get(rs, 'OmCost'))
                r['annual_production'] = num(get(rs, 'AnnualElectricProduction'))
                r['annual_consumption'] = num(get(rs, 'AnnualElectricConsumption'))
                r['excess_electricity'] = num(get(rs, 'ExcessElectricity'))
                r['unmet_load'] = num(get(rs, 'UnmetLoad'))
                r['capacity_shortage'] = num(get(rs, 'CapacityShortage'))
                r['shortage_hours'] = num(get(rs, 'CapacityShortageHours'))
                r['renewable_fraction'] = num(get(rs, 'RenewableFraction'))
                r['renewable_penetration'] = num(get(rs, 'RenewablePenetration'))
                r['total_fuel'] = num(get(rs, 'TotalFuel'))
                r['infeasible'] = get(rs, 'Infeasible')
                # PV
                r['pv_size'] = num(get(rs, 'PVs/PvSummary/Size'))
                r['pv_production'] = num(get(rs, 'PVs/PvSummary/TotalProduction'))
                r['pv_capital'] = num(get(rs, 'PVs/PvSummary/CapitalCost'))
                # Wind
                r['wind_quantity'] = num(get(rs, 'WindTurbines/WindTurbineSummary/Quantity'))
                r['wind_production'] = num(get(rs, 'WindTurbines/WindTurbineSummary/TotalProduction'))
                r['wind_capital'] = num(get(rs, 'WindTurbines/WindTurbineSummary/CapitalCost'))
                r['wind_om'] = num(get(rs, 'WindTurbines/WindTurbineSummary/OmCost'))
                # Storage
                s = 'Storage/StorageSummary'
                r['storage_quantity'] = num(get(rs, s + '/Quantity'))
                r['storage_nominal'] = num(get(rs, s + '/NominalCapacity'))
                r['storage_usable'] = num(get(rs, s + '/UsableNominalCapacity'))
                r['storage_throughput'] = num(get(rs, s + '/AnnualThroughput'))
                r['storage_autonomy'] = num(get(rs, s + '/Autonomy'))
                r['storage_capital'] = num(get(rs, s + '/CostSummary/StorageCostSummary/CapitalCost'))
                r['storage_replacement'] = num(get(rs, s + '/CostSummary/StorageCostSummary/ReplacementCost'))
                r['storage_om'] = num(get(rs, s + '/CostSummary/StorageCostSummary/OmCost'))
                # Converter
                r['converter_size'] = num(get(rs, 'Converter/Size'))
                r['inverter_mean'] = num(get(rs, 'Converter/InverterMeanOutput'))
                r['rectifier_mean'] = num(get(rs, 'Converter/RectifierMeanOutput'))
                # design variables
                design = {}
                odc = rs.find('OptimizationDesignCases')
                if odc is not None:
                    for dc in odc:
                        n = get(dc, 'Name')
                        v = get(dc, 'Value')
                        if n:
                            design[n] = v
                r['design'] = design
                cases.append(r)
    return cases


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else r'D:\chinhan\ST_Giai_doan_3_template.homer'
    out = sys.argv[2] if len(sys.argv) > 2 else r'D:\chinhan\homer_results.json'
    data = parse(path)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('cases:', len(data))
    for c in data:
        print(' %s (%s) NPC=%.0f COE=%.4f CAPEX=%.0f PV=%.0f Wind=%.0f Unmet=%.0f Excess=%.0f'
              % (c['controller'], c['dispatch'], c['net_present_cost'], c['cost_of_energy'],
                 c['capital_cost'], c['pv_production'], c['wind_production'],
                 c['unmet_load'], c['excess_electricity']))
