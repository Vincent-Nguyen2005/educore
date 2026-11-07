#!/bin/sh
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<'SQL'
CREATE ROLE tenant_a LOGIN PASSWORD 'local_a_only';
CREATE ROLE tenant_b LOGIN PASSWORD 'local_b_only';
CREATE DATABASE educore_a OWNER tenant_a;
CREATE DATABASE educore_b OWNER tenant_b;
REVOKE ALL ON DATABASE educore_a FROM PUBLIC;
REVOKE ALL ON DATABASE educore_b FROM PUBLIC;
GRANT CONNECT ON DATABASE educore_a TO tenant_a;
GRANT CONNECT ON DATABASE educore_b TO tenant_b;
SQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_a -f /docker-entrypoint-initdb.d/schema.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_b -f /docker-entrypoint-initdb.d/schema.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_a -c 'GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO tenant_a'
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_b -c 'GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO tenant_b'
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_a <<'SQL'
INSERT INTO public.formulas(version, weights) VALUES (1, '{"attendance":10,"midterm":30,"final":60}');
SQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname educore_b <<'SQL'
INSERT INTO public.formulas(version, weights) VALUES (1, '{"attendance":20,"midterm":20,"final":60}');
SQL
