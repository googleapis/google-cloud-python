import yaml
import os
import glob
import re

# Paths
LIBRARIAN_YAML = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/librarian.yaml"
POST_PROCESSING_DIR = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/.librarian/generator-input/client-post-processing"

# Load librarian.yaml
with open(LIBRARIAN_YAML, 'r') as f:
    librarian_data = yaml.safe_load(f)

libraries = librarian_data.get('libraries', [])

# Find all post-processing files
post_processing_files = glob.glob(os.path.join(POST_PROCESSING_DIR, "*.yaml"))

# Analyze post-processing files for mypy/noxfile replacements
mypy_replacements = {}
noxfile_mypy_replacements = {}

for file_path in post_processing_files:
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing {file_path}: {e}")
            continue
        
        if not data or 'replacements' not in data:
            continue
            
        for rep in data['replacements']:
            paths = rep.get('paths', [])
            for p in paths:
                # Extract package name from path: packages/<package_name>/...
                match = re.match(r"packages/([^/]+)/", p)
                if match:
                    package_name = match.group(1)
                    if "mypy.ini" in p:
                        if package_name not in mypy_replacements:
                            mypy_replacements[package_name] = []
                        mypy_replacements[package_name].append(file_path)
                    elif "noxfile.py" in p:
                        # Check if replacement is about mypy
                        before = rep.get('before', '')
                        after = rep.get('after', '')
                        if 'mypy' in before or 'mypy' in after:
                            if package_name not in noxfile_mypy_replacements:
                                noxfile_mypy_replacements[package_name] = []
                            noxfile_mypy_replacements[package_name].append(file_path)

# Prepare summary
summary = []

for lib in libraries:
    name = lib.get('name')
    apis = lib.get('apis', [])
    apis_populated = len(apis) > 0
    
    is_handwritten = not apis_populated
    is_hybrid = False
    
    reasons = []
    
    if is_handwritten:
        reasons.append("No 'apis' key in librarian.yaml")
    else:
        # Check if hybrid
        if name in mypy_replacements:
            is_hybrid = True
            reasons.append(f"mypy.ini replaced in {', '.join([os.path.basename(f) for f in mypy_replacements[name]])}")
        if name in noxfile_mypy_replacements:
            is_hybrid = True
            reasons.append(f"noxfile.py mypy session replaced in {', '.join([os.path.basename(f) for f in noxfile_mypy_replacements[name]])}")

    lib_type = "Handwritten" if is_handwritten else ("Hybrid" if is_hybrid else "GAPIC_AUTO")
    
    if lib_type in ["Handwritten", "Hybrid"]:
        summary.append({
            'name': name,
            'apis_populated': apis_populated,
            'type': lib_type,
            'reasons': '; '.join(reasons)
        })

# Output as Markdown Table
print("| Package Name | APIs Populated | Type | Reasons |")
print("| --- | --- | --- | --- |")
for item in summary:
    print(f"| {item['name']} | {item['apis_populated']} | {item['type']} | {item['reasons']} |")

