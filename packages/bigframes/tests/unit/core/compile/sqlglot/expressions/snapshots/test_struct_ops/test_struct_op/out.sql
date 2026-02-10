SELECT
  STRUCT(
    `bool_col` AS bool_col,
    `int64_col` AS int64_col,
    `float64_col` AS float64_col,
    `string_col` AS string_col
  ) AS `result_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`