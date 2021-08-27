import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated .kokoro files
# ----------------------------------------------------------------------------
templated_files = common.py_library()
s.move(templated_files / ".kokoro")
s.move(templated_files / ".trampolinerc")
s.move(templated_files / "docs", excludes=[
  "multiprocessing.rst", 
  "conf.py"
])

# Block pushing non-cloud libraries to Cloud RAD
s.replace(
    ".kokoro/docs/common.cfg",
    r'value: "docs-staging-v2"',
    r'value: "docs-staging-v2-staging"'
)


# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

s.replace(
    "docs/conf.py",
    "master_doc",
    "root_doc",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
