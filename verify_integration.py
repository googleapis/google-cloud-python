import re
import yaml
import os

def main():
    # Adjusted path to match your structure
    yaml_path = ".librarian/generator-input/client-post-processing/spanner-integration.yaml"
    
    if not os.path.exists(yaml_path):
        print(f"❌ Error: YAML not found at {yaml_path}")
        return

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)
    replacements = config.get("replacements", [])
    
    # Track which files actually exist locally
    all_paths = set()
    for r in replacements:
        for path in r.get("paths", []):
            all_paths.add(path)

    for file_path in sorted(all_paths):
        if not os.path.exists(file_path):
            print(f"⏭️  Skipping: {file_path} (not found)")
            continue

        with open(file_path, "r") as f:
            content = f.read()

        working_content = content
        modified = False
        
        print(f"\nPROCESSING: {file_path}")

        # PASS 1: Apply replacements
        for i, r in enumerate(replacements):
            if file_path in r.get("paths", []):
                # We check if the 'before' pattern exists
                if re.search(r["before"], working_content, flags=re.MULTILINE):
                    working_content = re.sub(r["before"], r["after"], working_content, flags=re.MULTILINE)
                    modified = True
                    print(f"  [Pass 1] Block {i+1}: Applied.")
                else:
                    print(f"  [Pass 1] Block {i+1}: No match (already applied or pattern mismatch).")

        if not modified:
            print("  No changes made.")
            continue

        # PASS 2: Idempotency check (Should be 0 matches now)
        idempotent_fail = False
        for i, r in enumerate(replacements):
            if file_path in r.get("paths", []):
                if re.search(r["before"], working_content, flags=re.MULTILINE):
                    print(f"  [Pass 2] ❌ FAIL: Block {i+1} matched again. Fix lookahead logic!")
                    idempotent_fail = True

        if not idempotent_fail:
            with open(file_path, "w") as f:
                f.write(working_content)
            print("  ✅ SUCCESS: Disk updated and verified idempotent.")
        else:
            print("  ⚠️  WARNING: File NOT updated due to idempotency failure.")

if __name__ == "__main__":
    main()