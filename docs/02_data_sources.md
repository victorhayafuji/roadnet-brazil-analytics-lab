# 02 — Catálogo de Fontes

> Os arquivos brutos **não são versionados** (ver [`.gitignore`](../.gitignore)).
> Amostras pequenas (header + 500 linhas) ficam em [`data/sample/`](../data/sample)
> para reprodutibilidade. Gere-as com `pwsh ./tasks.ps1 Sample`.

## Portais oficiais (DNIT)

| Recurso | URL |
|---|---|
| Dados Abertos DNIT | https://servicos.dnit.gov.br/dadosabertos/ |
| Condições do Pavimento | https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento |
| PNV e SNV | https://www.gov.br/dnit/pt-br/assuntos/atlas-e-mapas/pnv-e-snv |
| BIT Mapas (fase futura) | https://www.gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas |

## Bases da Fase 1

### 1. Levantamentos — malha pavimentada

| Campo | Valor |
|---|---|
| Nome da base | Condições do pavimento — malha pavimentada |
| Órgão responsável | DNIT |
| URL oficial | https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento |
| Arquivo utilizado | `data/raw/dnit/condicoes_pavimento/levantamentos_pavimentada_2026_05.csv` |
| Data de download | *a preencher* |
| Período de referência | mai/2026 (sufixo `2026_05`); avaliações com `Data Aval.` recentes |
| Formato | CSV; `;` delimitado; **UTF-8 com BOM** |
| Granularidade | 1 linha por levantamento de trecho/sentido (~209.204 linhas, 24 colunas) |
| Uso no projeto | Base principal de condição (Raw → Staging → Fato) |
| Limitações conhecidas | Decimal misto (`ICM` vírgula vs `ICM_Unificado` ponto); aspas escapadas em `Contrato`; `Km_Inicial > Km_Final` em sentido `C`/`D`; nulos como `"ND"` |

### 2. Levantamentos — malha não pavimentada

| Campo | Valor |
|---|---|
| Nome da base | Condições — malha não pavimentada |
| Órgão responsável | DNIT |
| URL oficial | https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento |
| Arquivo utilizado | `data/raw/dnit/condicoes_pavimento/levantamentos_nao_pavimentada_2026_05.csv` |
| Data de download | *a preencher* |
| Período de referência | mai/2026 (sufixo `2026_05`) |
| Formato | CSV; `;` delimitado; **UTF-8 com BOM** |
| Granularidade | 1 linha por levantamento de trecho/sentido (~15.961 linhas, 21 colunas) |
| Uso no projeto | Base complementar (Raw → Staging → Fato / mart unificado) |
| Limitações conhecidas | **Schema diferente** da pavimentada (sem `id_malha`, `ip`, `ic` etc.; com `corrugacoes`, `trilha_roda`, `secao_transversal`, `poca_dagua`, `poeira`); mesmo decimal misto |

### 3. SNV — Sistema Nacional de Viação

| Campo | Valor |
|---|---|
| Nome da base | SNV / Jurisdição de Vias |
| Órgão responsável | DNIT |
| URL oficial | https://www.gov.br/dnit/pt-br/assuntos/atlas-e-mapas/pnv-e-snv |
| Arquivo utilizado | `data/raw/dnit/snv/snv_202407a.xls` |
| Data de download | *a preencher* |
| Período de referência | jul/2024 (`202407a`) |
| Formato | **Excel binário antigo (.xls)** — ler com `xlrd`, não `openpyxl` |
| Granularidade | Trecho SNV (~7.600 linhas, 20 colunas); aba `TABELA SNV`, cabeçalho na 3ª linha |
| Uso no projeto | Referência da malha federal (Raw → Staging → Dimensões) |
| Limitações conhecidas | Pode não ser a versão mais recente — verificar antes de fechar a Fase 1 (ver [`06_decision_log.md`](06_decision_log.md)) |

## Diferenças entre os arquivos

- **Pavimentada vs não pavimentada:** schemas distintos (24 vs 21 colunas);
  qualquer mart unificado deve preservar e documentar as diferenças.
- **CSV vs XLS:** os levantamentos são CSV texto; o SNV é Excel binário e exige
  engine de leitura diferente.
