# Protocolos de exemplo — Rubedo Research Workspace

Dados fictícios; exemplos analíticos, não pesquisas empíricas nem resultados industriais validados. Utilize [o ambiente de pesquisa](../research/index.html) para reproduzir os cálculos.

## R01 — Sensibilidade de capacidade

Pergunta: como uma mudança isolada do ciclo afeta a capacidade estimada? Hipótese: um ciclo mais curto aumenta a produção estimada, mantendo as demais variáveis constantes. Método: 480 min, 45 s/un., disponibilidade 85%, rendimento 97%; ciclos de 36, 45 e 54 s. Métrica: unidades boas estimadas. O cálculo é `minutos × 60 / ciclo × disponibilidade × rendimento`, com percentuais convertidos em frações. A comparação não representa ganhos observados; ignora lotes, setups e variabilidade. Registre cada cenário e explique as limitações.

## R02 — Fila M/M/1

Pergunta: como a utilização afeta a espera? Compare chegadas de 6, 8 e 9 por hora para serviço de 10 por hora. Sob hipóteses de chegadas Poisson, serviço exponencial independente, servidor único e capacidade ilimitada, `ρ=λ/μ`, `L=ρ/(1−ρ)`, `Lq=ρ²/(1−ρ)`, `W=1/(μ−λ)` e `Wq=ρ/(μ−λ)` em horas. A interface converte tempos em minutos. Para λ≥μ não existe regime estacionário finito. A comparação é analítica, não uma simulação de eventos discretos. As distribuições e a estabilidade precisam ser verificadas antes de qualquer aplicação real.

## R05 — Registro reproduzível

Preencha título, pergunta, hipótese, método, métrica/unidade, fonte dos dados, resultado, limitações e próxima ação. Exporte JSON local com schema `rubedo.research.protocol.v1`. O usuário registra seus próprios resultados; a exportação não valida conteúdo nem envia dados; a importação explícita restaura somente protocolos locais de esquema compatível. Não há histórico automático. Preserve o arquivo junto de parâmetros, código e versão do experimento.

## R03 — Simulação com semente

Pergunta: as médias simuladas aproximam a espera teórica de nove minutos quando λ=6/h e μ=10/h? Execute 5 repetições, 500 chegadas descartadas e 3.000 observadas por repetição, semente 42. Repita a mesma configuração para checar reprodução; mude a semente e compare a variabilidade. Registre média, desvio entre repetições e diferenças da teoria. Não tratar coincidência como prova da adequação das distribuições. Em operação real, validar distribuições, independência e aquecimento.

## R04 — Alocação contínua de recursos

Pergunta: qual combinação contínua de dois produtos maximiza um valor sintético sob dois recursos? Use valor [3,5], consumos [[1,2],[3,2]], limites [8,12]. A interseção ótima é [2,3], objetivo 21. Compare os vértices; aumente um limite e registre a mudança. A solução não é um plano de produção inteiro nem uma estimativa financeira real. Não extrapolar sem verificar restrições e dados.

## Registros de referência

[Resultados JSON](../examples/reference-results.json) gerados por `node scripts/reference_results.js`. Verificar sem reescrever: `node scripts/reference_results.js --check`. São cinco casos sintéticos, não resultados experimentais observados. Preserve as sementes e entradas ao compartilhar registros com outras frentes, sempre mediante autorização.
