from pathlib import Path
import json


class RepositoryScanner:
    """
    Generic repository orchestrator.

    Responsibilities:
    - Discover files
    - Match metadata types from config
    - Select parser
    - Parse files
    - Return normalized documents

    Does NOT:
    - Build dependencies
    - Build graphs
    - Perform architectural analysis
    """

    def __init__(self, config_path, parser_registry):
        self.config_path = Path(config_path)
        self.parser_registry = parser_registry

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.source_root = Path(self.config['sourceRoot'])

    def scan(self):

        results = {
            'sourceRoot': str(self.source_root),
            'files': []
        }

        for metadata in self.config['salesforceMetadata']:

            metadata_type = metadata['type']
            directory = metadata.get('directory')
            extension = metadata.get('extension')
            parser_name = metadata.get('parser')

            if not directory or not extension or not parser_name:
                continue

            parser = self.parser_registry.get(parser_name)

            if parser is None:
                continue

            target_dir = self.source_root / directory

            if not target_dir.exists():
                continue

            for file_path in target_dir.rglob('*'):

                if not file_path.is_file():
                    continue

                if extension not in file_path.name:
                    continue

                try:
                    document = parser.parse(str(file_path))

                    results['files'].append({
                        'metadataType': metadata_type,
                        'parser': parser_name,
                        'file': str(file_path),
                        'document': document
                    })

                except Exception as ex:
                    results['files'].append({
                        'metadataType': metadata_type,
                        'parser': parser_name,
                        'file': str(file_path),
                        'error': str(ex)
                    })

        return results


if __name__ == '__main__':

    print('RepositoryScanner')
    print('Instantiate with parser registry.')

    print('\nExample:\n')

    print('registry = {')
    print('    "xml": XmlParser(),')
    print('    "json": JsonParser(),')
    print('    "code": TreeSitterCodeParser()')
    print('}')

    print('\nscanner = RepositoryScanner(')
    print('    "metadata-model.json",')
    print('    registry')
    print(')')

    print('\nresult = scanner.scan()')
