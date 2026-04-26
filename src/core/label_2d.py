"""Union-Find 2D labeling."""

def label_2d(mask):
    if not mask or not mask[0]:
        return []
    rows, cols, labeled, parent, comp_id = len(mask), len(mask[0]), [[0] * cols for _ in range(rows)], {}, 0
    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent[parent[parent[x]]]
            x = parent[x]
        return x
    for r in range(rows):
        for c in range(cols):
            if mask[r][c] == 0:
                continue
            root = (labeled[r-1][c] if r > 0 and labeled[r-1][c] > 0 else None) or (labeled[r][c-1] if c > 0 and labeled[r][c-1] > 0 else None)
            if root:
                labeled[r][c] = root
                if r > 0 and labeled[r-1][c] > 0: parent[find(labeled[r-1][c])] = root
                if c > 0 and labeled[r][c-1] > 0: parent[find(labeled[r][c-1])] = root
            else:
                comp_id += 1
                labeled[r][c] = parent[comp_id] = comp_id
    return [[find(labeled[r][c]) for c in range(cols)] for r in range(rows)]
