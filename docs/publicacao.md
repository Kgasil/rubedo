# Checklist de publicação — executar apenas com autorização

- Criar `Kgasil/rubedo` no GitHub (sugerido público, se aprovado), branch `main`, vazio. Confirmar disponibilidade do nome e permissões.
- Extrair o ZIP completo; preservar pastas e arquivos ocultos (`.github`). Verificar `node tests/mini.test.js`, `node tests/research.test.js`, `node tests/advanced.test.js`, `node scripts/reference_results.js --check` e `python3 tests/check_package.py`.
- Enviar os arquivos ao repositório, por exemplo usando GitHub Desktop ou `git` local. Se já houver arquivos na branch, clonar e mesclar em vez de sobrescrever histórico. Nenhum token no código.
- Configurar GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root. Confirmar o endereço real `https://kgasil.github.io/rubedo/` antes de criar links externos.
- Conferir CI, build/deploy, site em desktop e mobile, Mini Lab, Research Workspace, simulação com semente, otimização, importação e exportação JSON, mudança PT/EN, links, download, instalação manual em Chrome/Edge e exemplos. Não tratar CI como aceitação completa da extensão.
- Autorizado para o marco 01: inserir Rubedo após Genesis nos menus dos cinco sites, inclusive biblioteca e páginas secundárias com navegação comum; atualizar portal, README institucional, perfil e todos os READMEs relevantes. Não mudar marcos, versões ou funcionalidades existentes. Preservar K&G Vision → Genesis → Rubedo → Argus → Aeris → Lilium.
- Atualizar banners institucionais somente se aprovado, preservando assinatura K&G Vision e adicionando cor vermelho/laranja/dourado à paleta de projetos.
- Revisar os links internos, publicar e confirmar cada implantação por commit. Rubedo integra o marco 01; não alterar o histórico dos marcos anteriores ou versões dos demais projetos.
