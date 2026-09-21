"""Programacao dinamica 0/1 para selecao de atendimentos."""

def knapsack(points, capacity):
    """Estado dp[i][c] e melhor beneficio com os primeiros i pontos e capacidade c."""
    n = len(points); dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, p in enumerate(points, 1):
        w, v = p["recursos"], p["beneficio"] * p["pessoas"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i-1][c]
            if w <= c: dp[i][c] = max(dp[i][c], dp[i-1][c-w] + v)
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            chosen.append(points[i-1]); c -= points[i-1]["recursos"]
    chosen.reverse()
    return chosen, dp[n][capacity], dp
