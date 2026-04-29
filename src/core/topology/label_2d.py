"""Union-Find 2D labeling."""


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
def label_2d(mask):
    if not mask or not mask[0]:
        return []

    rows = len(mask)
    cols = len(mask[0])
    labeled = [[0] * cols for _ in range(rows)]
    parent = {}
    comp_id = 0

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent[parent[parent[x]]]
            x = parent[x]
        return x

    for r in range(rows):
        for c in range(cols):
            if mask[r][c] == 0:
                continue
            top = labeled[r - 1][c] if r > 0 and labeled[r - 1][c] > 0 else None
            left = labeled[r][c - 1] if c > 0 and labeled[r][c - 1] > 0 else None
            root = top or left
            if root:
                labeled[r][c] = root
                if top:
                    parent[find(top)] = root
                if left:
                    parent[find(left)] = root
            else:
                comp_id += 1
                labeled[r][c] = parent[comp_id] = comp_id
    return [[find(labeled[r][c]) for c in range(cols)] for r in range(rows)]
