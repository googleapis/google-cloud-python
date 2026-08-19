# bigframes.bigquery inputs and outputs policies

The goal of the [bigframes.bigquery
APIs](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.html#module-bigframes.bigquery)
is to provide the simplest possible mapping from BigQuery (GoogleSQL)
[functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-all)
and
[operations](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
to Python. "Simplest" is somewhat ambiguous though, when it comes to the types
involved and behaviors, so this document aims to expand on that vision with
specific examples.

## SQL and BigFrames expression types

<table>
  <tr>
   <td style="background-color: #c9daf8"><strong>SQL expression type(s)</strong>
   </td>
   <td style="background-color: #c9daf8"><strong>Python type(s)</strong>
   </td>
   <td style="background-color: #c9daf8"><strong>Notes</strong>
   </td>
   <td style="background-color: #c9daf8"><strong>Examples</strong>
   </td>
  </tr>
  <tr>
   <td>Column expression (usable in a SELECT clause)
   </td>
   <td><ul>

<li><a href="https://dataframes.bigquery.dev/reference/api/bigframes.pandas.Series.html#bigframes.pandas.Series">bpd.Series</a>
<li><a href="https://github.com/googleapis/google-cloud-python/blob/bdd1cc5e336ec329d994aef28ed1070f1d771b74/packages/bigframes/bigframes/core/col.py#L35">bigframes deferred expression</a></li></ul>

   </td>
   <td>Both Python Series and column expression should be supported as inputs,
   with the output reflecting the users input. Use a <a
   href="https://docs.python.org/3/library/typing.html#typing.TypeVar">TypeVar</a>
   rather than directly using union types to make type checking easier.
<p>
<strong>Special considerations for Series inputs:</strong>
<p>
If an input and output are both a Series with the same number of rows, make sure
the output Series is implicitly (row identity) alignable with the original
input. In other words, don't generate a table expression.
<p>
If there are multiple Series inputs, they should be implicitly aligned if
possible so as not to generate unnecessary table expressions.
   </td>
   <td>Most scalar <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-all">functions </a>accept one or more column expressions as input.
   </td>
  </tr>
  <tr>
   <td>Scalar values
   </td>
   <td><ul>

<li><a href="https://github.com/googleapis/google-cloud-python/blob/bdd1cc5e336ec329d994aef28ed1070f1d771b74/packages/bigframes/bigframes/core/col.py#L35">bigframes deferred expression</a></li></ul>

   </td>
   <td>Theoretically, we could try to get the type system to help the user
   disambiguate between this case and the "Column expression" case, but I think
   that's more trouble than it it's worth with regards to the expectations of
   Python users.
   </td>
   <td><ul>

<li>Options for models that support <a href="https://docs.cloud.google.com/bigquery/docs/hp-tuning-overview">hyperparameter tuning</a> in CREATE MODEL.</li></ul>

   </td>
  </tr>
  <tr>
   <td>Table expression
   </td>
   <td><a href="https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.html#bigframes.pandas.DataFrame">bpd.DataFrame</a>
<p>
All columns are included as normal columns in the input table expression,
including named index columns. If column names aren't unique or contain
characters not compatible with BigQuery flexible column names, raise an error.
<p>
Outputs are unordered and unindexed to allow for cleaner mapping with SQL.
   </td>
   <td>Most APIs that take a table expression as input, also output a table
   expression with the same number of rows and passing through all unused
   columns.

   <p>This should be used to pass through any index or ordering columns (as well
   as all other columns, if that's the SQL behavior), to allow for easy joining
   with the original input DataFrame.
   </td>
   <td>Same number of rows as the input, so we should preserve index and ordering:

   <ul>
   <li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=en">ML.PREDICT</a>
   </li></ul>

   <p>
   Different number of rows in output, so no need to preserve index or ordering.
   Default index / ordering should be specified with the Session's
   configuration:

   <ul>
   <li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=en">CREATE MODEL</a>
   <li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#search">SEARCH</a>
   <li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search">VECTOR_SEARCH</a>
   </li></ul>

   <p>
   Possible to have the same number of rows as the input, but joining with the original goes against the purpose of the feature:

   <ul>
   <li><a href="https://docs.cloud.google.com/bigquery/docs/differential-privacy#dp_define_privacy_unit_id">WITH DIFFERENTIAL_PRIVACY</a></li></ul>

   </td>
  </tr>
  <tr>
   <td>Table name
   </td>
   <td>string (referring to fully-qualified table ID, e.g. project.dataset.table / project.catalog.namespace.table)
   </td>
   <td>Some SQL APIs do not support or have limitations with arbitrary table expressions, instead taking in a table ID, such as <a href="https://docs.cloud.google.com/bigquery/docs/table-sampling">TABLESAMPLE</a> expression.
<p>
Also, <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#search">SEARCH</a> and <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search">VECTOR_SEARCH</a>, if you want the indexes attached to the table to actually apply.
<p>
For outputs, it might be preferable to output a table ID instead of a DataFrame, if the user is explicitly creating a table. For example, to_gbq() returns a string with the table name, which is useful for the case where BigFrame generates the table ID for the user.
   </td>
   <td>All of the items from the "Table expression" row above. APIs that require a table expression, but don't take a table ID can trivially take a table ID through a (SELECT * FROM table) subquery.
<p>
Some APIs only take a table ID and not an arbitrary table expression:<ul>

<li><a href="https://docs.cloud.google.com/bigquery/docs/table-sampling">TABLESAMPLE</a></li></ul>

   </td>
  </tr>
  <tr>
   <td>Aggregated table expression
   </td>
   <td>DataFrameGroupBy
   </td>
   <td>
   </td>
   <td><ul>

<li><a href="https://docs.cloud.google.com/bigquery/docs/analysis-rules">WITH AGGREGATION_THRESHOLD</a>
<li><a href="https://docs.cloud.google.com/bigquery/docs/differential-privacy#dp_define_privacy_unit_id">WITH DIFFERENTIAL_PRIVACY</a>
<li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#having_clause">HAVING</a> clause</li></ul>

   </td>
  </tr>
  <tr>
   <td>Analytic table expression
   </td>
   <td><ul>

<li>DataFrameGroupBy - feasibility TBD
<li>Deferred column Expression with a Window applied.</li></ul>

   </td>
   <td>
   </td>
   <td><ul>

<li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#qualify_clause">QUALIFY</a> clause</li></ul>

   </td>
  </tr>
  <tr>
   <td>Column name (unqualified*) \
 \
<em>*I've only encountered examples where the table name / table expression is passed in separately.</em>
   </td>
   <td>string,
<p>
For cases where the column name is used as an alias and we aren't using named Series:
<p>
dict[str, Expression]
   </td>
   <td>Often a table expression input is paired with a column name input, as is the case with the <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=en">CREATE MODEL</a> and <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search">VECTOR_SEARCH</a> APIs
<p>
If SQL expects a column name rather than a column expression, do not attempt to change this in Python. For example, don't allow a Series as a substitute for DataFrames + Column name. \
 \
If the associated table expression is input as a DataFrame, validate that these map cleanly to SQL and raise a ValueError if not. For example: \
<ul>

<li>Duplicate column names (excluding unnamed index columns).
<li>Column names that are some hashable value other than integer (which maps cleanly to a column name) or string.
<li>Any column name containing a punctuation mark that is not allowed by <a href="https://docs.cloud.google.com/bigquery/docs/schemas#flexible-column-names">BigQuery flexible column names</a>, such as ! or $.</li></ul>

   </td>
   <td><ul>

<li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=en">CREATE MODEL</a>
<li><a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search">VECTOR_SEARCH</a></li></ul>

   </td>
  </tr>
  <tr>
   <td>Literal values
   </td>
   <td>corresponding literal Python value (e.g. int, float, string)
   </td>
   <td>For cases where scalar values are also supported, it should be safe to start with this and then expand to support expressions without a breaking change, as is done in <a href="https://github.com/googleapis/google-cloud-python/pull/16606">https://github.com/googleapis/google-cloud-python/pull/16606</a>.
   </td>
   <td>Most scalar <a href="https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-all">functions </a>accept one or more literal values as input.
   </td>
  </tr>
  <tr>
   <td>Scalar subqueries
   </td>
   <td>Not supported yet, except implicitly in some aggregation use cases.
<p>
Would need some sort of bigframes deferred expression that can be tied to a table expression.
<p>
(Possibly DataFrame with 1 column?)
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>

## Python policies

### Naming

Take the SQL function name, keyword name (used as a function name in Python), or argument name and transform them to lower_snake_case to reflect Python conventions.

### Internal expressions

Prefer creating deferred BigFrames expression objects where feasible. For
example, all scalar outputting functions should return a
`bigframes.pandas.Series` or `bigframes.core.col.Expression` that wraps a
`bigframes.core.expression.Expression`.

Prefer returning a `bigframes.pandas.DataFrame` that wraps a
`bigframes.bigframes.core.bigframe_node.BigFrameNode`. See `from_bq_data_source` in
`bigframes.core.array_value.ArrayValue`, as an example.

Exceptions to this are cases where the output schema is likely to evolve or
differ in ways that are difficult to model, such as the `ML.PREDICT` SQL
function, where output columns differ based on the model type and support for
model types are frequently added to BigQuery. In these exceptional cases, the
generated query should run immediately and the returned value should wrap the
results.

### Argument syntax details

Arguments in Python can be one of:

* Positional
  * Supported by `*args` in Python, but not recommended. Positional arguments in SQL should map to named positional or keyword arguments in Python.
* Positional or keyword
  * Required positional arguments should be positional, just like they are in SQL.
* Keyword-only
  * All other arguments should be keyword-only. Use `, * ,` Python syntax to achieve this.

For optional parameters, use an optional sentinel (see: <https://stackoverflow.com/a/76606310/101923>) and omit the value from the generated SQL if the user doesn't explicitly provide one. This ensures that an explicit NULL / None value can be passed in.

```

from enum import Enum

class Default(Enum):
    token = 0

DEFAULT = Default.token

def spam(*, ham: list[str] | None | Default = DEFAULT):
    op_kwargs = {}

    if ham is not DEFAULT:
        op_kwargs['ham'] = "prosciutto"

    ...

```

### Scalar operations types policies

Many operations output a table expression. For these, the output type is always a DataFrame, regardless of the input types.

For scalar operations, there are three cases to consider when determining the output types:

<table>
  <tr>
   <td><strong>Scalar ops - Input type(s)</strong>
   </td>
   <td><strong>Scalar ops - Output type</strong>
   </td>
  </tr>
  <tr>
   <td>Expression
   </td>
   <td>Expression
   </td>
  </tr>
  <tr>
   <td>Series / DataFrame
   </td>
   <td>Series / DataFrame
<p>
Preserve ordering and index(es). Join inputs as needed before applying the operation.
   </td>
  </tr>
  <tr>
   <td>Mix of Expression and Series / DataFrame
   </td>
   <td>Series / DataFrame
<p>
Preserve ordering and index(es). Join inputs as needed before applying the operation.
   </td>
  </tr>
</table>

## Examples

### PIVOT SQL operator

SQL syntax ([docs](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#pivot_operator)):

```
FROM from_item[, ...] pivot_operator

pivot_operator:
  PIVOT(
    aggregate_function_call [as_alias][, ...]
    FOR input_column
    IN ( pivot_column [as_alias][, ...] )
  ) [AS alias]

as_alias:
  [AS] alias

```

SQL example:

```
WITH Produce AS (
  SELECT 'Kale' as product, 51 as sales, 'Q1' as quarter, 2020 as year UNION ALL
  SELECT 'Kale', 23, 'Q2', 2020 UNION ALL
  SELECT 'Kale', 45, 'Q3', 2020 UNION ALL
  SELECT 'Kale', 3, 'Q4', 2020 UNION ALL
  SELECT 'Kale', 70, 'Q1', 2021 UNION ALL
  SELECT 'Kale', 85, 'Q2', 2021 UNION ALL
  SELECT 'Apple', 77, 'Q1', 2020 UNION ALL
  SELECT 'Apple', 0, 'Q2', 2020 UNION ALL
  SELECT 'Apple', 1, 'Q1', 2021)
SELECT * FROM Produce

/*---------+-------+---------+------+
 | product | sales | quarter | year |
 +---------+-------+---------+------|
 | Kale    | 51    | Q1      | 2020 |
 | Kale    | 23    | Q2      | 2020 |
 | Kale    | 45    | Q3      | 2020 |
 | Kale    | 3     | Q4      | 2020 |
 | Kale    | 70    | Q1      | 2021 |
 | Kale    | 85    | Q2      | 2021 |
 | Apple   | 77    | Q1      | 2020 |
 | Apple   | 0     | Q2      | 2020 |
 | Apple   | 1     | Q1      | 2021 |
 +---------+-------+---------+------*/


SELECT * FROM
  Produce
  PIVOT(SUM(sales) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'))

/*---------+------+----+------+------+------+
 | product | year | Q1 | Q2   | Q3   | Q4   |
 +---------+------+----+------+------+------+
 | Apple   | 2020 | 77 | 0    | NULL | NULL |
 | Apple   | 2021 | 1  | NULL | NULL | NULL |
 | Kale    | 2020 | 51 | 23   | 45   | 3    |
 | Kale    | 2021 | 70 | 85   | NULL | NULL |
 +---------+------+----+------+------+------*/

```

Python definition:

```
def pivot(
    table_expression: bpd.DataFrame,
    *,
    aggregation: Expression | dict[str, Expression],
    input_column: str,
    pivot_columns: dict[str, float | str | ...] | Sequence[float | str | ...],
) -> bpd.DataFrame:
    ...
```

Since pivot creates a table expression, we run immediately.

 \
Python usage:

```
pivotted = bbq.pivot(
    my_produce_dataframe,
    aggregation=bpd.col("sales").sum(),
    input_column="quarter",
    pivot_columns=["Q1", "Q2", "Q3", "Q4"],
)
```

### UNPIVOT SQL operator

SQL syntax ([docs](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#unpivot_operator)):

```
FROM from_item[, ...] unpivot_operator

unpivot_operator:
  UNPIVOT [ { INCLUDE NULLS | EXCLUDE NULLS } ] (
    { single_column_unpivot | multi_column_unpivot }
  ) [unpivot_alias]

single_column_unpivot:
  values_column
  FOR name_column
  IN (columns_to_unpivot)

multi_column_unpivot:
  values_column_set
  FOR name_column
  IN (column_sets_to_unpivot)

values_column_set:
  (values_column[, ...])

columns_to_unpivot:
  unpivot_column [row_value_alias][, ...]

column_sets_to_unpivot:
  (unpivot_column [row_value_alias][, ...])

unpivot_alias and row_value_alias:
  [AS] alias
```

SQL example:

```
WITH Produce AS (
  SELECT 'Kale' as product, 51 as Q1, 23 as Q2, 45 as Q3, 3 as Q4 UNION ALL
  SELECT 'Apple', 77, 0, 25, 2)

-- SELECT * FROM Produce
/*---------+----+----+----+----+
 | product | Q1 | Q2 | Q3 | Q4 |
 +---------+----+----+----+----+
 | Kale    | 51 | 23 | 45 | 3  |
 | Apple   | 77 | 0  | 25 | 2  |
 +---------+----+----+----+----*/

SELECT * FROM Produce
UNPIVOT(sales FOR quarter IN (Q1, Q2, Q3, Q4))  -- single_column_unpivot

/*---------+-------+---------+
 | product | sales | quarter |
 +---------+-------+---------+
 | Kale    | 51    | Q1      |
 | Kale    | 23    | Q2      |
 | Kale    | 45    | Q3      |
 | Kale    | 3     | Q4      |
 | Apple   | 77    | Q1      |
 | Apple   | 0     | Q2      |
 | Apple   | 25    | Q3      |
 | Apple   | 2     | Q4      |
 +---------+-------+---------*/
```

Python definition:

```
def unpivot(
    table_expression: bpd.DataFrame,
    *,
    exclude_nulls: bool = True,
    values_column: str | Sequence[str],
    name_column: str,
    columns_to_unpivot: dict[str, str | int] | Sequence[str],
) -> bpd.DataFrame:
    ...
```

Since unpivot creates a table expression, we run immediately.

 \
Python usage:

```
unpivotted = bbq.unpivot(
    my_produce_dataframe,
    values_column="sales",
    name_column="quarter",
    columns_to_unpivot=["Q1", "Q2", "Q3", "Q4"],
)
```
