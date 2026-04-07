## Testing code samples

Code samples are very important for accurate documentation. We use the "doctest"
framework to ensure the samples are functioning as expected. After adding a code
sample, please ensure it is correct by running doctest. To run the samples
doctests for just a single method, refer to the following example:

```bash
pytest --doctest-modules bigframes/pandas/__init__.py::bigframes.pandas.cut
```
