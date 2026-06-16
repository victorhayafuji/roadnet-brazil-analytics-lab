-- RoadNet Brazil Analytics Lab — tabelas da camada RAW.
--
-- Princípio (CLAUDE.md §9.1): a raw armazena os dados COMO VIERAM da fonte.
--   * Todas as colunas de origem são TEXT — nada é convertido/corrigido aqui.
--     (ex.: ICM vem com vírgula "51,25" e ICM_Unificado com ponto "51.25";
--      Km_Inicial pode ser > Km_Final dependendo do Sentido — preservar tudo.)
--   * Conversão de tipo, decimal e validação acontecem só na camada staging.
--   * Metadados de linhagem: source_file, ingested_at, batch_id.
--
-- Nomes de coluna em snake_case, fiéis ao header original (acentos/espaços
-- normalizados: "Superfície" -> superficie, "Data Aval." -> data_aval).
-- Idempotente.

-- 1) Levantamentos de malha PAVIMENTADA (24 colunas de origem)
DROP TABLE IF EXISTS raw.raw_dnit_pavimentada;
CREATE TABLE raw.raw_dnit_pavimentada (
    id_malha                text,
    uf                      text,
    contrato                text,
    ano                     text,
    mes                     text,
    panela                  text,
    remendo                 text,
    trincamento             text,
    rocada                  text,
    drenagem                text,
    sinalizacao_vertical    text,
    sinalizacao_horizontal  text,
    rodovia                 text,
    km                      text,
    sentido                 text,
    km_inicial              text,
    km_final                text,
    num_faixas              text,
    superficie              text,
    data_aval               text,
    ip                      text,
    ic                      text,
    icm                     text,
    icm_unificado           text,
    -- metadados de linhagem
    source_file             text,
    ingested_at             timestamptz,
    batch_id                text
);

-- 2) Levantamentos de malha NÃO PAVIMENTADA (21 colunas de origem)
DROP TABLE IF EXISTS raw.raw_dnit_nao_pavimentada;
CREATE TABLE raw.raw_dnit_nao_pavimentada (
    uf                      text,
    contrato                text,
    ano                     text,
    mes                     text,
    rodovia                 text,
    km                      text,
    sentido                 text,
    panela                  text,
    corrugacoes             text,
    trilha_roda             text,
    secao_transversal       text,
    poca_dagua              text,
    drenagem                text,
    poeira                  text,
    km_inicial              text,
    km_final                text,
    num_faixas              text,
    superficie              text,
    data_aval               text,
    icm                     text,
    icm_unificado           text,
    -- metadados de linhagem
    source_file             text,
    ingested_at             timestamptz,
    batch_id                text
);

-- 3) SNV — Sistema Nacional de Viação (.xls binário, aba "TABELA SNV").
--    Schema descoberto na vistoria (ver docs/06_decision_log.md): o cabeçalho
--    real está na 2ª linha da aba; 20 colunas de origem (~7.601 trechos).
--    Todas TEXT — a raw preserva os valores como vieram.
DROP TABLE IF EXISTS raw.raw_dnit_snv;
CREATE TABLE raw.raw_dnit_snv (
    br                          text,
    uf                          text,
    tipo_de_trecho              text,
    desc_coinc                  text,
    codigo                      text,
    local_de_inicio             text,
    local_de_fim                text,
    km_inicial                  text,
    km_final                    text,
    extensao                    text,
    superficie_federal          text,
    obras                       text,
    federal_coincidente         text,
    administracao               text,
    ato_legal                   text,
    estadual_coincidente        text,
    superficie_est_coincidente  text,
    jurisdicao                  text,
    superficie                  text,
    unidade_local               text,
    -- metadados de linhagem
    source_file                 text,
    ingested_at                 timestamptz,
    batch_id                    text
);
