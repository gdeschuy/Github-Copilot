import sys
import json
from pathlib import Path
from json_parser import JsonParser
from xml_parser import XmlParser
from tree_sitter_parser import TreeSitterCodeParser


class UtilityParseWrapper:
    """
    Orchestration wrapper that loads dynamic metadata rules from the central config
    and injects them directly into the designated parser instances.
    """

    def __init__(self, config_path: str = "references/metadata-model.json"):
        self.config_path = Path(config_path)
        self.config_rules = self._load_config_rules()

    def _load_config_rules(self) -> dict:
        """Loads and indexes rules by directory and extension to support bundles."""
        if not self.config_path.exists():
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            indexed_rules = {}
            for item in data.get("salesforceMetadata", []):
                directory = item.get("directory")
                
                # Check of dit een geneste bundel is
                if item.get("isBundle") and "files" in item:
                    for sub_file in item["files"]:
                        ext = sub_file.get("extension")
                        # Combineer de hoofd-metadata info met de sub-file info
                        combined_rule = {**item, **sub_file}
                        indexed_rules[(directory, ext)] = combined_rule
                else:
                    # Normale platte structuur (ApexClass, CustomObject, etc.)
                    ext = item.get("extension")
                    indexed_rules[(directory, ext)] = item
                    
            return indexed_rules
        except (json.JSONDecodeError, IOError):
            return {}

    def execute(self, file_type: str, file_path: str):
        """
        Instantiates the correct parser node with its matching config rules 
        and streams the result straight to stdout.
        """
        path_obj = Path(file_path)
        ext = path_obj.suffix.lower()
        
        # 1. VEILIGE LOOKUP: Wandel door alle bovenliggende mappen (parents)
        # en kijk welke mapnaam (bijv. 'classes', 'lwc', 'objects') matcht met je config
        matched_rule = {}
        for parent in [path_obj.name] + [p.name for p in path_obj.parents]:
            if (parent, ext) in self.config_rules:
                matched_rule = self.config_rules[(parent, ext)]
                break

        # 2. Gebruik het overschreven file_type uit de gevonden regel, of val terug op het argument
        actual_file_type = matched_rule.get("fileType", file_type)

        try:
            if actual_file_type == "code":
                # Bepaal de tree-sitter language op basis van de extensie
                lang = "javascript" if ext == ".js" else "java"
                parser = TreeSitterCodeParser(language_name=lang, rules=matched_rule)
                
            elif actual_file_type == "xml":
                parser = XmlParser(rules=matched_rule)

            elif actual_file_type == "json":
                parser = JsonParser(rules=matched_rule)
                
            else:
                raise ValueError(f"Unknown abstract file type requested: {actual_file_type}")

            # Voer de parser uit
            output_data = parser.parse(file_path)
            
            # Voeg de metadataType context toe aan de output payload voor de graph reducer
            output_data["metadataType"] = matched_rule.get("type", "Unknown")

            # Stream het gestructureerde resultaat direct naar stdout
            print(json.dumps(output_data, indent=2, ensure_ascii=False))

        except Exception as e:
            error_payload = {
                "file": file_path,
                "fileType": actual_file_type,
                "error": str(e)
            }
            print(json.dumps(error_payload, indent=2), file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python utility_parse.py <file_type> <file_path>")
        sys.exit(1)

    # CLI arguments injected via the concurrent request router pipeline
    requested_type = sys.argv[1]
    requested_path = sys.argv[2]

    wrapper = UtilityParseWrapper()
    wrapper.execute(requested_type, requested_path)
