# Anywidget: align text left and numerics right

The "anywidget" rendering mode outputs an HTML table per page right now, but
the values need to be aligned according to their data type.

## Background

Anywidget currently renders pages like the following:

```html
<table border="1" class="dataframe table table-striped table-hover" id="table-346a8ee1-7f4e-4820-80bf-9a9921e448ad">
  <thead>
    <tr style="text-align: right;">
      <th>state</th>
      <th>gender</th>
      <th>year</th>
      <th>name</th>
      <th>number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>VA</td>
      <td>M</td>
      <td>1930</td>
      <td>Pat</td>
      <td>6</td>
    </tr>
    <!-- ... -->
    <tr>
      <td>TX</td>
      <td>M</td>
      <td>1968</td>
      <td>Kennith</td>
      <td>18</td>
    </tr>
  </tbody>
</table>
```

* This change fixes internal issue b/437697339.
* Numeric data should be right aligned so that it is easier to compare numbers,
  especially if they all are rounded to the same precision.
* Text data is better left aligned, since many languages read left to right.

## Acceptance Criteria

- [ ] Header cells should align left.
- [ ] Header cells should use the resize CSS property to allow resizing.
- [ ] STRING columns are left-aligned in the output of `TableWidget` in
     `bigframes/display/anywidget.py`.
- [ ] Numeric columns (INT64, FLOAT64, NUMERIC, BIGNUMERIC) are right-aligned
      in the output of `TableWidget` in `bigframes/display/anywidget.py`.
- [ ] Create option `DisplayOptions.precision` in
      `bigframes/_config/display_options.py` that can override the output
      precision (defaults to 6, just like `pandas.options.display.precision`).
- [ ] All other non-numeric column types, including BYTES, BOOLEAN, TIMESTAMP,
      and more, are left-aligned in the output of `TableWidget` in
      `bigframes/display/anywidget.py`.
- [ ] There are parameterized unit tests verifying the alignment is set
      correctly.

## Detailed Steps

### 1. Create Display Precision Configuration

- [ ] In `bigframes/_config/display_options.py`, add a new `precision` attribute to the `DisplayOptions` dataclass.
- [ ] Set the default value to `6`.
- [ ] Add precision to the items in `def pandas_repr` that get passed to the pandas options context.
- [ ] Add a docstring explaining that it controls the floating point output precision, similar to `pandas.options.display.precision`.
- [ ] Check these items off with `[x]` as they are completed.

### 2. Improve the headers

- [ ] Create `bigframes/display/html.py`.
- [ ] In `bigframes/display/html.py`, create a `def render_html(*, dataframe: pandas.DataFrame, table_id: str)` method.
- [ ] Loop through the column names to create the table head.
- [ ] Apply the `text-align: left` style to the header.
- [ ] Wrap the cell text in a resizable `div`.
- [ ] Check these items off with `[x]` as they are completed.

### 3. Implement Alignment and Precision Logic in TableWidget

- [ ] Create a helper function `_is_dtype_numeric(dtype)` that takes a pandas
      dtype returns True for types that that should be right-aligned. These
      dtypes should correspond to the BigQuery data types: `INT64`, `FLOAT64`,
      `NUMERIC`, `BIGNUMERIC`. Use the `bigframes.dtypes` module to map from
      pandas type to BigQuery type.
- [ ] In the loop that generates the table rows (`<td>` elements), add a function to determine the style based on the column's `dtype`.
- [ ] If the column's `dtype` is in the numeric set, apply the CSS style `text-align: right`.
- [ ] For all other `dtypes` (including `STRING`, `BYTES`, `BOOLEAN`, `TIMESTAMP`, etc.), apply `text-align: left`.
- [ ] When formatting floating-point numbers for display, use the `bigframes.options.display.precision` value.
- [ ] In `bigframes/display/anywidget.py`, modify the `_set_table_html` method of the `TableWidget` class to call `bigframes.display.html.render_html(...)`.
- [ ] Render the notebook at `notebooks/dataframes/anywidget_mode.ipynb` with
      the `jupyter nbconvert --to notebook --execute notebooks/dataframes/anywidget_mode.ipynb`
      command and validate that the rendered notebook includes the desired
      changes to the HTML tables.
- [ ] Check these items off with `[x]` as they are completed.

### 4. Add Parameterized Unit Tests

- [ ] Create a new test file: `tests/unit/display/test_html.py`.
- [ ] Create a parameterized test method, e.g., `test_render_html_alignment_and_precision`.
- [ ] Use `@pytest.mark.parametrize` to test various scenarios.
- [ ] **Scenario 1: Alignment.**
    - Create a sample `bigframes.dataframe.DataFrame` with columns of different types: a string, an integer, a float, and a boolean.
    - Render the `pandas.DataFrame` to HTML.
    - Assert that the integer and float column headers and data cells (`<th>` and `<td>`) have `style="text-align: right;"`.
    - Assert that the string and boolean columns have `style="text-align: left;"`.
- [ ] **Scenario 2: Precision.**
    - Create a `bigframes.dataframe.DataFrame` with a `FLOAT64` column containing a number with many decimal places (e.g., `3.14159265`).
    - Set `bigframes.options.display.precision = 4`.
    - Render the `pandas.DataFrame` to HTML.
    - Assert that the output string contains the number formatted to 4 decimal places (e.g., `3.1416`).
    - Remember to reset the option value after the test to avoid side effects.
- [ ] Check these items off with `[x]` as they are completed.

## Verification

*Specify the commands to run to verify the changes.*

- [ ] The `nox -r -s format lint lint_setup_py` linter should pass.
- [ ] The `nox -r -s mypy` static type checker should pass.
- [ ] The `nox -r -s docs docfx` docs should successfully build and include relevant docs in the output.
- [ ] All new and existing unit tests `pytest tests/unit` should pass.
- [ ] Identify all related system tests in the `tests/system` directories.
- [ ] All related system tests `pytest tests/system/small/path_to_relevant_test.py::test_name` should pass.
- [ ] Check these items off with `[x]` as they are completed.

## Constraints

Follow the guidelines listed in GEMINI.md at the root of the repository.
