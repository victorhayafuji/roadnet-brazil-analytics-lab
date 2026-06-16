# 04 — Regras de Qualidade

> Base: CLAUDE.md §10 + violações **já observadas** na vistoria de 2026-06-16.
> Stub de implementação: [`pipelines/quality/validate_raw_files.py`](../pipelines/quality/validate_raw_files.py).

## Regras obrigatórias

| Regra | Severidade |
|---|---|
| `state_code` (uf) não nulo | Erro |
| `road_code` (rodovia) não nulo | Erro |
| `km_start` não pode ser maior que `km_end` | Erro (ver nota direcional) |
| `segment_length_km` não pode ser negativo | Erro |
| `source_file` preenchido | Erro |
| `batch_id` preenchido | Erro |
| Duplicidade de `segment_key` | Alerta |
| % de nulos por coluna documentado | Alerta |

## Regras de consistência

- `state_code` com 2 caracteres.
- `road_code` em formato padronizado (`BR-NNN`).
- `km_start` / `km_end` numéricos.
- `segment_length_km = km_end - km_start`.
- Valores de classificação dentro de domínio conhecido.
- Linhas sem rodovia separadas para análise.

## Violações e armadilhas já observadas (a tratar no staging)

| # | Achado | Evidência | Tratamento sugerido |
|---|---|---|---|
| 1 | **`km_start > km_end`** existe nos dados | Linha com `Km_Inicial=90`, `Km_Final=89` (sentido `D`); o par sentido `C` aparece invertido | Decidir: normalizar com `min`/`max` ou manter por sentido. Documentar a decisão. |
| 2 | **Decimal misto na mesma linha** | `ICM="51,25"` (vírgula) vs `ICM_Unificado="51.25"` (ponto); `"2,5"` vs `"2.5"` | Converter vírgula→ponto antes do cast numérico no staging. |
| 3 | **Aspas escapadas** em `Contrato` | `"""26 00650/2025"""` | Já tratado na leitura (`quotechar='"'`); limpar resíduo de aspas no staging. |
| 4 | **Nulos como `"ND"`** | Campos de defeito com valor literal `ND` | Mapear `"ND"` → `NULL` no staging (na raw fica como veio). |
| 5 | **Encoding com BOM** | UTF-8 BOM no início do header | Já tratado: leitura com `utf-8-sig`. |
| 6 | **Schemas divergentes** | pavimentada (24 col) ≠ não pavimentada (21 col) | Manter tabelas separadas; unificar só em mart, preservando diferenças. |

## Princípio

A camada **raw preserva os valores como vieram** (CLAUDE.md §9.1). Toda correção
acima é responsabilidade do **staging**, nunca da ingestão.
