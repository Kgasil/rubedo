# Project Rubedo — planejamento após Public Lab 1.0

## Identidade e finalidade
- Project Rubedo — Ciência e Inovação / Science & Innovation.
- Turning knowledge into discovery. / Transformar conhecimento em descoberta.
- Ação: Discover / Descobrir.
- Paleta: fundo #21100D, vermelho #B52F2B, laranja #EE7441, dourado #EAC477, texto #F9E7D8. Símbolo geométrico de transformação, com vértices e cristal central. Proposta não registrada como marca.
- GRAAL: Genesis → Rubedo → Argus → Aeris → Lilium. Rubedo depois de Genesis, nunca antes. Manter K&G Vision como marca-mãe, não um sexto projeto. Não mexer no marco original (usuário o chama de marco 0; materiais existentes podem usar marco público 1.0). Não renumerar entregas anteriores.

## Escopo
Pesquisa aplicada, simulação computacional, pesquisa operacional, matemática aplicada e engenharia de produção. Não vender serviços ou prometer certificações. Evitar sobreposição: Genesis ensina por estudo autônomo, Rubedo investiga modelos e experimentos, Argus trabalha segurança/integração/assurance de IA, Aeris produtividade e Lilium análise empresarial. Rubedo pode usar dados sintéticos, públicos com licença ou explicitamente autorizados. Não publicar dados pessoais ou corporativos.

## Arquitetura pronta
Site estático bilíngue (PT/EN), aplicação local, extensão Chromium Manifest V3, motor JavaScript comum, ZIP dedicado, testes e CI. Interfaces Mini e Research em PT/EN. Sem backend, dependências externas de runtime, chaves, coleta, telemetria ou armazenamento de dados. A extensão não injeta código em páginas e não lê conteúdo automaticamente. Não usar eval para entradas do usuário.

## Roadmap proposto
1. Fundação: validar nome, aprovar identidade, criar repositório, publicar o pacote e validar páginas e extensão. Não afirmar lançamento antes de confirmação.
2. Modelos adicionais: filas M/M/1 analítica, sensibilidade, simulação de filas com semente e programação linear contínua de dois produtos preparados na 0.3.0; expansão para múltiplos servidores, restrições inteiras e eventos industriais permanece proposta.
3. Research Notes: caderno local e exportação e importação JSON preparados; ampliar para coleção de estudos, incluindo resultados inconclusivos.
4. Biblioteca de experimentos: exemplos industriais e científicos pequenos; evitar replicar os PDFs do Genesis. Exportação JSON implementada; CSV proposto, sem dados enviados.
5. Revisão de qualidade e futura integração ao ecossistema: ferramentas interoperáveis com exemplos autorizados, sem acoplar diretamente ou modificar os outros projetos.

## Automações
Implementada no pacote: GitHub Actions para sintaxe, testes e integridade do ZIP/links a cada push/PR ou acionamento manual. Executada no GitHub: [revisão técnica aprovada](https://github.com/Kgasil/rubedo/actions/runs/45749793253).
Preparados scripts de ZIP/SHA-256, registros de referência e CI de navegação headless; futuras propostas: auditoria periódica de links, revisão formal de acessibilidade, releases somente mediante aprovação e ampliação dos registros reproduzíveis. Não criar tarefa recorrente nem agendar publicação sem pedido explícito. O repositório já existe e executa as verificações por commit.

## Critérios de entrega
Site PT/EN, navegação consistente, Mini Lab 4 ferramentas, extensão 4 ferramentas, Research Workspace 4 modelos e caderno, pacote instalável, tutoriais, testes de cálculo, integridade de artefatos, documentação das hipóteses, nenhuma alegação exagerada. CI HTTP e implantação pública anterior confirmados; aceitação manual Chrome/Edge e validação industrial permanecem pendentes.

## Perspectiva organizacional
A [arquitetura do ecossistema](ecossistema.md) define missões próprias, interfaces futuras e limites atuais. Cada projeto tem autonomia de função e cooperação planejada; hoje não há subsidiárias ou equipes constituídas.
