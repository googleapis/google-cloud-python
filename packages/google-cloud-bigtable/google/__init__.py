from typing import List

try:
    import pkg_resources

    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil

    __path__: List[str] = pkgutil.extend_path(__path__, __name__)
