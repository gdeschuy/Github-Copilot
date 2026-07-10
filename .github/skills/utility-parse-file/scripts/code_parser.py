from pathlib import Path
import json
from tree_sitter import Language, Parser


class TreeSitterCodeParser:
    """
    Generic Tree-sitter parser.

    Supports any language for which a Tree-sitter grammar is available.

    Examples:
        parser.register_language('javascript', ts_js.language())
        parser.register_language('python', ts_python.language())
        parser.register_language('apex', ts_apex.language())

    Output is normalized so downstream dependency extractors can work
    independently of the source language.
    """

    def __init__(self):
        self.languages = {}

    def register_language(self, name: str, language):
        self.languages[name] = Language(language)

    def parse_file(self, file_path: str, language_name: str):
        source = Path(file_path).read_bytes()
        return self.parse_bytes(source, language_name, str(file_path))

    def parse_bytes(self, source: bytes, language_name: str, source_name='<memory>'):
        if language_name not in self.languages:
            raise ValueError(f'Language not registered: {language_name}')

        parser = Parser()
        parser.language = self.languages[language_name]

        tree = parser.parse(source)

        return {
            'file': source_name,
            'language': language_name,
            'rootType': tree.root_node.type,
            'symbols': self._extract_symbols(tree.root_node, source),
            'ast': self._node_to_dict(tree.root_node, source)
        }

    def _extract_symbols(self, node, source):
        symbols = {
            'classes': [],
            'functions': [],
            'imports': []
        }

        stack = [node]

        while stack:
            current = stack.pop()
            node_type = current.type

            if 'class' in node_type:
                symbols['classes'].append({
                    'type': node_type,
                    'text': self._node_text(current, source)
                })

            if 'function' in node_type or 'method' in node_type:
                symbols['functions'].append({
                    'type': node_type,
                    'text': self._node_text(current, source)
                })

            if 'import' in node_type:
                symbols['imports'].append({
                    'type': node_type,
                    'text': self._node_text(current, source)
                })

            stack.extend(reversed(current.children))

        return symbols

    def _node_to_dict(self, node, source):
        return {
            'type': node.type,
            'start': node.start_point,
            'end': node.end_point,
            'text': self._node_text(node, source),
            'children': [
                self._node_to_dict(child, source)
                for child in node.children
            ]
        }

    def _node_text(self, node, source):
        return source[node.start_byte:node.end_byte].decode(
            'utf-8',
            errors='ignore'
        )


if __name__ == '__main__':
    print('TreeSitterCodeParser loaded.')
    print('Register grammars before parsing.')
    print('Example: parser.register_language("javascript", ts_js.language())')
