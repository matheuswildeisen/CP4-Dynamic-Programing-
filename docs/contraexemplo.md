# Contraexemplo da estratégia gulosa

A capacidade é 8. Os três atendimentos têm distância zero, prioridade 1 e uma pessoa afetada. A é `(recursos=4, benefício=5)`, B é `(5, 5)` e C é `(8, 9)`.

A heurística ordena A antes de C porque o score de A é maior. Depois de escolher A, os itens B e C não cabem; o resultado é benefício 5. A programação dinâmica considera as combinações e escolhe C, com benefício 9. Portanto, Greedy não é ótimo nesta instância.

Para reproduzir:

```bash
python3 -m src.contraexemplo
```

A saída esperada contém `greedy_benefit: 5` e `optimal_benefit: 9`.
