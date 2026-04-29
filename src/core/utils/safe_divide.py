"""Safe division with the documented U-system zero contract.

``a : Ω`` is not treated as IEEE division by zero here.  Following
Universe/Math/13, the public core contract is:

* ``safe_divide(a, 0) == D(a) == 2a``;
* ``safe_divide(a, D(Id)) == H(a) == a/2``;
* otherwise use ordinary real division.
"""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║════════║══════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════╝


def safe_divide(a: object, b: object) -> object:
    """Divide ``a`` by ``b`` under the U-system branching convention."""
    from ..algebra import divide

    return divide(a, b)
