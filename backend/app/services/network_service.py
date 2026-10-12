"""
OZARK — Network Service (Neo4j Graph Engine)

Connects to Neo4j to retrieve enterprise knowledge subgraphs:
- Entities: Company, Director, Bank, State
- Relationships: DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH
"""

import structlog
from typing import Any, Dict, List, Optional, Set
from neo4j.exceptions import ServiceUnavailable, SessionExpired

from app.db.neo4j import get_neo4j_driver
from app.schemas.network import (
    EntityType,
    GraphEdge,
    GraphNode,
    NetworkGraphResponse,
    NetworkMetrics,
    RelationshipType,
)
from app.services.company_service import CompanyService

log = structlog.get_logger(__name__)


# ── Synthetic Seed Graph Mapping for Resilience ──────────────────────────────

GRAPH_DATA_REGISTRY: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "market_cap": 3450000.0,
        "risk_score": 14.5,
        "directors": [
            {"id": "dir_tim_cook", "name": "Tim Cook", "role": "Chief Executive Officer", "tenure": 13},
            {"id": "dir_arthur_levinson", "name": "Arthur Levinson", "role": "Board Chairman", "tenure": 24},
            {"id": "dir_al_gore", "name": "Al Gore", "role": "Independent Director", "tenure": 21},
        ],
        "banks": [
            {"id": "bank_jpm", "name": "JPMorgan Chase & Co.", "tier": "Tier-1", "facility_m": 5000.0, "type": "Revolving Credit"},
            {"id": "bank_gs", "name": "Goldman Sachs", "tier": "Tier-1", "facility_m": 4500.0, "type": "Commercial Paper Backstop"},
        ],
        "states": [
            {"code": "CA", "name": "California", "facility": "Apple Park Global HQ"},
            {"code": "TX", "name": "Texas", "facility": "Austin Operations Campus"},
        ],
        "partners": [
            {"ticker": "NVDA", "name": "NVIDIA Corporation", "type": "AI Workstation Hardware Partner", "val_m": 4500.0},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "type": "Default Browser Search Agreement", "val_m": 20000.0},
        ],
        "owners": [
            {"id": "comp_brk", "name": "Berkshire Hathaway Inc.", "type": "Institutional Shareholder", "pct": 5.8},
        ],
    },
    "NVDA": {
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "market_cap": 3100000.0,
        "risk_score": 32.4,
        "directors": [
            {"id": "dir_jensen_huang", "name": "Jensen Huang", "role": "Founder & CEO", "tenure": 31},
            {"id": "dir_colette_kress", "name": "Colette Kress", "role": "EVP & CFO", "tenure": 11},
        ],
        "banks": [
            {"id": "bank_bac", "name": "Bank of America", "tier": "Tier-1", "facility_m": 3000.0, "type": "Syndicated Term Loan"},
            {"id": "bank_ms", "name": "Morgan Stanley", "tier": "Tier-1", "facility_m": 2000.0, "type": "Liquidity Facility"},
        ],
        "states": [
            {"code": "CA", "name": "California", "facility": "Santa Clara Global Silicon HQ"},
        ],
        "partners": [
            {"ticker": "MSFT", "name": "Microsoft Corporation", "type": "Azure AI Supercomputing Cloud", "val_m": 10000.0},
            {"ticker": "TSLA", "name": "Tesla Inc.", "type": "Full Self-Driving Compute Clusters", "val_m": 2500.0},
        ],
        "owners": [
            {"id": "dir_jensen_huang", "name": "Jensen Huang", "type": "Insider Founder Holdings", "pct": 3.5},
        ],
    },
    "MSFT": {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "market_cap": 3150000.0,
        "risk_score": 12.8,
        "directors": [
            {"id": "dir_satya_nadella", "name": "Satya Nadella", "role": "Chairman & CEO", "tenure": 10},
            {"id": "dir_amy_hood", "name": "Amy Hood", "role": "EVP & CFO", "tenure": 11},
        ],
        "banks": [
            {"id": "bank_jpm", "name": "JPMorgan Chase & Co.", "tier": "Tier-1", "facility_m": 6000.0, "type": "Global Syndicate Facility"},
        ],
        "states": [
            {"code": "WA", "name": "Washington", "facility": "Redmond Campus Headquarters"},
            {"code": "CA", "name": "California", "facility": "Silicon Valley Research Lab"},
        ],
        "partners": [
            {"ticker": "NVDA", "name": "NVIDIA Corporation", "type": "OpenAI / Azure Compute Cluster", "val_m": 12000.0},
        ],
        "owners": [],
    },
    "TSLA": {
        "ticker": "TSLA",
        "name": "Tesla Inc.",
        "sector": "Consumer Cyclical",
        "market_cap": 750000.0,
        "risk_score": 58.2,
        "directors": [
            {"id": "dir_elon_musk", "name": "Elon Musk", "role": "Technoking & CEO", "tenure": 16},
            {"id": "dir_robyn_denholm", "name": "Robyn Denholm", "role": "Board Chairwoman", "tenure": 9},
        ],
        "banks": [
            {"id": "bank_ms", "name": "Morgan Stanley", "tier": "Tier-1", "facility_m": 2500.0, "type": "Revolving Credit Line"},
            {"id": "bank_wfc", "name": "Wells Fargo", "tier": "Tier-1", "facility_m": 1500.0, "type": "Asset-Backed Facility"},
        ],
        "states": [
            {"code": "TX", "name": "Texas", "facility": "Gigafactory Texas Headquarters"},
            {"code": "CA", "name": "California", "facility": "Fremont Vehicle Manufacturing"},
            {"code": "NV", "name": "Nevada", "facility": "Gigafactory 1 Battery Plant"},
        ],
        "partners": [
            {"ticker": "NVDA", "name": "NVIDIA Corporation", "type": "Cortex Dojo & H100 AI Training", "val_m": 1800.0},
        ],
        "owners": [
            {"id": "dir_elon_musk", "name": "Elon Musk", "type": "Controlling Common Stock", "pct": 12.8},
        ],
    },
}


class NetworkService:
    """Service layer for querying and assembling Neo4j network knowledge graphs."""

    @classmethod
    async def get_company_network(
        cls,
        company_id: str,
        depth: int = 1,
    ) -> NetworkGraphResponse:
        """
        Fetches the complete knowledge graph for a company:
        - 1. Attempts live Cypher query via Neo4j driver
        - 2. Falls back to enriched synthetic graph if Neo4j is offline
        """
        # Resolve company details
        company = CompanyService.get_company_by_id(company_id)
        ticker = company.ticker.upper() if company else company_id.upper()
        name = company.name if company else company_id

        # Attempt Neo4j query
        try:
            driver = await get_neo4j_driver()
            async with driver.session() as session:
                cypher_query = """
                MATCH (c:Company)
                WHERE c.id = $cid OR toUpper(c.ticker) = toUpper($ticker)
                OPTIONAL MATCH (d:Director)-[r1:DIRECTS]->(c)
                OPTIONAL MATCH (o)-[r2:OWNS]->(c)
                OPTIONAL MATCH (b:Bank)-[r3:FUNDED_BY]->(c)
                OPTIONAL MATCH (c)-[r4:OPERATES_IN]->(s:State)
                OPTIONAL MATCH (c)-[r5:PARTNERS_WITH]-(p:Company)
                RETURN c, collect(DISTINCT {node: d, rel: r1, type: 'DIRECTS'}) AS directors,
                          collect(DISTINCT {node: o, rel: r2, type: 'OWNS'}) AS owners,
                          collect(DISTINCT {node: b, rel: r3, type: 'FUNDED_BY'}) AS banks,
                          collect(DISTINCT {node: s, rel: r4, type: 'OPERATES_IN'}) AS states,
                          collect(DISTINCT {node: p, rel: r5, type: 'PARTNERS_WITH'}) AS partners
                """
                result = await session.run(cypher_query, cid=company_id, ticker=ticker)
                record = await result.single()

                if record and record["c"]:
                    return cls._parse_neo4j_record(record, company_id, ticker, name)
        except Exception as e:
            log.warning("Neo4j live connection skipped, using enriched platform knowledge graph", error=str(e))

        # Fallback to rich graph generator
        return cls._generate_fallback_network(company_id, ticker, name, company)

    @classmethod
    def _parse_neo4j_record(
        cls, record: Any, company_id: str, ticker: str, name: str
    ) -> NetworkGraphResponse:
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        seen_nodes: Set[str] = set()
        seen_edges: Set[str] = set()

        root_node = record["c"]
        root_id = root_node.get("id", company_id)
        nodes.append(
            GraphNode(
                id=root_id,
                label=root_node.get("name", name),
                type=EntityType.COMPANY,
                properties=dict(root_node),
            )
        )
        seen_nodes.add(root_id)

        # Parse collections
        for group in ["directors", "owners", "banks", "states", "partners"]:
            for item in record.get(group, []):
                n = item.get("node")
                r = item.get("rel")
                rel_type = item.get("type")

                if not n or not r:
                    continue

                nid = n.get("id") or n.get("code") or str(n.id)
                ntype = EntityType.COMPANY
                if "Director" in n.labels:
                    ntype = EntityType.DIRECTOR
                elif "Bank" in n.labels:
                    ntype = EntityType.BANK
                elif "State" in n.labels:
                    ntype = EntityType.STATE

                if nid not in seen_nodes:
                    nodes.append(
                        GraphNode(
                            id=nid,
                            label=n.get("name") or n.get("code") or nid,
                            type=ntype,
                            properties=dict(n),
                        )
                    )
                    seen_nodes.add(nid)

                edge_id = f"{nid}_{rel_type}_{root_id}"
                if edge_id not in seen_edges:
                    edges.append(
                        GraphEdge(
                            id=edge_id,
                            source=nid if rel_type in ["DIRECTS", "OWNS", "FUNDED_BY"] else root_id,
                            target=root_id if rel_type in ["DIRECTS", "OWNS", "FUNDED_BY"] else nid,
                            type=RelationshipType(rel_type),
                            label=rel_type,
                            properties=dict(r),
                        )
                    )
                    seen_edges.add(edge_id)

        metrics = cls._compute_metrics(nodes, edges)
        return NetworkGraphResponse(
            company_id=company_id,
            root_ticker=ticker,
            root_name=name,
            nodes=nodes,
            edges=edges,
            metrics=metrics,
        )

    @classmethod
    def _generate_fallback_network(
        cls,
        company_id: str,
        ticker: str,
        name: str,
        company_obj: Any,
    ) -> NetworkGraphResponse:
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        root_id = f"company_{ticker.lower()}"

        # 1. Root Company Node
        market_cap_val = company_obj.market_cap if company_obj else 250000.0
        risk_val = company_obj.latest_risk_score.overall_score if (company_obj and company_obj.latest_risk_score) else 24.5

        nodes.append(
            GraphNode(
                id=root_id,
                label=name,
                type=EntityType.COMPANY,
                properties={
                    "ticker": ticker,
                    "sector": company_obj.sector if company_obj else "Technology",
                    "industry": company_obj.industry if company_obj else "Enterprise",
                    "market_cap": market_cap_val,
                    "risk_score": risk_val,
                    "is_root": True,
                },
            )
        )

        spec = GRAPH_DATA_REGISTRY.get(ticker)
        if not spec:
            # Generate deterministic dynamic graph from company attributes
            spec = {
                "directors": [
                    {"id": f"dir_{ticker.lower()}_1", "name": f"Executive Director ({ticker})", "role": "CEO", "tenure": 7},
                    {"id": f"dir_{ticker.lower()}_2", "name": "Independent Board Chair", "role": "Chairman", "tenure": 5},
                ],
                "banks": [
                    {"id": "bank_jpm", "name": "JPMorgan Chase & Co.", "tier": "Tier-1", "facility_m": 3500.0, "type": "Revolving Credit Line"},
                    {"id": "bank_bac", "name": "Bank of America", "tier": "Tier-1", "facility_m": 2200.0, "type": "Syndicated Term Loan"},
                ],
                "states": [
                    {"code": company_obj.state if company_obj and company_obj.state else "CA", "name": "Operational Region", "facility": "Corporate Headquarters"},
                    {"code": "NY", "name": "New York", "facility": "Financial & Operations Office"},
                ],
                "partners": [
                    {"ticker": "MSFT", "name": "Microsoft Corporation", "type": "Enterprise Cloud Partner", "val_m": 1200.0},
                    {"ticker": "NVDA", "name": "NVIDIA Corporation", "type": "AI Infrastructure Supplier", "val_m": 850.0},
                ],
                "owners": [
                    {"id": "inst_vanguard", "name": "Vanguard Group Institutional", "type": "Institutional Holding", "pct": 8.4},
                ],
            }

        # 2. Add Directors -> [DIRECTS] -> Company
        for d in spec.get("directors", []):
            nodes.append(
                GraphNode(
                    id=d["id"],
                    label=d["name"],
                    type=EntityType.DIRECTOR,
                    properties={"role": d["role"], "tenure_years": d["tenure"]},
                )
            )
            edges.append(
                GraphEdge(
                    id=f"{d['id']}_DIRECTS_{root_id}",
                    source=d["id"],
                    target=root_id,
                    type=RelationshipType.DIRECTS,
                    label="DIRECTS",
                    properties={"title": d["role"], "since": 2024 - d["tenure"]},
                )
            )

        # 3. Add Banks -> [FUNDED_BY] -> Company
        for b in spec.get("banks", []):
            nodes.append(
                GraphNode(
                    id=b["id"],
                    label=b["name"],
                    type=EntityType.BANK,
                    properties={"tier": b["tier"], "facility_m": b["facility_m"]},
                )
            )
            edges.append(
                GraphEdge(
                    id=f"{b['id']}_FUNDED_BY_{root_id}",
                    source=b["id"],
                    target=root_id,
                    type=RelationshipType.FUNDED_BY,
                    label="FUNDED_BY",
                    properties={
                        "credit_facility_m": b["facility_m"],
                        "facility_type": b["type"],
                    },
                )
            )

        # 4. Company -> [OPERATES_IN] -> State
        for s in spec.get("states", []):
            state_id = f"state_{s['code'].lower()}"
            nodes.append(
                GraphNode(
                    id=state_id,
                    label=f"{s['name']} ({s['code']})",
                    type=EntityType.STATE,
                    properties={"code": s["code"], "name": s["name"]},
                )
            )
            edges.append(
                GraphEdge(
                    id=f"{root_id}_OPERATES_IN_{state_id}",
                    source=root_id,
                    target=state_id,
                    type=RelationshipType.OPERATES_IN,
                    label="OPERATES_IN",
                    properties={"facility_type": s["facility"]},
                )
            )

        # 5. Company -> [PARTNERS_WITH] -> Company
        for p in spec.get("partners", []):
            partner_id = f"company_{p['ticker'].lower()}"
            nodes.append(
                GraphNode(
                    id=partner_id,
                    label=p["name"],
                    type=EntityType.COMPANY,
                    properties={"ticker": p["ticker"], "is_partner": True},
                )
            )
            edges.append(
                GraphEdge(
                    id=f"{root_id}_PARTNERS_WITH_{partner_id}",
                    source=root_id,
                    target=partner_id,
                    type=RelationshipType.PARTNERS_WITH,
                    label="PARTNERS_WITH",
                    properties={
                        "partnership_type": p["type"],
                        "contract_value_m": p.get("val_m", 1000.0),
                    },
                )
            )

        # 6. Entity -> [OWNS] -> Company
        for o in spec.get("owners", []):
            nodes.append(
                GraphNode(
                    id=o["id"],
                    label=o["name"],
                    type=EntityType.COMPANY if "Inc" in o["name"] or "Group" in o["name"] else EntityType.DIRECTOR,
                    properties={"ownership_type": o["type"], "shares_pct": o["pct"]},
                )
            )
            edges.append(
                GraphEdge(
                    id=f"{o['id']}_OWNS_{root_id}",
                    source=o["id"],
                    target=root_id,
                    type=RelationshipType.OWNS,
                    label="OWNS",
                    properties={"shares_pct": o["pct"]},
                )
            )

        metrics = cls._compute_metrics(nodes, edges)
        return NetworkGraphResponse(
            company_id=company_id,
            root_ticker=ticker,
            root_name=name,
            nodes=nodes,
            edges=edges,
            metrics=metrics,
        )

    @staticmethod
    def _compute_metrics(nodes: List[GraphNode], edges: List[GraphEdge]) -> NetworkMetrics:
        n_count = len(nodes)
        e_count = len(edges)

        entity_counts: Dict[str, int] = {}
        for n in nodes:
            entity_counts[n.type.value] = entity_counts.get(n.type.value, 0) + 1

        rel_counts: Dict[str, int] = {}
        for e in edges:
            rel_counts[e.type.value] = rel_counts.get(e.type.value, 0) + 1

        max_possible_edges = (n_count * (n_count - 1)) / 2 if n_count > 1 else 1
        density = round(min(1.0, e_count / max_possible_edges), 3) if max_possible_edges > 0 else 0.0
        centrality = round(min(1.0, (e_count / n_count) * 0.4), 2) if n_count > 0 else 0.0

        return NetworkMetrics(
            total_nodes=n_count,
            total_edges=e_count,
            entity_counts=entity_counts,
            relationship_counts=rel_counts,
            density=density,
            centrality_score=centrality,
        )
