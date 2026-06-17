-- RoadNet Brazil Analytics Lab — STAGING (referência): malha pavimentada.
--
-- Transforma raw.raw_dnit_pavimentada (tudo TEXT) em uma tabela tipada e
-- padronizada. É aqui — não na raw — que as correções acontecem:
--   * nomes em inglês/snake_case padronizado (ver docs/03_data_dictionary.md);
--   * decimal vírgula → ponto antes do cast numérico (icm vem com vírgula);
--   * 'ND' (ausência) vira NULL nos campos categóricos;
--   * strings vazias viram NULL; UF normalizada; aspas escapadas removidas;
--   * segment_length_km = abs(km_end - km_start) (km invertido por sentido C/D);
--   * segment_key = chave analítica de trecho.
--
-- Padrão de REFERÊNCIA: replicar para stg_dnit_nao_pavimentada e stg_dnit_snv.
-- Idempotente (DROP + CREATE TABLE AS).

DROP TABLE IF EXISTS staging.stg_dnit_pavimentada;

CREATE TABLE staging.stg_dnit_pavimentada AS
WITH clean AS (
    SELECT
        NULLIF(trim(id_malha), '')                            AS mesh_id,
        upper(NULLIF(trim(uf), ''))                           AS state_code,
        NULLIF(trim(replace(contrato, '"', '')), '')          AS contract_code,
        NULLIF(trim(ano), '')::int                            AS survey_year,
        NULLIF(trim(mes), '')::int                            AS survey_month,
        NULLIF(panela, 'ND')                                  AS pothole,
        NULLIF(remendo, 'ND')                                 AS patch,
        NULLIF(trincamento, 'ND')                             AS cracking,
        NULLIF(rocada, 'ND')                                  AS mowing,
        NULLIF(drenagem, 'ND')                                AS drainage,
        NULLIF(sinalizacao_vertical, 'ND')                    AS vertical_signage,
        NULLIF(sinalizacao_horizontal, 'ND')                  AS horizontal_signage,
        NULLIF(trim(rodovia), '')                             AS road_code,
        NULLIF(replace(km, ',', '.'), '')::numeric            AS km_point,
        NULLIF(trim(sentido), '')                             AS direction,
        NULLIF(replace(km_inicial, ',', '.'), '')::numeric    AS km_start,
        NULLIF(replace(km_final, ',', '.'), '')::numeric      AS km_end,
        NULLIF(trim(num_faixas), '')::int                     AS num_lanes,
        NULLIF(trim(superficie), '')                          AS surface_type,
        NULLIF(trim(data_aval), '')::date                     AS survey_date,
        NULLIF(replace(ip, ',', '.'), '')::numeric            AS ip,
        NULLIF(replace(ic, ',', '.'), '')::numeric            AS ic,
        NULLIF(replace(icm, ',', '.'), '')::numeric           AS icm,
        NULLIF(replace(icm_unificado, ',', '.'), '')::numeric AS icm_unified,
        source_file,
        ingested_at,
        batch_id
    FROM raw.raw_dnit_pavimentada
)
SELECT
    *,
    abs(km_end - km_start) AS segment_length_km,
    coalesce(state_code, '') || '-' || coalesce(road_code, '') || '-' ||
        coalesce(km_start::text, '') || '-' || coalesce(km_end::text, '') || '-' ||
        coalesce(direction, '') AS segment_key
FROM clean;
