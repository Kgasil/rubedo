# Modelos, hipóteses e limites — Rubedo 0.3.0

Todos os modelos são explorações locais de problemas sintéticos. Não constituem validação industrial. As unidades devem ser consistentes. Entradas são decimais simples (vírgula ou ponto), sem separador de milhares. Não há inferência causal automática.

## M01 — Capacidade
Tempo planejado T em minutos, ciclo c em segundos/unidade, disponibilidade a e rendimento y em frações. Capacidade = 60T/c; produção após disponibilidade = capacidade × a; boas estimadas = capacidade × a × y. Ex.: 480 min, 45 s, 85%, 97% → 640 teóricas, 544 antes de perdas de qualidade, 527,68 boas. Fluxo contínuo idealizado; não é OEE completo e não considera setups, lotes, variabilidade ou restrições de material. Frações são estimativas, não peças garantidas.

## M02 — Linha serial ideal
Taxa limite = menor taxa das estações; produção = taxa × horas. Utilização ideal i = taxa limite/taxa i. Ex.: 120, 95, 110 un./h durante 8 h → estação 2, 760 un. Empates identificados. Não representa filas, bloqueios, falhas, buffers finitos ou recursos compartilhados.

## M03 — Comparação descritiva
Duas séries de 2–100 valores, média, desvio padrão amostral (n−1), diferença B−A e variação relativa à magnitude de A (indefinida se A=0). Ex.: A=[12,14,13,15,16], B=[15,16,17,16,18]; médias 14 e 16,4, diferença 2,4. Não testa significância nem causalidade. Valores separados por espaço, ponto e vírgula ou quebra de linha; decimal vírgula/ponto.

## M04 — Takt e demanda
Takt nominal = 60T/d, com demanda inteira de unidades boas. O ciclo máximo ajustado para perdas = takt × a × y. Saldo estimado = boas estimadas − demanda. Se a ou y for zero, a demanda positiva é inviável nas premissas. Ex.: 480 min, demanda 600, ciclo 45 s, 85%, 97% → takt 48 s, ciclo máximo ajustado 39,576 s, 527,68 boas e déficit de 72,32. Disponibilidade e rendimento fixos; não substitui estudo de capacidade ou balanceamento.

## R01 — Sensibilidade
Variação isolada do ciclo em −d%, 0 e +d%, com d de 0 a 90. Calcula a diferença contra o cenário base mantendo tempo, disponibilidade e rendimento constantes. Não é previsão empírica nem otimização.

## R02 — M/M/1 analítica
Chegadas Poisson λ e atendimento exponencial independente μ, ambos por hora, servidor único, FIFO, capacidade ilimitada e regime estacionário. Para λ<μ: ρ=λ/μ; L=ρ/(1−ρ); Lq=ρ²/(1−ρ); W=1/(μ−λ); Wq=ρ/(μ−λ). W/Wq são convertidos de horas a minutos. Para λ≥μ, não há regime estacionário finito; a interface sinaliza saturação. λ=6 e μ=10 → ρ=60%, W=15 min, Wq=9 min.

## R03 — Simulação estocástica M/M/1
Simulação por chegadas e conclusões, FIFO, inicialmente vazia. Intervalos e serviços exponenciais gerados por inversão com PRNG Mulberry32 de 32 bits (não criptográfico). A semente principal gera as sementes das repetições. Cada repetição reinicia o sistema, descarta as primeiras chegadas de aquecimento e observa n clientes subsequentes. A espera individual é o início do serviço menos a chegada; permanência soma espera e serviço. A média das médias das repetições, desvio amostral entre elas, mínimo e máximo são registrados. Comparação com R02 sob mesmas hipóteses; desvio das médias não é intervalo de confiança. A escolha do aquecimento pode deixar viés; próximo da saturação a variância cresce. Limites: λ, μ entre 0,01 e 10.000/h; λ<μ; 2–20 repetições, 10–20.000 observações, 0–20.000 aquecimento, máximo 400.000 chegadas por execução. Registros JSON incluem parâmetros, sementes e métricas; não prometem reproduzir bits idênticos em qualquer motor JS.

## R04 — Programação linear contínua
Maximizar vA*x+vB*y sujeito a a1*x+b1*y≤L1, a2*x+b2*y≤L2, x,y≥0. Enumerar interseções das quatro retas de fronteira, verificar viabilidade com tolerância numérica, comparar objetivos e relatar folgas e possíveis ótimos alternativos. Todos os parâmetros são não negativos (≤1.000.000); coeficientes positivos de consumo devem ser ≥0,000001 e cada produto deve consumir ao menos um recurso, para evitar domínio ilimitado. Ex.: valores [3,5], consumos [[1,2],[3,2]], limites [8,12] → x=2, y=3, objetivo 21, folgas zero. Modelo contínuo: não arredondar para obter plano inteiro. Não inclui custos fixos, setups, lotes, risco, sazonalidade ou mais de dois recursos. Condicionamento numérico extremo pode exigir solver especializado.

## R05 — Protocolo reproduzível
Schema `rubedo.research.protocol.v1`: título, pergunta e método obrigatórios; hipótese, métrica, origem, resultado, limitações e próxima ação opcionais. Máximo de 3.000 caracteres por campo. Exportação JSON, importação explícita de arquivo local ≤128 KiB com esquema validado; importação inválida preserva os campos. Não avalia veracidade, não envia e não mantém histórico. Conservar parâmetros, versão e dados autorizados junto do protocolo.

[Cinco casos de referência](../examples/reference-results.json) · [Protocolos](experimentos.md)
