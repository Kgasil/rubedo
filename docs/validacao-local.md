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
