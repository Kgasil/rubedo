# Validação local — preparação 0.3.0

- 28 verificações do Mini, 21 dos modelos analíticos/caderno e 22 avançadas (71 testes de regras no total).
- Cinco casos sintéticos reproduzidos pelo script de referência.
- Sintaxe JavaScript, referências locais, IDs únicos em HTML, manifesto, pacote da extensão e SHA-256 verificados.
- 36 verificações em Chromium headless: interface do portal, Mini Lab, Research Workspace e popup; tradução, largura mobile, cálculo, limpeza de resultado, gráficos, download JSON, importação e rejeição de arquivo inválido. Sem erros JavaScript nas páginas testadas.
- Capturas do portal desktop/mobile, Mini Lab, Research Workspace e popup, com inspeção visual do cabeçalho do portal e Mini. Um erro de doctype foi corrigido e os testes repetidos.
- **Limite importante:** a política do ambiente bloqueou navegação direta HTTP local e `file://`. Para os testes de interface, o HTML e seus recursos locais foram carregados em memória no navegador. Não houve teste de navegação entre URLs, instalação real da extensão, CSP de extensão, Chrome/Edge manual ou deploy GitHub Pages. O CI preparado usa HTTP local em ambiente GitHub e não foi executado ainda.
- A revisão científica é interna e exploratória; não é validação industrial, certificação ou revisão por pares. O marco original e os quatro projetos existentes não foram modificados nesta preparação.

## Marco 01 — 0.4.0

73 testes de regras e 38 verificações de interface em Chromium carregado em memória aprovados. Instalação real da extensão e implantação HTTP ainda requerem verificação.

## Revisão para a edição inicial 1.0

A execução HTTP anterior do GitHub Actions foi aprovada em [45747921238](https://github.com/Kgasil/rubedo/actions/runs/45747921238). A revisão adiciona testes de transferência de cenário; consulte a execução da revisão atual. A instalação em Chrome/Edge permanece pendente. Nenhuma alegação de validação industrial.

## Public Lab 1.0 — revisão técnica de lançamento

[CI aprovado](https://github.com/Kgasil/rubedo/actions/runs/45749793253), revisão `a2985b044fadad6dd52ff8039a945f2d4e7b838e`: 30 testes Mini + 21 de pesquisa + 22 avançados + 11 de transferência = 84. 43 verificações de interface Chromium HTTP sem erros de página, cinco casos reproduzidos e 65 referências locais em quatro HTMLs; pacote ZIP íntegro. A promoção 1.0 altera a documentação e o rótulo da edição pública, não os motores ou a extensão. A aceitação real da extensão em Chrome/Edge e a validação independente ainda estão pendentes.

## Candidato 1.0.1 — evidência CI (27/11/2026)

[46067486777](https://github.com/Kgasil/rubedo/actions/runs/46067486777): 257 comparações independentes sintéticas, 97 verificações HTTP, 12 testes de segurança, pacote reproduzível e instalação isolada Chromium confirmados. [Matriz de homologação](homologation-1.0.1.md). Windows, antivírus atualizado e revisão manual pendentes.
