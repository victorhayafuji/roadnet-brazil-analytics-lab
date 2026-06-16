-- RoadNet Brazil Analytics Lab — habilita Row Level Security nas tabelas raw.
--
-- Contexto (Supabase): sem policies, o RLS bloqueia os papéis anon/authenticated
-- (usados pela API/anon key). A ingestão usa CONEXÃO DIRETA (role postgres), que
-- IGNORA RLS — portanto a carga continua funcionando normalmente.
-- Ver docs/06_decision_log.md (decisão de banco / Supabase).

ALTER TABLE raw.raw_dnit_pavimentada    ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw.raw_dnit_nao_pavimentada ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw.raw_dnit_snv            ENABLE ROW LEVEL SECURITY;
