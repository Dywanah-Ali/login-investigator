-- T17: run once as your PostgreSQL administrator, from the repository root:
-- /usr/local/opt/postgresql@18/bin/psql -U postgres -d postgres -f backend/setup/postgres-reader-setup.sql
-- Choose a password when prompted. Put it in backend/.env as LI_PG_READER_PASSWORD.
-- Do not send either password in chat. li_admin grants SELECT within each new build.
\set ON_ERROR_STOP on
CREATE ROLE li_reader LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
\password li_reader
