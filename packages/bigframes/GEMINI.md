# Contribution guidelines, tailored for LLM agents

## Testing

We use `nox` to instrument our tests.

- To test your changes, run unit tests with `nox`:

  ```bash
  nox -r -s unit
  ```

- To run a single unit test:

  ```bash
  nox -r -s unit-3.13 -- -k <name of test>
  ```

- To run system tests, you can execute::

   # Run all system tests
   $ nox -r -s system

   # Run a single system test
   $ nox -r -s system-3.13 -- -k <name of test>

- The codebase must have better coverage than it had previously after each
  change. You can test coverage via `nox -s unit system cover` (takes a long
  time).

## Code Style

- We use the automatic code formatter `black`. You can run it using
  the nox session `format`. This will eliminate many lint errors. Run via:

  ```bash
  nox -r -s format
  ```

- PEP8 compliance is required, with exceptions defined in the linter configuration.
  If you have ``nox`` installed, you can test that you have not introduced
  any non-compliant code via:

  ```
  nox -r -s lint
  ```

## Documentation

If a method or property is implementing the same interface as a third-party
package such as pandas or scikit-learn, place the relevant docstring in the
corresponding `third_party/bigframes_vendored/package_name` directory, not in
the `bigframes` directory. Implementations may be placed in the `bigframes`
directory, though.

### Testing code samples

Code samples are very important for accurate documentation. We use the "doctest"
framework to ensure the samples are functioning as expected. After adding a code
sample, please ensure it is correct by running doctest. To run the samples
doctests for just a single method, refer to the following example:

```bash
pytest --doctest-modules bigframes/pandas/__init__.py::bigframes.pandas.cut
```

## Tips for implementing common BigFrames features

### Adding a scalar operator

For an example, see commit
[c5b7fdae74a22e581f7705bc0cf5390e928f4425](https://github.com/googleapis/python-bigquery-dataframes/commit/c5b7fdae74a22e581f7705bc0cf5390e928f4425).

To add a new scalar operator, follow these steps:

1.  **Define the operation dataclass:**
    - In `bigframes/operations/`, find the relevant file (e.g., `geo_ops.py` for geography functions) or create a new one.
    - Create a new dataclass inheriting from `base_ops.UnaryOp` for unary
      operators, `base_ops.BinaryOp` for binary operators, `base_ops.TernaryOp`
      for ternary operators, or `base_ops.NaryOp for operators with many
      arguments. Note that these operators are counting the number column-like
      arguments. A function that takes only a single column but several literal
      values would still be a `UnaryOp`.
    - Define the `name` of the operation and any parameters it requires.
    - Implement the `output_type` method to specify the data type of the result.

2.  **Export the new operation:**
    - In `bigframes/operations/__init__.py`, import your new operation dataclass and add it to the `__all__` list.

3.  **Implement the user-facing function (pandas-like):**

    - Identify the canonical function from pandas / geopandas / awkward array /
      other popular Python package that this operator implements.
    - Find the corresponding class in BigFrames. For example, the implementation
      for most geopandas.GeoSeries methods is in
      `bigframes/geopandas/geoseries.py`. Pandas Series methods are implemented
      in `bigframes/series.py` or one of the accessors, such as `StringMethods`
      in `bigframes/operations/strings.py`.
    - Create the user-facing function that will be called by users (e.g., `length`).
    - If the SQL method differs from pandas or geopandas in a way that can't be
      made the same, raise a `NotImplementedError` with an appropriate message and
      link to the feedback form.
    - Add the docstring to the corresponding file in
      `third_party/bigframes_vendored`, modeled after pandas / geopandas.

4.  **Implement the user-facing function (SQL-like):**

    - In `bigframes/bigquery/_operations/`, find the relevant file (e.g., `geo.py`) or create a new one.
    - Create the user-facing function that will be called by users (e.g., `st_length`).
    - This function should take a `Series` for any column-like inputs, plus any other parameters.
    - Inside the function, call `series._apply_unary_op`,
      `series._apply_binary_op`, or similar passing the operation dataclass you
      created.
    - Add a comprehensive docstring with examples.
    - In `bigframes/bigquery/__init__.py`, import your new user-facing function and add it to the `__all__` list.

5.  **Implement the compilation logic:**
    - In `bigframes/core/compile/scalar_op_compiler.py`:
        - If the BigQuery function has a direct equivalent in Ibis, you can often reuse an existing Ibis method.
        - If not, define a new Ibis UDF using `@ibis_udf.scalar.builtin` to map to the specific BigQuery function signature.
        - Create a new compiler implementation function (e.g., `geo_length_op_impl`).
        - Register this function to your operation dataclass using `@scalar_op_compiler.register_unary_op` or `@scalar_op_compiler.register_binary_op`.
        - This implementation will translate the BigQuery DataFrames operation into the appropriate Ibis expression.

6.  **Add Tests:**
    - Add system tests in the `tests/system/` directory to verify the end-to-end
      functionality of the new operator. Test various inputs, including edge cases
      and `NULL` values.

      Where possible, run the same test code against pandas or GeoPandas and
      compare that the outputs are the same (except for dtypes if BigFrames
      differs from pandas).
    - If you are overriding a pandas or GeoPandas property, add a unit test to
      ensure the correct behavior (e.g., raising `NotImplementedError` if the
      functionality is not supported).


## Constraints

- Only add git commits. Do not change git history.
- Follow the spec file for development.
  - Check off items in the "Acceptance
    criteria" and "Detailed steps" sections with `[x]`.
  - Please do this as they are completed.
  - Refer back to the spec after each step.
