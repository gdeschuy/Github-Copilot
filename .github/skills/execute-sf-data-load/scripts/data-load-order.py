import json
import sys
from pathlib import Path


class DataLoaderOrchestrator:
    """
    Analyzes the workspace graph and calculates the exact execution order 
    for Salesforce data loading based on Parent/Child dependencies.
    """

    def __init__(self, state_file: str):
        self.state_file = Path(state_file)

    def calculate_load_order(self) -> list:
        if not self.state_file.exists():
            return []

        with open(self.state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)

        # 1. Verzamel alle object-nodes die we hebben geparsed
        nodes = state.get("nodes", [])
        edges = state.get("edges", [])

        # Breng in kaart welke objecten afhankelijk zijn van welke parents
        # Formaat: { 'Contact': ['Account'], 'SBQQ__QuoteLine__c': ['SBQQ__Quote__c', 'Product2'] }
        dependencies = {}
        object_to_file = {}

        # Initialiseer de registers op basis van de nodes in de graph
        for node in nodes:
            obj_type = node.get("type")
            file_path = node.get("id")  # In data-mode is de ID het CSV/JSON pad
            if obj_type and file_path:
                dependencies[obj_type] = set()
                object_to_file[obj_type] = file_path

        # 2. Scan alle Edges en registreer de Parent-afhankelijkheden
        for edge in edges:
            source_obj = edge.get("sourceContext", "")  # Bijv: "CSV_Column:'AccountId'" -> we herleiden het naar het type via de node map
            # Veiliger: we kijken naar de source node (het bestand dat geparsed is)
            source_file = edge.get("source")
            target_obj = edge.get("target")
            relationship = edge.get("relationship")

            # Vind welk object-type bij dit bronbestand hoort
            source_obj_type = None
            for node in nodes:
                if node["id"] == source_file:
                    source_obj_type = node["type"]
                    break

            # Als het een Parent-relatie is, moet het 'target' object EERST geladen worden
            if relationship == "Parent" and source_obj_type and target_obj:
                if source_obj_type in dependencies and target_obj in dependencies:
                    dependencies[source_obj_type].add(target_obj)

        # 3. Kahn's Algoritme / Topological Sort om de volgorde te bepalen
        ordered_objects = []
        visited = set()
        temporary_marked = set()

        def visit(obj):
            if obj in temporary_marked:
                # Vangt circulaire dependencies op (fout in datamodel) safely op
                return
            if obj not in visited:
                temporary_marked.add(obj)
                # Bezoek eerst alle parents van dit object
                for parent in dependencies.get(obj, []):
                    visit(parent)
                temporary_marked.remove(obj)
                visited.add(obj)
                ordered_objects.append(obj)

        for obj in dependencies:
            if obj not in visited:
                visit(obj)

        # Vertaal de geordende objecten terug naar hun fysieke CSV-bestandspaden
        load_queue = []
        for obj in ordered_objects:
            if obj in object_to_file:
                load_queue.append({
                    "object": obj,
                    "file": object_to_file[obj]
                })

        return load_queue


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utility_data_loader_order.py <state_file_path>")
        sys.exit(1)

    orchestrator = DataLoaderOrchestrator(state_file=sys.argv[1])
    queue = orchestrator.calculate_load_order()

    # Spuug de exacte volgorde uit als een strakke JSON array naar stdout
    print(json.dumps(queue, indent=2))
