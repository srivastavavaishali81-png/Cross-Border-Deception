"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  MarkerType,
  BackgroundVariant,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import dagre from "dagre";

import { CompanyNode, DirectorNode, BankNode, StateNode } from "./CustomNodes";
import type { GraphEdgeData, GraphNodeData, NetworkGraphResponse } from "@/types/network";

interface NetworkGraphCanvasProps {
  graphData: NetworkGraphResponse;
  onSelectNode?: (node: GraphNodeData | null) => void;
  filterEntityType?: string;
  filterRelationshipType?: string;
}

const nodeTypes = {
  Company: CompanyNode,
  Director: DirectorNode,
  Bank: BankNode,
  State: StateNode,
};

const EDGE_COLORS: Record<string, string> = {
  DIRECTS: "#8b5cf6",      // violet-500
  OWNS: "#f59e0b",         // amber-500
  FUNDED_BY: "#10b981",    // emerald-500
  OPERATES_IN: "#06b6d4",  // cyan-500
  PARTNERS_WITH: "#6366f1",// indigo-500
};

function getLayoutedElements(
  nodes: Node[],
  edges: Edge[],
  direction = "TB"
) {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  const nodeWidth = 200;
  const nodeHeight = 80;

  dagreGraph.setGraph({
    rankdir: direction,
    ranksep: 90,
    nodesep: 60,
  });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
}

export function NetworkGraphCanvas({
  graphData,
  onSelectNode,
  filterEntityType = "all",
  filterRelationshipType = "all",
}: NetworkGraphCanvasProps) {
  // Convert graphData nodes & edges to ReactFlow format
  const rawNodes: Node[] = useMemo(() => {
    return graphData.nodes
      .filter((n) => filterEntityType === "all" || n.type === filterEntityType || n.properties.is_root)
      .map((n) => ({
        id: n.id,
        type: n.type,
        data: n,
        position: { x: 0, y: 0 },
      }));
  }, [graphData.nodes, filterEntityType]);

  const activeNodeIds = useMemo(() => new Set(rawNodes.map((n) => n.id)), [rawNodes]);

  const rawEdges: Edge[] = useMemo(() => {
    return graphData.edges
      .filter(
        (e) =>
          activeNodeIds.has(e.source) &&
          activeNodeIds.has(e.target) &&
          (filterRelationshipType === "all" || e.type === filterRelationshipType)
      )
      .map((e) => {
        const color = EDGE_COLORS[e.type] || "#64748b";
        return {
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          type: "smoothstep",
          animated: e.type === "PARTNERS_WITH" || e.type === "FUNDED_BY",
          style: { stroke: color, strokeWidth: 2 },
          labelStyle: { fill: color, fontWeight: 700, fontSize: 10 },
          labelBgStyle: { fill: "hsl(var(--card))", fillOpacity: 0.9, rx: 4, ry: 4 },
          labelBgPadding: [6, 2] as [number, number],
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color,
            width: 16,
            height: 16,
          },
          data: e,
        };
      });
  }, [graphData.edges, activeNodeIds, filterRelationshipType]);

  const { nodes: layoutedNodes, edges: layoutedEdges } = useMemo(() => {
    return getLayoutedElements(rawNodes, rawEdges, "TB");
  }, [rawNodes, rawEdges]);

  const [nodes, setNodes, onNodesChange] = useNodesState(layoutedNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(layoutedEdges);

  useEffect(() => {
    setNodes(layoutedNodes);
    setEdges(layoutedEdges);
  }, [layoutedNodes, layoutedEdges, setNodes, setEdges]);

  const handleNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      if (onSelectNode) {
        onSelectNode(node.data as unknown as GraphNodeData);
      }
    },
    [onSelectNode]
  );

  const handlePaneClick = useCallback(() => {
    if (onSelectNode) {
      onSelectNode(null);
    }
  }, [onSelectNode]);

  return (
    <div className="relative h-[650px] w-full rounded-2xl border border-border/70 bg-card/40 overflow-hidden backdrop-blur-md shadow-xl">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        onPaneClick={handlePaneClick}
        fitView
        minZoom={0.2}
        maxZoom={1.8}
        defaultEdgeOptions={{ type: "smoothstep" }}
      >
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="hsl(var(--muted-foreground) / 0.25)" />
        <Controls className="!bg-card/90 !border-border/80 !shadow-lg !rounded-xl !p-1" />
        <MiniMap
          nodeStrokeWidth={3}
          nodeColor={(n) => {
            if (n.type === "Company") return "#6366f1";
            if (n.type === "Director") return "#8b5cf6";
            if (n.type === "Bank") return "#10b981";
            if (n.type === "State") return "#06b6d4";
            return "#64748b";
          }}
          className="!bg-card/85 !border-border/70 !rounded-xl !shadow-lg hidden sm:block"
          maskColor="hsl(var(--background) / 0.7)"
        />
      </ReactFlow>
    </div>
  );
}
