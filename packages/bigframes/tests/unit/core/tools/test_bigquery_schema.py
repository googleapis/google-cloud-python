from google.cloud import bigquery
import pytest

from bigframes.core.tools import bigquery_schema


# --- Tests for _type_to_sql ---
@pytest.mark.parametrize(
    "field, expected_sql",
    [
        # Simple types
        # Note: the REST API will return Legacy SQL data types, but we need to
        # map to GoogleSQL. See internal issue b/428190014.
        (bigquery.SchemaField("test_field", "INTEGER"), "INT64"),
        (bigquery.SchemaField("test_field", "STRING"), "STRING"),
        (bigquery.SchemaField("test_field", "BOOLEAN"), "BOOL"),
        # RECORD/STRUCT types with nested fields directly
        (
            bigquery.SchemaField(
                "test_field",
                "RECORD",
                fields=(bigquery.SchemaField("sub_field", "STRING"),),
            ),
            "STRUCT<`sub_field` STRING>",
        ),
        (
            bigquery.SchemaField(
                "test_field",
                "STRUCT",
                fields=(
                    bigquery.SchemaField("sub_field", "INTEGER"),
                    bigquery.SchemaField("another", "BOOLEAN"),
                ),
            ),
            "STRUCT<`sub_field` INT64, `another` BOOL>",
        ),
        # Array is handled by _field_to_sql, instead.
        (bigquery.SchemaField("test_field", "NUMERIC", mode="REPEATED"), "NUMERIC"),
        (
            bigquery.SchemaField(
                "test_field",
                "RECORD",
                mode="REPEATED",
                fields=(bigquery.SchemaField("sub_field", "STRING"),),
            ),
            "STRUCT<`sub_field` STRING>",
        ),
    ],
)
def test_type_to_sql(field, expected_sql):
    assert bigquery_schema._type_to_sql(field) == expected_sql


# --- Tests for _field_to_sql ---
@pytest.mark.parametrize(
    "field, expected_sql",
    [
        # Simple field
        # Note: the REST API will return Legacy SQL data types, but we need to
        # map to GoogleSQL. See internal issue b/428190014.
        (bigquery.SchemaField("id", "INTEGER", "NULLABLE"), "`id` INT64"),
        (bigquery.SchemaField("name", "STRING", "NULLABLE"), "`name` STRING"),
        # Repeated field
        (bigquery.SchemaField("tags", "STRING", "REPEATED"), "`tags` ARRAY<STRING>"),
        # Repeated RECORD
        (
            bigquery.SchemaField(
                "addresses",
                "RECORD",
                "REPEATED",
                fields=(
                    bigquery.SchemaField("street", "STRING"),
                    bigquery.SchemaField("zip", "INTEGER"),
                ),
            ),
            "`addresses` ARRAY<STRUCT<`street` STRING, `zip` INT64>>",
        ),
        # Simple STRUCT
        (
            bigquery.SchemaField(
                "person",
                "STRUCT",
                "NULLABLE",
                fields=(
                    bigquery.SchemaField("age", "INTEGER"),
                    bigquery.SchemaField("city", "STRING"),
                ),
            ),
            "`person` STRUCT<`age` INT64, `city` STRING>",
        ),
    ],
)
def test_field_to_sql(field, expected_sql):
    assert bigquery_schema._field_to_sql(field) == expected_sql


# --- Tests for _to_struct ---
@pytest.mark.parametrize(
    "bqschema, expected_sql",
    [
        # Empty schema
        ((), "STRUCT<>"),
        # Simple fields
        (
            (
                bigquery.SchemaField("id", "INTEGER"),
                bigquery.SchemaField("name", "STRING"),
            ),
            "STRUCT<`id` INT64, `name` STRING>",
        ),
        # Nested RECORD/STRUCT
        (
            (
                bigquery.SchemaField("item_id", "INTEGER"),
                bigquery.SchemaField(
                    "details",
                    "RECORD",
                    "NULLABLE",
                    fields=(
                        bigquery.SchemaField("price", "NUMERIC"),
                        bigquery.SchemaField("currency", "STRING"),
                    ),
                ),
            ),
            "STRUCT<`item_id` INT64, `details` STRUCT<`price` NUMERIC, `currency` STRING>>",
        ),
        # Repeated field
        (
            (
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("emails", "STRING", "REPEATED"),
            ),
            "STRUCT<`user_id` STRING, `emails` ARRAY<STRING>>",
        ),
        # Mixed types including complex nested repeated
        (
            (
                bigquery.SchemaField("event_name", "STRING"),
                bigquery.SchemaField(
                    "participants",
                    "RECORD",
                    "REPEATED",
                    fields=(
                        bigquery.SchemaField("p_id", "INTEGER"),
                        bigquery.SchemaField("roles", "STRING", "REPEATED"),
                    ),
                ),
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
            ),
            "STRUCT<`event_name` STRING, `participants` ARRAY<STRUCT<`p_id` INT64, `roles` ARRAY<STRING>>>, `timestamp` TIMESTAMP>",
        ),
    ],
)
def test_to_struct(bqschema, expected_sql):
    assert bigquery_schema._to_struct(bqschema) == expected_sql


# --- Tests for to_sql_dry_run ---
@pytest.mark.parametrize(
    "bqschema, expected_sql",
    [
        # Empty schema
        ((), "UNNEST(ARRAY<STRUCT<>>[])"),
        # Simple schema
        (
            (
                bigquery.SchemaField("id", "INTEGER"),
                bigquery.SchemaField("name", "STRING"),
            ),
            "UNNEST(ARRAY<STRUCT<`id` INT64, `name` STRING>>[])",
        ),
        # Complex schema with nested and repeated fields
        (
            (
                bigquery.SchemaField("order_id", "STRING"),
                bigquery.SchemaField(
                    "items",
                    "RECORD",
                    "REPEATED",
                    fields=(
                        bigquery.SchemaField("item_name", "STRING"),
                        bigquery.SchemaField("quantity", "INTEGER"),
                    ),
                ),
            ),
            "UNNEST(ARRAY<STRUCT<`order_id` STRING, `items` ARRAY<STRUCT<`item_name` STRING, `quantity` INT64>>>>[])",
        ),
    ],
)
def test_to_sql_dry_run(bqschema, expected_sql):
    assert bigquery_schema.to_sql_dry_run(bqschema) == expected_sql
