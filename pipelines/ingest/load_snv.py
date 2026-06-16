"""Ingestão do SNV (.xls) -> raw.raw_dnit_snv.

O SNV é um Excel BINÁRIO antigo (.xls), lido com `xlrd` (openpyxl não lê .xls).
A aba de dados é `TABELA SNV`; as 2 primeiras linhas são título/versão/contato e
o cabeçalho real está na 3ª linha (índice 2), então `header=2`. ~7.601 trechos /
20 colunas.

Mesmo padrão das demais cargas: preserva valores como texto, adiciona linhagem,
TRUNCATE idempotente e carrega na camada raw.

Uso (a partir da raiz do repositório, com a venv ativa):
    py -3 -m pipelines.ingest.load_snv
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import text

from pipelines.utils.db import REPO_ROOT, get_engine
from pipelines.utils.io import read_dnit_xls

SOURCE_PATH = REPO_ROOT / "data" / "raw" / "dnit" / "snv" / "snv_202407a.xls"
SHEET_NAME = "TABELA SNV"
HEADER_ROW = 2  # 0-based: linhas 0 e 1 são título/versão/contato
TARGET_SCHEMA = "raw"
TARGET_TABLE = "raw_dnit_snv"
CHUNK_SIZE = 1_000


def main() -> int:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo de origem não encontrado: {SOURCE_PATH}\n"
            "Os dados brutos não são versionados — ver docs/02_data_sources.md."
        )

    print(f"[load_snv] lendo {SOURCE_PATH.name} (aba '{SHEET_NAME}') ...")
    df = read_dnit_xls(SOURCE_PATH, sheet_name=SHEET_NAME, header=HEADER_ROW)
    print(f"[load_snv] {len(df):,} linhas x {df.shape[1]} colunas")

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
    print(f"[load_snv] OK: {count:,} linhas em {TARGET_SCHEMA}.{TARGET_TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
