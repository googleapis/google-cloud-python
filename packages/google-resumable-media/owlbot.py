import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated .kokoro files
# ----------------------------------------------------------------------------
templated_files = common.py_library()
s.move(templated_files / ".kokoro")
s.move(templated_files / ".trampolinerc")
s.move(templated_files / ".github")
s.move(templated_files / "renovate.json")
s.move(templated_files / "docs", excludes=[
  "multiprocessing.rst", 
  "conf.py"
])

# Block pushing non-cloud libraries to Cloud RAD
s.replace(
    ".kokoro/docs/common.cfg",
    r'value: "docs-staging-v2"',
    r'value: "docs-staging-v2-dev"'
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
