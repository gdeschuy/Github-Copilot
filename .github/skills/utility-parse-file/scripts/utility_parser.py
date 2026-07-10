import sys
import json
from json_parser import JsonParser
from xml_parser import XmlParser
from tree_sitter_parser import TreeSitterCodeParser


def execute_utility_parser(parser_type: str, file_path: str):
    """
    Orchestrates individual parser nodes and guarantees clean stdout returns.
    """
    try:
        if parser_type == "json":
            parser = JsonParser()
        elif parser_type == "xml":
            parser = XmlParser()
        elif parser_type == "tree-sitter":
            parser = TreeSitterCodeParser()
        else:
            raise ValueError(f"Unknown parser type requested: {parser_type}")

        # Run parser execution
        output_data = parser.parse(file_path)
        
        # Stream structured JSON result directly back to utility router stdout
        print(json.dumps(output_data, indent=2, ensure_ascii=False))

    except Exception as e:
        error_payload = {
            "file": file_path,
            "parserType": parser_type,
            "error": str(e)
        }
        print(json.dumps(error_payload, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python utility_parse.py <parser_type> <file_path>")
        sys.exit(1)

    # Arguments injected dynamically via router skill execution context
    execute_utility_parser(sys.argv[1], sys.argv[2])
