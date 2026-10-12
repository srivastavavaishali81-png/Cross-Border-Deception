/**
OZARK — Network Graph Types
*/

export type EntityType = "Company" | "Director" | "Bank" | "State";

export type RelationshipType =
  | "DIRECTS"
  | "OWNS"
  | "FUNDED_BY"
  | "OPERATES_IN"
  | "PARTNERS_WITH";

export interface GraphNodeData {
  id: string;
  label: string;
  type: EntityType;
  properties: Record<string, unknown>;
  [key: string]: unknown;
}

export interface GraphEdgeData {
  id: string;
  source: string;
  target: string;
  type: RelationshipType;
  label: string;
  properties: Record<string, unknown>;
  [key: string]: unknown;
}

export interface NetworkMetrics {
  total_nodes: number;
  total_edges: number;
  entity_counts: Record<string, number>;
  relationship_counts: Record<string, number>;
  density: number;
  centrality_score: number;
}

export interface NetworkGraphResponse {
  company_id: string;
  root_ticker?: string;
  root_name?: string;
  nodes: GraphNodeData[];
  edges: GraphEdgeData[];
  metrics: NetworkMetrics;
}
