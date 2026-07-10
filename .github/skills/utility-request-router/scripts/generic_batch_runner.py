import os
import sys
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


class ConcurrentBatchRunner:
    """
    Windows-optimized parallel execution engine.
    Completely generic: passes parameters straight down the pipeline without hardcoded logic.
    """

    def __init__(self, worker_cmd: str, reducer_cmd: str, state_file: str):
        self.worker_cmd = worker_cmd
        self.reducer_cmd = reducer_cmd
        self.state_file = state_file

    def _execute_pipeline_node(self, file_path: str, file_type_arg: str, metadata_type_arg: str) -> str:
        """
        Executes a single pipeline command string: parser | reducer.
        Uses shell=True to guarantee that Windows CMD/PowerShell understands piping.
        """
        # Normaliseer slashes naar Windows backslashes (\) om path-crashes te voorkomen
        normalized_path = os.path.normpath(file_path)

        # Bouw het Windows-compatible gekoppelde pipe commando.
        # We geven file_type_arg en metadata_type_arg direct door zoals ze binnengekomen zijn in de router!
        full_command = (
            f'{self.worker_cmd} "{file_type_arg}" "{normalized_path}" | '
            f'{self.reducer_cmd} "{self.state_file}" "{metadata_type_arg}"'
        )

        try:
            # shell=True is CRUCIAAL op Windows om de '|' operator te laten werken in subprocessen
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                return f"Success: Processed {normalized_path}"
            else:
                return f"Error processing {normalized_path}: {result.stderr.strip()}"
        except Exception as ex:
            return f"Exception on {normalized_path}: {str(ex)}"

    def run(self, items_list: list, file_type: str, metadata_type: str):
        """Spawns thread workers up to the maximum capacity of the system CPU."""
        print(f"Starting batch runner. Allocating {len(items_list)} tasks across CPU threads...")
        
        with ThreadPoolExecutor() as executor:
            # Schiet alle processen gelijktijdig parallel af en geef de parameters dynamisch mee
            futures = {
                executor.submit(self._execute_pipeline_node, item, file_type, metadata_type): item 
                for item in items_list
            }
            
            for future in as_completed(futures):
                item = futures[future]
                try:
                    log_output = future.result()
                    print(log_output)
                except Exception as exc:
                    print(f"File {item} generated an exception: {exc}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel MapReduce Batch Runner for Windows")
    parser.add_argument("--worker", required=True, help="Base command for the worker parser")
    parser.add_argument("--reducer", required=True, help="Base command for the graph reducer")
    parser.add_argument("--items", required=True, help="Comma-separated list of relative file paths to process")
    parser.add_argument("--type", default="auto", help="Abstract file type (e.g. 'code', 'xml', 'json' or 'auto')")
    parser.add_argument("--metadata", default="Unknown", help="The Salesforce Metadata/SObject Type (e.g. 'ApexClass' or 'Account')")
    parser.add_argument("--state", default="workspace_state.json", help="Path to the central state database file")

    args = parser.parse_args()

    # Splits de komma-gescheiden lijst met bestanden op naar een schone Python list
    files_to_process = [f.strip() for f in args.items.split(",") if f.strip()]

    if not files_to_process:
        print("No valid file items provided. Exiting.")
        sys.exit(0)

    # Start de concurrent runner en geef de argumenten direct door
    runner = ConcurrentBatchRunner(
        worker_cmd=args.worker,
        reducer_cmd=args.reducer,
        state_file=args.state
    )
    runner.run(files_to_process, args.type, args.metadata)
