-- ============================================================
-- OZARK — Neo4j Initial Cypher Setup
-- Run via: cypher-shell -u neo4j -p <password> -f neo4j/001_initial_constraints.cypher
-- ============================================================

// ── Constraints ─────────────────────────────────────────────────────────────

// Example: unique constraint on a User node (uncomment when ready)
// CREATE CONSTRAINT user_id_unique IF NOT EXISTS
//   FOR (u:User)
//   REQUIRE u.id IS UNIQUE;

// ── Indexes ──────────────────────────────────────────────────────────────────

// Example: full-text index for search (uncomment when ready)
// CREATE FULLTEXT INDEX entity_name_fulltext IF NOT EXISTS
//   FOR (n:Entity)
//   ON EACH [n.name];

RETURN "Neo4j initial setup complete." AS status;
