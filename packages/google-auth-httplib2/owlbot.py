import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=100, cov_level=100)

paths = [".kokoro", ".github", ".flake8"]
for p in paths:
    s.move(templated_files / p)

# Remove the replacement below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")
