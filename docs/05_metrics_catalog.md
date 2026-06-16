# 05 — Catálogo de Métricas

> KPIs da Fase 1 (CLAUDE.md §11). As fórmulas assumem a camada staging já
> tipada; enquanto ela não existe, servem de especificação. Grão padrão:
> trecho/UF/rodovia.

## KPIs obrigatórios

| Métrica | Definição | Fórmula | Grão | Fonte | Limitação |
|---|---|---|---|---|---|
| Extensão analisada | Soma da extensão dos trechos avaliados | `SUM(km_end - km_start)` | trecho | stg pavimentada + não pavimentada | Depende de km consistente (ver regra #1) |
| Extensão por UF | Extensão somada por estado | `SUM(...) GROUP BY state_code` | UF | idem | Dupla contagem por sentido se não normalizado |
| Extensão por rodovia | Extensão somada por BR | `SUM(...) GROUP BY road_code` | rodovia | idem | idem |
| Qtd. de segmentos | Contagem de trechos únicos | `COUNT(DISTINCT segment_key)` | trecho | idem | `segment_key` a definir no staging |
| Distribuição por superfície | Pavimentada vs não pavimentada | `SUM(...) GROUP BY surface_type` | superfície | mart unificado | Schemas diferentes |
| Trechos críticos | Trechos classificados como ruins/críticos | filtro por regra de `icm_unified` documentada | trecho | stg | Faixa de corte a definir |
| Ranking UFs críticas | UFs com maior extensão crítica | `SUM(... WHERE critico) GROUP BY state_code ORDER BY ... DESC` | UF | mart | Depende da definição de "crítico" |
| Ranking rodovias críticas | BRs com maior extensão crítica | `... GROUP BY road_code ORDER BY ... DESC` | rodovia | mart | idem |

## KPIs opcionais

- Média de indicador (`icm_unified`) por UF / por rodovia.
- % de trechos sem classificação.
- % de inconsistências (regras de [`04_quality_rules.md`](04_quality_rules.md)).
- Top 10 rodovias por extensão analisada.
- Top 10 rodovias com pior condição.

## Pendência de definição

A faixa de corte de **"trecho crítico"** (sobre `icm_unified`) ainda não está
fixada — registrar a decisão em [`06_decision_log.md`](06_decision_log.md) antes
de publicar rankings.
