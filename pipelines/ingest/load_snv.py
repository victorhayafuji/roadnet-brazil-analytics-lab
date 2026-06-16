"""STUB (exercício manual) — SNV (.xls) -> raw.raw_dnit_snv.

Deixado intencionalmente incompleto (learning-first). O SNV é um Excel BINÁRIO
antigo (.xls), então a leitura difere dos CSVs:

  * Use pandas.read_excel(path, engine="xlrd")  — openpyxl NÃO lê .xls.
  * Inspecione primeiro: nº de abas, qual aba contém os dados, e a linha de
    cabeçalho real (pode haver linhas de título acima do header).
  * O schema ainda é DESCONHECIDO: a tabela raw.raw_dnit_snv hoje só tem
    metadados. Após inspecionar o .xls, acrescente as colunas (todas text) no
    DDL sql/ddl/01_raw_tables.sql e documente em docs/03_data_dictionary.md.
  * Verifique a recência: snv_202407a.xls é de jul/2024 — confirmar se há versão
    mais nova no portal do DNIT antes de fechar a Fase 1 (ver 06_decision_log.md).

Arquivo: data/raw/dnit/snv/snv_202407a.xls

TODO:
  1. Ler o .xls com xlrd e descobrir o schema real.
  2. Atualizar o DDL e o dicionário de dados.
  3. Carregar em raw.raw_dnit_snv seguindo o padrão de load_pavimentada.py.
"""
from __future__ import annotations


def main() -> int:
    raise NotImplementedError(
        "Implemente a leitura do .xls (engine='xlrd') e a carga do SNV "
        "(ver docstring deste arquivo)."
    )


if __name__ == "__main__":
    raise SystemExit(main())
