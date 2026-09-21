"""Maior intervalo por dividir e conquistar, incluindo caso cruzado."""
def _cross(values, lo, mid, hi):
    left_sum = float("-inf"); total = 0; left = mid
    for i in range(mid, lo-1, -1):
        total += values[i]
        if total > left_sum: left_sum, left = total, i
    right_sum = float("-inf"); total = 0; right = mid+1
    for j in range(mid+1, hi+1):
        total += values[j]
        if total > right_sum: right_sum, right = total, j
    return (left_sum + right_sum, left, right)

def max_interval(values):
    def solve(lo, hi):
        if lo == hi: return (values[lo], lo, hi)
        mid = (lo + hi) // 2
        a, b, c = solve(lo, mid), solve(mid+1, hi), _cross(values, lo, mid, hi)
        return max((a,b,c), key=lambda x: x[0])
    return (0, -1, -1) if not values else solve(0, len(values)-1)
