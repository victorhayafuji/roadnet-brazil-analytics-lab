"""Leitura defensiva de CSV e normalização de nomes de coluna.

Os CSVs do DNIT têm armadilhas reais (ver docs/04_quality_rules.md):
  * delimitador ';' e encoding UTF-8 COM BOM (ler com 'utf-8-sig');
  * aspas duplas escapadas em `Contrato` (ex.: \"\"\"26 00650/2025\"\"\");
  * colunas acentuadas/com espaço ("Superfície", "Data Aval.");
  * decimal inconsistente na mesma linha (ICM "51,25" vs ICM_Unificado "51.25").

Aqui NÃO corrigimos valores: lemos tudo como texto, preservando o conteúdo
original para a camada raw. Apenas os NOMES das colunas são padronizados.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


def normalize_column(name: str) -> str:
    """Converte um cabeçalho de origem para snake_case sem acentos.

    Exemplos:
        "Superfície"  -> "superficie"
        "Data Aval."  -> "data_aval"
        "Km_Inicial"  -> "km_inicial"
    """
    # Remove acentos (NFKD + descarta marcas de combinação).
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_name = decomposed.encode("ascii", "ignore").decode("ascii")
    # Tudo que não for alfanumérico vira separador.
    ascii_name = re.sub(r"[^0-9a-zA-Z]+", "_", ascii_name)
    return ascii_name.strip("_").lower()


def read_dnit_csv(path: str | Path) -> pd.DataFrame:
    """Lê um CSV do DNIT preservando os valores como texto.

    - sep=';'                  delimitador real do arquivo
    - encoding='utf-8-sig'     remove o BOM no início do header
    - dtype=str                nada é inferido/convertido
    - keep_default_na=False    strings ficam intactas (sem virar NaN)
    - quotechar='"'            trata as aspas escapadas corretamente
    """
    df = pd.read_csv(
        path,
        sep=";",
        encoding="utf-8-sig",
        dtype=str,
        keep_default_na=False,
        quotechar='"',
    )
    df.columns = [normalize_column(c) for c in df.columns]
    return df


def read_dnit_xls(
    path: str | Path,
    sheet_name: str,
    header: int = 0,
) -> pd.DataFrame:
    """Lê uma aba de um Excel binário antigo (.xls) preservando texto.

    O SNV é `.xls` binário (engine `xlrd`; `openpyxl` não lê). A aba de dados
    (`TABELA SNV`) tem linhas de título/versão/contato acima do cabeçalho real,
    então `header` aponta a linha (0-based) onde estão os nomes das colunas.

    - engine="xlrd"          formato .xls binário
    - dtype=str / na_filter=False  nada é inferido; células vazias viram ''
    """
    df = pd.read_excel(
        path,
        sheet_name=sheet_name,
        engine="xlrd",
        header=header,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
    )
    df.columns = [normalize_column(str(c)) for c in df.columns]
    return df
