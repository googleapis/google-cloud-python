SELECT
  `rowindex`,
  `int64_col`,
  `float64_col`,
  `int64_col` AS `duration_us`,
  CAST(FLOOR(`float64_col` * 1000000) AS INT64) AS `duration_s`,
  `int64_col` * 3600000000 AS `duration_w`,
  `int64_col` AS `duration_on_duration`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`