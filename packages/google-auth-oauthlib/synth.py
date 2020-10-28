import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=99,
    unit_test_external_dependencies=["click"],
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9"],
)
s.move(templated_files, excludes=["docs/multiprocessing.rst"])

# Change black paths
s.replace(
    "noxfile.py",
    """BLACK_PATHS =.*""",
    """BLACK_PATHS = ["docs", "google_auth_oauthlib", "tests", "noxfile.py", "setup.py"]""",
)
