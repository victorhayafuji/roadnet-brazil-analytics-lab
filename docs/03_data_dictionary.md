# 03 — Dicionário de Dados (v1)

> Mapeia o cabeçalho **original** → coluna **raw** (snake_case, fiel à origem) →
> coluna **padronizada** (alvo de staging) → tipo esperado → regra.
> Na camada raw **tudo é `text`**; a conversão acontece no staging.

## Malha pavimentada — `raw.raw_dnit_pavimentada`

| Original | Raw (snake_case) | Padronizado (staging) | Tipo | Descrição | Regra |
|---|---|---|---|---|---|
| `id_malha` | `id_malha` | `mesh_id` | text | Identificador da malha | — |
| `UF` | `uf` | `state_code` | text | Unidade federativa | 2 caracteres |
| `Contrato` | `contrato` | `contract_code` | text | Contrato | Limpar aspas escapadas (`"""..."""`) |
| `Ano` | `ano` | `survey_year` | int | Ano do levantamento | — |
| `Mes` | `mes` | `survey_month` | int | Mês do levantamento | 1–12 |
| `Panela` | `panela` | `pothole` | text | Defeito: panela | Domínio: Alta/Média/Baixa/ND |
| `Remendo` | `remendo` | `patch` | text | Defeito: remendo | Domínio conhecido |
| `Trincamento` | `trincamento` | `cracking` | text | Defeito: trincamento | Domínio conhecido |
| `Rocada` | `rocada` | `mowing` | text | Roçada | Domínio conhecido |
| `Drenagem` | `drenagem` | `drainage` | text | Drenagem | Domínio conhecido |
| `Sinalizacao_Vertical` | `sinalizacao_vertical` | `vertical_signage` | text | Sinalização vertical | Domínio conhecido |
| `Sinalizacao_Horizontal` | `sinalizacao_horizontal` | `horizontal_signage` | text | Sinalização horizontal | Domínio conhecido |
| `Rodovia` | `rodovia` | `road_code` | text | Código da rodovia (ex.: BR-210) | Formato `BR-NNN` |
| `km` | `km` | `km_point` | numeric | Km de referência | decimal |
| `Sentido` | `sentido` | `direction` | text | Sentido (C/D/…) | Domínio conhecido |
| `Km_Inicial` | `km_inicial` | `km_start` | numeric | Km inicial do trecho | decimal (ver nota km↓) |
| `Km_Final` | `km_final` | `km_end` | numeric | Km final do trecho | decimal (ver nota km↓) |
| `Num_Faixas` | `num_faixas` | `num_lanes` | int | Número de faixas | > 0 |
| `Superfície` | `superficie` | `surface_type` | text | Tipo de superfície | "Pavimentada" |
| `Data Aval.` | `data_aval` | `survey_date` | date | Data da avaliação | ISO `YYYY-MM-DD` |
| `IP` | `ip` | `ip` | numeric | Indicador IP | decimal |
| `IC` | `ic` | `ic` | numeric | Indicador IC | decimal |
| `ICM` | `icm` | `icm` | numeric | Índice de Condição da Manutenção | **decimal com vírgula** (ex.: `51,25`) |
| `ICM_Unificado` | `icm_unificado` | `icm_unified` | numeric | ICM unificado | **decimal com ponto** (ex.: `51.25`) |

## Malha não pavimentada — `raw.raw_dnit_nao_pavimentada`

| Original | Raw (snake_case) | Padronizado (staging) | Tipo | Descrição | Regra |
|---|---|---|---|---|---|
| `UF` | `uf` | `state_code` | text | UF | 2 caracteres |
| `Contrato` | `contrato` | `contract_code` | text | Contrato | Limpar aspas escapadas |
| `Ano` | `ano` | `survey_year` | int | Ano | — |
| `Mes` | `mes` | `survey_month` | int | Mês | 1–12 |
| `Rodovia` | `rodovia` | `road_code` | text | Rodovia | Formato `BR-NNN` |
| `km` | `km` | `km_point` | numeric | Km de referência | decimal |
| `Sentido` | `sentido` | `direction` | text | Sentido | Domínio conhecido |
| `Panela` | `panela` | `pothole` | text | Panela | Domínio conhecido |
| `Corrugacoes` | `corrugacoes` | `corrugations` | text | Corrugações | Domínio conhecido |
| `trilha_roda` | `trilha_roda` | `wheel_rut` | text | Trilha de roda | Domínio conhecido |
| `Secao_Transversal` | `secao_transversal` | `cross_section` | text | Seção transversal | Domínio conhecido |
| `Poca_dagua` | `poca_dagua` | `puddle` | text | Poça d'água | Domínio conhecido |
| `Drenagem` | `drenagem` | `drainage` | text | Drenagem | Domínio conhecido |
| `Poeira` | `poeira` | `dust` | text | Poeira | Domínio conhecido |
| `Km_Inicial` | `km_inicial` | `km_start` | numeric | Km inicial | decimal (ver nota km↓) |
| `Km_Final` | `km_final` | `km_end` | numeric | Km final | decimal (ver nota km↓) |
| `Num_Faixas` | `num_faixas` | `num_lanes` | int | Faixas | > 0 |
| `Superfície` | `superficie` | `surface_type` | text | Superfície | "Não pavimentada" |
| `Data Aval.` | `data_aval` | `survey_date` | date | Data da avaliação | ISO |
| `ICM` | `icm` | `icm` | numeric | ICM | **decimal com vírgula** |
| `ICM_Unificado` | `icm_unificado` | `icm_unified` | numeric | ICM unificado | **decimal com ponto** |

## SNV — `raw.raw_dnit_snv`

Aba `TABELA SNV` do `.xls`; cabeçalho real na **3ª linha** da planilha
(2 linhas de título/versão/contato acima). ~7.600 trechos / 20 colunas.

| Original | Raw (snake_case) | Padronizado (staging) | Tipo | Descrição | Regra |
|---|---|---|---|---|---|
| `BR` | `br` | `road_br` | text | Número da BR (ex.: `010`) | 3 dígitos |
| `UF` | `uf` | `state_code` | text | UF | 2 caracteres |
| `Tipo de trecho` | `tipo_de_trecho` | `segment_type` | text | Ex.: Eixo Principal | Domínio conhecido |
| `Desc Coinc` | `desc_coinc` | `coincidence_desc` | text | Descrição de coincidência | — |
| `Código` | `codigo` | `snv_code` | text | Código SNV do trecho (ex.: `010BDF0010`) | Chave do trecho SNV |
| `Local de Início` | `local_de_inicio` | `start_location` | text | Descrição do início | — |
| `Local de Fim` | `local_de_fim` | `end_location` | text | Descrição do fim | — |
| `km inicial` | `km_inicial` | `km_start` | numeric | Km inicial | decimal com ponto |
| `km final` | `km_final` | `km_end` | numeric | Km final | decimal com ponto |
| `Extensão` | `extensao` | `length_km` | numeric | Extensão do trecho | `= km_end - km_start` |
| `Superfície Federal` | `superficie_federal` | `federal_surface` | text | Superfície (federal) | ex.: PAV/DUP/LEN |
| `Obras` | `obras` | `works` | text | Obras | — |
| `Federal Coincidente` | `federal_coincidente` | `federal_coincident` | text | Códigos coincidentes | múltiplos separados por `;` |
| `Administração` | `administracao` | `administration` | text | Ex.: Convênio Adm. Federal/Estadual | — |
| `Ato legal` | `ato_legal` | `legal_act` | text | Ato legal | — |
| `Estadual Coincidente` | `estadual_coincidente` | `state_coincident` | text | Coincidência estadual | — |
| `Superfície Est. Coincidente` | `superficie_est_coincidente` | `state_coincident_surface` | text | Superfície est. coincidente | — |
| `Jurisdição` | `jurisdicao` | `jurisdiction` | text | Ex.: Federal | Domínio conhecido |
| `Superfície` | `superficie` | `surface` | text | Superfície (ex.: PAV) | Domínio conhecido |
| `Unidade Local` | `unidade_local` | `local_unit` | text | Unidade local do DNIT | — |

> Cruzamento com os levantamentos: `snv_code` / `road_br` + `uf` + faixa de km são
> os candidatos a chave para ligar o SNV às bases de condição (a definir no staging).

## Notas importantes

- **Nota km↓ (`Km_Inicial > Km_Final`):** observado em pares de sentido `C`/`D`
  (a mesma extensão aparece invertida por sentido). A regra do CLAUDE.md §10
  trata isso como **Erro**, mas é um artefato direcional — decidir no staging se
  normaliza (`min`/`max`) ou mantém por sentido. Ver [`04_quality_rules.md`](04_quality_rules.md).
- **Decimal misto:** `icm` usa vírgula e `icm_unificado` usa ponto **na mesma
  linha**. O staging deve converter vírgula→ponto antes do cast numérico.
- **Nulos:** ausência é codificada como a string `"ND"`, não como vazio.
