from pathlib import Path
import csv
import json
import sys
import time
import tracemalloc
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from src.brute_force import brute_force_max_interval
from src.divide_conquer import max_interval
from src.dynamic_programming import knapsack
from src.greedy import greedy_route

ROOT = Path(__file__).parent
F1 = ROOT / "figures" / "questao1"
F2 = ROOT / "figures" / "questao2"

def measure(function, argument, repetitions=3):
    times = []
    peaks = []
    result = None
    for _ in range(repetitions):
        tracemalloc.start()
        started = time.perf_counter()
        result = function(argument)
        times.append(time.perf_counter() - started)
        _, peak = tracemalloc.get_traced_memory()
        peaks.append(peak)
        tracemalloc.stop()
    return result, statistics_mean(times), max(peaks)

def statistics_mean(values):
    return sum(values) / len(values)

def load_q1():
    points = []
    with (ROOT / "data" / "problema1.csv").open(encoding="utf8") as file:
        for row in csv.DictReader(file):
            for key in ("pessoas", "prioridade", "recursos", "beneficio"):
                row[key] = int(row[key])
            points.append(row)
    edges = {}
    with (ROOT / "data" / "problema1_edges.csv").open(encoding="utf8") as file:
        for row in csv.DictReader(file):
            if row["bloqueada"] == "0":
                origin = row["origem"]
                destination = row["destino"]
                distance = int(row["distancia"])
                edges.setdefault(origin, []).append((destination, distance))
                edges.setdefault(destination, []).append((origin, distance))
    return points, edges

def draw_q1(points, edges, selected, dp):
    coordinates = {"Centro": (50, 50)}
    for index, point in enumerate(points):
        angle = 2 * 3.141592653589793 * index / len(points)
        coordinates[point["nome"]] = (50 + 40 * __import__("math").cos(angle), 50 + 40 * __import__("math").sin(angle))
    selected_names = {point["nome"] for point in selected}
    plt.figure(figsize=(10, 7))
    for origin, adjacent in edges.items():
        for destination, distance in adjacent:
            if origin < destination:
                x1, y1 = coordinates[origin]
                x2, y2 = coordinates[destination]
                plt.plot([x1, x2], [y1, y2], color="#bdbdbd", linewidth=0.7, alpha=0.7)
                plt.text((x1 + x2) / 2, (y1 + y2) / 2, str(distance), fontsize=5, color="#666666")
    for point in points:
        x, y = coordinates[point["nome"]]
        color = "#1b9e77" if point["nome"] in selected_names else "#d95f02"
        plt.scatter(x, y, c=color, s=90)
        plt.text(x + 1, y + 1, point["nome"], fontsize=7)
    plt.scatter(50, 50, c="black", marker="*", s=220, label="Centro")
    plt.title("Questão 1 — Grafo ponderado")
    plt.legend()
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(F1 / "figura1_grafo.png", dpi=180)
    plt.close()
    scores = sorted((point.get("score", 0), point["nome"]) for point in selected)[::-1]
    plt.figure(figsize=(10, 4))
    plt.bar([item[1] for item in scores], [item[0] for item in scores], color="#377eb8")
    plt.xticks(rotation=60)
    plt.title("Questão 1 — Sequência gulosa de atendimento")
    plt.ylabel("score local")
    plt.tight_layout()
    plt.savefig(F1 / "figura2_greedy.png", dpi=180)
    plt.close()
    plt.figure(figsize=(10, 4))
    plt.imshow(dp, aspect="auto", origin="lower", cmap="viridis")
    plt.colorbar(label="benefício acumulado")
    plt.xlabel("capacidade c")
    plt.ylabel("i pontos")
    plt.title("Questão 1 — Evolução da matriz DP")
    plt.tight_layout()
    plt.savefig(F1 / "figura3_dp.png", dpi=180)
    plt.close()

def draw_q2(values, interval, sizes, brute_times, divide_times):
    plt.figure(figsize=(12, 4))
    plt.plot(values, color="#555555", linewidth=0.7)
    plt.axvspan(interval[1], interval[2], color="red", alpha=0.25, label="intervalo D&C")
    plt.title("Questão 2 — Criticidade ao longo do tempo")
    plt.xlabel("registro")
    plt.ylabel("criticidade")
    plt.legend()
    plt.tight_layout()
    plt.savefig(F2 / "figura1_serie_temporal.png", dpi=180)
    plt.close()
    levels = [(0, 500), (0, 250), (250, 500), (0, 125), (125, 250), (250, 375), (375, 500)]
    labels = ["problema", "metade A", "metade B", "A1", "A2", "B1", "B2"]
    xs = [0, 1, 1, 2, 2, 2, 2]
    ys = [6, 5, 5, 4, 4, 4, 4]
    plt.figure(figsize=(8, 5))
    plt.scatter(xs, ys, s=900, c=["#4daf4a", "#377eb8", "#377eb8", "#984ea3", "#984ea3", "#ff7f00", "#ff7f00"])
    for x, y, label, bounds in zip(xs, ys, labels, levels):
        plt.text(x, y, f"{label}\n[{bounds[0]},{bounds[1]})", ha="center", va="center", fontsize=8)
    plt.axis("off")
    plt.title("Questão 2 — Decomposição dos 500 registros processados")
    plt.tight_layout()
    plt.savefig(F2 / "figura2_divide_conquer.png", dpi=180)
    plt.close()
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, brute_times, "o-", label="Força bruta O(n²)")
    plt.plot(sizes, divide_times, "o-", label="D&C O(n log n)")
    plt.xlabel("n")
    plt.ylabel("tempo médio (s)")
    plt.title("Questão 2 — Escalabilidade")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(F2 / "figura3_escalabilidade.png", dpi=180)
    plt.close()

def main():
    points, edges = load_q1()
    greedy_result, greedy_time, greedy_memory = measure(lambda data: greedy_route(data[0], data[1], 120), (points, edges))
    greedy_selected, remaining = greedy_result
    candidates = [point for point in points if point["nome"] in {item[0] for item in edges.get("Centro", [])}]
    dp_result, dp_time, dp_memory = measure(lambda data: knapsack(data, 120), candidates)
    dp_selected, dp_benefit, dp_matrix = dp_result
    for point in greedy_selected:
        point["score"] = point["score"]
    draw_q1(points, edges, dp_selected, dp_matrix)
    records = []
    with (ROOT / "data" / "problema2.csv").open(encoding="utf8") as file:
        records.extend(csv.DictReader(file))
    values = [float(row["criticidade"]) for row in records[:500]]
    brute_result, brute_time_500, brute_memory_500 = measure(brute_force_max_interval, values)
    divide_result, divide_time_500, divide_memory_500 = measure(max_interval, values)
    sizes = [100, 250, 500, 1000, 2000, 5000]
    brute_times = []
    divide_times = []
    memory_results = []
    for size in sizes:
        data = (values * ((size + len(values) - 1) // len(values)))[:size]
        _, brute_time, brute_memory = measure(brute_force_max_interval, data)
        _, divide_time, divide_memory = measure(max_interval, data)
        brute_times.append(brute_time)
        divide_times.append(divide_time)
        memory_results.append({"n": size, "brute_peak_bytes": brute_memory, "divide_peak_bytes": divide_memory})
    draw_q2(values, divide_result, sizes, brute_times, divide_times)
    results = {"q1": {"greedy_count": len(greedy_selected), "greedy_remaining": remaining, "greedy_time_seconds": greedy_time, "greedy_peak_bytes": greedy_memory, "dp_count": len(dp_selected), "dp_benefit": dp_benefit, "dp_time_seconds": dp_time, "dp_peak_bytes": dp_memory}, "q2": {"brute": brute_result, "divide_conquer": divide_result, "operations_brute_500": 500 * 501 // 2, "brute_time_500_seconds": brute_time_500, "divide_time_500_seconds": divide_time_500, "brute_peak_500_bytes": brute_memory_500, "divide_peak_500_bytes": divide_memory_500, "sizes": sizes, "brute_times": brute_times, "dc_times": divide_times, "memory": memory_results}}
    (ROOT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf8")
    print("Experimentos concluídos")

if __name__ == "__main__":
    main()
