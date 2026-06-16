"""STUB (exercício manual) — validações da camada raw.

Learning-first: implemente estas checagens você mesmo. A lista abaixo vem das
regras de qualidade do CLAUDE.md §10 e das violações já observadas na vistoria
(ver docs/04_quality_rules.md). Sugestão: consultar raw.raw_dnit_pavimentada /
raw.raw_dnit_nao_pavimentada via pipelines.utils.db.get_engine().

Checagens mínimas a implementar:
  [ ] uf não nulo e com 2 caracteres.
  [ ] rodovia (road_code) não nulo / formato padronizado.
  [ ] km_inicial e km_final numéricos (lembrar do decimal misto — vírgula vs ponto).
  [ ] CONTAR quantas linhas têm km_inicial > km_final (existe! ligado ao Sentido).
  [ ] icm vs icm_unificado: medir divergência de separador decimal.
  [ ] source_file e batch_id preenchidos em todas as linhas.
  [ ] % de nulos por coluna (e valores "ND" tratados como ausentes).
  [ ] duplicidade de chave de trecho (a definir no staging).

Saída esperada: um relatório (print ou tabela) com contagem por regra e
severidade (Erro/Alerta), sem ALTERAR os dados.
"""
from __future__ import annotations


def main() -> int:
    raise NotImplementedError(
        "Implemente as validações da camada raw (ver docstring e docs/04_quality_rules.md)."
    )


if __name__ == "__main__":
    raise SystemExit(main())
