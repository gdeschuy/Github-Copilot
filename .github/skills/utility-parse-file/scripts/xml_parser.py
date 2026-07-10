from pathlib import Path
import json
import sys
import re
from xml.etree import ElementTree as ET


class XmlParser:
    """
    Generic XML parser for metadata analysis.
    Supports dynamic pattern matching for extracting dependencies (consumes/provides) 
    defined in the central metadata model.
    """

    def __init__(self, rules: dict = None):
        # Sla de rules (provides/consumes) op die vanuit het metadata-model worden ingeladen
        self.rules = rules or {}

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)

        tree = ET.parse(file_path)
        root = tree.getroot()

        elements = self._extract_elements(root)
        tag_index = self.build_tag_index(elements)

        summary = {
            "file": str(file_path),
            "rootTag": self._strip_namespace(root.tag),
            "elements": elements,
            "tagIndex": tag_index,
            "provides": [],      # Definities op XML-niveau
            "dependencies": []   # Gevonden relaties (consumes)
        }

        # Voer de patroonherkenning uit op basis van de ingeladen configuratieregels
        self._apply_metadata_rules(elements, summary)

        return summary

    def _extract_elements(self, element):
        result = {
            "tag": self._strip_namespace(element.tag),
            "text": element.text.strip() if element.text and element.text.strip() else None,
            "attributes": dict(element.attrib),
            "children": []
        }

        for child in element:
            result["children"].append(self._extract_elements(child))

        return result

    @staticmethod
    def _strip_namespace(tag: str) -> str:
        if "}" in tag:
            return tag.split("}", 1)[1]
        return tag

    def find_tags(self, node: dict, tag_name: str):
        results = []
        if node["tag"] == tag_name:
            results.append(node)

        for child in node.get("children", []):
            results.extend(self.find_tags(child, tag_name))
        return results

    def find_text_values(self, node: dict, tag_name: str):
        values = []
        if node["tag"] == tag_name and node.get("text"):
            values.append(node["text"])

        for child in node.get("children", []):
            values.extend(self.find_text_values(child, tag_name))
        return values

    def build_tag_index(self, node: dict, index=None):
        if index is None:
            index = {}

        tag_name = node["tag"]
        index.setdefault(tag_name, []).append({
            "text": node["text"],
            "attributes": node["attributes"]
        })

        for child in node.get("children", []):
            self.build_tag_index(child, index)

        return index

    def _apply_metadata_rules(self, root_node: dict, summary: dict):
        """
        Recursively scans the extracted XML tree and tests text/tags against 
        the pattern rules defined in the metadata model.
        """
        consumes_rules = self.rules.get("consumes", [])
        provides_rules = self.rules.get("provides", [])

        # Start een interne recursieve scan over alle platte nodes in de boom
        def scan_tree(node):
            node_tag = node["tag"]
            node_text = node["text"] or ""

            # 1. Evalueer 'consumes' regels (Dependencies)
            for rule in consumes_rules:
                pattern = rule.get("pattern")
                if not pattern:
                    continue

                try:
                    compiled_regex = re.compile(pattern)
                    # We testen of het patroon voorkomt in de tekst óf de tagnaam zelf
                    match = compiled_regex.search(node_text) or compiled_regex.search(node_tag)
                    
                    if match:
                        # Als er een named capture group (?P<target>...) in de regex zit, pakken we die
                        group_dict = match.groupdict()
                        target = group_dict.get("target") if "target" in group_dict else match.group(1) if match.groups() else node_text
                        
                        if target:
                            summary["dependencies"].append({
                                "type": rule.get("relationship", "xml_dependency"),
                                "target": target,
                                "sourceContext": f"XML_Tag:<{node_tag}>"
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
                    match = compiled_regex.search(node_text) or compiled_regex.search(node_tag)
                    
                    if match:
                        summary["provides"].append({
                            "relationship": rule.get("relationship"),
                            "scope": rule.get("scope", "element"),
                            "attachedTo": node_tag
                        })
                except re.error:
                    continue

            # Ga dieper de boom in
            for child in node.get("children", []):
                scan_tree(child)

        scan_tree(root_node)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python xml_parser.py <xml-file> [rules_json_string]')
        sys.exit(1)

    # Laad optionele rules in als JSON-string via de CLI (ingespoten door utility_parse.py)
    injected_rules = {}
    if len(sys.argv) > 2:
        try:
            injected_rules = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    parser = XmlParser(rules=injected_rules)
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
