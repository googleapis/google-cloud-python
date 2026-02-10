SELECT
  `bool_col`,
  `float64_col` <> 0 AS `float64_col`,
  `float64_col` <> 0 AS `float64_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`