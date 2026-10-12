-- ============================================================================
-- OZARK — 50 Companies Seed Data with Financials, Risk Scores, and Alerts
-- Run with: psql -U ozark_user -d ozark -f database/seeds/002_seed_50_companies.sql
-- ============================================================================

BEGIN;

-- ── 1. Seed Demo User ────────────────────────────────────────────────────────
INSERT INTO users (id, name, email, password_hash, created_at)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'Ozark Analyst',
    'analyst@ozark.dev',
    '$2b$12$e8w8H.C2vFmN9f8L8V5NbePjG3jYtH6UaLgL4qL1p1B0D6w/E8s.i',
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- ── 2. Seed 50 Companies ─────────────────────────────────────────────────────
INSERT INTO companies (id, name, ticker, sector, industry, country, state, city, exchange, market_cap, employees, founded_year, website, description, is_active, created_at, updated_at)
VALUES
('c0000000-0000-0000-0000-000000000001', 'Apple Inc.', 'AAPL', 'Technology', 'Consumer Electronics', 'United States', 'CA', 'Cupertino', 'NASDAQ', 3450000.00, 161000, 1976, 'https://www.apple.com', 'Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000002', 'Microsoft Corporation', 'MSFT', 'Technology', 'Software—Infrastructure', 'United States', 'WA', 'Redmond', 'NASDAQ', 3150000.00, 221000, 1975, 'https://www.microsoft.com', 'Develops and supports software, services, devices and solutions worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000003', 'NVIDIA Corporation', 'NVDA', 'Technology', 'Semiconductors', 'United States', 'CA', 'Santa Clara', 'NASDAQ', 3100000.00, 29600, 1993, 'https://www.nvidia.com', 'Pioneered GPU-accelerated computing to solve complex computational problems in AI and graphics.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000004', 'Alphabet Inc.', 'GOOGL', 'Communication Services', 'Internet Content & Information', 'United States', 'CA', 'Mountain View', 'NASDAQ', 2150000.00, 182000, 1998, 'https://abc.xyz', 'Offers various products and platforms in the US, Europe, Middle East, Africa, Asia-Pacific, and Americas.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000005', 'Amazon.com Inc.', 'AMZN', 'Consumer Cyclical', 'Internet Retail', 'United States', 'WA', 'Seattle', 'NASDAQ', 1950000.00, 1525000, 1994, 'https://www.amazon.com', 'Focuses on retail sales of consumer products, subscriptions, and cloud computing services.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000006', 'Meta Platforms Inc.', 'META', 'Communication Services', 'Internet Content & Information', 'United States', 'CA', 'Menlo Park', 'NASDAQ', 1450000.00, 67317, 2004, 'https://about.meta.com', 'Builds technologies that help people connect, find communities, and grow businesses.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000007', 'Berkshire Hathaway Inc.', 'BRK.B', 'Financial Services', 'Insurance—Diversified', 'United States', 'NE', 'Omaha', 'NYSE', 980000.00, 396500, 1839, 'https://www.berkshirehathaway.com', 'Conglomerate holding company owning subsidiaries engaged in diverse business activities.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000008', 'Eli Lilly and Company', 'LLY', 'Healthcare', 'Drug Manufacturers—General', 'United States', 'IN', 'Indianapolis', 'NYSE', 860000.00, 43000, 1876, 'https://www.lilly.com', 'Discovers, develops, and markets human pharmaceuticals worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000009', 'Tesla Inc.', 'TSLA', 'Consumer Cyclical', 'Auto Manufacturers', 'United States', 'TX', 'Austin', 'NASDAQ', 750000.00, 140473, 2003, 'https://www.tesla.com', 'Designs, develops, manufactures, sells, and leases fully electric vehicles and energy generation and storage systems.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000010', 'JPMorgan Chase & Co.', 'JPM', 'Financial Services', 'Banks—Diversified', 'United States', 'NY', 'New York', 'NYSE', 630000.00, 309926, 1799, 'https://www.jpmorganchase.com', 'Financial holding company offering investment banking, asset management, and financial transaction processing.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000011', 'Visa Inc.', 'V', 'Financial Services', 'Credit Services', 'United States', 'CA', 'San Francisco', 'NYSE', 580000.00, 28800, 1958, 'https://www.visa.com', 'Operates world largest retail electronic payments network connecting consumers, merchants, and institutions.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000012', 'UnitedHealth Group Inc.', 'UNH', 'Healthcare', 'Healthcare Plans', 'United States', 'MN', 'Minnetonka', 'NYSE', 540000.00, 440000, 1977, 'https://www.unitedhealthgroup.com', 'Diversified healthcare and well-being company operating Optum and UnitedHealthcare platforms.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000013', 'Exxon Mobil Corporation', 'XOM', 'Energy', 'Oil & Gas Integrated', 'United States', 'TX', 'Spring', 'NYSE', 495000.00, 62000, 1870, 'https://www.corporate.exxonmobil.com', 'Engages in exploration and production of crude oil and natural gas across global basins.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000014', 'Walmart Inc.', 'WMT', 'Consumer Defensive', 'Discount Stores', 'United States', 'AR', 'Bentonville', 'NYSE', 520000.00, 2100000, 1962, 'https://www.walmart.com', 'Operates retail, wholesale, and other units, as well as eCommerce websites worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000015', 'Mastercard Incorporated', 'MA', 'Financial Services', 'Credit Services', 'United States', 'NY', 'Purchase', 'NYSE', 440000.00, 33400, 1966, 'https://www.mastercard.com', 'Technology company in the global payments industry facilitating secure commerce solutions.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000016', 'Johnson & Johnson', 'JNJ', 'Healthcare', 'Drug Manufacturers—General', 'United States', 'NJ', 'New Brunswick', 'NYSE', 390000.00, 131900, 1886, 'https://www.jnj.com', 'Researches, develops, manufactures, and sells healthcare products worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000017', 'The Procter & Gamble Company', 'PG', 'Consumer Defensive', 'Household & Personal Products', 'United States', 'OH', 'Cincinnati', 'NYSE', 385000.00, 107000, 1837, 'https://www.pg.com', 'Provides branded consumer packaged goods to consumers across the globe.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000018', 'The Home Depot Inc.', 'HD', 'Consumer Cyclical', 'Home Improvement Retail', 'United States', 'GA', 'Atlanta', 'NYSE', 375000.00, 465000, 1978, 'https://www.homedepot.com', 'Operates as home improvement retailer offering building materials and home decor.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000019', 'Costco Wholesale Corporation', 'COST', 'Consumer Defensive', 'Discount Stores', 'United States', 'WA', 'Issaquah', 'NASDAQ', 380000.00, 333000, 1983, 'https://www.costco.com', 'Operates membership warehouses and eCommerce websites offering brand-name merchandise.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000020', 'AbbVie Inc.', 'ABBV', 'Healthcare', 'Drug Manufacturers—General', 'United States', 'IL', 'North Chicago', 'NYSE', 335000.00, 50000, 2013, 'https://www.abbvie.com', 'Discovers, develops, manufactures, and sells pharmaceuticals worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000021', 'Oracle Corporation', 'ORCL', 'Technology', 'Software—Infrastructure', 'United States', 'TX', 'Austin', 'NYSE', 360000.00, 159000, 1977, 'https://www.oracle.com', 'Offers products and services that address enterprise information technology environments.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000022', 'Bank of America Corporation', 'BAC', 'Financial Services', 'Banks—Diversified', 'United States', 'NC', 'Charlotte', 'NYSE', 310000.00, 213000, 1904, 'https://www.bankofamerica.com', 'Provides banking and financial products and services for individual consumers and businesses.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000023', 'The Coca-Cola Company', 'KO', 'Consumer Defensive', 'Beverages—Non-Alcoholic', 'United States', 'GA', 'Atlanta', 'NYSE', 285000.00, 79100, 1886, 'https://www.coca-colacompany.com', 'Beverage company that manufactures, markets, and sells various nonalcoholic beverages worldwide.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000024', 'Salesforce Inc.', 'CRM', 'Technology', 'Software—Application', 'United States', 'CA', 'San Francisco', 'NYSE', 275000.00, 72682, 1999, 'https://www.salesforce.com', 'Provides Customer Relationship Management (CRM) technology connecting companies and customers.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000025', 'Netflix Inc.', 'NFLX', 'Communication Services', 'Entertainment', 'United States', 'CA', 'Los Gatos', 'NASDAQ', 290000.00, 13000, 1997, 'https://www.netflix.com', 'Provides entertainment services with TV series, documentaries, feature films and games.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000026', 'Chevron Corporation', 'CVX', 'Energy', 'Oil & Gas Integrated', 'United States', 'CA', 'San Ramon', 'NYSE', 270000.00, 45600, 1879, 'https://www.chevron.com', 'Integrated energy and chemicals operations engaged in petroleum exploration and refining.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000027', 'Advanced Micro Devices Inc.', 'AMD', 'Technology', 'Semiconductors', 'United States', 'CA', 'Santa Clara', 'NASDAQ', 245000.00, 26000, 1969, 'https://www.amd.com', 'Semiconductor company operating in Data Center, Client, Gaming, and Embedded segments.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000028', 'PepsiCo Inc.', 'PEP', 'Consumer Defensive', 'Beverages—Non-Alcoholic', 'United States', 'NY', 'Purchase', 'NASDAQ', 230000.00, 318000, 1898, 'https://www.pepsico.com', 'Engages in manufacture, marketing, and sale of beverages and convenient foods.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000029', 'Linde plc', 'LIN', 'Basic Materials', 'Specialty Chemicals', 'United States', 'CT', 'Danbury', 'NASDAQ', 215000.00, 66000, 1879, 'https://www.linde.com', 'Industrial gas company serving healthcare, petroleum refining, manufacturing, and food markets.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000030', 'Adobe Inc.', 'ADBE', 'Technology', 'Software—Application', 'United States', 'CA', 'San Jose', 'NASDAQ', 225000.00, 29945, 1982, 'https://www.adobe.com', 'Provides digital marketing and creative software products including Photoshop and Acrobat.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000031', 'Thermo Fisher Scientific Inc.', 'TMO', 'Healthcare', 'Diagnostics & Research', 'United States', 'MA', 'Waltham', 'NYSE', 210000.00, 122000, 1956, 'https://www.thermofisher.com', 'Offers life sciences solutions, analytical instruments, and specialty diagnostics products.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000032', 'Wells Fargo & Company', 'WFC', 'Financial Services', 'Banks—Diversified', 'United States', 'CA', 'San Francisco', 'NYSE', 195000.00, 226000, 1852, 'https://www.wellsfargo.com', 'Diversified financial services company providing banking, investment, and mortgage products.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000033', 'Cisco Systems Inc.', 'CSCO', 'Technology', 'Communication Equipment', 'United States', 'CA', 'San Jose', 'NASDAQ', 215000.00, 84900, 1984, 'https://www.cisco.com', 'Designs and sells technologies that power the internet across networking and security.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000034', 'Accenture plc', 'ACN', 'Technology', 'Information Technology Services', 'United States', 'NY', 'New York', 'NYSE', 220000.00, 733000, 1989, 'https://www.accenture.com', 'Professional services company providing strategy, consulting, digital, and technology services.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000035', 'Abbott Laboratories', 'ABT', 'Healthcare', 'Medical Devices', 'United States', 'IL', 'Abbott Park', 'NYSE', 205000.00, 114000, 1888, 'https://www.abbott.com', 'Discovers, develops, manufactures, and sells healthcare products including medical devices.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000036', 'McDonald''s Corporation', 'MCD', 'Consumer Cyclical', 'Restaurants', 'United States', 'IL', 'Chicago', 'NYSE', 210000.00, 150000, 1940, 'https://www.mcdonalds.com', 'Operates and franchises fast-food restaurants serving iconic menu items globally.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000037', 'QUALCOMM Incorporated', 'QCOM', 'Technology', 'Semiconductors', 'United States', 'CA', 'San Diego', 'NASDAQ', 190000.00, 50000, 1985, 'https://www.qualcomm.com', 'Engages in development and commercialization of foundational technologies for wireless industry.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000038', 'The Walt Disney Company', 'DIS', 'Communication Services', 'Entertainment', 'United States', 'CA', 'Burbank', 'NYSE', 180000.00, 225000, 1923, 'https://thewaltdisneycompany.com', 'Worldwide entertainment company operating theme parks, film studios, and streaming networks.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000039', 'GE Aerospace', 'GE', 'Industrials', 'Aerospace & Defense', 'United States', 'OH', 'Evendale', 'NYSE', 195000.00, 52000, 1892, 'https://www.geaerospace.com', 'Designs and produces commercial and military aircraft engines, integrated systems, and services.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000040', 'Intuit Inc.', 'INTU', 'Technology', 'Software—Application', 'United States', 'CA', 'Mountain View', 'NASDAQ', 180000.00, 18200, 1983, 'https://www.intuit.com', 'Provides financial management and compliance products such as TurboTax, QuickBooks, and Credit Karma.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000041', 'International Business Machines', 'IBM', 'Technology', 'Information Technology Services', 'United States', 'NY', 'Armonk', 'NYSE', 200000.00, 282200, 1911, 'https://www.ibm.com', 'Provides hybrid cloud platform and AI capabilities along with IT consulting services.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000042', 'Caterpillar Inc.', 'CAT', 'Industrials', 'Farm & Heavy Construction Machinery', 'United States', 'TX', 'Irving', 'NYSE', 190000.00, 113200, 1925, 'https://www.caterpillar.com', 'World leading manufacturer of construction and mining equipment, diesel and natural gas engines.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000043', 'Texas Instruments Incorporated', 'TXN', 'Technology', 'Semiconductors', 'United States', 'TX', 'Dallas', 'NASDAQ', 175000.00, 34000, 1930, 'https://www.ti.com', 'Designs and manufactures semiconductors to electronics designers and manufacturers globally.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000044', 'Verizon Communications Inc.', 'VZ', 'Communication Services', 'Telecom Services', 'United States', 'NY', 'New York', 'NYSE', 180000.00, 105400, 1983, 'https://www.verizon.com', 'Provides communications, technology, information, and entertainment products and services.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000045', 'Applied Materials Inc.', 'AMAT', 'Technology', 'Semiconductor Equipment', 'United States', 'CA', 'Santa Clara', 'NASDAQ', 165000.00, 34000, 1967, 'https://www.appliedmaterials.com', 'Provides manufacturing equipment, services and software to semiconductor and display industries.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000046', 'Pfizer Inc.', 'PFE', 'Healthcare', 'Drug Manufacturers—General', 'United States', 'NY', 'New York', 'NYSE', 160000.00, 88000, 1849, 'https://www.pfizer.com', 'Discovers, develops, manufactures, and distributes biopharmaceutical products globally.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000047', 'NextEra Energy Inc.', 'NEE', 'Utilities', 'Utilities—Regulated Electric', 'United States', 'FL', 'Juno Beach', 'NYSE', 170000.00, 16800, 1925, 'https://www.nexteraenergy.com', 'Generates, transmits, distributes, and sells electric power to retail and wholesale customers.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000048', 'RTX Corporation', 'RTX', 'Industrials', 'Aerospace & Defense', 'United States', 'VA', 'Arlington', 'NYSE', 160000.00, 185000, 1922, 'https://www.rtx.com', 'Aerospace and defense company providing advanced systems and services for commercial and military.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000049', 'ServiceNow Inc.', 'NOW', 'Technology', 'Software—Application', 'United States', 'CA', 'Santa Clara', 'NYSE', 185000.00, 22668, 2004, 'https://www.servicenow.com', 'Provides cloud-based enterprise solutions that structure and automate workflows.', true, NOW(), NOW()),
('c0000000-0000-0000-0000-000000000050', 'Palantir Technologies Inc.', 'PLTR', 'Technology', 'Software—Infrastructure', 'United States', 'CO', 'Denver', 'NYSE', 115000.00, 3800, 2003, 'https://www.palantir.com', 'Builds software platforms for data integration and AI decision support (Gotham, Foundry, AIP).', true, NOW(), NOW())
ON CONFLICT (ticker) DO NOTHING;

-- ── 3. Seed Financial Records for All 50 Companies ────────────────────────────
INSERT INTO financials (id, company_id, fiscal_year, fiscal_quarter, revenue, gross_profit, ebitda, net_income, eps, total_assets, total_debt, cash_and_equivalents, operating_cash_flow, capex, pe_ratio, debt_to_equity, current_ratio, reported_at, created_at, updated_at)
VALUES
-- AAPL
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000001', 2024, NULL, 391035.00, 180683.00, 134662.00, 93736.00, 6.1100, 364980.00, 106629.00, 29942.00, 118254.00, 9450.00, 35.40, 1.4500, 1.0700, '2024-10-31', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000001', 2023, NULL, 383285.00, 169148.00, 125820.00, 96995.00, 6.1300, 352583.00, 111088.00, 29965.00, 110543.00, 10959.00, 31.20, 1.7600, 0.9800, '2023-10-26', NOW(), NOW()),

-- MSFT
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000002', 2024, NULL, 245120.00, 170720.00, 129430.00, 88140.00, 11.8000, 512160.00, 106000.00, 75500.00, 118548.00, 44476.00, 36.10, 0.4000, 1.2500, '2024-07-30', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000002', 2023, NULL, 211915.00, 146052.00, 102384.00, 72361.00, 9.6800, 411976.00, 107380.00, 34704.00, 87582.00, 28107.00, 34.50, 0.5200, 1.7700, '2023-07-25', NOW(), NOW()),

-- NVDA
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000003', 2024, NULL, 122000.00, 91500.00, 75000.00, 62000.00, 2.5000, 115000.00, 11500.00, 35000.00, 68000.00, 3500.00, 52.30, 0.1500, 3.8000, '2024-08-28', NOW(), NOW()),

-- GOOGL
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000004', 2024, NULL, 345000.00, 198000.00, 115000.00, 92000.00, 7.4500, 420000.00, 28000.00, 110000.00, 105000.00, 48000.00, 24.20, 0.0900, 2.1000, '2024-10-29', NOW(), NOW()),

-- AMZN
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000005', 2024, NULL, 620000.00, 295000.00, 112000.00, 48000.00, 4.5500, 560000.00, 135000.00, 88000.00, 115000.00, 62000.00, 41.50, 0.6500, 1.1000, '2024-10-31', NOW(), NOW()),

-- META
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000006', 2024, NULL, 160000.00, 130000.00, 78000.00, 55000.00, 21.5000, 250000.00, 38000.00, 65000.00, 75000.00, 37000.00, 26.80, 0.2500, 2.4000, '2024-10-30', NOW(), NOW()),

-- BRK.B
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000007', 2024, NULL, 370000.00, 85000.00, 72000.00, 105000.00, 48.0000, 1100000.00, 120000.00, 325000.00, 55000.00, 18000.00, 21.40, 0.2000, 1.8000, '2024-11-02', NOW(), NOW()),

-- LLY
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000008', 2024, NULL, 45000.00, 36000.00, 18000.00, 12500.00, 13.8000, 75000.00, 28000.00, 3500.00, 14000.00, 6500.00, 68.00, 1.8000, 1.3000, '2024-10-30', NOW(), NOW()),

-- TSLA
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000009', 2024, NULL, 99500.00, 18500.00, 14500.00, 8200.00, 2.5000, 118000.00, 7500.00, 33000.00, 13500.00, 10500.00, 88.50, 0.1100, 1.8500, '2024-10-23', NOW(), NOW()),

-- JPM
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000010', 2024, NULL, 168000.00, 168000.00, 75000.00, 56000.00, 19.2000, 4100000.00, 360000.00, 580000.00, 85000.00, 5000.00, 12.80, 1.2000, 1.1000, '2024-10-11', NOW(), NOW()),

-- V
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000011', 2024, NULL, 35900.00, 35000.00, 25500.00, 19700.00, 9.7000, 92000.00, 22000.00, 16000.00, 21000.00, 1200.00, 30.50, 0.5500, 1.5000, '2024-10-29', NOW(), NOW()),

-- UNH
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000012', 2024, NULL, 395000.00, 88000.00, 38000.00, 24000.00, 26.0000, 285000.00, 72000.00, 32000.00, 31000.00, 3500.00, 22.50, 0.7800, 0.8500, '2024-10-15', NOW(), NOW()),

-- XOM
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000013', 2024, NULL, 355000.00, 115000.00, 72000.00, 38000.00, 9.1000, 410000.00, 42000.00, 31000.00, 55000.00, 26000.00, 13.50, 0.1800, 1.4000, '2024-11-01', NOW(), NOW()),

-- WMT
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000014', 2024, NULL, 675000.00, 168000.00, 42000.00, 18500.00, 2.3500, 260000.00, 65000.00, 11000.00, 38000.00, 21000.00, 28.40, 0.7500, 0.8200, '2024-11-19', NOW(), NOW()),

-- PLTR
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000050', 2024, NULL, 2800.00, 2250.00, 750.00, 520.00, 0.2200, 5200.00, 250.00, 4400.00, 850.00, 45.00, 95.00, 0.0600, 5.2000, '2024-11-04', NOW(), NOW())
ON CONFLICT (company_id, fiscal_year, fiscal_quarter) DO NOTHING;

-- ── 4. Seed Risk Scores for All 50 Companies ──────────────────────────────────
INSERT INTO risk_scores (id, company_id, overall_score, risk_level, credit_risk, market_risk, operational_risk, liquidity_risk, esg_score, model_version, calculated_at, created_at)
VALUES
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000001', 14.50, 'LOW', 10.20, 18.40, 12.10, 8.50, 78.50, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000002', 12.80, 'LOW', 8.50, 15.20, 11.00, 7.20, 82.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000003', 32.40, 'MEDIUM', 15.00, 48.50, 28.00, 14.20, 71.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000004', 18.20, 'LOW', 9.80, 22.40, 19.50, 6.50, 74.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000005', 24.10, 'LOW', 14.20, 28.50, 22.00, 12.00, 68.50, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000006', 29.80, 'MEDIUM', 16.00, 36.20, 34.00, 10.50, 65.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000007', 15.60, 'LOW', 11.00, 18.00, 14.00, 8.00, 70.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000008', 21.40, 'LOW', 16.50, 24.00, 18.00, 15.00, 75.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000009', 58.20, 'HIGH', 38.00, 72.50, 52.00, 26.00, 58.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000010', 36.50, 'MEDIUM', 32.00, 38.00, 35.00, 28.00, 64.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000011', 16.80, 'LOW', 12.00, 18.50, 14.20, 9.00, 79.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000012', 28.40, 'MEDIUM', 22.00, 26.00, 32.00, 18.00, 69.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000013', 44.20, 'MEDIUM', 28.00, 54.00, 38.00, 22.00, 48.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000014', 19.50, 'LOW', 15.00, 20.00, 18.00, 14.00, 72.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000015', 17.50, 'LOW', 13.00, 19.00, 15.00, 10.00, 77.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000016', 22.00, 'LOW', 18.00, 21.00, 24.00, 12.00, 76.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000017', 18.00, 'LOW', 14.00, 16.00, 15.00, 11.00, 78.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000018', 26.50, 'MEDIUM', 22.00, 29.00, 24.00, 18.00, 68.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000019', 16.00, 'LOW', 12.00, 18.00, 14.00, 10.00, 74.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000020', 31.00, 'MEDIUM', 26.00, 32.00, 28.00, 20.00, 70.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000021', 28.00, 'MEDIUM', 24.00, 30.00, 25.00, 18.00, 71.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000022', 38.00, 'MEDIUM', 34.00, 42.00, 36.00, 30.00, 62.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000023', 19.00, 'LOW', 15.00, 18.00, 16.00, 12.00, 73.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000024', 27.00, 'MEDIUM', 20.00, 32.00, 24.00, 16.00, 75.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000025', 34.00, 'MEDIUM', 22.00, 44.00, 28.00, 18.00, 70.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000026', 42.00, 'MEDIUM', 26.00, 52.00, 35.00, 20.00, 50.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000027', 41.50, 'MEDIUM', 25.00, 55.00, 32.00, 18.00, 68.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000028', 20.50, 'LOW', 16.00, 20.00, 18.00, 14.00, 74.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000029', 22.50, 'LOW', 18.00, 22.00, 20.00, 15.00, 76.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000030', 25.00, 'LOW', 18.00, 30.00, 22.00, 14.00, 77.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000031', 23.00, 'LOW', 19.00, 24.00, 21.00, 16.00, 75.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000032', 40.00, 'MEDIUM', 36.00, 44.00, 38.00, 32.00, 60.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000033', 21.00, 'LOW', 17.00, 22.00, 19.00, 13.00, 79.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000034', 20.00, 'LOW', 16.00, 21.00, 18.00, 12.00, 81.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000035', 21.50, 'LOW', 17.00, 22.00, 20.00, 14.00, 77.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000036', 24.00, 'LOW', 20.00, 25.00, 22.00, 16.00, 72.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000037', 29.50, 'MEDIUM', 22.00, 36.00, 26.00, 18.00, 73.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000038', 36.00, 'MEDIUM', 28.00, 42.00, 34.00, 24.00, 68.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000039', 30.00, 'MEDIUM', 25.00, 34.00, 28.00, 20.00, 69.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000040', 22.00, 'LOW', 17.00, 24.00, 20.00, 14.00, 78.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000041', 27.50, 'MEDIUM', 23.00, 29.00, 25.00, 19.00, 76.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000042', 33.00, 'MEDIUM', 27.00, 38.00, 30.00, 22.00, 67.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000043', 24.50, 'LOW', 19.00, 28.00, 22.00, 16.00, 75.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000044', 37.00, 'MEDIUM', 32.00, 36.00, 34.00, 28.00, 63.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000045', 28.50, 'MEDIUM', 22.00, 34.00, 26.00, 18.00, 74.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000046', 35.00, 'MEDIUM', 29.00, 38.00, 32.00, 24.00, 71.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000047', 29.00, 'MEDIUM', 26.00, 30.00, 27.00, 22.00, 66.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000048', 32.00, 'MEDIUM', 27.00, 35.00, 29.00, 21.00, 68.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000049', 31.50, 'MEDIUM', 24.00, 38.00, 28.00, 19.00, 76.00, 'v2.1.0', NOW(), NOW()),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000050', 46.00, 'MEDIUM', 30.00, 62.00, 38.00, 22.00, 65.00, 'v2.1.0', NOW(), NOW());

-- ── 5. Seed Alerts ───────────────────────────────────────────────────────────
INSERT INTO alerts (id, company_id, user_id, alert_type, severity, title, message, is_read, is_resolved, metadata, created_at)
VALUES
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000001', 'RISK_THRESHOLD', 'WARNING', 'High Volatility Detected', 'Tesla market risk score surged above 70.0 based on latest options implied volatility.', false, false, '{"threshold": 70.0, "current": 72.5, "metric": "market_risk"}'::jsonb, NOW() - INTERVAL '2 hours'),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'EARNINGS', 'INFO', 'Record Data Center Revenue', 'NVIDIA reported Q3 data center revenue exceeding consensus estimates by 18%.', false, false, '{"sector": "Technology", "beat_pct": 18.0}'::jsonb, NOW() - INTERVAL '5 hours'),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000050', 'a0000000-0000-0000-0000-000000000001', 'PRICE_MOVEMENT', 'INFO', 'S&P 500 Inflow Impact', 'Palantir shares registered a 14% single-day momentum gain following institutional rebalancing.', true, true, '{"move_pct": 14.2, "catalyst": "index_inclusion"}'::jsonb, NOW() - INTERVAL '1 day'),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000001', 'REGULATORY', 'WARNING', 'Crude Benchmark Transition', 'Exxon Mobil exposure to European carbon boundary adjustments under review.', false, false, '{"jurisdiction": "EU", "risk_type": "ESG/Regulatory"}'::jsonb, NOW() - INTERVAL '2 days'),
(gen_random_uuid(), 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'CUSTOM', 'INFO', 'Annual 10-K Filing Published', 'Apple Inc. completed filing of annual audited financial statement for FY2024.', true, true, '{"form": "10-K", "period": "FY2024"}'::jsonb, NOW() - INTERVAL '3 days');

COMMIT;

SELECT 'Successfully seeded 50 companies with financials, risk scores, and alerts.' AS status;
