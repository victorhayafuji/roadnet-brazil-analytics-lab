# RoadNet Brazil Analytics Lab

Projeto de Analytics Engineering para construção de uma base analítica sobre a malha rodoviária brasileira, utilizando dados públicos do DNIT.

## Objetivo

Construir um pipeline analítico com ingestão, profiling, padronização, qualidade de dados, modelagem e primeiros KPIs sobre rodovias brasileiras.

## Fase atual

Fase 1 — MVP tabular com dados do SNV e condições de pavimento.

## Fontes iniciais

- DNIT — Sistema Nacional de Viação / Jurisdição de Vias
- DNIT — Condições do Pavimento
- Levantamentos de rodovias pavimentadas e não pavimentadas

## Stack prevista

- Python
- PostgreSQL
- SQL
- dbt
- Power BI
- Git/GitHub

## Como reproduzir (Fase 1)

> Requer **Python 3.12** (`py -3`). No Windows, use o PowerShell 7 (`pwsh`).
> O banco é **Supabase** (Postgres gerenciado) — os schemas `raw/staging/marts`
> e as tabelas raw já estão provisionados. Ver `docs/06_decision_log.md`.

```powershell
# 1. Ambiente
pwsh ./tasks.ps1 Setup            # cria .venv e instala requirements.txt

# 2. Credenciais
Copy-Item .env.example .env        # cole a Session pooler string + senha do Supabase
                                   # (painel: Project -> Connect -> Session pooler)

# 3. (Opcional) recriar schemas/tabelas raw + RLS — já provisionado no Supabase
pwsh ./tasks.ps1 DbInit            # ou apenas: pwsh ./tasks.ps1 Rls

# 4. Ingestão de referência (malha pavimentada -> raw.raw_dnit_pavimentada)
pwsh ./tasks.ps1 IngestPavimentada

# 5. (Opcional) amostras pequenas versionadas em data/sample/
pwsh ./tasks.ps1 Sample
```

As ingestões da malha não pavimentada e do SNV (`.xls`) e as validações de
qualidade são **stubs** intencionais (princípio *learning-first*) — implemente-os
seguindo `pipelines/ingest/load_pavimentada.py` como modelo.

## Documentação

- [`docs/01_project_overview.md`](docs/01_project_overview.md) — visão geral
- [`docs/02_data_sources.md`](docs/02_data_sources.md) — catálogo de fontes
- [`docs/03_data_dictionary.md`](docs/03_data_dictionary.md) — dicionário de dados
- [`docs/04_quality_rules.md`](docs/04_quality_rules.md) — regras de qualidade
- [`docs/05_metrics_catalog.md`](docs/05_metrics_catalog.md) — catálogo de métricas
- [`docs/06_decision_log.md`](docs/06_decision_log.md) — decisões
- [`CLAUDE.md`](CLAUDE.md) — fonte da verdade operacional

## Observação

Os arquivos brutos de dados não são versionados neste repositório (ver
`.gitignore`). As fontes oficiais e instruções de obtenção estão documentadas em
[`docs/02_data_sources.md`](docs/02_data_sources.md); amostras pequenas ficam em
`data/sample/`.