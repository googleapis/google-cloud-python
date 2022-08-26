# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""This script is used to synthesize generated parts of this library."""
import re

import synthtool as s
import synthtool.gcp as gcp

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(microgenerator=True)

# Just move templates for building docs and releases
# Presubmit and continuous are configured differently
s.move(templated_files / ".trampolinerc")
s.move(templated_files / "renovate.json")
s.move(templated_files / ".kokoro" / "docker")
s.move(templated_files / ".kokoro" / "docs")
s.move(templated_files / ".kokoro" / "release.sh")
s.move(templated_files / ".kokoro" / "trampoline_v2.sh")
s.move(templated_files / ".kokoro" / "trampoline.sh")
s.move(templated_files / ".kokoro" / "populate-secrets.sh")
s.move(templated_files / ".kokoro" / "release")
s.move(templated_files / ".kokoro" / "requirements.in")
s.move(templated_files / ".kokoro" / "requirements.txt")
s.move(templated_files / ".kokoro" / "publish-docs.sh")

# Replace the Apache Licenses in the `.kokoro` directory
# with the BSD license expected in this repository
s.replace(
    ".kokoro/**/*",
    "# Copyright.*(\d{4}).*# limitations under the License\.",
    """# Copyright \g<1> Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd""",
    flags=re.DOTALL
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
