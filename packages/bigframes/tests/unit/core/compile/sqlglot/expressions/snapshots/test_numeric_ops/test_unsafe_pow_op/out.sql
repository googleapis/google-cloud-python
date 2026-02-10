SELECT
  POWER(`int64_col`, `int64_col`) AS `int_pow_int`,
  POWER(`int64_col`, `float64_col`) AS `int_pow_float`,
  POWER(`float64_col`, `int64_col`) AS `float_pow_int`,
  POWER(`float64_col`, `float64_col`) AS `float_pow_float`,
  POWER(`int64_col`, CAST(`bool_col` AS INT64)) AS `int_pow_bool`,
  POWER(CAST(`bool_col` AS INT64), `int64_col`) AS `bool_pow_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
WHERE
  (
    `int64_col` >= 0
  ) AND (
    `int64_col` <= 10
  )