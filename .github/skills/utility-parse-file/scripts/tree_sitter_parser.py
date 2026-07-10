from pathlib import Path
import json
import sys
import re
from tree_sitter import Parser
import tree_sitter_languages


class TreeSitterCodeParser:
    """
    Stateful AST Code Parser using Tree-Sitter & Dynamic Regex Pattern Matching.
    Achieves method-level granularity for classes, annotations, and dependencies.
    """

    def __init__(self, language_name: str = "java", rules: dict = None):
        self.language_name = language_name.lower()
        self.language = tree_sitter_languages.get_language(self.language_name)
        self.parser = Parser()
        self.parser.set_language(self.language)
        
        # Sla de rules (provides/consumes) op die vanuit het metadata-model worden ingeladen
        self.rules = rules or {}

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        source_bytes = bytes(source_code, "utf-8")
        tree = self.parser.parse(source_bytes)
        root_node = tree.root_node

        summary = {
            "file": str(file_path),
            "parserLanguage": self.language_name,
            "classes": [],
            "provides": [],      # Annotaties/Scopes op klasse-niveau
            "dependencies": []   # Relaties (zowel klasse- als methode-niveau)
        }
        
        # Start de stateful traversie (beginnend zonder actieve methode-context)
        self._traverse_tree(root_node, source_code, summary, current_method=None)
        
        # Voer aanvullende regex-gebaseerde patroonherkenning uit op basis van het metadata-model
        self._apply_regex_rules(source_code, summary)
        
        return summary

    def _traverse_tree(self, node, source, summary, current_method=None):
        # 1. Herken Class Declaraties
        if node.type in ("class_declaration", "interface_declaration", "enum_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                class_name = source[name_node.start_byte:name_node.end_byte]
                summary["classes"].append(class_name)

        # 2. Herken Method Declaraties (Zet de methode-context voor sub-nodes)
        elif node.type == "method_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                current_method = source[name_node.start_byte:name_node.end_byte]

        # 3. Herken Annotations (bijv. @AuraEnabled, @future)
        elif node.type == "annotation":
            name_node = node.child_by_field_name("name")
            if name_node:
                annotation_name = source[name_node.start_byte:name_node.end_byte]
                
                # Check of dit matcht met een 'provides' regel uit je JSON model
                provides_rules = self.rules.get("provides", [])
                for rule in provides_rules:
                    if rule.get("pattern", "").strip("@") == annotation_name:
                        summary["provides"].append({
                            "relationship": rule.get("relationship"),
                            "scope": "method" if current_method else "class",
                            "attachedTo": current_method if current_method else summary["classes"][-1] if summary["classes"] else "unknown"
                        })

        # 4. Herken Relaties: Overerving (extends/implements)
        elif node.type in ("superclass", "interfaces"):
            text = source[node.start_byte:node.end_byte]
            cleaned_types = text.replace("extends", "").replace("implements", "").replace(" ", "").split(",")
            for t in cleaned_types:
                if t:
                    summary["dependencies"].append({
                        "type": "extends_or_implements",
                        "target": t,
                        "sourceMethod": current_method  # Meestal None (klasse-niveau)
                    })

        # 5. Herken Relaties: Object Instanties (new MyClass()) op methode-granulariteit
        elif node.type == "object_creation_expression":
            type_node = node.child_by_field_name("type")
            if type_node:
                target_class = source[type_node.start_byte:type_node.end_byte]
                summary["dependencies"].append({
                    "type": "instantiation",
                    "target": target_class,
                    "sourceMethod": current_method  # Gekoppeld aan de actieve methode!
                })

        # Recursief door de AST bladeren en de actieve methode-context doorgeven
        for child in node.children:
            self._traverse_tree(child, source, summary, current_method)

    def _apply_regex_rules(self, source, summary):
        """Applies dynamic regex pattern matching defined in the metadata-model config."""
        consumes_rules = self.rules.get("consumes", [])
        
        for rule in consumes_rules:
            pattern = rule.get("pattern")
            if not pattern:
                continue
                
            try:
                # Componeer en voer de regex uit
                compiled_regex = re.compile(pattern)
                for match in compiled_regex.finditer(source):
                    # Als de regex een 'named capture group' (?P<target>...) bevat, pakken we die dynamisch uit
                    group_dict = match.groupdict()
                    target = group_dict.get("target") if "target" in group_dict else match.group(1) if match.groups() else None
                    
                    if target:
                        # Zoek terug in welke methode deze match waarschijnlijk plaatsvond op basis van byte-positie (optioneel, nu plat gelogd via patroon)
                        summary["dependencies"].append({
                            "type": rule.get("relationship", "pattern_matched"),
                            "target": target,
                            "sourceMethod": "regex_extracted"
                        })
            except re.error:
                # Skip defecte regex patronen veilig
                continue


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tree_sitter_parser.py <code-file> [rules_json_string]')
        sys.exit(1)

    # Laad optionele rules in als JSON-string via de CLI (ingespoten door utility_parse.py)
    injected_rules = {}
    if len(sys.argv) > 2:
        try:
            injected_rules = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    parser = TreeSitterCodeParser(language_name="java", rules=injected_rules)
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
