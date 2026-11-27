# Rubedo Mini — 1.0.0 · prévia experimental

Capacidade de produção aproximada, comparação descritiva de séries e takt/demanda. PT/EN, exemplos fictícios, cópia e exportação JSON local, ícones próprios. O Mini Lab e a extensão também identificam gargalos em uma linha serial ideal. Os resultados não substituem análise profissional, teste de hipótese ou validação industrial.

## Instalação manual / Manual installation

1. Baixe [Rubedo Mini v1.0.0](../downloads/Rubedo-Mini-v1.0.0-install.zip) e extraia em pasta permanente.
2. Abra `chrome://extensions/` ou `edge://extensions/` em um computador.
3. Ative o modo desenvolvedor, se permitido, e escolha **Carregar sem compactação**.
4. Selecione a pasta que contém `manifest.json`.
5. Abra Rubedo Mini no menu de extensões e experimente um exemplo. Fixe o ícone se desejar.

Atualização: substitua os arquivos e clique em Recarregar. Remoção: clique em Remover. Confira o [SHA-256](../downloads/SHA256SUMS.txt). Não contorne políticas administrativas. A interface do popup foi testada isoladamente em Chromium; instalação real e comportamento do popup em Chrome/Edge ainda exigem aceitação manual. Não publicada nas lojas.

Manifest V3 sem permissões declaradas, scripts de conteúdo, background, conta, telemetria ou armazenamento persistente. Copiar/baixar exige ação explícita. O JSON contém os valores inseridos: não use dados confidenciais. Os arquivos permanecem no dispositivo. Não executa códigos fornecidos pelo usuário.

**English:** Extract the ZIP, open the browser extension manager, enable Developer mode where permitted, choose Load unpacked, select the folder containing manifest.json, and open Rubedo Mini. Reload to update; Remove to uninstall. Experimental local calculations, not a validated decision tool. Actual extension installation remains untested.

[Mini Lab](../mini/index.html) · [Site e tutorial](../index.html#instalar) · [Model assumptions](../docs/modelos.md)

[Site e tutorial](https://kgasil.github.io/rubedo/#instalar) · [Download ZIP](https://github.com/Kgasil/rubedo/raw/refs/heads/main/downloads/Rubedo-Mini-v1.0.0-install.zip). A versão 1.0.0 inclui gargalos, perdas de disponibilidade e qualidade e cobertura da demanda.

**Candidato / Candidate 1.0.1:** a fonte nesta branch e os JSONs exportados identificam 1.0.1. O ZIP público 1.0.0 continua intacto. Candidate packaging is staging-only; no new release or store submission.

### Candidate installation / Instalação do candidato

Authorized isolated evaluation only. Build into an empty staging directory using `python3 scripts/package_extension.py --output-dir /path/to/empty-stage`. Compare SHA-256 with the candidate CI log and scan the exact ZIP with updated protection before extracting. Use a clean Chrome/Edge profile and Load unpacked only if permitted; never disable security controls. Verify all four tools, local JSON export, language switching and removal. No store listing or paid feature. See [candidate gates](../docs/security-candidate-1.0.1.md).

**Acceptance update:** isolated bundled Chromium install succeeded in CI 46067486777 with the exact candidate ZIP hash. This is not branded Chrome/Edge Windows acceptance or antivirus approval. [Manual evidence instructions](../docs/windows-acceptance-1.0.1.md).
