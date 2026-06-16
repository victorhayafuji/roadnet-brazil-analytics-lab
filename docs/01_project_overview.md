# 01 — Visão Geral do Projeto

> Documento de contexto. A fonte da verdade operacional é o [`CLAUDE.md`](../CLAUDE.md).

## O que é

O **RoadNet Brazil Analytics Lab** é um projeto de portfólio em Dados, BI e
Analytics Engineering que constrói uma base analítica sobre a **malha rodoviária
brasileira** a partir de dados públicos oficiais do **DNIT**.

## Objetivo de carreira

Demonstrar domínio prático de ingestão, profiling, padronização, modelagem
analítica, qualidade de dados, SQL, Python, PostgreSQL, dbt/SQL modular e
Power BI — apoiando a transição para Analytics/BI Engineering e Engenharia de
Dados.

## Princípio condutor

**Learning-first / manual-first.** A prioridade é entender cada etapa, não
terminar rápido. Não automatizar o que ainda não foi compreendido — em especial
o profiling e a análise permanecem manuais na Fase 1.

## Fase ativa

**Fase 1 — MVP tabular** da malha e das condições de pavimento, respondendo a
perguntas como: extensão analisada por UF, rodovias com maior extensão avaliada,
distribuição das condições, trechos críticos e inconsistências das bases.

## Camadas de dados

`raw` (dados como vieram) → `staging` (padronizado) → `marts` (analítico).
Ver DDL em [`sql/ddl/`](../sql/ddl) e modelos futuros em [`dbt/models/`](../dbt/models).

## Estado atual (2026-06-16)

Fundação executável criada: ambiente (`requirements.txt`, `.env.example`,
`tasks.ps1`), DDL da camada raw, ingestão de referência da malha pavimentada e
documentação base. Staging, marts, KPIs e leitura do SNV (`.xls`) são os
próximos passos — ver [`06_decision_log.md`](06_decision_log.md).
