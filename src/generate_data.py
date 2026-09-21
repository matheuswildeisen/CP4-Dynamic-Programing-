"""Gera os dois conjuntos de dados com seed do grupo."""
from pathlib import Path
import csv, random
SEED = 42

def generate_q1(path):
    rng = random.Random(SEED); names = [f"Ponto_{i:02d}" for i in range(1,21)]
    rows=[]
    for i,n in enumerate(names):
        rows.append({"nome":n,"pessoas":rng.randint(50,500),"prioridade":rng.randint(1,5),"recursos":rng.randint(8,35),"beneficio":rng.randint(5,20)})
    with open(path,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    edges=[]
    for i in range(20):
        edges.append(("Centro", names[i], rng.randint(5,80)))
    for _ in range(35):
        a,b=rng.sample(names,2); edges.append((a,b,rng.randint(5,100)))
    with open(Path(path).with_name('problema1_edges.csv'),'w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['origem','destino','distancia','bloqueada']); w.writerows([(*e, int(rng.random()<0.12)) for e in edges])

def generate_q2(path):
    rng=random.Random(SEED); regions=['Norte','Sul','Leste','Oeste','Centro']; rows=[]
    for i in range(2000):
        consumption=max(20, rng.gauss(100,25) + (80 if i%168 in range(18,22) else 0))
        priority=rng.randint(1,5); capacity=160+rng.gauss(0,15); cost=round(consumption*rng.uniform(.3,.9),2)
        excess=max(0, consumption-capacity); criticality=round(consumption+3*excess+10*priority,2)
        rows.append([f'2026-01-{(i//24)%28+1:02d} {i%24:02d}:00',rng.choice(regions),round(consumption,2),round(capacity,2),priority,cost,criticality])
    with open(path,'w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['timestamp','regiao','consumo','capacidade','prioridade','custo','criticidade']); w.writerows(rows)

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1] / 'data'; generate_q1(root/'problema1.csv'); generate_q2(root/'problema2.csv')
