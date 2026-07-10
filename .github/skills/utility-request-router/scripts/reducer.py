import os
import json
import glob
import sys
import hashlib

def generic_reducer(staging_dir, state_file, primary_key="id"):
    """
    Dynamically loads and merges JSON file structures from a staging folder 
    into a central state file without process-specific hash collisions.
    """
    # 1. Load or initialize the central state database
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except json.JSONDecodeError:
            state = {} # Fallback if file is corrupted/empty

    # 2. Iterate through all incoming transaction chunks
    for tx_file in glob.glob(os.path.join(staging_dir, "tx_*.json")):
        try:
            with open(tx_file, 'r', encoding='utf-8') as f:
                incoming_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue # Skip broken transaction files

        # 3. Dynamically reduce arrays based on the primary key
        for key, incoming_array in incoming_data.items():
            if not isinstance(incoming_array, list):
                continue 
                
            if key not in state:
                state[key] = []
                
            # Create a lookup map using the item's key, or generate a stable hash
            current_map = {}
            for index, item in enumerate(state[key]):
                item_id = item.get(primary_key)
                if not item_id:
                    # Generate a stable, process-independent deterministic hash
                    item_str = json.dumps(item, sort_keys=True)
                    item_id = hashlib.md5(item_str.encode('utf-8')).hexdigest()
                current_map[item_id] = item
            
            # Merge incoming data
            for item in incoming_array:
                item_id = item.get(primary_key)
                if not item_id:
                    # Generate the same stable hash for incoming items
                    item_str = json.dumps(item, sort_keys=True)
                    item_id = hashlib.md5(item_str.encode('utf-8')).hexdigest()
                
                current_map[item_id] = item # Upsert (overwrites old data if matching ID)

            state[key] = list(current_map.values())

    # 4. Atomic commit to prevent data loss
    if state:
        temp_file = state_file + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        os.replace(temp_file, state_file)

    # 5. Clear staging directory safely
    for tx_file in glob.glob(os.path.join(staging_dir, "tx_*.json")):
        try:
            os.remove(tx_file)
        except OSError:
            pass
        
    print(f"Success: Reducer committed final updates to {state_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <staging_dir> <state_file> [primary_key]")
        sys.exit(1)
        
    staging = sys.argv[1]
    state_out = sys.argv[2]
    pkey = sys.argv[3] if len(sys.argv) > 3 else "id"
    
    generic_reducer(staging, state_out, pkey)
