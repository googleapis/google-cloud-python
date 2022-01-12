try:
    import pkg_resources

    pkg_resources.declare_namespace(__name__)
except ImportError:
    pass
