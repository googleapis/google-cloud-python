import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated .kokoro files
# ----------------------------------------------------------------------------
templated_files = common.py_library()
s.move(templated_files / ".kokoro")
s.move(templated_files / ".trampolinerc")
s.move(templated_files / "docs", excludes=["multiprocessing.rst", "conf.py"])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
