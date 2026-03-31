SELECT
  `rowindex`,
  `int64_col`,
  `bool_col`,
  `float64_col`,
  CASE
    WHEN `int64_col` = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`int64_col`, `int64_col`)) AS INT64)
  END AS `int_div_int`,
  CASE
    WHEN 1 = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`int64_col`, 1)) AS INT64)
  END AS `int_div_1`,
  CASE
    WHEN 0.0 = CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64) * `int64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`int64_col`, 0.0)) AS INT64)
  END AS `int_div_0`,
  NULL AS `int_div_null`,
  CASE
    WHEN `float64_col` = CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64) * `int64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`int64_col`, `float64_col`)) AS INT64)
  END AS `int_div_float`,
  CASE
    WHEN `int64_col` = CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64) * `float64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`float64_col`, `int64_col`)) AS INT64)
  END AS `float_div_int`,
  CASE
    WHEN 0.0 = CAST(0 AS INT64)
    THEN CAST('Infinity' AS FLOAT64) * `float64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`float64_col`, 0.0)) AS INT64)
  END AS `float_div_0`,
  NULL AS `float_div_null`,
  CASE
    WHEN CAST(`bool_col` AS INT64) = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * `int64_col`
    ELSE CAST(FLOOR(IEEE_DIVIDE(`int64_col`, CAST(`bool_col` AS INT64))) AS INT64)
  END AS `int_div_bool`,
  CASE
    WHEN `int64_col` = CAST(0 AS INT64)
    THEN CAST(0 AS INT64) * CAST(`bool_col` AS INT64)
    ELSE CAST(FLOOR(IEEE_DIVIDE(CAST(`bool_col` AS INT64), `int64_col`)) AS INT64)
  END AS `bool_div_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`