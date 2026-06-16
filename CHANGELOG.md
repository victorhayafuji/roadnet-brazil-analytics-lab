# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

> **Como o versionamento é registrado neste projeto:**
> - O **histórico Git** (`git log`) é a fonte da verdade — cada commit é um
>   registro datado e descritivo (padrão *Conventional Commits*).
> - Este **CHANGELOG.md** consolida, por versão, o que mudou (visão legível).
> - O **decision log** (`docs/06_decision_log.md`) registra o *porquê* das
>   decisões técnicas.

## [Não lançado]

### Adicionado
- `docs/07_arquitetura_e_fluxo.md`: documento técnico do fluxo de engenharia de
  dados (raw → staging → marts) com diagrama Mermaid e mapa código → função.

A ser implementado na sequência da Fase 1 (exercícios learning-first):

- Ingestão da malha não pavimentada e do SNV (`.xls` via `xlrd`).
- Validações de qualidade da camada raw.
- Camada staging (padronização de tipos, decimal vírgula→ponto, `segment_key`).
- Marts e KPIs (extensão por UF/rodovia, trechos críticos).

## [0.1.0] - 2026-06-16

Fundação da Fase 1 — ambiente, banco, ingestão de referência e documentação.

### Adicionado
- Ambiente reprodutível: `requirements.txt`, `.env.example`, `tasks.ps1`.
- Camada raw no PostgreSQL/Supabase: schemas `raw`/`staging`/`marts`, tabelas
  `raw_dnit_pavimentada`, `raw_dnit_nao_pavimentada`, `raw_dnit_snv` e RLS.
- Pacote `pipelines/`: utilitários (`db`, `io`, `run_sql`), ingestão de
  referência da malha pavimentada (209.204 linhas carregadas) e stubs
  documentados para as demais cargas/validações.
- Amostras versionadas em `data/sample/` para reprodutibilidade.
- Documentação base `docs/01..06` (visão geral, fontes, dicionário, qualidade,
  métricas, decision log) e scaffold de profiling em `notebooks/`.

### Corrigido
- `CLAUDE.md` reconciliado com o layout real em disco (§6, §7, §15 + §4.4).
- Stack: `.xls` passa a usar `xlrd` (não `openpyxl`).
- Ingestão: `chunksize=1.000` para respeitar o limite de 65.535 parâmetros por
  statement do Postgres.

### Segurança
- RLS habilitado nas tabelas `raw` (resolve o aviso crítico do Supabase).
- Segredos fora do versionamento: `.env` ignorado; apenas `.env.example` com
  placeholders é versionado.

[Não lançado]: https://github.com/victorhayafuji/roadnet-brazil-analytics-lab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/victorhayafuji/roadnet-brazil-analytics-lab/releases/tag/v0.1.0
