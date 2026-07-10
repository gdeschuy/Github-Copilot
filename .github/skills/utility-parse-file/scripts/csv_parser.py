from pathlib import Path
import csv
import json
import sys
import re


class CsvParser:
    """
    Generic CSV parser for metadata and data lineage analysis.
    Converts flat tabular rows into indexable objects and applies regex rules.
    """

    def __init__(self, rules: dict = None):
        self.rules = rules or {}

    def parse(self, file_path: str) -> dict:
        file_path = Path(file_path)

        rows = []
        key_index = {}

        # Lees het CSV bestand veilig in met de ingebouwde csv module
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            # DictReader gebruikt de eerste rij automatisch als kolomkoppen (headers)
            reader = csv.DictReader(f)
            
            for index, row in enumerate(reader):
                # Maak van de rij een schone dictionary
                row_dict = dict(row)
                rows.append(row_dict)
                
                # Bouw een platte index op van alle waarden per kolom voor snelle lookups
                for col_name, value in row_dict.items():
                    if value:
                        key_index.setdefault(col_name, []).append(value)

        summary = {
            "file": str(file_path),
            "rootType": "CsvTable",
            "data": rows,          # Lijst met alle records (rijen)
            "keyIndex": key_index, # Index per kolomnaam
            "provides": [],
            "dependencies": []
        }

        # Voer de consumes/provides patroonherkenning uit over de rijen
        self._apply_metadata_rules(rows, summary)

        return summary

    def _apply_metadata_rules(self, rows: list, summary: dict):
        """Scans all CSV rows and matches column values against the metadata rules."""
        consumes_rules = self.rules.get("consumes", [])

        for index, row in enumerate(rows):
            for col_name, value in row.items():
                if not value:
                    continue

                for rule in consumes_rules:
                    pattern = rule.get("pattern")
                    if not pattern:
                        continue

                    try:
                        compiled_regex = re.compile(pattern)
                        # Test de regex op de waarde in de actieve cel
                        match = compiled_regex.search(str(value))
                        
                        if match:
                            group_dict = match.groupdict()
                            target = group_dict.get("target") if "target" in group_dict else match.group(1) if match.groups() else str(value)
                            
                            if target:
                                summary["dependencies"].append({
                                    "type": rule.get("relationship", "csv_dependency"),
                                    "target": target,
                                    "sourceContext": f"CSV_Row:[{index}]_Column:'{col_name}'"
                                })
                    except re.error:
                        continue


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python csv_parser.py <csv-file> [rules_json_string]')
        sys.exit(1)

    injected_rules = {}
    if len(sys.argv) > 2:
        try:
            injected_rules = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    parser = CsvParser(rules=injected_rules)
    document = parser.parse(sys.argv[1])
    print(json.dumps(document, indent=2, ensure_ascii=False))
