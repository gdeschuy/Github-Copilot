from pathlib import Path
import json


class JsonParser:
    """
    Generic JSON parser for metadata analysis.

    Responsibilities:
    - Parse JSON files
    - Flatten nested structures
    - Build key indexes
    - Search keys and values
    - Provide a normalized structure to dependency engines

    This parser deliberately contains no Salesforce-specific logic.
    """

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            'file': str(file_path),
            'rootType': type(data).__name__,
            'data': data,
            'keyIndex': self.build_key_index(data)
        }

    def build_key_index(self, obj, index=None):
        if index is None:
            index = {}

        if isinstance(obj, dict):
            for key, value in obj.items():
                # Alleen toevoegen als het een platte waarde is (geen dict of list)
                if not isinstance(value, (dict, list)):
                    index.setdefault(key, []).append(value)
                else:
                    # Als het een dict/list is, willen we wellicht alleen de aanwezigheid loggen,
                    # maar we vermijden het dupliceren van de hele sub-boom.
                    index.setdefault(key, []).append("[Nested Structure]")
                
                # Altijd recursief verder zoeken
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


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('Usage: python json_parser.py <json-file>')
        sys.exit(1)

    parser = JsonParser()
    document = parser.parse(sys.argv[1])

    print(json.dumps(document, indent=2, ensure_ascii=False))
