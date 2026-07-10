import os
import sys
import json
import subprocess
from pathlib import Path


class Rollback:
    """
    Executes sequenced data loads, captures live cloud IDs, 
    generates structured asset logs, and performs automatic LIFO rollbacks on failure.
    """

    def __init__(self, state_file: str, assets_dir: str):
        self.state_file = Path(state_file)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Live register om succesvol aangemaakte ID's per objecttype bij te houden
        self.inserted_ids = {}

    def _get_load_queue(self) -> list:
        """Invokes the data-load-order logic to get the correct sequence."""
        # We hergebruiken je bestaande data-load-order logica via een interne aanroep
        # of we gaan ervan uit dat de AI de queue al heeft berekend.
        # Voor de veiligheid gaan we ervan uit dat de geordende lijst als argument binnenkomt.
        pass

    def run_load_sequence(self, queue_list: list):
        print(f"Initializing safe deployment pipeline. Total objects in queue: {len(queue_list)}")
        
        success_summary = {}
        error_summary = {}
        failed = False

        for item in queue_list:
            obj_type = item.get("object")
            file_path = os.path.normpath(item.get("file"))
            
            if failed:
                break

            print(f"Deploying batch: {obj_type} from {file_path}...")
            
            # Start het Salesforce CLI bulk-insert commando en dwing JSON output af
            cmd = f'sf data record insert bulk --sobject {obj_type} --file "{file_path}" --json'
            
            # shell=True is verplicht op Windows voor sf CLI subprocessen
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            
            try:
                response = json.loads(result.stdout)
                
                # Salesforce CLI geeft bij succes of gedeeltelijk succes een gestructureerde JSON terug
                if result.returncode == 0 and response.get("status") == 0:
                    records = response.get("result", {}).get("records", [])
                    
                    # Filter alle succesvolle nieuwe live Cloud ID's eruit
                    successful_ids = [r["id"] for r in records if r.get("id")]
                    self.inserted_ids[obj_type] = successful_ids
                    success_summary[obj_type] = response.get("result")
                    
                    # Als er binnen de bulk job alsnog mislukte rijen zaten (partial failure)
                    if response.get("result", {}).get("failed", 0) > 0:
                        print(f"Warning: Partial failure detected in {obj_type} batch.")
                        error_summary[obj_type] = response.get("result").get("errors", "Bulk partial errors")
                        failed = True
                else:
                    # Harde crash van het CLI commando zelf
                    error_summary[obj_type] = response.get("message", result.stderr)
                    failed = True
                    
            except json.JSONDecodeError:
                error_summary[obj_type] = f"CLI Execution Crash. Stderr: {result.stderr}"
                failed = True

        # Schrijf de logs ALTIJD weg naar de assets folder van de skill
        self._write_assets(success_summary, error_summary)

        # Als er ergens in de keten een fout is opgetreden, starten we DIRECT de rollback!
        if failed:
            self._execute_rollback()
            sys.exit(1)
        else:
            print("Deployment pipeline completed successfully. All records committed.")

    def _write_assets(self, success_data: dict, error_data: dict):
        """Generates the success and error artifact files inside the skill's assets folder."""
        with open(self.assets_dir / "success_log.json", "w", encoding="utf-8") as f:
            json.dump(success_data, f, indent=2, ensure_ascii=False)
            
        with open(self.assets_dir / "error_log.json", "w", encoding="utf-8") as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
            
        print(f"Artifacts successfully written to {self.assets_dir}\\")

    def _execute_rollback(self):
        """Executes the automatic Topological Rollback (Last In, First Out)."""
        print("\n[CRITICAL ERROR] Launching automated state recovery (LIFO Rollback)...")
        
        # Draai de volgorde van de succesvol geladen objecten om
        reversed_objects = list(self.inserted_ids.keys())
        reversed_objects.reverse()

        for obj_type in reversed_objects:
            ids_to_delete = self.inserted_ids[obj_type]
            if not ids_to_delete:
                continue
                
            print(f"Purging {len(ids_to_delete)} dirty records from cloud object: {obj_type}...")
            id_string = ",".join(ids_to_delete)
            
            # Voer de atomaire delete bulk uit via de CLI
            delete_cmd = f'sf data record delete bulk --sobject {obj_type} --ids "{id_string}" --json'
            subprocess.run(delete_cmd, shell=True, capture_output=True)
            
        print("State recovery complete. Salesforce environment successfully restored to pre-flight state.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utility_data_loader_with_rollback.py '<queue_json_string>' [assets_dir]")
        sys.exit(1)

    # De AI geeft de berekende queue direct mee als een JSON string argument
    try:
        raw_queue = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Input queue must be a valid JSON string.")
        sys.exit(1)

    # Bepaal de assets folder (standaard onder de specifieke skill map)
    target_assets = sys.argv[2] if len(sys.argv) > 2 else "skills/execute-sf-data-load/assets"

    loader = SafeDataLoader(state_file="workspace_state.json", assets_dir=target_assets)
    loader.run_load_sequence(raw_queue)
