"""
OZARK Backend — Network Graph Endpoints

Provides endpoints:
- GET /network/{company_id} (and /api/network/{company_id}, /api/v1/network/{company_id})
Returns complete knowledge graph JSON across Entities:
  - Company, Director, Bank, State
And Relationships:
  - DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH
"""

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.network import NetworkGraphResponse
from app.services.network_service import NetworkService

router = APIRouter(prefix="/network", tags=["network"])


@router.get(
    "/{company_id}",
    response_model=NetworkGraphResponse,
    summary="Get enterprise knowledge graph by company ID or ticker",
    description=(
        "Retrieves multi-hop Neo4j enterprise relationship network connecting:\n"
        "- Entities: Company, Director, Bank, State\n"
        "- Relationships: DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH\n"
        "Returns formatted nodes, labeled edges, and topological network graph metrics."
    ),
)
async def get_company_network_graph(
    company_id: str,
    depth: int = Query(default=1, ge=1, le=3, description="Graph traversal hop depth (1-3)"),
):
    try:
        graph = await NetworkService.get_company_network(company_id, depth=depth)
        return graph
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assemble network graph for '{company_id}': {str(e)}",
        )
