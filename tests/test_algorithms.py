import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from src.brute_force import brute_force_max_interval
from src.contraexemplo import run
from src.divide_conquer import max_interval
from src.dynamic_programming import knapsack
from src.greedy import greedy_route


def test_brute_and_divide_conquer_agree():
    values = [-2, 3, -1, 4, -10, 5, 2]
    assert brute_force_max_interval(values)[0][0] == max_interval(values)[0]


def test_dp_capacity_and_optimality():
    points = [{"nome": "a", "recursos": 3, "beneficio": 10, "pessoas": 1}, {"nome": "b", "recursos": 4, "beneficio": 9, "pessoas": 1}, {"nome": "c", "recursos": 5, "beneficio": 16, "pessoas": 1}]
    chosen, value, _ = knapsack(points, 7)
    assert sum(item["recursos"] for item in chosen) <= 7
    assert value == 19


def test_greedy_respects_capacity():
    points = [{"nome": "a", "recursos": 4, "beneficio": 5, "pessoas": 10, "prioridade": 2}, {"nome": "b", "recursos": 4, "beneficio": 4, "pessoas": 10, "prioridade": 1}]
    selected, remaining = greedy_route(points, {"Centro": [("a", 10), ("b", 10)]}, 5)
    assert remaining >= 0
    assert len(selected) == 1


def test_greedy_counterexample():
    result = run()
    assert result["greedy_benefit"] == 5
    assert result["optimal_benefit"] == 9


def test_dataset_minimums():
    root = Path(__file__).parents[1]
    with (root / "data" / "problema1.csv").open(encoding="utf8") as file:
        assert len(list(csv.DictReader(file))) == 20
    with (root / "data" / "problema1_edges.csv").open(encoding="utf8") as file:
        edges = list(csv.DictReader(file))
        assert len(edges) >= 35
        assert any(row["bloqueada"] == "1" for row in edges)
    with (root / "data" / "problema2.csv").open(encoding="utf8") as file:
        assert len(list(csv.DictReader(file))) >= 1000
