# Decision Log

> Toda decisão que altere modelagem, fonte, regra de qualidade ou métrica deve
> ser registrada aqui.

## 2026-06-16 — Camada staging: padrão e decisões (pavimentada)

**Decisão:** materializar a staging como **tabela** (`CREATE TABLE AS`, idempotente)
e concentrar nela todas as correções. `staging.stg_dnit_pavimentada` é a
**referência** a ser replicada para as demais bases.

**Regras aplicadas:**
- decimal **vírgula→ponto** antes do cast numérico (`replace(col, ',', '.')`);
- `'ND'` (ausência) → `NULL` nos campos categóricos; strings vazias → `NULL`;
- `state_code` em maiúsculas; aspas escapadas removidas de `contract_code`;
- `segment_length_km = abs(km_end - km_start)` — resolve o `km` invertido por
  sentido (C/D) garantindo extensão não negativa;
- `segment_key = state_code-road_code-km_start-km_end-direction`.

**Validação:** 209.204 linhas, tipos corretos, decimal convertido, 0 comprimentos
negativos. A `segment_key` ainda pode ter duplicatas (alerta) — investigar.

**Status:** Fechado para a pavimentada; não pavimentada e SNV ficam como
replicação (learning-first).

---

## 2026-06-16 — Schema do SNV descoberto (.xls)

**Decisão:** ler o SNV da aba `TABELA SNV` com `header=2` (as 2 primeiras linhas
são título/versão/contato) e materializar as **20 colunas** como `text` em
`raw.raw_dnit_snv` (~7.600 trechos).

**Motivo:** o `.xls` tinha o schema desconhecido e um cabeçalho deslocado; a
inspeção com `xlrd`/pandas revelou a estrutura (ver `docs/03_data_dictionary.md`).

**Observações:** `Federal Coincidente` traz múltiplos códigos separados por `;`
(preservado como texto); `Código` (ex.: `010BDF0010`) é o candidato a chave para
cruzar o SNV com as bases de condição no staging.

**Status:** Fechado (tabela criada e carregada).

---

## 2026-06-16 — Banco da Fase 1: Supabase (Postgres gerenciado)

**Decisão:** hospedar o banco no **Supabase** (PostgreSQL 17 gerenciado), em vez
de Postgres local. Projeto `roadnet-brazil-analytics-lab` (ref `xouojrxuneiglizaqmwg`),
região São Paulo (`sa-east-1`). Schemas `raw/staging/marts` e tabelas raw já
provisionados via integração.

**Motivo:** sem Postgres instalado localmente; Supabase remove o atrito de infra
na Fase 1 (foco em modelagem/SQL/qualidade), é Postgres real (stack inalterada) e
deixa o banco sempre acessível e compartilhável para portfólio.

**Caveats documentados:**
- Conexão de ingestão deve usar a **Session pooler** (porta 5432), não a
  Transaction pooler (6543) — esta quebra prepared statements do psycopg3.
- Projeto do free tier **pausa após ~1 semana** sem uso (despausar no painel).
- RLS desabilitado nas tabelas `raw` (schema não exposto pela API; acesso só por
  conexão direta). Recomendado ativar RLS sem policies (a conexão `postgres`
  ignora RLS e a ingestão segue funcionando).

**Alternativa futura:** Postgres local via Docker para praticar infra (Fase 4 —
benchmark local vs cloud). `.env.example` mantém o template local comentado.

**Status:** Fechado (provisionado); RLS a confirmar pelo responsável.

---

## 2026-06-16 — Estrutura em disco como layout canônico

**Decisão:** adotar o layout real em disco (`pipelines/`, `airflow/`,
`dbt/models/{staging,intermediate,marts}`, `dbt/tests/`, `sql/ddl`,
`sql/analysis`, `data/{external,sample}`) como canônico e atualizar o
`CLAUDE.md` §6/§7/§15 para refletir, em vez de recriar `src/`, `dbt/roadnet/` e
`sql/00_setup..03_marts`.

**Motivo:** a estrutura já existia e segue convenções comuns (layout dbt padrão;
`pipelines/` para código de ingestão). Reescrever o documento preserva trabalho.

**Mapeamento:** `src/{ingest,quality,utils}` → `pipelines/{ingest,quality,utils}`;
`dbt/roadnet/` → `dbt/models/*`; DDL → `sql/ddl/`; queries → `sql/analysis/`.

**Status:** Fechado.

---

## 2026-06-16 — Leitura do SNV `.xls` com `xlrd` (correção de stack)

**Decisão:** usar `xlrd` para ler `snv_202407a.xls`; manter `openpyxl` apenas
para `.xlsx` futuro.

**Motivo:** `openpyxl` (indicado originalmente no CLAUDE.md §6) **não lê** o
formato binário `.xls`. `xlrd>=2.0` mantém suporte a `.xls`.

**Status:** Fechado (stack corrigido em `requirements.txt` e CLAUDE.md §6).

---

## 2026-06-16 — Política de separador decimal

**Decisão:** na camada **raw**, preservar os valores como vieram (texto); a
conversão vírgula→ponto e o cast numérico acontecem só no **staging**.

**Motivo:** os dados trazem decimal inconsistente na mesma linha
(`icm="51,25"` vírgula vs `icm_unificado="51.25"` ponto). Corrigir na ingestão
violaria o princípio "não corrigir na raw" (CLAUDE.md §9.1).

**Status:** Aberto (implementar no staging).

---

## 2026-06-16 — `km_inicial > km_final` é artefato direcional

**Decisão:** documentar o achado e decidir o tratamento no staging (normalizar
com `min`/`max` ou manter por sentido) — ainda não fixado.

**Motivo:** a regra do CLAUDE.md §10 marca `km_start > km_end` como Erro, mas a
inversão ocorre de forma sistemática entre os sentidos `C`/`D` do mesmo trecho.

**Status:** Aberto.

---

## 2026-06-16 — Recência do SNV `202407a`

**Decisão:** usar `snv_202407a.xls` (jul/2024) para iniciar; verificar se há
versão mais recente no portal do DNIT **antes de fechar a Fase 1**.

**Motivo:** arquivo já disponível localmente e suficiente para profiling inicial.

**Risco:** pode existir versão mais atual do SNV.

**Status:** Aberto.
