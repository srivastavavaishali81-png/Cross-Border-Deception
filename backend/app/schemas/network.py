"""
OZARK — Network Graph Schemas (Pydantic v2)
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    COMPANY = "Company"
    DIRECTOR = "Director"
    BANK = "Bank"
    STATE = "State"


class RelationshipType(str, Enum):
    DIRECTS = "DIRECTS"
    OWNS = "OWNS"
    FUNDED_BY = "FUNDED_BY"
    OPERATES_IN = "OPERATES_IN"
    PARTNERS_WITH = "PARTNERS_WITH"


class GraphNode(BaseModel):
    id: str
    label: str
    type: EntityType
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: RelationshipType
    relationship: Optional[RelationshipType] = None
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        if self.relationship is None:
            self.relationship = self.type


class NetworkMetrics(BaseModel):
    total_nodes: int
    total_edges: int
    entity_counts: Dict[str, int] = Field(default_factory=dict)
    relationship_counts: Dict[str, int] = Field(default_factory=dict)
    density: float = 0.0
    centrality_score: float = 0.0


class NetworkGraphResponse(BaseModel):
    company_id: str
    root_ticker: Optional[str] = None
    root_name: Optional[str] = None
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    metrics: NetworkMetrics
