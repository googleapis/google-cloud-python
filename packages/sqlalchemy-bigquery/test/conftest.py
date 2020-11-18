from sqlalchemy.dialects import registry

registry.register("bigquery", "pybigquery.sqlalchemy_bigquery", "BigQueryDialect")
