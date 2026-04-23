#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝


import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp
import yaml
from scipy.stats import linregress

# Load data
codata_df = pd.read_csv('codata_2022.csv')
lhc_df = pd.read_csv('lhc_particles.csv').dropna(subset=['Q'])
lhc_df['ln_m'] = np.log(lhc_df['mass'])

# Load registry
with open('formulas_registry.yaml', 'r', encoding='utf-8') as f:
    registry = yaml.safe_load(f)['formulas']

results = []

mp_proton = codata_df[codata_df['Quantity'].str.contains('proton mass energy equivalent in MeV', case=False, na=False)][
    'Value'].iloc[0]

for fmla in registry:
    fid = fmla['id']
    ftype = fmla['type']

    if ftype == 'codata_lookup':
        mask = codata_df['Quantity'].str.contains(fmla['codata_query'], case=False, na=False)
        val = codata_df.loc[mask, 'Value'].iloc[0] if mask.any() else np.nan
        expected = fmla.get('expected', np.nan)
        diff = abs(val - expected) / expected * 100 if expected and not np.isnan(expected) else 0

    elif ftype == 'sympy':
        expr_str = fmla['formula']
        expr = sp.sympify(expr_str)
        subs = {k: v for k, v in fmla['inputs'].items()}
        if 'm' in subs:
            subs['m'] = fmla['params']['m']
        subs['mp'] = mp_proton
        subs = {k: float(v) if isinstance(v, (int, float)) else v for k, v in subs.items()}
        val = float(expr.subs(subs))
        expected_str = fmla.get('expected', '0')
        expected_num = float(re.sub(r'[~]', '', expected_str))
        diff = abs(val - expected_num) / expected_num * 100

    elif ftype == 'linear_fit':
        slope, intercept, r, p, se = linregress(lhc_df['Q'], lhc_df['ln_m'])
        val = slope
        expected = fmla.get('expected', np.nan)
        diff = abs(val - expected) / expected * 100 if expected else 0

    else:
        val = np.nan
        diff = np.nan

    results.append({
        'id': fid,
        'name': fmla['name'],
        'computed': round(val, 4),
        'expected': fmla.get('expected'),
        'diff_%': round(diff, 2) if not np.isnan(diff) else np.nan
    })

res_df = pd.DataFrame(results)

# Create reports
os.makedirs('reports', exist_ok=True)
res_df.to_markdown('reports/all_constants.md', index=False)
res_df.to_csv('reports/all_constants.csv', index=False)

# Plot
plt.figure(figsize=(8, 6))
plt.scatter([float(re.sub(r'[~]', '', e)) if isinstance(e, str) else e for e in res_df['expected']], res_df['computed'],
            alpha=0.7)
plt.plot([0, 5], [0, 5], 'r--', label='Ideal')
plt.xlabel('Expected')
plt.ylabel('Computed')
plt.title('Constants Verification')
plt.legend()
plt.savefig('reports/constants_scatter.png', dpi=150)
plt.close()

print('=== RESULTS ===')
print(res_df)
print('\nReports saved in reports/')
