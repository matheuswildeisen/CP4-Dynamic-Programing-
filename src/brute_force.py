"""Forca bruta para maior intervalo contiguo de criticidade."""
def brute_force_max_interval(values):
    best = (0, -1, -1)
    operations = 0
    for i in range(len(values)):
        total = 0
        for j in range(i, len(values)):
            total += values[j]; operations += 1
            if total > best[0]: best = (total, i, j)
    return best, operations
