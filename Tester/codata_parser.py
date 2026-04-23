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
from pandas import DataFrame
from numpy import nan

def parse_value(s):
    """Parse messy value like '7294.299 541 71' or '6.644 657 3450 e-27'"""
    s = re.sub(r'\s+', '', s)  # Remove spaces
    s = re.sub(r'e(\+?)(\d+)', r' scientific E\g<1>\g<2>', s)  # Prep
    try:
        return float(s.replace('e-', 'E-').replace('e+', 'E+'))
    except ValueError:
        return nan

with open('Universe/Физические_константы.md', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

data = []
in_table = False
header_row = None

for i, line in enumerate(lines):
    line = line.strip()
    if 'Quantity | Value | Uncertainty | Unit' in line:
        in_table = True
        continue
    if in_table and line.startswith('|') and '---' not in line:
        parts = [p.strip() for p in line.split('|')][1:-1]  # Clean parts
        if len(parts) == 4:
            qty, val_str, unc_str, unit = parts
            val = parse_value(val_str)
            unc = parse_value(unc_str) if unc_str != '(exact)' else 0.0
            data.append({'Quantity': qty, 'Value': val, 'Uncertainty': unc, 'Unit': unit})

df: DataFrame = DataFrame(data)
df.to_csv('codata_2022.csv', index=False)
print('CODATA CSV created. Shape:', df.shape)
print(df[df['Quantity'].str.contains('proton|mass|MeV', case=False, na=False)][['Quantity', 'Value', 'Uncertainty']])
