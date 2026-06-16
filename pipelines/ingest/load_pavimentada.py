"""Ingestão de REFERÊNCIA — malha pavimentada -> raw.raw_dnit_pavimentada.

Este é o script completo que serve de modelo para os demais (não-pavimentada e
SNV, hoje stubs). Princípios:

  * Lê o CSV como TEXTO, sem corrigir valores (decimal/km ficam para o staging).
  * Adiciona metadados de linhagem: source_file, ingested_at, batch_id.
  * Carrega na camada raw em lotes (chunks), fazendo TRUNCATE antes para que
    a re-execução seja idempotente (não duplica linhas).

Uso (a partir da raiz do repositório, com a venv ativa):
    py -3 -m pipelines.ingest.load_pavimentada
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
    / "levantamentos_pavimentada_2026_05.csv"
)
TARGET_SCHEMA = "raw"
TARGET_TABLE = "raw_dnit_pavimentada"
# method="multi" monta um INSERT multi-linha; o Postgres limita 65.535 parâmetros
# por statement. Com 27 colunas (24 origem + 3 metadados), o teto seguro é
# ~2.400 linhas/chunk. Usamos 1.000 por margem (e melhor feedback de progresso).
CHUNK_SIZE = 1_000


def main() -> int:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo de origem não encontrado: {SOURCE_PATH}\n"
            "Os dados brutos não são versionados — ver docs/02_data_sources.md."
        )

    print(f"[load_pavimentada] lendo {SOURCE_PATH.name} ...")
    df = read_dnit_csv(SOURCE_PATH)
    print(f"[load_pavimentada] {len(df):,} linhas x {df.shape[1]} colunas")

    # Metadados de linhagem (iguais para todo o lote).
    df["source_file"] = SOURCE_PATH.name
    df["ingested_at"] = datetime.now(timezone.utc)
    df["batch_id"] = uuid.uuid4().hex

    engine = get_engine()
    # TRUNCATE para tornar a carga idempotente (não acumula em re-execuções).
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
    print(f"[load_pavimentada] OK: {count:,} linhas em {TARGET_SCHEMA}.{TARGET_TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
