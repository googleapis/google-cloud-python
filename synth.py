import json
import os
from pathlib import Path

import synthtool as s 

repo_path = "/usr/local/google/home/busunkim/github/google-cloud-python"

api_dirs = [
    Path(repo_path) / p for p in os.listdir(repo_path) if os.path.exists(Path(repo_path) / p / "README.rst")
]

print(api_dirs[0])
for d in api_dirs:
	with open(d / ".repo-metadata.json") as f:
		metadata = json.load(f)
		documentation = metadata['client_documentation']
	s.replace(d / "*.rst", "(_Setup Authentication\.:) https://.*\.github\.io/google-cloud-python/.*/core/auth.html", f"\g<1> https://googleapis.dev/python/google-api-core/latest/auth.html")
	s.replace(d / "docs/*.rst", "(.*) https://.*\.github\.io/google-cloud-python/latest/.*/.*\.html", f"\g<1> {documentation}")