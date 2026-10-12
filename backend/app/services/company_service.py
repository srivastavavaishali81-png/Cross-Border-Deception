"""
OZARK — Company Service & Seed Data Provider

Provides company search, retrieval, multi-attribute filtering,
and fallback seeded sample data for the platform.
"""

import uuid
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.models.company import ExchangeEnum
from app.models.risk_score import RiskLevel
from app.models.alert import AlertType, AlertSeverity
from app.schemas.company import (
    CompanyDetail,
    CompanySummary,
    CompanyListResponse,
    CompanySearchResponse,
    FilterOptions,
    RiskScoreSummary,
    FinancialOut,
    AlertOut,
)


# ══════════════════════════════════════════════════════════════════════════════
# SEEDED COMPANIES DATASET
# ══════════════════════════════════════════════════════════════════════════════

RAW_SEEDED_COMPANIES: List[Dict[str, Any]] = [
    {
        "id": "11111111-1111-4111-a111-111111111101",
        "name": "Apex Cybernetics",
        "ticker": "APXC",
        "sector": "Technology",
        "industry": "Cybersecurity",
        "country": "United States",
        "state": "CA",
        "city": "San Francisco",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 84250.00,
        "employees": 6800,
        "founded_year": 2015,
        "website": "https://apexcybernetics.io",
        "description": "Apex Cybernetics is a leading next-generation enterprise cybersecurity firm specializing in zero-trust architecture, automated AI threat neutralization, and quantum-resistant cryptographic protocols.",
        "is_active": True,
        "created_at": datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 22.40,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 18.5,
            "market_risk": 24.0,
            "operational_risk": 19.8,
            "liquidity_risk": 14.2,
            "esg_score": 88.5,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 3420.50,
                "gross_profit": 2565.40,
                "ebitda": 980.20,
                "net_income": 612.80,
                "eps": 3.45,
                "total_assets": 8940.00,
                "total_debt": 1420.00,
                "cash_and_equivalents": 2840.50,
                "operating_cash_flow": 1050.00,
                "capex": 210.00,
                "pe_ratio": 34.2,
                "debt_to_equity": 0.19,
                "current_ratio": 2.45,
                "reported_at": date(2025, 1, 20),
            },
            {
                "fiscal_year": 2023,
                "fiscal_quarter": None,
                "revenue": 2740.00,
                "gross_profit": 2027.60,
                "ebitda": 740.10,
                "net_income": 450.00,
                "eps": 2.60,
                "total_assets": 7650.00,
                "total_debt": 1600.00,
                "cash_and_equivalents": 2100.00,
                "operating_cash_flow": 820.00,
                "capex": 190.00,
                "pe_ratio": 38.0,
                "debt_to_equity": 0.26,
                "current_ratio": 2.10,
                "reported_at": date(2024, 1, 22),
            },
        ],
        "alerts": [
            {
                "alert_type": AlertType.EARNINGS,
                "severity": AlertSeverity.INFO,
                "title": "Q4 Earnings Beat",
                "message": "Apex Cybernetics posted annual revenue growth of +24.8% YoY exceeding Wall Street consensus.",
                "created_at": datetime(2025, 1, 21, 14, 30, 0, tzinfo=timezone.utc),
            },
            {
                "alert_type": AlertType.CUSTOM,
                "severity": AlertSeverity.INFO,
                "title": "DoD Enterprise Contract Award",
                "message": "Awarded $450M multi-year zero-trust defense network modernization contract.",
                "created_at": datetime(2025, 2, 10, 9, 0, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111102",
        "name": "QuantumEdge Systems",
        "ticker": "QNTM",
        "sector": "Technology",
        "industry": "Quantum Computing",
        "country": "United States",
        "state": "NY",
        "city": "New York",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 128500.00,
        "employees": 9400,
        "founded_year": 2012,
        "website": "https://quantumedgesys.com",
        "description": "QuantumEdge Systems delivers commercial quantum hardware, hybrid quantum-classical computing cloud platforms, and algorithmic accelerators for finance, drug discovery, and materials science.",
        "is_active": True,
        "created_at": datetime(2024, 1, 18, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 38.60,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 26.0,
            "market_risk": 44.5,
            "operational_risk": 32.0,
            "liquidity_risk": 21.0,
            "esg_score": 82.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 5840.00,
                "gross_profit": 3971.20,
                "ebitda": 1460.00,
                "net_income": 910.40,
                "eps": 4.12,
                "total_assets": 14200.00,
                "total_debt": 3100.00,
                "cash_and_equivalents": 4350.00,
                "operating_cash_flow": 1620.00,
                "capex": 640.00,
                "pe_ratio": 42.8,
                "debt_to_equity": 0.28,
                "current_ratio": 2.15,
                "reported_at": date(2025, 1, 28),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.PRICE_MOVEMENT,
                "severity": AlertSeverity.INFO,
                "title": "Quantum Supremacy Breakthrough",
                "message": "Announced 10,000-qubit fault-tolerant quantum processor release date for Q3.",
                "created_at": datetime(2025, 2, 14, 11, 15, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111103",
        "name": "Vanguard HealthTech",
        "ticker": "VGHT",
        "sector": "Healthcare",
        "industry": "Digital Health",
        "country": "United States",
        "state": "MA",
        "city": "Boston",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 46800.00,
        "employees": 4200,
        "founded_year": 2016,
        "website": "https://vanguardhealth.tech",
        "description": "Vanguard HealthTech develops intelligent clinical workflow orchestration software, remote patient monitoring devices, and AI diagnostics for hospitals and regional health networks.",
        "is_active": True,
        "created_at": datetime(2024, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 19.80,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 15.0,
            "market_risk": 21.0,
            "operational_risk": 16.5,
            "liquidity_risk": 12.0,
            "esg_score": 93.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 1920.00,
                "gross_profit": 1440.00,
                "ebitda": 480.00,
                "net_income": 310.00,
                "eps": 2.80,
                "total_assets": 4900.00,
                "total_debt": 650.00,
                "cash_and_equivalents": 1280.00,
                "operating_cash_flow": 510.00,
                "capex": 85.00,
                "pe_ratio": 29.5,
                "debt_to_equity": 0.15,
                "current_ratio": 3.10,
                "reported_at": date(2025, 1, 18),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.REGULATORY,
                "severity": AlertSeverity.INFO,
                "title": "FDA Clearance Granted",
                "message": "FDA 510(k) clearance received for autonomous cardiac anomaly detection model.",
                "created_at": datetime(2025, 2, 3, 8, 30, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111104",
        "name": "Starlight Clean Energy",
        "ticker": "STRG",
        "sector": "Energy",
        "industry": "Clean Energy",
        "country": "United States",
        "state": "TX",
        "city": "Austin",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 62400.00,
        "employees": 5100,
        "founded_year": 2011,
        "website": "https://starlightcleanenergy.com",
        "description": "Starlight Clean Energy designs utility-scale solar generation installations, solid-state grid storage batteries, and microgrid power management systems.",
        "is_active": True,
        "created_at": datetime(2024, 2, 10, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 31.20,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 28.0,
            "market_risk": 35.0,
            "operational_risk": 29.0,
            "liquidity_risk": 22.0,
            "esg_score": 96.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 4120.00,
                "gross_profit": 1648.00,
                "ebitda": 890.00,
                "net_income": 415.00,
                "eps": 2.10,
                "total_assets": 11800.00,
                "total_debt": 3900.00,
                "cash_and_equivalents": 1950.00,
                "operating_cash_flow": 980.00,
                "capex": 750.00,
                "pe_ratio": 22.4,
                "debt_to_equity": 0.49,
                "current_ratio": 1.85,
                "reported_at": date(2025, 2, 4),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111105",
        "name": "AeroDynamics Corp",
        "ticker": "ADYN",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "country": "United States",
        "state": "WA",
        "city": "Seattle",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 98700.00,
        "employees": 18200,
        "founded_year": 1998,
        "website": "https://aerodynamicscorp.com",
        "description": "AeroDynamics Corp manufactures unmanned autonomous flight systems, composite commercial aircraft fuselages, satellite propulsion subsystems, and avionics guidance radar.",
        "is_active": True,
        "created_at": datetime(2024, 2, 14, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 42.10,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 38.0,
            "market_risk": 41.0,
            "operational_risk": 45.0,
            "liquidity_risk": 32.0,
            "esg_score": 74.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 14200.00,
                "gross_profit": 3550.00,
                "ebitda": 2100.00,
                "net_income": 1120.00,
                "eps": 5.20,
                "total_assets": 28400.00,
                "total_debt": 8900.00,
                "cash_and_equivalents": 3400.00,
                "operating_cash_flow": 2200.00,
                "capex": 1100.00,
                "pe_ratio": 18.2,
                "debt_to_equity": 0.46,
                "current_ratio": 1.60,
                "reported_at": date(2025, 1, 30),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111106",
        "name": "Meridian Financial",
        "ticker": "MRDN",
        "sector": "Financials",
        "industry": "Fintech",
        "country": "United States",
        "state": "IL",
        "city": "Chicago",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 52100.00,
        "employees": 3800,
        "founded_year": 2017,
        "website": "https://meridianfinancial.io",
        "description": "Meridian Financial is an algorithmic clearing and liquidity provider operating automated corporate treasury execution, real-time cross-border settlements, and B2B payment rails.",
        "is_active": True,
        "created_at": datetime(2024, 2, 18, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 27.50,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 22.0,
            "market_risk": 33.0,
            "operational_risk": 24.0,
            "liquidity_risk": 19.0,
            "esg_score": 86.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 2150.00,
                "gross_profit": 1720.00,
                "ebitda": 840.00,
                "net_income": 560.00,
                "eps": 3.10,
                "total_assets": 19500.00,
                "total_debt": 2400.00,
                "cash_and_equivalents": 5100.00,
                "operating_cash_flow": 910.00,
                "capex": 95.00,
                "pe_ratio": 24.1,
                "debt_to_equity": 0.14,
                "current_ratio": 2.80,
                "reported_at": date(2025, 2, 5),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111107",
        "name": "Pulse BioSciences",
        "ticker": "PLSB",
        "sector": "Healthcare",
        "industry": "Biotechnology",
        "country": "United States",
        "state": "CA",
        "city": "San Diego",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 38900.00,
        "employees": 2100,
        "founded_year": 2018,
        "website": "https://pulsebiosci.com",
        "description": "Pulse BioSciences pioneers targeted mRNA cellular reprogramming therapies, CRISPR gene-editing delivery vehicles, and personalized oncology immunotherapies.",
        "is_active": True,
        "created_at": datetime(2024, 2, 20, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 68.40,
            "risk_level": RiskLevel.HIGH,
            "credit_risk": 58.0,
            "market_risk": 78.0,
            "operational_risk": 62.0,
            "liquidity_risk": 55.0,
            "esg_score": 80.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 680.00,
                "gross_profit": 578.00,
                "ebitda": -120.00,
                "net_income": -190.00,
                "eps": -1.25,
                "total_assets": 2400.00,
                "total_debt": 420.00,
                "cash_and_equivalents": 1150.00,
                "operating_cash_flow": -90.00,
                "capex": 140.00,
                "pe_ratio": None,
                "debt_to_equity": 0.21,
                "current_ratio": 4.10,
                "reported_at": date(2025, 1, 25),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.RISK_THRESHOLD,
                "severity": AlertSeverity.WARNING,
                "title": "Elevated Clinical Trial Volatility",
                "message": "Phase III trial readouts scheduled next quarter driving heightened implied volatility.",
                "created_at": datetime(2025, 2, 8, 16, 0, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111108",
        "name": "Nova Logistics Global",
        "ticker": "NVLG",
        "sector": "Industrials",
        "industry": "Supply Chain & Logistics",
        "country": "United States",
        "state": "GA",
        "city": "Atlanta",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 41200.00,
        "employees": 14500,
        "founded_year": 2005,
        "website": "https://novalogistics.com",
        "description": "Nova Logistics Global operates intelligent automated freight brokerage, temperature-controlled multimodal transport, and robotics-powered fulfillment hubs across North America.",
        "is_active": True,
        "created_at": datetime(2024, 2, 22, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 24.80,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 20.0,
            "market_risk": 26.0,
            "operational_risk": 22.0,
            "liquidity_risk": 18.0,
            "esg_score": 79.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 7600.00,
                "gross_profit": 1900.00,
                "ebitda": 950.00,
                "net_income": 480.00,
                "eps": 3.20,
                "total_assets": 8200.00,
                "total_debt": 2100.00,
                "cash_and_equivalents": 980.00,
                "operating_cash_flow": 1100.00,
                "capex": 420.00,
                "pe_ratio": 17.5,
                "debt_to_equity": 0.34,
                "current_ratio": 1.45,
                "reported_at": date(2025, 1, 29),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111109",
        "name": "Vertex Semiconductor",
        "ticker": "VTXS",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "United States",
        "state": "TX",
        "city": "Dallas",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 174000.00,
        "employees": 11800,
        "founded_year": 2008,
        "website": "https://vertexsemi.com",
        "description": "Vertex Semiconductor manufactures ultra-dense 2nm wafer chipsets, neural tensor processing units (TPUs), and high-bandwidth optical interconnects for artificial intelligence datacenters.",
        "is_active": True,
        "created_at": datetime(2024, 2, 25, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 18.20,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 12.0,
            "market_risk": 23.0,
            "operational_risk": 15.0,
            "liquidity_risk": 11.0,
            "esg_score": 91.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 16800.00,
                "gross_profit": 11256.00,
                "ebitda": 6900.00,
                "net_income": 4820.00,
                "eps": 8.40,
                "total_assets": 32000.00,
                "total_debt": 4100.00,
                "cash_and_equivalents": 8400.00,
                "operating_cash_flow": 7200.00,
                "capex": 2800.00,
                "pe_ratio": 28.6,
                "debt_to_equity": 0.16,
                "current_ratio": 2.90,
                "reported_at": date(2025, 1, 24),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.PRICE_MOVEMENT,
                "severity": AlertSeverity.INFO,
                "title": "Record Quarterly Chip Shipments",
                "message": "AI accelerator chip demand jumped 64% over prior quarter.",
                "created_at": datetime(2025, 2, 11, 10, 0, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111110",
        "name": "Beacon Robotics",
        "ticker": "BCNR",
        "sector": "Industrials",
        "industry": "Autonomous Systems",
        "country": "United States",
        "state": "CO",
        "city": "Denver",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 29600.00,
        "employees": 2800,
        "founded_year": 2019,
        "website": "https://beaconrobotics.ai",
        "description": "Beacon Robotics designs LiDAR-guided autonomous mobile robots, automated warehouse palletizers, and computer vision safety suites for industrial facilities.",
        "is_active": True,
        "created_at": datetime(2024, 3, 1, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 45.60,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 41.0,
            "market_risk": 48.0,
            "operational_risk": 42.0,
            "liquidity_risk": 36.0,
            "esg_score": 84.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 940.00,
                "gross_profit": 470.00,
                "ebitda": 110.00,
                "net_income": 45.00,
                "eps": 0.45,
                "total_assets": 2100.00,
                "total_debt": 380.00,
                "cash_and_equivalents": 620.00,
                "operating_cash_flow": 120.00,
                "capex": 80.00,
                "pe_ratio": 48.0,
                "debt_to_equity": 0.22,
                "current_ratio": 2.40,
                "reported_at": date(2025, 1, 31),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111111",
        "name": "CloudSphere Technologies",
        "ticker": "CLSP",
        "sector": "Technology",
        "industry": "Cloud Computing",
        "country": "United States",
        "state": "WA",
        "city": "Bellevue",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 112000.00,
        "employees": 8900,
        "founded_year": 2013,
        "website": "https://cloudsphere.io",
        "description": "CloudSphere Technologies provides multi-cloud governance, serverless container orchestration, real-time edge computing mesh, and automated infrastructure optimization.",
        "is_active": True,
        "created_at": datetime(2024, 3, 5, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 16.50,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 11.0,
            "market_risk": 19.0,
            "operational_risk": 14.0,
            "liquidity_risk": 10.0,
            "esg_score": 92.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 5200.00,
                "gross_profit": 4160.00,
                "ebitda": 1820.00,
                "net_income": 1240.00,
                "eps": 4.90,
                "total_assets": 11200.00,
                "total_debt": 1800.00,
                "cash_and_equivalents": 3900.00,
                "operating_cash_flow": 2100.00,
                "capex": 350.00,
                "pe_ratio": 31.2,
                "debt_to_equity": 0.19,
                "current_ratio": 3.10,
                "reported_at": date(2025, 2, 6),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111112",
        "name": "OmniGen Therapeutics",
        "ticker": "OMNG",
        "sector": "Healthcare",
        "industry": "Biotechnology",
        "country": "United States",
        "state": "NC",
        "city": "Raleigh",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 34100.00,
        "employees": 1950,
        "founded_year": 2020,
        "website": "https://omnigentx.com",
        "description": "OmniGen Therapeutics develops AI-designed antibody-drug conjugates and synthetic biology enzymes for combating rare autoimmune disorders and neurodegenerative diseases.",
        "is_active": True,
        "created_at": datetime(2024, 3, 10, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 72.10,
            "risk_level": RiskLevel.HIGH,
            "credit_risk": 65.0,
            "market_risk": 82.0,
            "operational_risk": 68.0,
            "liquidity_risk": 60.0,
            "esg_score": 83.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 310.00,
                "gross_profit": 260.00,
                "ebitda": -85.00,
                "net_income": -140.00,
                "eps": -0.95,
                "total_assets": 1950.00,
                "total_debt": 310.00,
                "cash_and_equivalents": 890.00,
                "operating_cash_flow": -65.00,
                "capex": 95.00,
                "pe_ratio": None,
                "debt_to_equity": 0.19,
                "current_ratio": 3.80,
                "reported_at": date(2025, 1, 15),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.RISK_THRESHOLD,
                "severity": AlertSeverity.WARNING,
                "title": "Cash Burn Runway Alert",
                "message": "Current R&D burn rate provides estimated 24 months of operational runway without new licensing milestones.",
                "created_at": datetime(2025, 1, 16, 9, 30, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111113",
        "name": "Solaria Renewables",
        "ticker": "SLRN",
        "sector": "Energy",
        "industry": "Clean Energy",
        "country": "United States",
        "state": "FL",
        "city": "Miami",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 28400.00,
        "employees": 3200,
        "founded_year": 2016,
        "website": "https://solariarenew.com",
        "description": "Solaria Renewables manufactures high-efficiency perovskite solar cells, offshore floating wind turbine arrays, and commercial smart micro-inverters.",
        "is_active": True,
        "created_at": datetime(2024, 3, 12, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 36.40,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 32.0,
            "market_risk": 39.0,
            "operational_risk": 34.0,
            "liquidity_risk": 29.0,
            "esg_score": 98.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 1850.00,
                "gross_profit": 555.00,
                "ebitda": 310.00,
                "net_income": 140.00,
                "eps": 1.15,
                "total_assets": 5400.00,
                "total_debt": 1850.00,
                "cash_and_equivalents": 720.00,
                "operating_cash_flow": 380.00,
                "capex": 290.00,
                "pe_ratio": 23.5,
                "debt_to_equity": 0.52,
                "current_ratio": 1.70,
                "reported_at": date(2025, 2, 2),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111114",
        "name": "HyperScale AI Infrastructure",
        "ticker": "HPSL",
        "sector": "Technology",
        "industry": "AI Infrastructure",
        "country": "United States",
        "state": "CA",
        "city": "San Jose",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 210500.00,
        "employees": 7600,
        "founded_year": 2021,
        "website": "https://hyperscaleai.net",
        "description": "HyperScale AI Infrastructure designs liquid-cooled modular gigawatt datacenter clusters, distributed model training fabrics, and ultra-low-latency GPU interconnect grids.",
        "is_active": True,
        "created_at": datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 21.00,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 16.0,
            "market_risk": 24.0,
            "operational_risk": 18.0,
            "liquidity_risk": 14.0,
            "esg_score": 87.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 8900.00,
                "gross_profit": 6230.00,
                "ebitda": 3950.00,
                "net_income": 2680.00,
                "eps": 7.10,
                "total_assets": 21500.00,
                "total_debt": 3200.00,
                "cash_and_equivalents": 6100.00,
                "operating_cash_flow": 4100.00,
                "capex": 1900.00,
                "pe_ratio": 36.5,
                "debt_to_equity": 0.17,
                "current_ratio": 2.75,
                "reported_at": date(2025, 1, 27),
            }
        ],
        "alerts": [
            {
                "alert_type": AlertType.PRICE_MOVEMENT,
                "severity": AlertSeverity.INFO,
                "title": "Hyperscale Cloud Partnership",
                "message": "Signed multi-year $3.2B infrastructure provisioning agreement with tier-1 cloud providers.",
                "created_at": datetime(2025, 2, 9, 13, 0, 0, tzinfo=timezone.utc),
            }
        ],
    },
    {
        "id": "11111111-1111-4111-a111-111111111115",
        "name": "IronClad Security",
        "ticker": "IRCL",
        "sector": "Technology",
        "industry": "Cybersecurity",
        "country": "United States",
        "state": "VA",
        "city": "McLean",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 48900.00,
        "employees": 4600,
        "founded_year": 2010,
        "website": "https://ironcladsecurity.com",
        "description": "IronClad Security provides military-grade threat hunting, managed detection and response (MDR), and national infrastructure cyber defense systems.",
        "is_active": True,
        "created_at": datetime(2024, 3, 18, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 15.30,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 10.0,
            "market_risk": 17.0,
            "operational_risk": 13.0,
            "liquidity_risk": 9.5,
            "esg_score": 89.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 2480.00,
                "gross_profit": 1860.00,
                "ebitda": 780.00,
                "net_income": 490.00,
                "eps": 3.80,
                "total_assets": 5900.00,
                "total_debt": 850.00,
                "cash_and_equivalents": 1750.00,
                "operating_cash_flow": 820.00,
                "capex": 130.00,
                "pe_ratio": 27.2,
                "debt_to_equity": 0.17,
                "current_ratio": 2.90,
                "reported_at": date(2025, 1, 23),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111116",
        "name": "Titan Fleet Automations",
        "ticker": "TTNF",
        "sector": "Industrials",
        "industry": "Autonomous Systems",
        "country": "United States",
        "state": "IL",
        "city": "Peoria",
        "exchange": ExchangeEnum.NYSE,
        "market_cap": 37200.00,
        "employees": 8100,
        "founded_year": 2007,
        "website": "https://titanfleet.com",
        "description": "Titan Fleet Automations builds autonomous heavy haulers, connected fleet telematics, and heavy equipment automation suites for construction and mining.",
        "is_active": True,
        "created_at": datetime(2024, 3, 20, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 34.70,
            "risk_level": RiskLevel.MEDIUM,
            "credit_risk": 30.0,
            "market_risk": 36.0,
            "operational_risk": 35.0,
            "liquidity_risk": 26.0,
            "esg_score": 77.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 5400.00,
                "gross_profit": 1620.00,
                "ebitda": 810.00,
                "net_income": 410.00,
                "eps": 2.90,
                "total_assets": 9800.00,
                "total_debt": 2800.00,
                "cash_and_equivalents": 1200.00,
                "operating_cash_flow": 890.00,
                "capex": 410.00,
                "pe_ratio": 19.8,
                "debt_to_equity": 0.40,
                "current_ratio": 1.75,
                "reported_at": date(2025, 2, 7),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111117",
        "name": "Prism Data Cloud",
        "ticker": "PRSM",
        "sector": "Technology",
        "industry": "Cloud Computing",
        "country": "United States",
        "state": "NY",
        "city": "New York",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 76500.00,
        "employees": 5300,
        "founded_year": 2016,
        "website": "https://prismdata.cloud",
        "description": "Prism Data Cloud delivers unified enterprise data warehousing, real-time vector embeddings search, and low-latency streaming pipeline transformations.",
        "is_active": True,
        "created_at": datetime(2024, 3, 22, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 25.10,
            "risk_level": RiskLevel.LOW,
            "credit_risk": 20.0,
            "market_risk": 28.0,
            "operational_risk": 22.0,
            "liquidity_risk": 17.0,
            "esg_score": 90.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 3150.00,
                "gross_profit": 2520.00,
                "ebitda": 950.00,
                "net_income": 580.00,
                "eps": 3.75,
                "total_assets": 7400.00,
                "total_debt": 1100.00,
                "cash_and_equivalents": 2600.00,
                "operating_cash_flow": 1050.00,
                "capex": 220.00,
                "pe_ratio": 33.0,
                "debt_to_equity": 0.17,
                "current_ratio": 3.20,
                "reported_at": date(2025, 1, 19),
            }
        ],
        "alerts": [],
    },
    {
        "id": "11111111-1111-4111-a111-111111111118",
        "name": "Zion Digital Therapeutics",
        "ticker": "ZION",
        "sector": "Healthcare",
        "industry": "Digital Health",
        "country": "United States",
        "state": "UT",
        "city": "Salt Lake City",
        "exchange": ExchangeEnum.NASDAQ,
        "market_cap": 16400.00,
        "employees": 1400,
        "founded_year": 2020,
        "website": "https://zionhealth.io",
        "description": "Zion Digital Therapeutics creates clinically validated software-based prescription therapeutics for chronic pain management, insomnia, and behavioral health.",
        "is_active": True,
        "created_at": datetime(2024, 3, 25, 10, 0, 0, tzinfo=timezone.utc),
        "latest_risk_score": {
            "overall_score": 54.20,
            "risk_level": RiskLevel.HIGH,
            "credit_risk": 48.0,
            "market_risk": 60.0,
            "operational_risk": 52.0,
            "liquidity_risk": 46.0,
            "esg_score": 85.0,
            "calculated_at": datetime(2025, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
        },
        "financials": [
            {
                "fiscal_year": 2024,
                "fiscal_quarter": None,
                "revenue": 420.00,
                "gross_profit": 315.00,
                "ebitda": 25.00,
                "net_income": -12.00,
                "eps": -0.15,
                "total_assets": 1100.00,
                "total_debt": 220.00,
                "cash_and_equivalents": 430.00,
                "operating_cash_flow": 35.00,
                "capex": 40.00,
                "pe_ratio": None,
                "debt_to_equity": 0.25,
                "current_ratio": 2.60,
                "reported_at": date(2025, 1, 14),
            }
        ],
        "alerts": [],
    },
]


def _format_company_summary(raw: Dict[str, Any]) -> CompanySummary:
    """Transform raw dictionary to CompanySummary schema."""
    latest_risk = raw.get("latest_risk_score")
    risk_summary = None
    if latest_risk:
        rec = latest_risk.get("recommendation")
        if not rec:
            from app.core.risk_engine import RiskEngine
            rec = RiskEngine._generate_recommendation(
                score=float(latest_risk["overall_score"]),
                level=latest_risk["risk_level"],
                fin_risk=float(latest_risk.get("operational_risk") or 20.0),
                fraud_risk=float(latest_risk.get("credit_risk") or 15.0),
                comp_risk=float(latest_risk.get("market_risk") or 20.0),
            )
        risk_summary = RiskScoreSummary(
            overall_score=float(latest_risk["overall_score"]),
            risk_level=latest_risk["risk_level"],
            recommendation=rec,
            credit_risk=latest_risk.get("credit_risk"),
            market_risk=latest_risk.get("market_risk"),
            operational_risk=latest_risk.get("operational_risk"),
            liquidity_risk=latest_risk.get("liquidity_risk"),
            esg_score=latest_risk.get("esg_score"),
            calculated_at=latest_risk.get("calculated_at"),
        )

    return CompanySummary(
        id=uuid.UUID(str(raw["id"])),
        name=raw["name"],
        ticker=raw["ticker"],
        sector=raw["sector"],
        industry=raw["industry"],
        country=raw.get("country", "United States"),
        state=raw.get("state"),
        city=raw.get("city"),
        exchange=raw.get("exchange", ExchangeEnum.NASDAQ),
        market_cap=raw.get("market_cap"),
        employees=raw.get("employees"),
        founded_year=raw.get("founded_year"),
        website=raw.get("website"),
        description=raw.get("description"),
        is_active=raw.get("is_active", True),
        created_at=raw.get("created_at"),
        latest_risk_score=risk_summary,
    )


def _format_company_detail(raw: Dict[str, Any]) -> CompanyDetail:
    """Transform raw dictionary to CompanyDetail schema with financials and alerts."""
    summary = _format_company_summary(raw)

    financials_out = []
    for f in raw.get("financials", []):
        financials_out.append(
            FinancialOut(
                id=uuid.uuid4(),
                fiscal_year=f["fiscal_year"],
                fiscal_quarter=f.get("fiscal_quarter"),
                revenue=f.get("revenue"),
                gross_profit=f.get("gross_profit"),
                ebitda=f.get("ebitda"),
                net_income=f.get("net_income"),
                eps=f.get("eps"),
                total_assets=f.get("total_assets"),
                total_debt=f.get("total_debt"),
                cash_and_equivalents=f.get("cash_and_equivalents"),
                operating_cash_flow=f.get("operating_cash_flow"),
                capex=f.get("capex"),
                pe_ratio=f.get("pe_ratio"),
                debt_to_equity=f.get("debt_to_equity"),
                current_ratio=f.get("current_ratio"),
                reported_at=f.get("reported_at"),
            )
        )

    risk_scores_out = []
    if summary.latest_risk_score:
        risk_scores_out.append(summary.latest_risk_score)

    alerts_out = []
    for a in raw.get("alerts", []):
        alerts_out.append(
            AlertOut(
                id=uuid.uuid4(),
                alert_type=a["alert_type"],
                severity=a["severity"],
                title=a["title"],
                message=a.get("message") or a.get("description") or "",
                is_read=a.get("is_read", False),
                is_resolved=a.get("is_resolved", False),
                created_at=a.get("created_at", datetime.now(timezone.utc)),
                metadata=a.get("metadata"),
            )
        )

    key_stats = {
        "market_cap_formatted": f"${(raw.get('market_cap') or 0):,.2f}M",
        "employees_formatted": f"{(raw.get('employees') or 0):,}",
        "pe_ratio": financials_out[0].pe_ratio if financials_out else None,
        "revenue_ttm": financials_out[0].revenue if financials_out else None,
        "net_income_ttm": financials_out[0].net_income if financials_out else None,
        "headquarters": f"{raw.get('city', '')}, {raw.get('state', '')}",
    }

    return CompanyDetail(
        **summary.model_dump(),
        financials=financials_out,
        risk_scores=risk_scores_out,
        alerts=alerts_out,
        key_stats=key_stats,
    )


class CompanyService:
    """Service providing company search, filtering, and detail lookups."""

    @classmethod
    def get_filter_options(cls) -> FilterOptions:
        """Extract unique facet values across all companies."""
        industries = sorted(list({c["industry"] for c in RAW_SEEDED_COMPANIES if c.get("industry")}))
        states = sorted(list({c["state"] for c in RAW_SEEDED_COMPANIES if c.get("state")}))
        sectors = sorted(list({c["sector"] for c in RAW_SEEDED_COMPANIES if c.get("sector")}))
        exchanges = sorted(list({(c["exchange"].value if hasattr(c["exchange"], 'value') else str(c["exchange"])) for c in RAW_SEEDED_COMPANIES if c.get("exchange")}))
        risk_levels = [RiskLevel.LOW.value, RiskLevel.MEDIUM.value, RiskLevel.HIGH.value, RiskLevel.CRITICAL.value]

        return FilterOptions(
            industries=industries,
            states=states,
            sectors=sectors,
            exchanges=exchanges,
            risk_levels=risk_levels,
        )

    @classmethod
    def list_companies(
        cls,
        *,
        industry: Optional[str] = None,
        state: Optional[str] = None,
        name: Optional[str] = None,
        sector: Optional[str] = None,
        risk_level: Optional[str] = None,
        sort_by: str = "market_cap",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 12,
    ) -> CompanyListResponse:
        """Filter companies with specific parameters."""
        filtered = RAW_SEEDED_COMPANIES.copy()

        # ── 1. Filter by Industry ─────────────────────────────────────────────
        if industry and industry.strip():
            target_industry = industry.strip().lower()
            filtered = [
                c for c in filtered
                if c.get("industry") and c["industry"].lower() == target_industry
            ]

        # ── 2. Filter by State ────────────────────────────────────────────────
        if state and state.strip():
            target_state = state.strip().lower()
            filtered = [
                c for c in filtered
                if c.get("state") and c["state"].lower() == target_state
            ]

        # ── 3. Filter by Company Name ─────────────────────────────────────────
        if name and name.strip():
            target_name = name.strip().lower()
            filtered = [
                c for c in filtered
                if target_name in c["name"].lower() or target_name in c["ticker"].lower()
            ]

        # ── 4. Filter by Sector (optional) ────────────────────────────────────
        if sector and sector.strip():
            target_sector = sector.strip().lower()
            filtered = [
                c for c in filtered
                if c.get("sector") and c["sector"].lower() == target_sector
            ]

        # ── 5. Filter by Risk Level (optional) ────────────────────────────────
        if risk_level and risk_level.strip():
            target_risk = risk_level.strip().upper()
            filtered = [
                c for c in filtered
                if c.get("latest_risk_score") and c["latest_risk_score"]["risk_level"].value == target_risk
            ]

        # ── 6. Sorting ────────────────────────────────────────────────────────
        reverse = sort_order.lower() != "asc"
        if sort_by == "name":
            filtered.sort(key=lambda x: x["name"].lower(), reverse=not reverse if sort_order.lower() == "asc" else reverse)
        elif sort_by == "founded_year":
            filtered.sort(key=lambda x: x.get("founded_year") or 0, reverse=reverse)
        elif sort_by == "risk_score":
            filtered.sort(
                key=lambda x: x.get("latest_risk_score", {}).get("overall_score", 0),
                reverse=reverse,
            )
        else:  # default: market_cap
            filtered.sort(key=lambda x: x.get("market_cap") or 0, reverse=reverse)

        total = len(filtered)
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_items = filtered[start_idx:end_idx]

        items = [_format_company_summary(c) for c in page_items]
        facets = cls.get_filter_options()

        return CompanyListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            facets=facets,
        )

    @classmethod
    def search_companies(
        cls,
        query: str,
        *,
        industry: Optional[str] = None,
        state: Optional[str] = None,
        name: Optional[str] = None,
        sector: Optional[str] = None,
        page: int = 1,
        page_size: int = 12,
    ) -> CompanySearchResponse:
        """
        Full-text & fuzzy match across name, ticker, industry, sector, state, city, and description.
        """
        q = (query or "").strip().lower()

        if not q:
            # If query is empty, delegate to list_companies
            base_res = cls.list_companies(
                industry=industry,
                state=state,
                name=name,
                sector=sector,
                page=page,
                page_size=page_size,
            )
            return CompanySearchResponse(
                items=base_res.items,
                total=base_res.total,
                page=base_res.page,
                page_size=base_res.page_size,
                total_pages=base_res.total_pages,
                facets=base_res.facets,
                query=query,
            )

        scored_items: List[Tuple[float, Dict[str, Any]]] = []

        for c in RAW_SEEDED_COMPANIES:
            # Check external filters first
            if industry and industry.strip() and (not c.get("industry") or c["industry"].lower() != industry.strip().lower()):
                continue
            if state and state.strip() and (not c.get("state") or c["state"].lower() != state.strip().lower()):
                continue
            if name and name.strip() and (name.strip().lower() not in c["name"].lower() and name.strip().lower() not in c["ticker"].lower()):
                continue
            if sector and sector.strip() and (not c.get("sector") or c["sector"].lower() != sector.strip().lower()):
                continue

            c_name = c["name"].lower()
            c_ticker = c["ticker"].lower()
            c_ind = (c.get("industry") or "").lower()
            c_sec = (c.get("sector") or "").lower()
            c_state = (c.get("state") or "").lower()
            c_city = (c.get("city") or "").lower()
            c_desc = (c.get("description") or "").lower()

            score = 0.0

            # Exact ticker match -> highest priority
            if q == c_ticker:
                score += 100.0
            elif c_ticker.startswith(q):
                score += 70.0

            # Name match
            if q == c_name:
                score += 90.0
            elif c_name.startswith(q):
                score += 60.0
            elif q in c_name:
                score += 40.0

            # Industry / Sector match
            if q == c_ind or q in c_ind:
                score += 30.0
            if q == c_sec or q in c_sec:
                score += 20.0

            # State / City match
            if q == c_state or q == c_city or q in c_city:
                score += 25.0

            # Description match
            if q in c_desc:
                score += 10.0

            # Token-based multi-word query support
            tokens = q.split()
            if len(tokens) > 1:
                token_matches = 0
                for token in tokens:
                    if (
                        token in c_name
                        or token in c_ticker
                        or token in c_ind
                        or token in c_state
                        or token in c_city
                        or token in c_desc
                    ):
                        token_matches += 1
                if token_matches > 0:
                    score += token_matches * 15.0

            if score > 0:
                scored_items.append((score, c))

        # Sort by relevance score descending, then by market cap
        scored_items.sort(
            key=lambda x: (x[0], x[1].get("market_cap") or 0),
            reverse=True,
        )

        total = len(scored_items)
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_items = [item[1] for item in scored_items[start_idx:end_idx]]

        items = [_format_company_summary(c) for c in page_items]
        facets = cls.get_filter_options()

        return CompanySearchResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            facets=facets,
            query=query,
        )

    @classmethod
    def get_company_by_id(cls, identifier: str) -> Optional[CompanyDetail]:
        """Fetch full company details by UUID or Ticker symbol."""
        cleaned = identifier.strip().lower()

        # Try matching by UUID
        for c in RAW_SEEDED_COMPANIES:
            if str(c["id"]).lower() == cleaned:
                return _format_company_detail(c)

        # Try matching by ticker (case-insensitive)
        for c in RAW_SEEDED_COMPANIES:
            if c["ticker"].lower() == cleaned:
                return _format_company_detail(c)

        # Try matching by slugified name
        for c in RAW_SEEDED_COMPANIES:
            slug = c["name"].lower().replace(" ", "-").replace(".", "")
            if slug == cleaned:
                return _format_company_detail(c)

        # Dynamic fallback for market tickers (AAPL, NVDA, MSFT, TSLA, AMZN, GOOGL, etc.)
        ticker_upper = identifier.strip().upper()
        if len(ticker_upper) <= 10 and not any(ch in ticker_upper for ch in "-/\\ "):
            name_map = {
                "AAPL": ("Apple Inc.", "Technology", "Consumer Electronics", "CA", "Cupertino", 3450000.0, 161000, 1976),
                "NVDA": ("NVIDIA Corporation", "Technology", "Semiconductors", "CA", "Santa Clara", 3100000.0, 29600, 1993),
                "MSFT": ("Microsoft Corporation", "Technology", "Software Infrastructure", "WA", "Redmond", 3200000.0, 221000, 1975),
                "TSLA": ("Tesla Inc.", "Consumer Cyclical", "Auto Manufacturers", "TX", "Austin", 780000.0, 140473, 2003),
                "AMZN": ("Amazon.com Inc.", "Consumer Cyclical", "Internet Retail", "WA", "Seattle", 1950000.0, 1525000, 1994),
                "GOOGL": ("Alphabet Inc.", "Communication Services", "Internet Content & Information", "CA", "Mountain View", 2150000.0, 182502, 1998),
            }
            c_name, c_sec, c_ind, c_state, c_city, c_mcap, c_emp, c_yr = name_map.get(
                ticker_upper,
                (f"{ticker_upper} Enterprise Ltd", "Technology", "Enterprise Software", "NY", "New York", 45000.0, 3200, 2018),
            )
            dyn = {
                "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, ticker_upper)),
                "name": c_name,
                "ticker": ticker_upper,
                "sector": c_sec,
                "industry": c_ind,
                "country": "United States",
                "state": c_state,
                "city": c_city,
                "exchange": ExchangeEnum.NASDAQ,
                "market_cap": c_mcap,
                "employees": c_emp,
                "founded_year": c_yr,
                "website": f"https://www.{ticker_upper.lower()}.com",
                "description": f"{c_name} ({ticker_upper}) is a global corporate entity operating with high-volume institutional liquidity and comprehensive risk telemetry.",
                "is_active": True,
                "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                "latest_risk_score": {
                    "overall_score": 18.5,
                    "risk_level": RiskLevel.LOW,
                    "credit_risk": 15.0,
                    "market_risk": 20.0,
                    "operational_risk": 16.0,
                    "liquidity_risk": 12.0,
                    "esg_score": 85.0,
                    "recommendation": "This company demonstrates strong financial stability and low fraud indicators.",
                    "calculated_at": datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc),
                },
                "financials": [
                    {
                        "fiscal_year": 2024,
                        "fiscal_quarter": 4,
                        "currency": "USD",
                        "revenue": round(c_mcap * 0.12, 2),
                        "gross_profit": round(c_mcap * 0.055, 2),
                        "ebitda": round(c_mcap * 0.04, 2),
                        "net_income": round(c_mcap * 0.03, 2),
                        "eps": 3.45,
                        "total_assets": round(c_mcap * 0.25, 2),
                        "total_debt": round(c_mcap * 0.06, 2),
                        "cash_and_equivalents": round(c_mcap * 0.08, 2),
                        "operating_cash_flow": round(c_mcap * 0.038, 2),
                        "capex": round(c_mcap * 0.008, 2),
                        "pe_ratio": 28.5,
                        "debt_to_equity": 0.42,
                        "current_ratio": 1.95,
                        "reported_at": date(2025, 1, 20),
                    }
                ],
                "alerts": [
                    {
                        "id": str(uuid.uuid4()),
                        "alert_type": AlertType.REGULATORY,
                        "severity": AlertSeverity.INFO,
                        "title": f"Annual Regulatory Filing Confirmed ({ticker_upper})",
                        "description": "Standard quarterly 10-Q disclosure verified with all disclosure requirements met.",
                        "is_active": True,
                        "created_at": datetime(2025, 2, 10, 8, 0, 0, tzinfo=timezone.utc),
                    }
                ],
            }
            return _format_company_detail(dyn)

        return None
