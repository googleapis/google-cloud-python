SELECT
  COALESCE(`bool_col` IN (TRUE, FALSE), FALSE) AS `bools`,
  COALESCE(`int64_col` IN (1, 2, 3), FALSE) AS `ints`,
  `int64_col` IS NULL AS `ints_w_null`,
  COALESCE(`int64_col` IN (1.0, 2.0, 3.0), FALSE) AS `floats`,
  FALSE AS `strings`,
  COALESCE(`int64_col` IN (2.5, 3), FALSE) AS `mixed`,
  FALSE AS `empty`,
  FALSE AS `empty_wo_match_nulls`,
  COALESCE(`int64_col` IN (123456), FALSE) AS `ints_wo_match_nulls`,
  (
    `float64_col` IS NULL
  ) OR `float64_col` IN (1, 2, 3) AS `float_in_ints`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`