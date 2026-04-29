"""Dual power: ``(x+vε)ⁿ = xⁿ + n·xⁿ⁻¹·v·ε``."""


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
def dual_power(x, v, n=2):
    """Return the primal and ε coefficient of ``(x + vε) ** n``."""
    exponent = float(n)
    x_value = float(x)
    return x_value**exponent, exponent * (x_value ** (exponent - 1.0)) * float(v)
