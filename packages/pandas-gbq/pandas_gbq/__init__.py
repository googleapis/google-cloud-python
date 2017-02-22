from .gbq import to_gbq, read_gbq  # noqa

# use the closest tagged version if possible
from ._version import get_versions
v = get_versions()
__version__ = v.get('closest-tag', v['version'])
del get_versions, v
