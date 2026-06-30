import yaml
import os
import glob
import re

POST_PROCESSING_DIR = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/.librarian/generator-input/client-post-processing"

post_processing_files = glob.glob(os.path.join(POST_PROCESSING_DIR, "*.yaml"))

print("=== Noxfile Replacements ===")
for file_path in post_processing_files:
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            continue
        
        if not data or 'replacements' not in data:
            continue
            
        for rep in data['replacements']:
            paths = rep.get('paths', [])
            for p in paths:
                if "noxfile.py" in p:
                    print(f"File: {os.path.basename(file_path)}")
                    print(f"Path: {p}")
                    print(f"Before: {rep.get('before', '')}")
                    print(f"After: {rep.get('after', '')}")
                    print("-" * 20)
