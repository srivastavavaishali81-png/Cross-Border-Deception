"""
OZARK — Async Database Seeder

Seeds 50 realistic companies across diverse sectors, including:
- Companies metadata
- Financial statements (annual / quarterly)
- ML risk scores and sub-metrics
- Alerts with JSON payloads
- Demo users

Usage:
    python -m app.db.seed
"""

import asyncio
import os
import sys
import uuid
from datetime import date, datetime, timedelta, timezone

import structlog

# Allow imports from backend root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy import select
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.alert import Alert, AlertSeverity, AlertType
from app.models.company import Company, ExchangeEnum
from app.models.financial import Financial
from app.models.risk_score import RiskLevel, RiskScore
from app.models.user import User

log = structlog.get_logger(__name__)

COMPANIES_DATA = [
    {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "country": "United States", "state": "CA", "city": "Cupertino", "exchange": ExchangeEnum.NASDAQ, "market_cap": 3450000.0, "employees": 161000, "founded_year": 1976, "website": "https://www.apple.com", "description": "Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories."},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software—Infrastructure", "country": "United States", "state": "WA", "city": "Redmond", "exchange": ExchangeEnum.NASDAQ, "market_cap": 3150000.0, "employees": 221000, "founded_year": 1975, "website": "https://www.microsoft.com", "description": "Develops and supports software, services, devices and solutions worldwide."},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "country": "United States", "state": "CA", "city": "Santa Clara", "exchange": ExchangeEnum.NASDAQ, "market_cap": 3100000.0, "employees": 29600, "founded_year": 1993, "website": "https://www.nvidia.com", "description": "Pioneered GPU-accelerated computing to solve complex computational problems in AI and graphics."},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "country": "United States", "state": "CA", "city": "Mountain View", "exchange": ExchangeEnum.NASDAQ, "market_cap": 2150000.0, "employees": 182000, "founded_year": 1998, "website": "https://abc.xyz", "description": "Offers various products and platforms in the US, Europe, Middle East, Africa, Asia-Pacific, and Americas."},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "country": "United States", "state": "WA", "city": "Seattle", "exchange": ExchangeEnum.NASDAQ, "market_cap": 1950000.0, "employees": 1525000, "founded_year": 1994, "website": "https://www.amazon.com", "description": "Focuses on retail sales of consumer products, subscriptions, and cloud computing services."},
    {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Communication Services", "industry": "Internet Content & Information", "country": "United States", "state": "CA", "city": "Menlo Park", "exchange": ExchangeEnum.NASDAQ, "market_cap": 1450000.0, "employees": 67317, "founded_year": 2004, "website": "https://about.meta.com", "description": "Builds technologies that help people connect, find communities, and grow businesses."},
    {"ticker": "BRK.B", "name": "Berkshire Hathaway Inc.", "sector": "Financial Services", "industry": "Insurance—Diversified", "country": "United States", "state": "NE", "city": "Omaha", "exchange": ExchangeEnum.NYSE, "market_cap": 980000.0, "employees": 396500, "founded_year": 1839, "website": "https://www.berkshirehathaway.com", "description": "Conglomerate holding company owning subsidiaries engaged in diverse business activities."},
    {"ticker": "LLY", "name": "Eli Lilly and Company", "sector": "Healthcare", "industry": "Drug Manufacturers—General", "country": "United States", "state": "IN", "city": "Indianapolis", "exchange": ExchangeEnum.NYSE, "market_cap": 860000.0, "employees": 43000, "founded_year": 1876, "website": "https://www.lilly.com", "description": "Discovers, develops, and markets human pharmaceuticals worldwide."},
    {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "country": "United States", "state": "TX", "city": "Austin", "exchange": ExchangeEnum.NASDAQ, "market_cap": 750000.0, "employees": 140473, "founded_year": 2003, "website": "https://www.tesla.com", "description": "Designs, develops, manufactures, sells, and leases electric vehicles and energy storage systems."},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services", "industry": "Banks—Diversified", "country": "United States", "state": "NY", "city": "New York", "exchange": ExchangeEnum.NYSE, "market_cap": 630000.0, "employees": 309926, "founded_year": 1799, "website": "https://www.jpmorganchase.com", "description": "Financial holding company offering investment banking, asset management, and financial services."},
    {"ticker": "V", "name": "Visa Inc.", "sector": "Financial Services", "industry": "Credit Services", "country": "United States", "state": "CA", "city": "San Francisco", "exchange": ExchangeEnum.NYSE, "market_cap": 580000.0, "employees": 28800, "founded_year": 1958, "website": "https://www.visa.com", "description": "Operates the worlds largest retail electronic payments network connecting consumers and merchants."},
    {"ticker": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare", "industry": "Healthcare Plans", "country": "United States", "state": "MN", "city": "Minnetonka", "exchange": ExchangeEnum.NYSE, "market_cap": 540000.0, "employees": 440000, "founded_year": 1977, "website": "https://www.unitedhealthgroup.com", "description": "Diversified healthcare and well-being company operating Optum and UnitedHealthcare platforms."},
    {"ticker": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy", "industry": "Oil & Gas Integrated", "country": "United States", "state": "TX", "city": "Spring", "exchange": ExchangeEnum.NYSE, "market_cap": 495000.0, "employees": 62000, "founded_year": 1870, "website": "https://www.corporate.exxonmobil.com", "description": "Engages in exploration and production of crude oil and natural gas across global basins."},
    {"ticker": "WMT", "name": "Walmart Inc.", "sector": "Consumer Defensive", "industry": "Discount Stores", "country": "United States", "state": "AR", "city": "Bentonville", "exchange": ExchangeEnum.NYSE, "market_cap": 520000.0, "employees": 2100000, "founded_year": 1962, "website": "https://www.walmart.com", "description": "Operates retail, wholesale, and other units, as well as eCommerce websites worldwide."},
    {"ticker": "MA", "name": "Mastercard Incorporated", "sector": "Financial Services", "industry": "Credit Services", "country": "United States", "state": "NY", "city": "Purchase", "exchange": ExchangeEnum.NYSE, "market_cap": 440000.0, "employees": 33400, "founded_year": 1966, "website": "https://www.mastercard.com", "description": "Technology company in the global payments industry facilitating commerce solutions."},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Drug Manufacturers—General", "country": "United States", "state": "NJ", "city": "New Brunswick", "exchange": ExchangeEnum.NYSE, "market_cap": 390000.0, "employees": 131900, "founded_year": 1886, "website": "https://www.jnj.com", "description": "Researches, develops, manufactures, and sells healthcare products worldwide."},
    {"ticker": "PG", "name": "The Procter & Gamble Company", "sector": "Consumer Defensive", "industry": "Household & Personal Products", "country": "United States", "state": "OH", "city": "Cincinnati", "exchange": ExchangeEnum.NYSE, "market_cap": 385000.0, "employees": 107000, "founded_year": 1837, "website": "https://www.pg.com", "description": "Provides branded consumer packaged goods to consumers across the globe."},
    {"ticker": "HD", "name": "The Home Depot Inc.", "sector": "Consumer Cyclical", "industry": "Home Improvement Retail", "country": "United States", "state": "GA", "city": "Atlanta", "exchange": ExchangeEnum.NYSE, "market_cap": 375000.0, "employees": 465000, "founded_year": 1978, "website": "https://www.homedepot.com", "description": "Operates as home improvement retailer offering building materials and home decor."},
    {"ticker": "COST", "name": "Costco Wholesale Corporation", "sector": "Consumer Defensive", "industry": "Discount Stores", "country": "United States", "state": "WA", "city": "Issaquah", "exchange": ExchangeEnum.NASDAQ, "market_cap": 380000.0, "employees": 333000, "founded_year": 1983, "website": "https://www.costco.com", "description": "Operates membership warehouses and eCommerce websites offering brand-name merchandise."},
    {"ticker": "ABBV", "name": "AbbVie Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers—General", "country": "United States", "state": "IL", "city": "North Chicago", "exchange": ExchangeEnum.NYSE, "market_cap": 335000.0, "employees": 50000, "founded_year": 2013, "website": "https://www.abbvie.com", "description": "Discovers, develops, manufactures, and sells pharmaceuticals worldwide."},
    {"ticker": "ORCL", "name": "Oracle Corporation", "sector": "Technology", "industry": "Software—Infrastructure", "country": "United States", "state": "TX", "city": "Austin", "exchange": ExchangeEnum.NYSE, "market_cap": 360000.0, "employees": 159000, "founded_year": 1977, "website": "https://www.oracle.com", "description": "Offers products and services that address enterprise information technology environments."},
    {"ticker": "BAC", "name": "Bank of America Corporation", "sector": "Financial Services", "industry": "Banks—Diversified", "country": "United States", "state": "NC", "city": "Charlotte", "exchange": ExchangeEnum.NYSE, "market_cap": 310000.0, "employees": 213000, "founded_year": 1904, "website": "https://www.bankofamerica.com", "description": "Provides banking and financial products and services for consumers and corporations."},
    {"ticker": "KO", "name": "The Coca-Cola Company", "sector": "Consumer Defensive", "industry": "Beverages—Non-Alcoholic", "country": "United States", "state": "GA", "city": "Atlanta", "exchange": ExchangeEnum.NYSE, "market_cap": 285000.0, "employees": 79100, "founded_year": 1886, "website": "https://www.coca-colacompany.com", "description": "Beverage company that manufactures, markets, and sells various nonalcoholic beverages worldwide."},
    {"ticker": "CRM", "name": "Salesforce Inc.", "sector": "Technology", "industry": "Software—Application", "country": "United States", "state": "CA", "city": "San Francisco", "exchange": ExchangeEnum.NYSE, "market_cap": 275000.0, "employees": 72682, "founded_year": 1999, "website": "https://www.salesforce.com", "description": "Provides Customer Relationship Management technology connecting companies and customers."},
    {"ticker": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services", "industry": "Entertainment", "country": "United States", "state": "CA", "city": "Los Gatos", "exchange": ExchangeEnum.NASDAQ, "market_cap": 290000.0, "employees": 13000, "founded_year": 1997, "website": "https://www.netflix.com", "description": "Provides entertainment services with TV series, documentaries, feature films and games."},
    {"ticker": "CVX", "name": "Chevron Corporation", "sector": "Energy", "industry": "Oil & Gas Integrated", "country": "United States", "state": "CA", "city": "San Ramon", "exchange": ExchangeEnum.NYSE, "market_cap": 270000.0, "employees": 45600, "founded_year": 1879, "website": "https://www.chevron.com", "description": "Integrated energy operations engaged in petroleum exploration, refining, and chemicals."},
    {"ticker": "AMD", "name": "Advanced Micro Devices Inc.", "sector": "Technology", "industry": "Semiconductors", "country": "United States", "state": "CA", "city": "Santa Clara", "exchange": ExchangeEnum.NASDAQ, "market_cap": 245000.0, "employees": 26000, "founded_year": 1969, "website": "https://www.amd.com", "description": "Semiconductor company operating in Data Center, Client, Gaming, and Embedded segments."},
    {"ticker": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Defensive", "industry": "Beverages—Non-Alcoholic", "country": "United States", "state": "NY", "city": "Purchase", "exchange": ExchangeEnum.NASDAQ, "market_cap": 230000.0, "employees": 318000, "founded_year": 1898, "website": "https://www.pepsico.com", "description": "Engages in the manufacture, marketing, and sale of beverages and convenient foods globally."},
    {"ticker": "LIN", "name": "Linde plc", "sector": "Basic Materials", "industry": "Specialty Chemicals", "country": "United States", "state": "CT", "city": "Danbury", "exchange": ExchangeEnum.NASDAQ, "market_cap": 215000.0, "employees": 66000, "founded_year": 1879, "website": "https://www.linde.com", "description": "Industrial gas company serving healthcare, petroleum refining, manufacturing, and food markets."},
    {"ticker": "ADBE", "name": "Adobe Inc.", "sector": "Technology", "industry": "Software—Application", "country": "United States", "state": "CA", "city": "San Jose", "exchange": ExchangeEnum.NASDAQ, "market_cap": 225000.0, "employees": 29945, "founded_year": 1982, "website": "https://www.adobe.com", "description": "Provides digital marketing and creative software products including Photoshop and Acrobat."},
    {"ticker": "TMO", "name": "Thermo Fisher Scientific Inc.", "sector": "Healthcare", "industry": "Diagnostics & Research", "country": "United States", "state": "MA", "city": "Waltham", "exchange": ExchangeEnum.NYSE, "market_cap": 210000.0, "employees": 122000, "founded_year": 1956, "website": "https://www.thermofisher.com", "description": "Offers life sciences solutions, analytical instruments, and specialty diagnostics products."},
    {"ticker": "WFC", "name": "Wells Fargo & Company", "sector": "Financial Services", "industry": "Banks—Diversified", "country": "United States", "state": "CA", "city": "San Francisco", "exchange": ExchangeEnum.NYSE, "market_cap": 195000.0, "employees": 226000, "founded_year": 1852, "website": "https://www.wellsfargo.com", "description": "Diversified financial services company providing banking, investment, and mortgage products."},
    {"ticker": "CSCO", "name": "Cisco Systems Inc.", "sector": "Technology", "industry": "Communication Equipment", "country": "United States", "state": "CA", "city": "San Jose", "exchange": ExchangeEnum.NASDAQ, "market_cap": 215000.0, "employees": 84900, "founded_year": 1984, "website": "https://www.cisco.com", "description": "Designs and sells technologies that power the internet across networking and security."},
    {"ticker": "ACN", "name": "Accenture plc", "sector": "Technology", "industry": "Information Technology Services", "country": "United States", "state": "NY", "city": "New York", "exchange": ExchangeEnum.NYSE, "market_cap": 220000.0, "employees": 733000, "founded_year": 1989, "website": "https://www.accenture.com", "description": "Professional services company providing strategy, consulting, digital, and technology services."},
    {"ticker": "ABT", "name": "Abbott Laboratories", "sector": "Healthcare", "industry": "Medical Devices", "country": "United States", "state": "IL", "city": "Abbott Park", "exchange": ExchangeEnum.NYSE, "market_cap": 205000.0, "employees": 114000, "founded_year": 1888, "website": "https://www.abbott.com", "description": "Discovers, develops, manufactures, and sells healthcare products including medical devices."},
    {"ticker": "MCD", "name": "McDonald's Corporation", "sector": "Consumer Cyclical", "industry": "Restaurants", "country": "United States", "state": "IL", "city": "Chicago", "exchange": ExchangeEnum.NYSE, "market_cap": 210000.0, "employees": 150000, "founded_year": 1940, "website": "https://www.mcdonalds.com", "description": "Operates and franchises fast-food restaurants serving iconic menu items globally."},
    {"ticker": "QCOM", "name": "QUALCOMM Incorporated", "sector": "Technology", "industry": "Semiconductors", "country": "United States", "state": "CA", "city": "San Diego", "exchange": ExchangeEnum.NASDAQ, "market_cap": 190000.0, "employees": 50000, "founded_year": 1985, "website": "https://www.qualcomm.com", "description": "Engages in development and commercialization of foundational technologies for wireless industry."},
    {"ticker": "DIS", "name": "The Walt Disney Company", "sector": "Communication Services", "industry": "Entertainment", "country": "United States", "state": "CA", "city": "Burbank", "exchange": ExchangeEnum.NYSE, "market_cap": 180000.0, "employees": 225000, "founded_year": 1923, "website": "https://thewaltdisneycompany.com", "description": "Worldwide entertainment company operating theme parks, film studios, and streaming networks."},
    {"ticker": "GE", "name": "GE Aerospace", "sector": "Industrials", "industry": "Aerospace & Defense", "country": "United States", "state": "OH", "city": "Evendale", "exchange": ExchangeEnum.NYSE, "market_cap": 195000.0, "employees": 52000, "founded_year": 1892, "website": "https://www.geaerospace.com", "description": "Designs and produces commercial and military aircraft engines, systems, and services."},
    {"ticker": "INTU", "name": "Intuit Inc.", "sector": "Technology", "industry": "Software—Application", "country": "United States", "state": "CA", "city": "Mountain View", "exchange": ExchangeEnum.NASDAQ, "market_cap": 180000.0, "employees": 182000, "founded_year": 1983, "website": "https://www.intuit.com", "description": "Provides financial management and compliance products such as TurboTax, QuickBooks, and Credit Karma."},
    {"ticker": "IBM", "name": "International Business Machines", "sector": "Technology", "industry": "Information Technology Services", "country": "United States", "state": "NY", "city": "Armonk", "exchange": ExchangeEnum.NYSE, "market_cap": 200000.0, "employees": 282200, "founded_year": 1911, "website": "https://www.ibm.com", "description": "Provides hybrid cloud platform and AI capabilities along with IT consulting services."},
    {"ticker": "CAT", "name": "Caterpillar Inc.", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "country": "United States", "state": "TX", "city": "Irving", "exchange": ExchangeEnum.NYSE, "market_cap": 190000.0, "employees": 113200, "founded_year": 1925, "website": "https://www.caterpillar.com", "description": "World leading manufacturer of construction and mining equipment, diesel and gas engines."},
    {"ticker": "TXN", "name": "Texas Instruments Incorporated", "sector": "Technology", "industry": "Semiconductors", "country": "United States", "state": "TX", "city": "Dallas", "exchange": ExchangeEnum.NASDAQ, "market_cap": 175000.0, "employees": 34000, "founded_year": 1930, "website": "https://www.ti.com", "description": "Designs and manufactures semiconductors for electronics designers and manufacturers globally."},
    {"ticker": "VZ", "name": "Verizon Communications Inc.", "sector": "Communication Services", "industry": "Telecom Services", "country": "United States", "state": "NY", "city": "New York", "exchange": ExchangeEnum.NYSE, "market_cap": 180000.0, "employees": 105400, "founded_year": 1983, "website": "https://www.verizon.com", "description": "Provides communications, technology, information, and entertainment products and services."},
    {"ticker": "AMAT", "name": "Applied Materials Inc.", "sector": "Technology", "industry": "Semiconductor Equipment", "country": "United States", "state": "CA", "city": "Santa Clara", "exchange": ExchangeEnum.NASDAQ, "market_cap": 165000.0, "employees": 34000, "founded_year": 1967, "website": "https://www.appliedmaterials.com", "description": "Provides manufacturing equipment, services and software to semiconductor and display industries."},
    {"ticker": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers—General", "country": "United States", "state": "NY", "city": "New York", "exchange": ExchangeEnum.NYSE, "market_cap": 160000.0, "employees": 88000, "founded_year": 1849, "website": "https://www.pfizer.com", "description": "Discovers, develops, manufactures, and distributes biopharmaceutical products globally."},
    {"ticker": "NEE", "name": "NextEra Energy Inc.", "sector": "Utilities", "industry": "Utilities—Regulated Electric", "country": "United States", "state": "FL", "city": "Juno Beach", "exchange": ExchangeEnum.NYSE, "market_cap": 170000.0, "employees": 16800, "founded_year": 1925, "website": "https://www.nexteraenergy.com", "description": "Generates, transmits, distributes, and sells electric power to retail and wholesale customers."},
    {"ticker": "RTX", "name": "RTX Corporation", "sector": "Industrials", "industry": "Aerospace & Defense", "country": "United States", "state": "VA", "city": "Arlington", "exchange": ExchangeEnum.NYSE, "market_cap": 160000.0, "employees": 185000, "founded_year": 1922, "website": "https://www.rtx.com", "description": "Aerospace and defense company providing advanced systems and services for commercial and military."},
    {"ticker": "NOW", "name": "ServiceNow Inc.", "sector": "Technology", "industry": "Software—Application", "country": "United States", "state": "CA", "city": "Santa Clara", "exchange": ExchangeEnum.NYSE, "market_cap": 185000.0, "employees": 22668, "founded_year": 2004, "website": "https://www.servicenow.com", "description": "Provides cloud-based enterprise solutions that structure and automate workflows."},
    {"ticker": "PLTR", "name": "Palantir Technologies Inc.", "sector": "Technology", "industry": "Software—Infrastructure", "country": "United States", "state": "CO", "city": "Denver", "exchange": ExchangeEnum.NYSE, "market_cap": 115000.0, "employees": 3800, "founded_year": 2003, "website": "https://www.palantir.com", "description": "Builds software platforms for data integration and AI decision support (Gotham, Foundry, AIP)."}
]


async def seed_database() -> None:
    """Populate database with 50 companies, financials, risk scores, alerts, and demo user."""
    async with AsyncSessionLocal() as session:
        # 1. Demo User
        user_stmt = select(User).where(User.email == "analyst@ozark.dev")
        res = await session.execute(user_stmt)
        user = res.scalar_one_or_none()
        if not user:
            user = User(
                id=uuid.UUID("a0000000-0000-0000-0000-000000000001"),
                name="Ozark Analyst",
                email="analyst@ozark.dev",
                password_hash=hash_password("Ozark@1234"),
            )
            session.add(user)
            await session.flush()
            log.info("Created demo user", email=user.email)

        # 2. Companies, Financials, Risk Scores
        created_count = 0
        for i, c_data in enumerate(COMPANIES_DATA, start=1):
            stmt = select(Company).where(Company.ticker == c_data["ticker"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if existing:
                continue

            company_id = uuid.UUID(f"c0000000-0000-0000-0000-{i:012d}")
            company = Company(id=company_id, **c_data)
            session.add(company)
            await session.flush()

            # Generate Financials
            rev = round(c_data["market_cap"] * 0.15 + (i * 120.0), 2)
            gp = round(rev * 0.48, 2)
            ni = round(rev * 0.18, 2)
            ebitda = round(rev * 0.28, 2)
            fin_annual = Financial(
                company_id=company.id,
                fiscal_year=2024,
                fiscal_quarter=None,
                revenue=rev,
                gross_profit=gp,
                ebitda=ebitda,
                net_income=ni,
                eps=round(ni / 15000.0, 4) if ni > 0 else 0.5,
                total_assets=round(rev * 1.2, 2),
                total_debt=round(rev * 0.35, 2),
                cash_and_equivalents=round(rev * 0.22, 2),
                operating_cash_flow=round(ebitda * 0.85, 2),
                capex=round(rev * 0.08, 2),
                pe_ratio=round(20.0 + (i % 25), 2),
                debt_to_equity=round(0.4 + (i % 10) * 0.1, 4),
                current_ratio=round(1.1 + (i % 5) * 0.2, 4),
                reported_at=date(2024, 10, 15),
            )
            session.add(fin_annual)

            # Generate Risk Score
            score_val = round(12.0 + (i * 1.35) % 65.0, 2)
            risk_level = RiskLevel.from_score(score_val)
            r_score = RiskScore(
                company_id=company.id,
                overall_score=score_val,
                risk_level=risk_level,
                credit_risk=round(score_val * 0.85, 2),
                market_risk=round(min(score_val * 1.25, 95.0), 2),
                operational_risk=round(score_val * 0.9, 2),
                liquidity_risk=round(score_val * 0.6, 2),
                esg_score=round(85.0 - (score_val * 0.3), 2),
                model_version="v2.1.0",
                calculated_at=datetime.now(timezone.utc),
            )
            session.add(r_score)

            # Generate sample alert for some companies
            if i % 5 == 0:
                alert = Alert(
                    company_id=company.id,
                    user_id=user.id,
                    alert_type=AlertType.RISK_THRESHOLD if score_val > 45 else AlertType.EARNINGS,
                    severity=AlertSeverity.WARNING if score_val > 45 else AlertSeverity.INFO,
                    title=f"Automated risk surveillance update for {company.name}",
                    message=f"Risk score monitored at {score_val} with {risk_level} severity flag.",
                    is_read=False,
                    is_resolved=False,
                    alert_metadata={"score": score_val, "level": risk_level.value, "ticker": company.ticker},
                    created_at=datetime.now(timezone.utc) - timedelta(hours=i),
                )
                session.add(alert)

            created_count += 1

        await session.commit()
        log.info(f"Seeding completed successfully: {created_count} companies processed.")


if __name__ == "__main__":
    asyncio.run(seed_database())
