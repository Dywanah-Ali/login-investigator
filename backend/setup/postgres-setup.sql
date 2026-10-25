-- One-time setup of the knowledge base's PostgreSQL (knowledge-base ticket 09).
--
-- Run it once, as your own superuser, from the repository folder:
--
--   /usr/local/opt/postgresql@18/bin/psql -U postgres -d postgres -f backend/setup/postgres-setup.sql
--
-- `-U` names your superuser: `postgres` here, or the one pgAdmin shows under the server's
-- Properties, Connection, Username. Without it psql tries your Mac username.
--
-- psql asks for your superuser's password, then twice for the new role's password, which you
-- choose. Put the new role's password in backend/.env as LI_PG_PASSWORD. Your superuser's password
-- never goes into .env.
--
-- It makes two things:
--
--   li_admin     A limited role. It can log in and create databases, and nothing more: it is not a
--                superuser and owns nothing else on the server. The tests use it to create a fresh
--                database per test session and drop it afterwards.
--   li_template  A template database with pgvector enabled. pgvector is not a trusted extension,
--                so only a superuser can enable it. Every fresh database is copied from this one
--                and has pgvector already, so the limited role never needs that power.
--
-- Prerequisite: pgvector installed for this server (`brew install pgvector`).

\set ON_ERROR_STOP on

CREATE ROLE li_admin LOGIN CREATEDB;
\password li_admin

CREATE DATABASE li_template;
\connect li_template
CREATE EXTENSION vector;

\connect postgres
-- A template takes no connections, so a copy is never refused because a tool such as pgAdmin is
-- browsing it. To upgrade pgvector later, allow connections, run ALTER EXTENSION vector UPDATE in
-- li_template, then disallow them again.
ALTER DATABASE li_template WITH IS_TEMPLATE true ALLOW_CONNECTIONS false;
