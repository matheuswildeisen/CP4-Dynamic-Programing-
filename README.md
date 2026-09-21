# Checkpoint 4 — Algoritmos e Estruturas de Dados

> **Atenção:** os integrantes e respectivos RM devem ser preenchidos pelo grupo antes da entrega.

## Identificação
### Integrantes e RM: 
- Gabriel Ciriaco de Oliveira Silva – RM564880 
- Mariana Souza Franca – RM562353 
- Matheus Von Koss Wildeisen – RM561539 
- Vinicius Mafra Paiva – RM565916

### Turma: 2ESPW

## Problemas e modelo

A Questão 1 modela logística de emergência como um grafo ponderado esparso. O vértice `Centro` representa o centro de distribuição e os demais vértices representam pontos de atendimento. As arestas possuem distância e podem estar bloqueadas. A seleção de regiões é um problema 0/1 de mochila: cada região é um item, `recursos` é o peso e `beneficio × pessoas` é o valor.

A Questão 2 usa 2.000 registros horários sintéticos. A criticidade é `consumo + 3 × max(0, consumo - capacidade) + 10 × prioridade`. Procuramos o intervalo contíguo de maior soma de criticidade, implementando força bruta e dividir e conquistar sem função pronta de máximo intervalo.

## Estruturas de dados

Usamos `list` para preservar a sequência temporal e permitir iteração; `dict` para mapear regiões/pontos a dados e obter acesso médio O(1); `tuple` para representar arestas e resultados imutáveis; `set` para testes de pertencimento sem varredura linear; e uma lista compatível com heap para priorizações. A escolha é funcional: cada estrutura corresponde ao padrão de acesso do algoritmo, em vez de ser usada apenas para cumprir uma lista.

## Algoritmos

- **Greedy:** calcula `score = benefício × (1 + prioridade/10) × pessoas / (recursos × (1 + distância/100))` e seleciona, em ordem decrescente, itens que ainda cabem. É uma decisão localmente vantajosa por benefício ajustado por recurso e custo de deslocamento; não há garantia de optimalidade.
- **Programação dinâmica:** `DP[i][c]` guarda o melhor benefício dos primeiros `i` candidatos com capacidade `c`. A decisão é excluir ou incluir o item `i`; caso-base é zero item ou capacidade zero; recorrência é `max(DP[i-1][c], DP[i-1][c-w_i]+v_i)` quando cabe. A reconstrução compara linhas consecutivas de trás para frente.
- **Força bruta:** enumera explicitamente todos os pares de início/fim do intervalo.
- **Dividir e conquistar:** divide o vetor ao meio, resolve esquerda e direita, resolve o maior intervalo que cruza o meio e combina escolhendo o maior dos três.

## Execução

```bash
python3 -m pip install -r requirements.txt
python3 run_experiments.py
pytest -q
```

Os dados podem ser regenerados por `python3 -m src.generate_data` após ajustar `SEED`. As figuras são salvas em `figures/questao1` e `figures/questao2`. O script também registra médias de execução e pico de memória em `results.json` usando `tracemalloc`. As cópias `notebooks/questao1_executado.ipynb` e `notebooks/questao2_executado.ipynb` comprovam uma execução bem-sucedida.

## Resultados e contraexemplo

O arquivo `results.json` registra as medições da execução. O arquivo `docs/contraexemplo.md` e o módulo `src/contraexemplo.py` demonstram `Greedy ≠ ótimo` na instância: capacidade 8; A=(peso 4, valor 5), B=(peso 5, valor 5), C=(peso 8, valor 9). A regra gulosa escolhe A e obtém 5, enquanto a DP escolhe C e obtém 9.

## Complexidade

Para a Questão 1, construir e percorrer o grafo custa `O(V+E)` quando representado por listas de adjacência. Ordenar os candidatos da heurística gulosa custa `O(N log N)` e a seleção linear custa `O(N)`. A DP possui `N` linhas e `C+1` colunas, portanto tempo `O(NC)` e espaço `O(NC)` nesta implementação; a reconstrução percorre `O(N)` itens. Para a Questão 2, a força bruta possui dois loops de início/fim, gerando `T(n)=O(n²)` e espaço auxiliar `O(1)`. A dividir e conquistar satisfaz `T(n)=2T(n/2)+O(n)` pelo caso cruzado, logo `O(n log n)`; a pilha recursiva ocupa `O(log n)`.

Se o conjunto crescer de 1.000 para 1.000.000 registros, dividir e conquistar continua viável em tempo assintótico (`n log n`), enquanto força bruta se torna impraticável (`n²`). Em produção, uma solução linear de Kadane seria ainda mais adequada, mas não foi usada porque o checkpoint exige a comparação específica entre força bruta e dividir e conquistar.

## Limitações e itens para finalizar pelo grupo

É necessário preencher nomes/RMs e, se aplicável, trocar a seed oficial. O layout do grafo agora é determinístico e as métricas de tempo e memória são geradas automaticamente. Ainda dependem do grupo a criação/publicação do repositório GitHub, a URL e os commits progressivos reais, além da preparação da explicação individual e da apresentação.

## Decisão algorítmica mais importante (até 300 palavras)

A decisão mais importante foi separar a priorização local da seleção ótima. A estratégia gulosa é interpretável e rápida, pois ordena candidatos por benefício ajustado por pessoas, prioridade, recursos e distância. Entretanto, ela não garante a melhor combinação quando a capacidade é limitada: escolher um item muito atraente pode impedir uma combinação posterior de maior benefício. Por isso, usamos programação dinâmica 0/1 para a decisão final sobre os mesmos candidatos. A DP exige `O(NC)` tempo e memória, enquanto a gulosa exige `O(N log N)` tempo e memória linear. Descartamos força bruta para a Questão 1 porque seu espaço de combinações cresce exponencialmente; também não usamos bibliotecas de otimização prontas, pois o objetivo é demonstrar a recorrência, os estados e a reconstrução. Para a Questão 2, escolhemos dividir e conquistar em vez de manter apenas força bruta: a decomposição e o caso cruzado tornam visível a origem do `O(n log n)`, e os experimentos mostram a diferença de escalabilidade. A escolha final equilibra qualidade da solução e explicabilidade: Greedy fornece uma ordem operacional, DP garante a melhor seleção dentro da capacidade e os algoritmos da Questão 2 permitem relacionar diretamente implementação, experimento e análise assintótica.

### Validação executada:
- python3 -m src.generate_data
- python3 run_experiments.py
- python3 -m pytest -q
- Resultado esperado atual: 5 passed.

### Como rodar:
python3 -m pip install -r requirements.txt
python3 -m src.generate_data
python3 run_experiments.py
python3 -m pytest -q