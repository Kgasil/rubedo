# GRAAL Security & Trust 1.1 — Etapa 04 / Rubedo Mini
Data: 2026-11-26. Escopo: extensão 1.0.0 e integridade do ZIP histórico 0.3.0. Sem alteração de produto, design ou pacotes.

## Evidência dos originais
Snapshot: cf5274868c11e5b6cfb41a5ad1a1c49c2cf1fa45 (backup-graal-security-trust-1.1-2026-11-26).

| Versão | Bytes | SHA-256 recalculado | Git blob |
|---|---:|---|---|
| 1.0.0 | 32089 | 1799dc6ccadd786eb960f38c4f7d67cf241e9630942a9e69daebfe96fcfe6ab2 | 6e2cc0c5ce73c1158ad0c2a87b210f72c700514e |
| 0.3.0 | 21671 | ee1bcf4a225783dd60a332ba1720d14127c2c9b88f213ee8e29f4872bd12f1c8 | 9bfa52643f4a082292c8394224a60e1c1b14ad2e |

Ambos os blobs coincidem entre main e backup. Cada ZIP tem nove entradas únicas previstas, sem executáveis nativos; cabeçalhos locais e centrais consistentes, sem comentários, dados extras ou entradas criptografadas identificadas na inspeção. 1.0.0 usa ZIP_STORED: CRC das nove entradas aprovado; hash coincide com SHA256SUMS.txt. 0.3.0 usa DEFLATE: CRC sobre dados descompactados e manifesto histórico serão verificados pela CI, não pela leitura dos bytes comprimidos.

## Revisão integral dos arquivos de runtime 1.0.0
- Manifest V3, action popup e quatro ícones; nenhuma permission, host permission, content script, background ou native messaging declarada.
- core.js: quatro cálculos locais (capacidade, gargalos, experimentos e takt); valida entradas numéricas e limites, não executa código fornecido pelo usuário. Não há chamadas de rede ou acesso ao sistema de arquivos.
- ui.js: resultados inseridos por textContent; idioma PT/EN; cópia explícita via clipboard.writeText e exportação JSON via Blob URL local, revogada após uso. Não há leitura automática de clipboard, envio externo ou persistência observados. O JSON inclui entradas; não utilizar dados confidenciais.
- popup.html e style.css: recursos locais, sem dependências de rede identificadas; quatro ícones PNG com assinatura e dimensões correspondentes (16,32,48,128). A CI verificará também CRC dos chunks e fim do PNG.
- Não há dependência externa de runtime declarada ou incorporada ao pacote. Dependências de teste separadas: Python biblioteca padrão, Node 22, Playwright 1.57.0 e Chromium; actions checkout v4, setup-node v4 e setup-python v5. Não se trata de auditoria de toda a cadeia transitiva de ferramentas CI.
- Nenhum comportamento malicioso evidente encontrado no código 1.0.0. Limitações: cálculos idealizados não substituem validação industrial. O comentário de core.js e o campo version do JSON exportado ainda referenciam 0.3.0, embora manifesto e interface sejam 1.0.0; discrepância de metadados preexistente, não evidência de malware. Preservada nesta fase.
- O packager existente usa arquivos explícitos, ordenados, timestamp fixo e ZIP_STORED; não foi executado para não substituir os originais.

## Validação
- Novo verificador tests/verify_mini_package.py: hash fixado de ambos os ZIPs, lista exata, CRC descompactado, manifesto, PNG e paridade da versão atual com a fonte. SHA-256 histórico fixado no teste, sem alterar SHA256SUMS.txt ou packager.
- CI existente executa 30 casos Mini, testes de pesquisa, cenários e interface Chromium. Acrescentado o novo verificador à CI; resultados a confirmar.
- Não houve análise por Defender ou instalação real de extensão no Chrome/Edge nesta etapa. Testes Chromium do popup isolado não comprovam aceitação de extensão instalada. Sem assinatura ou aprovação de distribuição. Nenhum custo assumido.

## Confirmação CI na etapa 06
[Execução 45878528621](https://github.com/Kgasil/rubedo/actions/runs/45878528621): concluída com sucesso. Ambos os jobs (rules-and-package e browser) aprovados, incluindo verificador dos ZIPs atuais e históricos, testes Node e interface Chromium. Não é scan Defender nem instalação nativa.
