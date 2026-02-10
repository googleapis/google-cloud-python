SELECT
  CASE WHEN `bool_col` THEN `int64_col` END AS `single_case`,
  CASE WHEN `bool_col` THEN `int64_col` WHEN `bool_col` THEN `int64_too` END AS `double_case`,
  CASE WHEN `bool_col` THEN `bool_col` WHEN `bool_col` THEN `bool_col` END AS `bool_types_case`,
  CASE
    WHEN `bool_col`
    THEN `int64_col`
    WHEN `bool_col`
    THEN CAST(`bool_col` AS INT64)
    WHEN `bool_col`
    THEN `float64_col`
  END AS `mixed_types_cast`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`