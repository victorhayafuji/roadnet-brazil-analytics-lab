-- RoadNet Brazil Analytics Lab — criação das schemas analíticas.
-- Camadas: raw (dados como vieram), staging (padronizado), marts (analítico).
-- Idempotente: pode ser re-executado sem erro.

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
