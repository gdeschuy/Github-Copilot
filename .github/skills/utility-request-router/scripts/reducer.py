import os
import json
import glob
import sys

def generic_reducer(staging_dir, state_file, primary_key="id"):
    """
    Dynamically loads and merges any JSON file structure from a staging folder 
    into a central state file by matching a primary key.
    """
    # 1. Load or initialize the central state database
    state = {}
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)

    # 2. Iterate through all incoming transaction chunks
    for tx_file in glob.glob(os.path.join(staging_dir, "tx_*.json")):
        with open(tx_file, 'r') as f:
            incoming_data = json.load(f)
        
        # 3. Dynamically reduce arrays based on the primary key
        for key, incoming_array in incoming_data.items():
            if not isinstance(incoming_array, list):
                continue # Skip metadata fields that aren't lists
                
            # Initialize the array in the master state if it doesn't exist
            if key not in state:
                state[key] = []
                
            # Convert current state collection to a dictionary map for upserts
            # Edges might use a fallback or a custom compound key if "id" isn't present
            current_map = {item.get(primary_key, index): item for index, item in enumerate(state[key])}
            
            for item in incoming_array:
                item_id = item.get(primary_key)
                if item_id:
                    current_map[item_id] = item # Upsert logic
                else:
                    # Fallback for edges or objects without explicit string IDs
                    # Generates a stable unique hash based on sorted object properties
                    fallback_id = hash(frozenset(sorted(item.items())))
                    current_map[fallback_id] = item

            state[key] = list(current_map.values())

    # 4. Atomic commit to prevent data loss
    temp_file = state_file + ".tmp"
    with open(temp_file, 'w') as f:
        json.dump(state, f, indent=2)
    os.replace(temp_file, state_file)

    # 5. Clear staging directory for the next task
    for tx_file in glob.glob(os.path.join(staging_dir, "tx_*.json")):
        os.remove(tx_file)
        
    print(f"Success: Reducer committed final updates to {state_file}")

if __name__ == "__main__":
    # Accepts arguments via the terminal/skill execution window
    generic_reducer(sys.argv[1], sys.argv[2])
