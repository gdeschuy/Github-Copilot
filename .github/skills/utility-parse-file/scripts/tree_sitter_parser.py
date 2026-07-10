from pathlib import Path
import json
import sys
from tree_sitter import Parser
import tree_sitter_languages


class TreeSitterCodeParser:
    """
    Generic AST Code Parser using Tree-Sitter.
    Extracts high-level code constructs and potential tokens for dependency mapping.
    """

    def __init__(self, language_name: str = "java"):
        # Sla de string naam op zodat we deze later dynamisch kunnen loggen
        self.language_name = language_name.lower()
        self.language = tree_sitter_languages.get_language(self.language_name)
        self.parser = Parser()
        self.parser.set_language(self.language)

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Correcte, veilige parsing voor moderne tree-sitter wrappers
        source_bytes = bytes(source_code, "utf-8")
        tree = self.parser.parse(source_bytes)
        root_node = tree.root_node

        # Dynamisch de opgeslagen language_name gebruiken in plaats van hardcoding
        summary = {
            "file": str(file_path),
            "parserLanguage": self.language_name,
            "classes": [],
            "dependencies": []
        }
        
        self._traverse_tree(root_node, source_code, summary)
        return summary

    def _traverse_tree(self, node, source, summary):
        if node.type in ("class_declaration", "interface_declaration", "enum_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                summary["classes"].append(source[name_node.start_byte:name_node.end_byte])

        if node.type in ("superclass", "interfaces"):
            text = source[node.start_byte:node.end_byte]
            cleaned_types = text.replace("extends", "").replace("implements", "").replace(" ", "").split(",")
            for t in cleaned_types:
                if t:
                    summary["dependencies"].append({"type": "extends_or_implements", "target": t})

        if node.type == "object_creation_expression":
            type_node = node.child_by_field_name("type")
            if type_node:
                target_class = source[type_node.start_byte:type_node.end_byte]
                summary["dependencies"].append({"type": "instantiation", "target": target_class})

        for child in node.children:
            self._traverse_tree(child, source, summary)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tree_sitter_parser.py <code-file> [language_name]')
        sys.exit(1)

    # Optioneel: sta toe dat je de taal ook via de CLI kunt meegeven, bijv: python tree_sitter_parser.py file.cls apex
    lang = sys.argv[2] if len(sys.argv) > 2 else "java"

    parser = TreeSitterCodeParser(language_name=lang)
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
