-- ============================================================
-- OZARK — PostgreSQL Seed Data
-- Run AFTER migrations: psql -U ozark_user -d ozark -f seeds/001_seed_initial.sql
-- ============================================================

-- Example: seed a default admin user (password hash is a placeholder)
-- INSERT INTO users (id, email, name, hashed_password, created_at)
-- VALUES (
--   gen_random_uuid(),
--   'admin@ozark.dev',
--   'Admin',
--   '$2b$12$placeholder_hash',
--   NOW()
-- );

-- Add your seed statements here as tables are defined.
SELECT 'Seed script loaded. Add INSERT statements as models are created.' AS status;
