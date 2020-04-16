from synthtool.sources import git
from pathlib import Path

from subprocess import run

import synthtool as s

url = git.make_repo_clone_url("googleapis/api-common-protos")

api_common_protos = git.clone(url)
s.copy(api_common_protos / "google", "google")