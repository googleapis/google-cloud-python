import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=100,
    cov_level=100,
    unit_test_external_dependencies=["flask", "pytest-localserver"],
)

paths = [".kokoro", ".github", ".flake8", "renovate.json", "docs"]
for p in paths:
    s.move(templated_files / p, excludes=["workflows", "multiprocessing.rst"])

