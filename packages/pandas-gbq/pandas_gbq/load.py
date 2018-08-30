"""Helper methods for loading data into BigQuery"""

import six
from google.cloud import bigquery

import pandas_gbq.schema


def encode_chunk(dataframe):
    """Return a file-like object of CSV-encoded rows.

    Args:
      dataframe (pandas.DataFrame): A chunk of a dataframe to encode
    """
    csv_buffer = six.StringIO()
    dataframe.to_csv(
        csv_buffer,
        index=False,
        header=False,
        encoding="utf-8",
        float_format="%.15g",
        date_format="%Y-%m-%d %H:%M:%S.%f",
    )

    # Convert to a BytesIO buffer so that unicode text is properly handled.
    # See: https://github.com/pydata/pandas-gbq/issues/106
    body = csv_buffer.getvalue()
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    body = body.encode("utf-8")
    return six.BytesIO(body)


def encode_chunks(dataframe, chunksize=None):
    dataframe = dataframe.reset_index(drop=True)
    if chunksize is None:
        yield 0, encode_chunk(dataframe)
        return

    remaining_rows = len(dataframe)
    total_rows = remaining_rows
    start_index = 0
    while start_index < total_rows:
        end_index = start_index + chunksize
        chunk_buffer = encode_chunk(dataframe[start_index:end_index])
        start_index += chunksize
        remaining_rows = max(0, remaining_rows - chunksize)
        yield remaining_rows, chunk_buffer


def load_chunks(
    client,
    dataframe,
    dataset_id,
    table_id,
    chunksize=None,
    schema=None,
    location=None,
):
    destination_table = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = "WRITE_APPEND"
    job_config.source_format = "CSV"

    if schema is None:
        schema = pandas_gbq.schema.generate_bq_schema(dataframe)

    # Manually create the schema objects, adding NULLABLE mode
    # as a workaround for
    # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/4456
    for field in schema["fields"]:
        if "mode" not in field:
            field["mode"] = "NULLABLE"

    job_config.schema = [
        bigquery.SchemaField.from_api_repr(field) for field in schema["fields"]
    ]

    chunks = encode_chunks(dataframe, chunksize=chunksize)
    for remaining_rows, chunk_buffer in chunks:
        yield remaining_rows
        client.load_table_from_file(
            chunk_buffer,
            destination_table,
            job_config=job_config,
            location=location,
        ).result()
