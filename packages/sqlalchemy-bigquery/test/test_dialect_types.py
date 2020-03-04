import importlib


# https://docs.sqlalchemy.org/en/13/core/type_basics.html#vendor-specific-types
def test_types_import():
    """Demonstrate behavior of importing types independent of any other import."""
    dialect_module = importlib.import_module("pybigquery.sqlalchemy_bigquery")
    custom_types = getattr(dialect_module, "_type_map")
    for type_name, type_value in custom_types.items():
        assert getattr(dialect_module, type_name) == type_value
