import yaml
import os
import glob
import re
import csv

# Paths
LIBRARIAN_YAML = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/librarian.yaml"
POST_PROCESSING_DIR = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/.librarian/generator-input/client-post-processing"
OUTPUT_CSV = "/usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/feat-centralize-mypy/scratch/library_analysis.csv"

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
            continue
        
        if not data or 'replacements' not in data:
            continue
            
        for rep in data['replacements']:
            paths = rep.get('paths', [])
            for p in paths:
                match = re.match(r"packages/([^/]+)/", p)
                if match:
                    package_name = match.group(1)
                    if "mypy.ini" in p:
                        if package_name not in mypy_replacements:
                            mypy_replacements[package_name] = []
                        mypy_replacements[package_name].append(file_path)
                    elif "noxfile.py" in p:
                        before = rep.get('before', '')
                        after = rep.get('after', '')
                        # Broader check for mypy relevance
                        if 'mypy' in before or 'mypy' in after or 'check-untyped-defs' in before or 'check-untyped-defs' in after:
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
    
    if not is_handwritten:
        if name in mypy_replacements or name in noxfile_mypy_replacements:
            is_hybrid = True

    lib_type = "Handwritten" if is_handwritten else ("Hybrid" if is_hybrid else "GAPIC_AUTO")
    
    summary.append({
        'Package Name': name,
        'APIs Populated': apis_populated,
        'Detected Type': lib_type,
        'Has Mypy Post-Processing': is_hybrid
    })

# Add google-cloud-spanner-dbapi-driver manually as it's not in librarian.yaml but in packages/
summary.append({
    'Package Name': 'google-cloud-spanner-dbapi-driver',
    'APIs Populated': False,
    'Detected Type': 'Handwritten',
    'Has Mypy Post-Processing': False
})

# Write to CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    fieldnames = ['Package Name', 'APIs Populated', 'Detected Type', 'Has Mypy Post-Processing']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in summary:
        writer.writerow(row)

print(f"Analysis saved to {OUTPUT_CSV}")
