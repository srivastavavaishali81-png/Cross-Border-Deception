"""
OZARK Backend — Unit & API Tests for Neo4j Network Graph Integration

Tests cover:
- Entities: Company, Director, Bank, State
- Relationships: DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH
- GET /api/network/{company_id}
- GET /network/{company_id}
- GET /api/v1/network/{company_id}
- Topological Graph Metrics
"""

import pytest
from httpx import AsyncClient

from app.schemas.network import (
    EntityType,
    RelationshipType,
    NetworkGraphResponse,
    GraphNode,
    GraphEdge,
)
from app.services.network_service import NetworkService


@pytest.mark.asyncio
async def test_network_service_synthetic_graph():
    """Verify NetworkService generates complete multi-entity graph with all 4 entities & 5 relationships."""
    graph = await NetworkService.get_company_network("AAPL", depth=1)
    
    assert isinstance(graph, NetworkGraphResponse)
    assert graph.company_id == "AAPL"
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0

    # Verify all 4 required entities exist
    node_types = {node.type for node in graph.nodes}
    assert EntityType.COMPANY in node_types
    assert EntityType.DIRECTOR in node_types
    assert EntityType.BANK in node_types
    assert EntityType.STATE in node_types

    # Verify all 5 required relationships exist
    edge_types = {edge.relationship for edge in graph.edges}
    assert RelationshipType.DIRECTS in edge_types
    assert RelationshipType.OWNS in edge_types
    assert RelationshipType.FUNDED_BY in edge_types
    assert RelationshipType.OPERATES_IN in edge_types
    assert RelationshipType.PARTNERS_WITH in edge_types

    # Verify metrics structure
    assert graph.metrics.total_nodes == len(graph.nodes)
    assert graph.metrics.total_edges == len(graph.edges)
    assert graph.metrics.density >= 0.0
    assert graph.metrics.entity_counts.get("Company", 0) >= 1
    assert graph.metrics.entity_counts.get("Director", 0) >= 1
    assert graph.metrics.entity_counts.get("Bank", 0) >= 1
    assert graph.metrics.entity_counts.get("State", 0) >= 1


@pytest.mark.asyncio
async def test_network_endpoint_api_network(client: AsyncClient):
    """Verify GET /api/network/{company_id} returns 200 OK with valid JSON graph."""
    response = await client.get("/api/network/AAPL")
    assert response.status_code == 200
    data = response.json()

    assert data["company_id"] == "AAPL"
    assert "nodes" in data
    assert "edges" in data
    assert "metrics" in data

    # Check node attributes
    for node in data["nodes"]:
        assert "id" in node
        assert "label" in node
        assert "type" in node
        assert node["type"] in ["Company", "Director", "Bank", "State"]

    # Check edge attributes
    for edge in data["edges"]:
        assert "id" in edge
        assert "source" in edge
        assert "target" in edge
        assert "relationship" in edge
        assert edge["relationship"] in [
            "DIRECTS",
            "OWNS",
            "FUNDED_BY",
            "OPERATES_IN",
            "PARTNERS_WITH",
        ]


@pytest.mark.asyncio
async def test_network_endpoint_v1_and_root(client: AsyncClient):
    """Verify alias endpoints /api/v1/network/{id} and /network/{id} work identically."""
    resp_v1 = await client.get("/api/v1/network/NVDA")
    assert resp_v1.status_code == 200
    data_v1 = resp_v1.json()
    assert data_v1["company_id"] == "NVDA"

    resp_root = await client.get("/network/MSFT")
    assert resp_root.status_code == 200
    data_root = resp_root.json()
    assert data_root["company_id"] == "MSFT"


@pytest.mark.asyncio
async def test_network_depth_parameter(client: AsyncClient):
    """Verify depth query parameter is accepted and parsed."""
    response = await client.get("/api/network/TSLA?depth=2")
    assert response.status_code == 200
    data = response.json()
    assert data["company_id"] == "TSLA"
