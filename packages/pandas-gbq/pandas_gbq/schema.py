"""Helper methods for BigQuery schemas"""


def generate_bq_schema(dataframe, default_type="STRING"):
    """Given a passed dataframe, generate the associated Google BigQuery schema.

    Arguments:
        dataframe (pandas.DataFrame): D
    default_type : string
        The default big query type in case the type of the column
        does not exist in the schema.
    """

    # If you update this mapping, also update the table at
    # `docs/source/writing.rst`.
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


def update_schema(schema_old, schema_new):
    """
    Given an old BigQuery schema, update it with a new one.

    Where a field name is the same, the new will replace the old. Any
    new fields not present in the old schema will be added.

    Arguments:
        schema_old: the old schema to update
        schema_new: the new schema which will overwrite/extend the old
    """
    old_fields = schema_old["fields"]
    new_fields = schema_new["fields"]
    output_fields = list(old_fields)

    field_indices = {field["name"]: i for i, field in enumerate(output_fields)}

    for field in new_fields:
        name = field["name"]
        if name in field_indices:
            # replace old field with new field of same name
            output_fields[field_indices[name]] = field
        else:
            # add new field
            output_fields.append(field)

    return {"fields": output_fields}
