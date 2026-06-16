"""Conexão ao PostgreSQL para o RoadNet Brazil Analytics Lab.

Lê as credenciais de um arquivo `.env` (ver `.env.example`) e devolve uma
engine SQLAlchemy. Preferimos `DATABASE_URL`; se ausente, montamos a URL a
partir das variáveis `PG*`.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, Engine, create_engine

# Raiz do repositório (…/roadnet-brazil-analytics-lab).
REPO_ROOT = Path(__file__).resolve().parents[2]


def _build_url() -> str | URL:
    """Resolve a URL de conexão a partir do ambiente / .env.

    Prioriza `DATABASE_URL` (assume-se já corretamente percent-encoded). Caso
    ausente, monta a URL a partir das variáveis `PG*` com `URL.create`, que faz
    o encoding de usuário/senha automaticamente — assim senhas com caracteres
    especiais (`@`, `*`, `/`, etc.) funcionam sem escaping manual.
    """
    load_dotenv(REPO_ROOT / ".env")

    url = os.getenv("DATABASE_URL")
    if url:
        return url

    return URL.create(
        "postgresql+psycopg",
        username=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD") or None,
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        database=os.getenv("PGDATABASE", "postgres"),
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Engine SQLAlchemy compartilhada (cacheada por processo)."""
    return create_engine(_build_url(), future=True)
