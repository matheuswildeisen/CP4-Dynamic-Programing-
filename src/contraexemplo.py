from src.dynamic_programming import knapsack
from src.greedy import greedy_route


def run():
    points = [
        {"nome": "A", "pessoas": 1, "prioridade": 1, "recursos": 4, "beneficio": 5},
        {"nome": "B", "pessoas": 1, "prioridade": 1, "recursos": 5, "beneficio": 5},
        {"nome": "C", "pessoas": 1, "prioridade": 1, "recursos": 8, "beneficio": 9},
    ]
    edges = {"Centro": [(point["nome"], 0) for point in points]}
    greedy, remaining = greedy_route(points, edges, 8)
    optimal, value, _ = knapsack(points, 8)
    return {"greedy": [point["nome"] for point in greedy], "greedy_benefit": sum(point["beneficio"] * point["pessoas"] for point in greedy), "greedy_remaining": remaining, "optimal": [point["nome"] for point in optimal], "optimal_benefit": value}


if __name__ == "__main__":
    print(run())
