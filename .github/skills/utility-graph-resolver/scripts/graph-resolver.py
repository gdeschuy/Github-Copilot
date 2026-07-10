import json
import sys
from pathlib import Path


class GraphResolver:
    """
    Analyzes the central graph database and returns only the unresolved 
    dependencies (missing nodes) to prevent LLM context-window exhaustion.
    """

    def __init__(self, state_file: str, source_root: str = "."):
        self.state_file = Path(state_file)
        self.source_root = Path(source_root)

    def get_unresolved_dependencies(self) -> list:
        if not self.state_file.exists():
            return []

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except json.JSONDecodeError:
            return []

        # 1. Verzamel alle unieke bestanden die al succesvol geparsed zijn (Nodes)
        parsed_nodes = {node["id"] for node in state.get("nodes", [])}

        # 2. Verzamel alle targets die ergens als dependency (Edge) zijn genoemd
        all_discovered_targets = {edge["target"] for edge in state.get("edges", [])}

        unresolved_files = []

        # 3. Match de ontdekte klassen/targets naar echte bestandspaden
        for target in all_discovered_targets:
            # We zoeken naar de bijbehorende .cls of .trigger file in de repository
            # Dit voorkomt dat de AI zelf handmatig door mappen moet rglobben
            possible_paths = list(self.source_root.rglob(f"{target}.cls")) + \
                             list(self.source_root.rglob(f"{target}.trigger"))

            for path in possible_paths:
                relative_path = str(path.relative_to(self.source_root) if path.is_absolute() else path)
                
                # Als het bestand wel bestaat in je repo, maar nog NIET als node in de graph staat:
                if relative_path not in parsed_nodes:
                    unresolved_files.append(relative_path)

        return list(set(unresolved_files))  # Dedupliceren


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utility_graph_resolver.py <state_file_path> [source_root]")
        sys.exit(1)

    state_path = sys.argv[1]
    root_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    resolver = GraphResolver(state_file=state_path, source_root=root_dir)
    unresolved = resolver.get_unresolved_dependencies()

    # Geef een extreem compacte JSON array terug aan de AI via stdout
    print(json.dumps(unresolved, indent=2))
