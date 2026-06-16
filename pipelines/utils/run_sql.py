"""Executa arquivos .sql contra o PostgreSQL do projeto.

Uso (a partir da raiz do repositório):
    py -3 -m pipelines.utils.run_sql sql/ddl/00_create_schemas.sql sql/ddl/01_raw_tables.sql

Cada arquivo é enviado como um único script (psycopg v3 aceita múltiplos
comandos separados por ';' quando não há parâmetros). Útil para rodar os DDL
idempotentes da camada raw.
"""
from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import text

from pipelines.utils.db import get_engine


def run_sql_file(path: str | Path) -> None:
    path = Path(path)
    sql = path.read_text(encoding="utf-8")
    engine = get_engine()
    with engine.begin() as conn:
        # exec_driver_sql usa o cursor nativo do psycopg, que aceita um script
        # com múltiplos statements em uma única chamada.
        conn.exec_driver_sql(sql)
    print(f"[run_sql] OK: {path}")


def main(argv: list[str]) -> int:
    if not argv:
        print("uso: python -m pipelines.utils.run_sql <arquivo.sql> [arquivo.sql ...]")
        return 2
    for arg in argv:
        run_sql_file(arg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
