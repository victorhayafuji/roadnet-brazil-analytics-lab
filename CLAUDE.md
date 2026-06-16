# CLAUDE.md — RoadNet Brazil Analytics Lab

> **Fonte da verdade operacional do projeto.**  
> Em caso de conflito entre este arquivo, anotações soltas, prompts antigos ou documentos auxiliares, **prevalece este `CLAUDE.md`**.
>
> **Projeto:** RoadNet Brazil Analytics Lab  
> **Fase ativa:** Fase 1 — MVP tabular da malha rodoviária e condições de pavimento  
> **Objetivo de carreira:** Analytics Engineering, BI Engineering e transição gradual para Engenharia de Dados  
> **Modo de execução:** aprendizado manual-first — evitar automação excessiva por agentes de IA  
> **Última revisão:** 2026-06-16

---

## 0. Contexto rápido

O **RoadNet Brazil Analytics Lab** é um projeto de portfólio em Dados, BI e Analytics Engineering voltado à construção de uma base analítica sobre a **malha rodoviária brasileira**, utilizando dados públicos oficiais, principalmente do **DNIT**.

A proposta é demonstrar domínio prático de:

- ingestão de dados públicos;
- organização de dados brutos;
- profiling;
- padronização;
- modelagem analítica;
- qualidade de dados;
- SQL;
- Python;
- PostgreSQL;
- dbt ou SQL modular;
- Power BI;
- documentação técnica;
- raciocínio de produto de dados.

O projeto também deve gerar aprendizados e referências reutilizáveis para o **DataCommunity Hub**, especialmente nas frentes de benchmarks, governança, dados públicos, qualidade de dados e construção de produtos analíticos.

---

## 1. Princípio principal do projeto

Este projeto é **learning-first**.

A prioridade não é terminar rápido.  
A prioridade é entender profundamente cada etapa:

1. de onde o dado vem;
2. como ele está estruturado;
3. quais problemas possui;
4. como deve ser tratado;
5. como deve ser modelado;
6. quais métricas são confiáveis;
7. quais limitações precisam ser documentadas.

### Regra de ouro

> Não automatizar aquilo que ainda não foi compreendido.

Ferramentas de IA podem apoiar revisão, documentação e esclarecimento, mas **não devem substituir o raciocínio técnico** durante a Fase 1.

---

## 2. Objetivo da Fase 1

Construir uma primeira base analítica confiável sobre rodovias brasileiras usando:

- SNV / Jurisdição de Vias;
- levantamentos de condições de pavimento;
- levantamentos de trechos não pavimentados.

A entrega da Fase 1 deve permitir responder perguntas como:

- Qual é a extensão analisada por UF?
- Quais rodovias possuem maior extensão avaliada?
- Como as condições de pavimento se distribuem por UF?
- Quais trechos podem ser considerados críticos?
- Quais inconsistências existem nas bases públicas?
- Como transformar arquivos brutos em uma camada analítica documentada?

---

## 3. Fontes oficiais e referências

### 3.1 DNIT — Dados Abertos

Portal oficial de dados abertos do DNIT. Deve ser usado como fonte primária para datasets relacionados a rodovias, condições de pavimento, tráfego, obras, pesagem e jurisdição de vias.

URL de referência:  
https://servicos.dnit.gov.br/dadosabertos/

### 3.2 DNIT — Condições do Pavimento

Dataset oficial com avaliações de condições de manutenção do pavimento e da malha sob jurisdição do DNIT.

URL de referência:  
https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento

### 3.3 DNIT — PNV e SNV

Página oficial sobre Plano Nacional de Viação e Sistema Nacional de Viação. Deve ser usada para consultar versões oficiais do SNV e orientações sobre os trechos.

URL de referência:  
https://www.gov.br/dnit/pt-br/assuntos/atlas-e-mapas/pnv-e-snv

### 3.4 Ministério dos Transportes — BIT Mapas

Fonte complementar para mapas rodoviários, rodovias concedidas e bases georreferenciadas. Entrará com mais força em fases futuras.

URL de referência:  
https://www.gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas

---

## 4. Bases iniciais da Fase 1

### 4.1 Arquivos já selecionados

Os arquivos iniciais do projeto são:

```text
data/raw/dnit/snv/snv_202407a.xls
data/raw/dnit/condicoes_pavimento/levantamentos_pavimentada_2026_05.csv
data/raw/dnit/condicoes_pavimento/levantamentos_nao_pavimentada_2026_05.csv
```

### 4.2 Papel de cada base

| Arquivo | Papel no projeto | Camada |
|---|---|---|
| `snv_202407a.xls` | Base de referência da malha rodoviária federal | Raw → Staging → Dimensões |
| `levantamentos_pavimentada_2026_05.csv` | Base principal de condição da malha pavimentada | Raw → Staging → Fato |
| `levantamentos_nao_pavimentada_2026_05.csv` | Base complementar para trechos não pavimentados | Raw → Staging → Fato / Mart unificado |

### 4.3 Atenção sobre recência

O arquivo `snv_202407a.xls` pode não ser a versão mais recente do SNV.  
Antes de fechar a Fase 1, verificar se existe versão mais atual no portal oficial do DNIT.

Se a versão mais recente for adotada, registrar a decisão em:

```text
docs/06_decision_log.md
```

---

## 5. Escopo ativo da Fase 1

### 5.1 Dentro do escopo

- Organizar arquivos brutos em `data/raw`.
- Criar catálogo de fontes.
- Fazer profiling inicial dos arquivos.
- Criar dicionário de dados v1.
- Criar camada raw no banco.
- Criar camada staging com nomes e tipos padronizados.
- Criar chaves analíticas de trecho.
- Criar primeiras tabelas marts.
- Criar regras básicas de qualidade.
- Calcular KPIs iniciais.
- Documentar decisões, limitações e problemas encontrados.

### 5.2 Fora do escopo da Fase 1

Não implementar agora:

- Airflow;
- Prefect;
- PostGIS;
- BigQuery;
- Power BI avançado;
- mapas interativos;
- dados de tráfego;
- dados de obras;
- dados de concessões;
- ANTT;
- CNT;
- dashboards finais;
- API;
- frontend;
- automação completa de ponta a ponta.

Esses itens pertencem a fases futuras.

---

## 6. Stack técnica da Fase 1

| Camada | Tecnologia recomendada | Observação |
|---|---|---|
| Linguagem | Python | Leitura, profiling e carga |
| Bibliotecas | pandas, openpyxl, sqlalchemy, psycopg | Adicionar conforme necessidade |
| Banco | PostgreSQL | Base local do projeto |
| Transformação | SQL modular ou dbt Core | Começar simples; evoluir para dbt |
| BI | Power BI | Apenas exploração inicial na Fase 1 |
| Documentação | Markdown | README, dicionário, catálogo e decision log |
| Versionamento | Git/GitHub | Commits pequenos e descritivos |

---

## 7. Estrutura de repositório

```text
roadnet-brazil-analytics-lab/
├── README.md
├── CLAUDE.md
├── docs/
│   ├── 01_project_overview.md
│   ├── 02_data_sources.md
│   ├── 03_data_dictionary.md
│   ├── 04_quality_rules.md
│   ├── 05_metrics_catalog.md
│   └── 06_decision_log.md
├── data/
│   ├── raw/
│   │   └── dnit/
│   │       ├── snv/
│   │       └── condicoes_pavimento/
│   ├── processed/
│   └── samples/
├── notebooks/
│   └── 01_data_profiling.ipynb
├── src/
│   ├── ingest/
│   │   ├── load_snv.py
│   │   ├── load_pavimentada.py
│   │   └── load_nao_pavimentada.py
│   ├── quality/
│   │   └── validate_raw_files.py
│   └── utils/
│       └── normalize_columns.py
├── sql/
│   ├── 00_setup/
│   ├── 01_raw/
│   ├── 02_staging/
│   └── 03_marts/
├── dbt/
│   └── roadnet/
├── powerbi/
└── references/
```

---

## 8. Workflow manual da Fase 1

### Etapa 1 — Organizar arquivos brutos

Objetivo: garantir que os arquivos originais estejam preservados.

Checklist:

- [ ] Criar estrutura `data/raw/dnit`.
- [ ] Salvar arquivos originais sem alteração.
- [ ] Registrar nome do arquivo, fonte e data de download.
- [ ] Não editar os arquivos brutos manualmente.
- [ ] Criar cópias apenas em `data/processed` se necessário.

---

### Etapa 2 — Catálogo de fontes

Arquivo de destino:

```text
docs/02_data_sources.md
```

Cada fonte deve ter:

| Campo | Preencher |
|---|---|
| Nome da base | |
| Órgão responsável | |
| URL oficial | |
| Arquivo utilizado | |
| Data de download | |
| Período de referência | |
| Formato | |
| Granularidade | |
| Uso no projeto | |
| Limitações conhecidas | |

Critério de pronto:

- [ ] Todas as bases da Fase 1 catalogadas.
- [ ] URLs oficiais registradas.
- [ ] Diferenças entre arquivos documentadas.
- [ ] Recência das fontes registrada.

---

### Etapa 3 — Profiling inicial

Arquivo de destino:

```text
notebooks/01_data_profiling.ipynb
```

Checagens mínimas para cada arquivo:

- [ ] Quantidade de linhas.
- [ ] Quantidade de colunas.
- [ ] Nomes das colunas.
- [ ] Tipos inferidos.
- [ ] Percentual de nulos por coluna.
- [ ] Duplicidades.
- [ ] Valores distintos de UF.
- [ ] Valores distintos de rodovia.
- [ ] Range de km inicial e km final.
- [ ] Campos de indicadores disponíveis.
- [ ] Possíveis problemas de encoding, separador ou decimal.

Perguntas de aprendizado:

- Qual é a granularidade real da base?
- Cada linha representa um trecho, um levantamento, um ponto ou uma observação?
- Quais campos podem ser usados como chave?
- Quais campos são indicadores?
- Quais campos são dimensões?

---

### Etapa 4 — Dicionário de dados

Arquivo de destino:

```text
docs/03_data_dictionary.md
```

Modelo:

| Campo original | Campo padronizado | Tipo esperado | Descrição | Regra |
|---|---|---|---|---|
| `UF` | `state_code` | text | Unidade federativa | Deve ter 2 caracteres |
| `Rodovia` | `road_code` | text | Código da rodovia | Padronizar formato |
| `Km_Inicial` | `km_start` | numeric | Km inicial do trecho | Não pode ser maior que `km_end` |
| `Km_Final` | `km_end` | numeric | Km final do trecho | Deve ser >= `km_start` |
| `ICM_Unificado` | `icm_unified` | text/numeric | Indicador consolidado | Validar domínio |

Critério de pronto:

- [ ] Campos principais documentados.
- [ ] Campos de chave identificados.
- [ ] Campos de métrica identificados.
- [ ] Campos descartados ou ignorados justificados.
- [ ] Diferenças entre pavimentada e não pavimentada documentadas.

---

## 9. Camadas de dados

### 9.1 Camada raw

Objetivo: armazenar os dados como vieram da fonte.

Tabelas previstas:

```text
raw_dnit_snv
raw_dnit_pavimentada
raw_dnit_nao_pavimentada
```

Regras:

- Preservar nomes originais sempre que possível.
- Adicionar `source_file`.
- Adicionar `ingested_at`.
- Adicionar `batch_id`.
- Não corrigir valores na raw.
- Não remover colunas sem registrar decisão.

---

### 9.2 Camada staging

Objetivo: padronizar nomes, tipos e campos mínimos para análise.

Tabelas previstas:

```text
stg_dnit_snv
stg_dnit_pavimentada
stg_dnit_nao_pavimentada
```

Transformações mínimas:

- Converter nomes para `snake_case`.
- Padronizar UF.
- Padronizar rodovia.
- Converter km para número decimal.
- Normalizar sentido.
- Criar `segment_key`.
- Remover espaços excedentes.
- Converter strings vazias para `null`.
- Manter referência ao arquivo de origem.

Exemplo de chave de trecho:

```text
state_code || '-' || road_code || '-' || km_start || '-' || km_end || '-' || direction
```

A chave pode mudar conforme o profiling revelar melhor granularidade.

---

### 9.3 Camada mart

Objetivo: criar tabelas analíticas para KPI e visualização.

Tabelas previstas:

```text
dim_state
dim_road
dim_segment
fact_road_condition
mart_condition_by_state
mart_condition_by_road
mart_critical_segments
```

A Fase 1 pode criar uma visão unificada entre pavimentada e não pavimentada, desde que as diferenças entre os schemas sejam preservadas e documentadas.

Tabela possível:

```text
mart_road_condition_unified
```

---

## 10. Regras de qualidade

### 10.1 Regras obrigatórias

| Regra | Severidade |
|---|---|
| `state_code` não pode ser nulo | Erro |
| `road_code` não pode ser nulo | Erro |
| `km_start` não pode ser maior que `km_end` | Erro |
| `segment_length_km` não pode ser negativo | Erro |
| `source_file` deve estar preenchido | Erro |
| `batch_id` deve estar preenchido | Erro |
| Duplicidade de `segment_key` deve ser investigada | Alerta |
| Percentual de nulos por coluna deve ser documentado | Alerta |

### 10.2 Regras de consistência

- `state_code` deve ter 2 caracteres.
- `road_code` deve estar em formato padronizado.
- `km_start` e `km_end` devem ser numéricos.
- `segment_length_km = km_end - km_start`.
- Valores de classificação devem estar em domínio conhecido.
- Linhas sem rodovia devem ser separadas para análise.

---

## 11. KPIs da Fase 1

### 11.1 KPIs obrigatórios

| KPI | Descrição |
|---|---|
| Extensão analisada | Soma da extensão dos trechos avaliados |
| Extensão por UF | Soma da extensão por estado |
| Extensão por rodovia | Soma da extensão por BR |
| Quantidade de segmentos | Contagem de trechos únicos |
| Distribuição por tipo de superfície | Pavimentada vs não pavimentada |
| Trechos críticos | Trechos classificados como ruins/críticos conforme regra documentada |
| Ranking de UFs críticas | UFs com maior extensão crítica |
| Ranking de rodovias críticas | Rodovias com maior extensão crítica |

### 11.2 KPIs opcionais

- Média de indicador por UF.
- Média de indicador por rodovia.
- Percentual de trechos sem classificação.
- Percentual de inconsistências.
- Top 10 rodovias por extensão analisada.
- Top 10 rodovias com pior condição.

---

## 12. Métricas e regras de negócio

Arquivo de destino:

```text
docs/05_metrics_catalog.md
```

Cada métrica deve conter:

| Campo | Descrição |
|---|---|
| Nome da métrica | |
| Definição | |
| Fórmula | |
| Grão | |
| Fonte | |
| Limitações | |
| Exemplo de query | |

Exemplo:

```text
Métrica: Extensão analisada
Definição: soma da extensão dos trechos avaliados na base de pavimento.
Fórmula: SUM(km_end - km_start)
Grão: trecho/UF/rodovia
Fonte: stg_dnit_pavimentada e stg_dnit_nao_pavimentada
Limitação: depende da consistência dos campos de km inicial e km final.
```

---

## 13. Decision log

Arquivo de destino:

```text
docs/06_decision_log.md
```

Modelo:

```text
# Decision Log

## 2026-06-16 — Uso do SNV 202407A na Fase 1

Decisão:
Usar o arquivo `snv_202407a.xls` como base inicial da Fase 1.

Motivo:
Arquivo já disponível localmente e suficiente para iniciar profiling e modelagem.

Risco:
Pode existir versão mais recente do SNV.

Mitigação:
Verificar versão mais atual no portal oficial do DNIT antes de fechar a Fase 1.

Status:
Aberto.
```

Toda decisão que alterar modelagem, fonte, regra de qualidade ou métrica deve ser registrada.

---

## 14. Critério de pronto da Fase 1

A Fase 1 só pode ser considerada concluída quando:

- [ ] Arquivos brutos organizados.
- [ ] Catálogo de fontes preenchido.
- [ ] Profiling inicial documentado.
- [ ] Dicionário de dados v1 criado.
- [ ] Raw tables carregadas.
- [ ] Staging tables criadas.
- [ ] Nomes e tipos padronizados.
- [ ] `segment_key` definido e documentado.
- [ ] Pelo menos 5 regras de qualidade implementadas.
- [ ] Pelo menos 3 marts criados.
- [ ] Pelo menos 5 KPIs calculáveis via SQL.
- [ ] Limitações conhecidas documentadas.
- [ ] README com instrução de execução.
- [ ] Decision log preenchido.
- [ ] Pelo menos uma análise executiva inicial produzida.

---

## 15. Comandos previstos

### 15.1 Ambiente Python

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas openpyxl sqlalchemy psycopg[binary] python-dotenv
```

### 15.2 Profiling

```bash
jupyter notebook notebooks/01_data_profiling.ipynb
```

### 15.3 Carga inicial

```bash
python src/ingest/load_snv.py
python src/ingest/load_pavimentada.py
python src/ingest/load_nao_pavimentada.py
```

### 15.4 Validação

```bash
python src/quality/validate_raw_files.py
```

Os comandos podem mudar conforme o projeto evoluir. Toda mudança deve ser registrada no README.

---

## 16. Boas práticas de desenvolvimento

- Fazer commits pequenos.
- Um commit por etapa lógica.
- Não misturar ingestão, modelagem e dashboard no mesmo commit.
- Documentar decisões antes de mudar regra de negócio.
- Não sobrescrever raw files.
- Não apagar dados inconsistentes sem registrar.
- Preferir clareza a sofisticação.
- Priorizar SQL legível.
- Priorizar documentação simples e útil.
- Explicar no README como reproduzir o projeto.

---

## 17. Convenções de nomenclatura

### 17.1 Schemas

```text
raw
staging
marts
```

### 17.2 Tabelas

```text
raw_dnit_pavimentada
stg_dnit_pavimentada
fact_road_condition
dim_road
mart_condition_by_state
```

### 17.3 Colunas

Usar `snake_case`.

Exemplos:

```text
state_code
road_code
km_start
km_end
segment_length_km
source_file
ingested_at
batch_id
```

---

## 18. Perguntas de aprendizado

Ao final da Fase 1, o responsável pelo projeto deve conseguir responder:

1. Qual é a diferença entre raw, staging e mart?
2. Por que não devemos alterar arquivos brutos?
3. Qual é a granularidade da base de pavimento?
4. Como foi definida a chave de trecho?
5. Quais são as limitações de cruzar SNV com levantamentos de pavimento?
6. Quais regras de qualidade foram aplicadas?
7. Quais KPIs são confiáveis?
8. Quais KPIs ainda precisam de validação?
9. Quais decisões foram tomadas e por quê?
10. O que entraria na Fase 2?

---

## 19. Roadmap futuro

### Fase 2 — Enriquecimento operacional

Possíveis inclusões:

- Contagem de tráfego;
- PNCT;
- dados de obras;
- obras por UF/rodovia;
- criticidade combinando tráfego + condição.

### Fase 3 — Geodados

Possíveis inclusões:

- PostGIS;
- shapefiles;
- BIT Mapas;
- mapas no Power BI;
- análise espacial;
- integração com malha georreferenciada.

### Fase 4 — Benchmark técnico

Possíveis inclusões:

- BigQuery;
- custo local vs cloud;
- tempo de ingestão;
- tempo de transformação;
- volume processado;
- documentação para DataCommunity Hub.

### Fase 5 — Produto de referência

Possíveis inclusões:

- publicação no GitHub;
- artigo técnico;
- dashboard público;
- seção no DataCommunity Hub;
- desafios técnicos derivados do projeto.

---

## 20. Regra final

Este projeto deve evoluir com consistência, não com pressa.

A Fase 1 será considerada bem-sucedida se gerar:

- entendimento real das fontes;
- base analítica inicial;
- documentação clara;
- primeiras métricas confiáveis;
- aprendizado demonstrável;
- material aproveitável no portfólio.

> Melhor um pipeline simples, documentado e explicado com domínio técnico do que uma arquitetura complexa que não pode ser defendida em entrevista.
