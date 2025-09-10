-- Create a read-only role for MCP
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bi_ro') THEN
    CREATE ROLE bi_ro LOGIN PASSWORD 'bi_ro_pass';
  END IF;
END$$;

GRANT CONNECT ON DATABASE retail TO bi_ro;
GRANT USAGE ON SCHEMA public TO bi_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO bi_ro;

-- Optional: allow select on existing views too
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO bi_ro;
