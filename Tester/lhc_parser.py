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

import re
import pandas as pd
import numpy as np

def parse_mass(mass_str):
    """Parse '10530 ± 10', '4449.8 ± 3.0', '4694^{+16}_{-5}' → central, unc_low, unc_high"""
    # Central
    central_match = re.search(r'(\d+(?:\.\d+)?)', mass_str)
    if not central_match:
        return np.nan, np.nan, np.nan
    central = float(central_match.group(1))
    
    # Symmetric ±
    sym_match = re.search(r'±\s*(\d+(?:\.\d+)?)', mass_str)
    if sym_match:
        unc = float(sym_match.group(1))
        return central, unc, unc
    
    # Asymmetric + -
    up_match = re.search(r'\+\s*(\d+(?:\.\d+)?)', mass_str)
    down_match = re.search(r'-\s*(\d+(?:\.\d+)?)', mass_str)
    unc_low = float(down_match.group(1)) if down_match else 0
    unc_high = float(up_match.group(1)) if up_match else 0
    return central, unc_low, unc_high

with open('Physics/Вибрации/Вселенная_и_вибрации.md', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

data = []
in_table = False

for line in lines:
    line = line.strip()
    if line.startswith('| № | Вибрация | Масса'):
        in_table = True
        continue
    if in_table and line.startswith('|') and not line.startswith('|---'):
        parts = [p.strip() for p in line.split('|')][1:-1]
        if len(parts) >= 4:  # №, name, mass, Q, ...
            num = parts[0]
            name = parts[1]
            mass_str = parts[2]
            q_str = parts[3]
            
            central, unc_low, unc_high = parse_mass(mass_str)
            q = int(q_str) if q_str.isdigit() else np.nan
            
            data.append({'id': num, 'name': name, 'mass': central, 'unc_low': unc_low, 'unc_high': unc_high, 'Q': q})

df = pd.DataFrame(data)
df.to_csv('lhc_particles.csv', index=False)
print('LHCb CSV created. Shape:', df.shape)
print(df.head())
print('Q groups:', df['Q'].value_counts().sort_index())
