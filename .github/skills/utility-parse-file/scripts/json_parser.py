from pathlib import Path
import json
import sys
import re


class JsonParser:
    """
    Generic JSON parser for metadata analysis.
    Supports memory-optimized key indexing and dynamic pattern matching 
    for dependency extraction (consumes/provides).
    """

    def __init__(self, rules: dict = None):
        # Sla de rules (provides/consumes) op die vanuit het metadata-model worden ingeladen
        self.rules = rules or {}

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        summary = {
            'file': str(file_path),
            'rootType': type(data).__name__,
            'data': data,
            'keyIndex': self.build_key_index(data),
            'provides': [],      # Definities op JSON-niveau
            'dependencies': []   # Gevonden relaties (consumes)
        }

        # Voer de patroonherkenning uit op de geladen JSON-structuur
        self._apply_metadata_rules(data, summary)

        return summary

    def build_key_index(self, obj, index=None):
        if index is None:
            index = {}

        if isinstance(obj, dict):
            for key, value in obj.items():
                # GEHEUGENOPTIMALISATIE: Sla alleen platte waarden op om memory bloat te voorkomen
                if not isinstance(value, (dict, list)):
                    index.setdefault(key, []).append(value)
                else:
                    index.setdefault(key, []).append("[Nested Structure]")
                
                self.build_key_index(value, index)

        elif isinstance(obj, list):
            for item in obj:
                self.build_key_index(item, index)

        return index

    def find_key(self, obj, key_name):
        results = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == key_name:
                    results.append(value)
                results.extend(self.find_key(value, key_name))
        elif isinstance(obj, list):
            for item in obj:
                results.extend(self.find_key(item, key_name))
        return results

    def find_value(self, obj, target_value):
        results = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if value == target_value:
                    results.append({key: value})
                results.extend(self.find_value(value, target_value))
        elif isinstance(obj, list):
            for item in obj:
                results.extend(self.find_value(item, target_value))
        return results

    def flatten_paths(self, obj, path=''):
        paths = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f'{path}.{key}' if path else key
                paths.extend(self.flatten_paths(value, new_path))
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                new_path = f'{path}[{index}]'
                paths.extend(self.flatten_paths(item, new_path))
        else:
            paths.append({
                'path': path,
                'value': obj
            })
        return paths

    def _apply_metadata_rules(self, root_obj, summary: dict):
        """
        Recursively scans the JSON object graph and applies regex patterns 
        to keys and string values based on the metadata model.
        """
        consumes_rules = self.rules.get("consumes", [])
        provides_rules = self.rules.get("provides", [])

        def scan_node(node, current_key="root"):
            # Converteer de huidige node naar string als het een platte waarde is voor regex-tests
            node_str_value = str(node) if not isinstance(node, (dict, list)) else ""

            # 1. Evalueer 'consumes' regels (Dependencies)
            for rule in consumes_rules:
                pattern = rule.get("pattern")
                if not pattern:
                    continue

                try:
                    compiled_regex = re.compile(pattern)
                    # We testen het patroon zowel op de actieve JSON-key als op de string-waarde
                    match = compiled_regex.search(node_str_value) or compiled_regex.search(current_key)
                    
                    if match:
                        group_dict = match.groupdict()
                        target = group_dict.get("target") if "target" in group_dict else match.group(1) if match.groups() else node_str_value
                        
                        if target:
                            summary["dependencies"].append({
                                "type": rule.get("relationship", "json_dependency"),
                                "target": target,
                                "sourceContext": f"JSON_Key:'{current_key}'"
                            })
                except re.error:
                    continue

            # 2. Evalueer 'provides' regels (Capabilities)
            for rule in provides_rules:
                pattern = rule.get("pattern")
                if not pattern:
                    continue

                try:
                    compiled_regex = re.compile(pattern)
                    match = compiled_regex.search(node_str_value) or compiled_regex.search(current_key)
                    
                    if match:
                        summary["provides"].append({
                            "relationship": rule.get("relationship"),
                            "scope": rule.get("scope", "element"),
                            "attachedTo": current_key
                        })
                except re.error:
                    continue

            # Ga recursief dieper de JSON-structuur in
            if isinstance(node, dict):
                for k, v in node.items():
                    scan_node(v, current_key=k)
            elif isinstance(node, list):
                for item in node:
                    scan_node(item, current_key=current_key)

        scan_node(root_obj)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python json_parser.py <json-file> [rules_json_string]')
        sys.exit(1)

    # Laad optionele rules in als JSON-string via de CLI (ingespoten door utility_parse.py)
    injected_rules = {}
    if len(sys.argv) > 2:
        try:
            injected_rules = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    parser = JsonParser(rules=injected_rules)
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
