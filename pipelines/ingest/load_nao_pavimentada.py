"""STUB (exercício manual) — malha não pavimentada -> raw.raw_dnit_nao_pavimentada.

Deixado intencionalmente incompleto: o princípio learning-first do CLAUDE.md
pede que você implemente esta carga você mesmo, usando
`pipelines/ingest/load_pavimentada.py` como modelo.

Diferenças a observar em relação à base pavimentada:
  * 21 colunas (não 24): NÃO existem id_malha, remendo, trincamento, rocada,
    sinalizacao_vertical, sinalizacao_horizontal, ip, ic.
  * Colunas exclusivas: corrugacoes, trilha_roda, secao_transversal,
    poca_dagua, poeira.
  * Mesmo problema de decimal misto (icm "2,5" vs icm_unificado "2.5").
  * Tabela destino: raw.raw_dnit_nao_pavimentada
  * Arquivo: data/raw/dnit/condicoes_pavimento/levantamentos_nao_pavimentada_2026_05.csv

TODO:
  1. Apontar SOURCE_PATH para o CSV de não pavimentada.
  2. Reaproveitar read_dnit_csv() e o padrão de metadados/TRUNCATE/to_sql.
  3. Conferir a contagem (~15.961 linhas) ao final.
"""
from __future__ import annotations


def main() -> int:
    raise NotImplementedError(
        "Implemente a ingestão da malha não pavimentada usando "
        "load_pavimentada.py como referência (ver docstring deste arquivo)."
    )


if __name__ == "__main__":
    raise SystemExit(main())
