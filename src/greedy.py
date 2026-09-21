"""Heuristica gulosa para priorizar pontos de atendimento."""

def score(point, distance):
    """Pontuacao local: beneficio por recurso, ajustada por prioridade e distancia."""
    return (point["beneficio"] * (1 + point["prioridade"] / 10) * point["pessoas"]) / (point["recursos"] * (1 + distance / 100))

def greedy_route(points, edges, capacity, start="Centro"):
    """Seleciona candidatos enquanto ha capacidade, ordenando por score decrescente."""
    distances = {name: d for name, d in edges.get(start, [])}
    candidates = []
    for p in points:
        if p["nome"] in distances and p["recursos"] <= capacity:
            q = dict(p); q["distancia_centro"] = distances[p["nome"]]; q["score"] = score(q, q["distancia_centro"]); candidates.append(q)
    candidates.sort(key=lambda x: (-x["score"], x["distancia_centro"], x["nome"]))
    selected, remaining = [], capacity
    for p in candidates:
        if p["recursos"] <= remaining:
            selected.append(p); remaining -= p["recursos"]
    return selected, remaining
