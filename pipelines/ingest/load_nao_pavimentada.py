"""Ingestão da malha NÃO PAVIMENTADA -> raw.raw_dnit_nao_pavimentada.

Replica o padrão de `load_pavimentada.py` (a referência). A única diferença real
é o arquivo de origem e a tabela destino — o schema tem 21 colunas (sem id_malha,
remendo, trincamento, rocada, sinalização, ip, ic; com corrugacoes, trilha_roda,
secao_transversal, poca_dagua, poeira). Os valores continuam preservados como
texto (decimal misto icm "2,5" vs icm_unificado "2.5" tratado só no staging).

Uso (a partir da raiz do repositório, com a venv ativa):
    py -3 -m pipelines.ingest.load_nao_pavimentada
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import text

from pipelines.utils.db import REPO_ROOT, get_engine
from pipelines.utils.io import read_dnit_csv

SOURCE_PATH = (
    REPO_ROOT
    / "data" / "raw" / "dnit" / "condicoes_pavimento"
    / "levantamentos_nao_pavimentada_2026_05.csv"
)
TARGET_SCHEMA = "raw"
TARGET_TABLE = "raw_dnit_nao_pavimentada"
CHUNK_SIZE = 1_000


def main() -> int:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo de origem não encontrado: {SOURCE_PATH}\n"
            "Os dados brutos não são versionados — ver docs/02_data_sources.md."
        )

    print(f"[load_nao_pavimentada] lendo {SOURCE_PATH.name} ...")
    df = read_dnit_csv(SOURCE_PATH)
    print(f"[load_nao_pavimentada] {len(df):,} linhas x {df.shape[1]} colunas")

    df["source_file"] = SOURCE_PATH.name
    df["ingested_at"] = datetime.now(timezone.utc)
    df["batch_id"] = uuid.uuid4().hex

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TARGET_SCHEMA}.{TARGET_TABLE}"))

    df.to_sql(
        TARGET_TABLE,
        engine,
        schema=TARGET_SCHEMA,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method="multi",
    )

    with engine.connect() as conn:
        count = conn.execute(
            text(f"SELECT count(*) FROM {TARGET_SCHEMA}.{TARGET_TABLE}")
        ).scalar_one()
    print(f"[load_nao_pavimentada] OK: {count:,} linhas em {TARGET_SCHEMA}.{TARGET_TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
