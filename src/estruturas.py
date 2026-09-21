"""Estruturas de dados usadas no checkpoint."""
from collections import defaultdict
import heapq

def index_by_region(records):
    """Retorna dict regiao -> lista de registros, com acesso O(1) ao grupo."""
    result = defaultdict(list)
    for record in records:
        result[record["regiao"]].append(record)
    return dict(result)

def build_peak_heap(records):
    """Cria max-heap por criticidade usando tuplas negativas."""
    return [(-r["criticidade"], r["timestamp"], r["regiao"]) for r in records]
