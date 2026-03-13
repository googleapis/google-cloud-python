SELECT
  `rowindex`,
  `int64_col`,
  `bool_col`,
  `int64_col` * `int64_col` AS `int_mul_int`,
  `int64_col` * 1 AS `int_mul_1`,
  `int64_col` * CAST(`bool_col` AS INT64) AS `int_mul_bool`,
  CAST(`bool_col` AS INT64) * `int64_col` AS `bool_mul_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`