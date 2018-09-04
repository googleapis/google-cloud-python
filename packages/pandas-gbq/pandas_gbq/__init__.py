from .gbq import to_gbq, read_gbq, Context, context  # noqa

from ._version import get_versions

versions = get_versions()
__version__ = versions.get("closest-tag", versions["version"])
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
