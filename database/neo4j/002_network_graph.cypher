// ============================================================================
// OZARK — Neo4j Knowledge Graph Schema & Seed Data
// Entities: Company, Director, Bank, State
// Relationships: DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH
// ============================================================================

// ── 1. Create Constraints ───────────────────────────────────────────────────
CREATE CONSTRAINT company_id_unique IF NOT EXISTS
  FOR (c:Company) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT company_ticker_unique IF NOT EXISTS
  FOR (c:Company) REQUIRE c.ticker IS UNIQUE;

CREATE CONSTRAINT director_id_unique IF NOT EXISTS
  FOR (d:Director) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT bank_id_unique IF NOT EXISTS
  FOR (b:Bank) REQUIRE b.id IS UNIQUE;

CREATE CONSTRAINT state_code_unique IF NOT EXISTS
  FOR (s:State) REQUIRE s.code IS UNIQUE;

// ── 2. Create Indexes ───────────────────────────────────────────────────────
CREATE INDEX company_name_idx IF NOT EXISTS
  FOR (c:Company) ON (c.name);

CREATE INDEX director_name_idx IF NOT EXISTS
  FOR (d:Director) ON (d.name);

// ── 3. Seed State Nodes ─────────────────────────────────────────────────────
MERGE (ca:State {code: 'CA', name: 'California', country: 'United States'})
MERGE (wa:State {code: 'WA', name: 'Washington', country: 'United States'})
MERGE (ny:State {code: 'NY', name: 'New York', country: 'United States'})
MERGE (tx:State {code: 'TX', name: 'Texas', country: 'United States'})
MERGE (il:State {code: 'IL', name: 'Illinois', country: 'United States'})
MERGE (ga:State {code: 'GA', name: 'Georgia', country: 'United States'})
MERGE (ne:State {code: 'NE', name: 'Nebraska', country: 'United States'});

// ── 4. Seed Bank Nodes ──────────────────────────────────────────────────────
MERGE (jpm:Bank {id: 'bank_jpm', name: 'JPMorgan Chase & Co.', tier: 'Tier-1', country: 'United States', rating: 'A+'})
MERGE (bac:Bank {id: 'bank_bac', name: 'Bank of America', tier: 'Tier-1', country: 'United States', rating: 'A'})
MERGE (gs:Bank {id: 'bank_gs', name: 'Goldman Sachs', tier: 'Tier-1', country: 'United States', rating: 'A+'})
MERGE (ms:Bank {id: 'bank_ms', name: 'Morgan Stanley', tier: 'Tier-1', country: 'United States', rating: 'A'})
MERGE (wfc:Bank {id: 'bank_wfc', name: 'Wells Fargo', tier: 'Tier-1', country: 'United States', rating: 'BBB+'});

// ── 5. Seed Core Company Nodes ──────────────────────────────────────────────
MERGE (aapl:Company {
  id: 'c0000000-0000-0000-0000-000000000001',
  name: 'Apple Inc.',
  ticker: 'AAPL',
  sector: 'Technology',
  market_cap: 3450000.0,
  risk_score: 14.5
})
MERGE (msft:Company {
  id: 'c0000000-0000-0000-0000-000000000002',
  name: 'Microsoft Corporation',
  ticker: 'MSFT',
  sector: 'Technology',
  market_cap: 3150000.0,
  risk_score: 12.8
})
MERGE (nvda:Company {
  id: 'c0000000-0000-0000-0000-000000000003',
  name: 'NVIDIA Corporation',
  ticker: 'NVDA',
  sector: 'Technology',
  market_cap: 3100000.0,
  risk_score: 32.4
})
MERGE (googl:Company {
  id: 'c0000000-0000-0000-0000-000000000004',
  name: 'Alphabet Inc.',
  ticker: 'GOOGL',
  sector: 'Communication Services',
  market_cap: 2150000.0,
  risk_score: 18.2
})
MERGE (tsla:Company {
  id: 'c0000000-0000-0000-0000-000000000009',
  name: 'Tesla Inc.',
  ticker: 'TSLA',
  sector: 'Consumer Cyclical',
  market_cap: 750000.0,
  risk_score: 58.2
})
MERGE (brk:Company {
  id: 'c0000000-0000-0000-0000-000000000007',
  name: 'Berkshire Hathaway Inc.',
  ticker: 'BRK.B',
  sector: 'Financial Services',
  market_cap: 980000.0,
  risk_score: 15.6
});

// ── 6. Seed Director Nodes ──────────────────────────────────────────────────
MERGE (tim:Director {id: 'dir_tim_cook', name: 'Tim Cook', role: 'Chief Executive Officer', tenure_years: 13})
MERGE (satya:Director {id: 'dir_satya_nadella', name: 'Satya Nadella', role: 'Chairman & CEO', tenure_years: 10})
MERGE (jensen:Director {id: 'dir_jensen_huang', name: 'Jensen Huang', role: 'Founder & CEO', tenure_years: 31})
MERGE (elon:Director {id: 'dir_elon_musk', name: 'Elon Musk', role: 'Technoking & CEO', tenure_years: 16})
MERGE (warren:Director {id: 'dir_warren_buffett', name: 'Warren Buffett', role: 'Chairman & CEO', tenure_years: 54})
MERGE (sundar:Director {id: 'dir_sundar_pichai', name: 'Sundar Pichai', role: 'CEO', tenure_years: 9})
MERGE (arthur:Director {id: 'dir_arthur_levinson', name: 'Arthur Levinson', role: 'Independent Board Chairman', tenure_years: 24});

// ── 7. Seed Relationships ───────────────────────────────────────────────────

// [DIRECTS]
MERGE (tim)-[:DIRECTS {title: 'CEO', since: 2011, committee: 'Executive'}]->(aapl)
MERGE (arthur)-[:DIRECTS {title: 'Board Chairman', since: 2000, committee: 'Governance'}]->(aapl)
MERGE (satya)-[:DIRECTS {title: 'Chairman & CEO', since: 2014, committee: 'Executive'}]->(msft)
MERGE (jensen)-[:DIRECTS {title: 'CEO', since: 1993, committee: 'Executive'}]->(nvda)
MERGE (elon)-[:DIRECTS {title: 'CEO', since: 2008, committee: 'Product Oversight'}]->(tsla)
MERGE (warren)-[:DIRECTS {title: 'CEO & Chair', since: 1970, committee: 'Investment'}]->(brk)
MERGE (sundar)-[:DIRECTS {title: 'CEO', since: 2015, committee: 'Executive'}]->(googl)

// [OWNS]
MERGE (brk)-[:OWNS {shares_pct: 5.8, shares_held_m: 905.5, value_billion: 175.0}]->(aapl)
MERGE (elon)-[:OWNS {shares_pct: 12.8, voting_rights: 'Super-voting'}]->(tsla)
MERGE (warren)-[:OWNS {shares_pct: 15.6, voting_rights: 'Control Class A'}]->(brk)

// [FUNDED_BY]
MERGE (jpm)-[:FUNDED_BY {credit_facility_m: 5000.0, facility_type: 'Revolving Credit', interest_rate: 'SOFR + 0.65%'}]->(aapl)
MERGE (gs)-[:FUNDED_BY {credit_facility_m: 4500.0, facility_type: 'Commercial Paper Backstop', interest_rate: 'SOFR + 0.55%'}]->(msft)
MERGE (bac)-[:FUNDED_BY {credit_facility_m: 3000.0, facility_type: 'Syndicated Term Loan', interest_rate: 'SOFR + 0.85%'}]->(nvda)
MERGE (ms)-[:FUNDED_BY {credit_facility_m: 2500.0, facility_type: 'Asset-backed Liquidity', interest_rate: 'SOFR + 1.10%'}]->(tsla)

// [OPERATES_IN]
MERGE (aapl)-[:OPERATES_IN {facility_type: 'Global HQ & Research (Apple Park)', since: 1977}]->(ca)
MERGE (msft)-[:OPERATES_IN {facility_type: 'Corporate Headquarters', since: 1986}]->(wa)
MERGE (nvda)-[:OPERATES_IN {facility_type: 'Silicon Engineering Center', since: 1993}]->(ca)
MERGE (googl)-[:OPERATES_IN {facility_type: 'Googleplex Global HQ', since: 1998}]->(ca)
MERGE (tsla)-[:OPERATES_IN {facility_type: 'Gigafactory Texas & HQ', since: 2021}]->(tx)
MERGE (brk)-[:OPERATES_IN {facility_type: 'Holding HQ', since: 1839}]->(ne)

// [PARTNERS_WITH]
MERGE (msft)-[:PARTNERS_WITH {partnership_type: 'AI Infrastructure & Supercomputing', contract_value_m: 10000.0}]->(nvda)
MERGE (aapl)-[:PARTNERS_WITH {partnership_type: 'Default Search Agreement', annual_licensing_m: 20000.0}]->(googl)
MERGE (googl)-[:PARTNERS_WITH {partnership_type: 'TPU & GPU Accelerated Cloud', contract_value_m: 4500.0}]->(nvda);

RETURN "Neo4j OZARK Graph populated with 4 Entities and 5 Relationships." AS status;
