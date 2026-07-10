from pathlib import Path
import json
import sys
from xml.etree import ElementTree as ET


class XmlParser:
    """
    Generic XML parser for metadata analysis.
    """

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)

        tree = ET.parse(file_path)
        root = tree.getroot()

        elements = self._extract_elements(root)
        tag_index = self.build_tag_index(elements)

        return {
            "file": str(file_path),
            "rootTag": self._strip_namespace(root.tag),
            "elements": elements,
            "tagIndex": tag_index
        }

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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python xml_parser.py <xml-file>')
        sys.exit(1)

    parser = XmlParser()
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
