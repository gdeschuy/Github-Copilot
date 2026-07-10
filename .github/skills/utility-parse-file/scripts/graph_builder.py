
from pathlib import Path
import json
from collections import defaultdict


class RepositoryGraphBuilder:
    """
    Builds a consolidated AI-friendly repository knowledge graph.

    Input format:

    nodes = [
        {
            "id": "CaseService",
            "type": "ApexClass",
            "path": "classes/CaseService.cls"
        }
    ]

    edges = [
        {
            "source": "CaseFlow",
            "target": "CaseService",
            "relationship": "InvocableMethod"
        }
    ]
    """

    def build(self, nodes, edges, metadata=None):

        metadata = metadata or {}

        graph_nodes = {}

        incoming = defaultdict(set)
        outgoing = defaultdict(set)

        for edge in edges:
            outgoing[edge['source']].add(edge['target'])
            incoming[edge['target']].add(edge['source'])

        for node in nodes:

            node_id = node['id']

            graph_nodes[node_id] = {
                'type': node.get('type'),
                'path': node.get('path'),
                'dependencies': sorted(list(outgoing[node_id])),
                'usedBy': sorted(list(incoming[node_id])),
                'fanIn': len(incoming[node_id]),
                'fanOut': len(outgoing[node_id]),
                'riskScore': self._calculate_risk(
                    len(incoming[node_id]),
                    len(outgoing[node_id])
                )
            }

        statistics = self._build_statistics(nodes, edges)

        cycles = self._find_cycles(graph_nodes)
        orphans = self._find_orphans(graph_nodes)

        return {
            'metadata': metadata,
            'statistics': statistics,
            'nodes': graph_nodes,
            'edges': edges,
            'cycles': cycles,
            'orphans': orphans
        }

    def _calculate_risk(self, fan_in, fan_out):
        return min(100, fan_in * 2 + fan_out)

    def _build_statistics(self, nodes, edges):

        by_type = defaultdict(int)

        for node in nodes:
            by_type[node.get('type', 'Unknown')] += 1

        return {
            'totalNodes': len(nodes),
            'totalEdges': len(edges),
            'metadataTypes': dict(by_type)
        }

    def _find_orphans(self, nodes):

        results = []

        for node_id, node in nodes.items():
            if node['fanIn'] == 0 and node['fanOut'] == 0:
                results.append(node_id)

        return sorted(results)

    def _find_cycles(self, nodes):

        cycles = []
        visited = set()

        def dfs(current, stack):

            if current in stack:
                idx = stack.index(current)
                cycles.append(stack[idx:] + [current])
                return

            if current in visited:
                return

            visited.add(current)

            for dependency in nodes[current]['dependencies']:
                if dependency in nodes:
                    dfs(dependency, stack + [current])

        for node_name in nodes:
            dfs(node_name, [])

        unique = []
        seen = set()

        for cycle in cycles:
            key = tuple(cycle)
            if key not in seen:
                seen.add(key)
                unique.append(cycle)

        return unique


if __name__ == '__main__':

    example_nodes = [
        {
            'id': 'CaseFlow',
            'type': 'Flow',
            'path': 'flows/CaseFlow.flow-meta.xml'
        },
        {
            'id': 'CaseService',
            'type': 'ApexClass',
            'path': 'classes/CaseService.cls'
        }
    ]

    example_edges = [
        {
            'source': 'CaseFlow',
            'target': 'CaseService',
            'relationship': 'InvocableMethod'
        }
    ]

    builder = RepositoryGraphBuilder()

    graph = builder.build(
        example_nodes,
        example_edges,
        metadata={
            'sourceRoot': 'force-app/main/default'
        }
    )

    out = Path('repository-knowledge-graph.json')
    out.write_text(
        json.dumps(graph, indent=2),
        encoding='utf-8'
    )

    print(f'Generated: {out}')
