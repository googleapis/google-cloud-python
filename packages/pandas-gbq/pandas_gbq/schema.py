"""Helper methods for BigQuery schemas"""


def generate_bq_schema(dataframe, default_type="STRING"):
    """Given a passed dataframe, generate the associated Google BigQuery schema.

    Arguments:
        dataframe (pandas.DataFrame): D
    default_type : string
        The default big query type in case the type of the column
        does not exist in the schema.
    """

    type_mapping = {
        "i": "INTEGER",
        "b": "BOOLEAN",
        "f": "FLOAT",
        "O": "STRING",
        "S": "STRING",
        "U": "STRING",
        "M": "TIMESTAMP",
    }

    fields = []
    for column_name, dtype in dataframe.dtypes.iteritems():
        fields.append(
            {
                "name": column_name,
                "type": type_mapping.get(dtype.kind, default_type),
            }
        )

    return {"fields": fields}
