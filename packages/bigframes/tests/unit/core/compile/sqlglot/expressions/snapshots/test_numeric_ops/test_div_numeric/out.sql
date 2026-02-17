SELECT
  `rowindex`,
  `int64_col`,
  `bool_col`,
  `float64_col`,
  IEEE_DIVIDE(`int64_col`, `int64_col`) AS `int_div_int`,
  IEEE_DIVIDE(`int64_col`, 1) AS `int_div_1`,
  IEEE_DIVIDE(`int64_col`, 0.0) AS `int_div_0`,
  IEEE_DIVIDE(`int64_col`, `float64_col`) AS `int_div_float`,
  IEEE_DIVIDE(`float64_col`, `int64_col`) AS `float_div_int`,
  IEEE_DIVIDE(`float64_col`, 0.0) AS `float_div_0`,
  IEEE_DIVIDE(`int64_col`, CAST(`bool_col` AS INT64)) AS `int_div_bool`,
  IEEE_DIVIDE(CAST(`bool_col` AS INT64), `int64_col`) AS `bool_div_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`