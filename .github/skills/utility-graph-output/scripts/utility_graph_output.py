import os
import json
import sys
import hashlib
from pathlib import Path


class GraphReducer:
    """
    Consumes parsed source file data and safely merges it into a central
    graph database (workspace_state.json) using stable MD5 hashes.
    """

    def __init__(self, state_file: str):
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Loads the central state database or initializes a fresh graph schema."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Fallback if the file is corrupted or empty
                pass
        
        return {
            "nodes": [],
            "edges": []
        }

    @staticmethod
    def _generate_stable_id(data: dict) -> str:
        """Generates a process-independent deterministic MD5 hash for dictionary objects."""
        # sort_keys guarantees that identical keys in different orders produce the same hash
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.md5(serialized.encode('utf-8')).hexdigest()

    def integrate_document(self, parsed_doc: dict, metadata_type: str):
        """
        Transforms raw parser output into standardized nodes and edges,
        then integrates them into the central state map.
        """
        file_path = parsed_doc.get("file")
        if not file_path:
            return

        # 1. Integrate the File as a Node
        node_id = file_path
        new_node = {
            "id": node_id,
            "name": Path(file_path).name,
            "type": metadata_type,
            "parser": parsed_doc.get("parserLanguage", parsed_doc.get("rootTag", "generic"))
        }

        # Index current nodes by ID to prevent duplicates (Upsert logic)
        node_map = {n["id"]: n for n in self.state["nodes"]}
        node_map[node_id] = new_node
        self.state["nodes"] = list(node_map.values())

        # 2. Extract and Integrate Edges (Dependencies)
        # Supports tree-sitter structures ("dependencies") and fallback XML/JSON parsing
        incoming_dependencies = parsed_doc.get("dependencies", [])
        
        edge_map = {}
        # Pre-populate edge map with existing items using their stable hash as key
        for e in self.state["edges"]:
            edge_id = e.get("id") or self._generate_stable_id({k: v for k, v in e.items() if k != "id"})
            e["id"] = edge_id  # Ensure historical edges have an explicit ID
            edge_map[edge_id] = e

        for dep in incoming_dependencies:
            target = dep.get("target")
            dep_type = dep.get("type", "dependency")
            
            if not target:
                continue

            # Construct edge relationship skeleton
            edge_data = {
                "source": node_id,
                "target": target,
                "relationship": dep_type
            }
            
            # Generate deterministic unique key for this relationship
            stable_edge_id = self._generate_stable_id(edge_data)
            edge_data["id"] = stable_edge_id
            
            # Upsert into map
            edge_map[stable_edge_id] = edge_data

        self.state["edges"] = list(edge_map.values())

    def commit(self):
        """Executes an atomic file replacement to completely prevent data corruption."""
        temp_file = self.state_file.with_suffix('.json.tmp')
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
            
        # Atomic switch on POSIX/Windows systems
        os.replace(temp_file, self.state_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python utility_graph_output.py <state_file_path> <metadata_type>")
        print("Expects raw parser JSON payload injected via standard input (stdin).")
        sys.exit(1)

    state_path_arg = sys.argv[1]
    metadata_type_arg = sys.argv[2]

    # Read the pipeline stdout from stdin directly in-memory
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print("Error: Stdin stream is empty.", file=sys.stderr)
            sys.exit(1)
            
        parsed_payload = json.loads(raw_input)
    except json.JSONDecodeError as err:
        print(f"Error: Stdin did not provide valid JSON. {err}", file=sys.stderr)
        sys.exit(1)

    # Initialize reducer, merge transaction record, and commit
    reducer = GraphReducer(state_file=state_path_arg)
    reducer.integrate_document(parsed_payload, metadata_type=metadata_type_arg)
    reducer.commit()
    
    print(f"Success: Consolidated dependencies safely into {state_path_arg}")
