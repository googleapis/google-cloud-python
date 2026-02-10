SELECT
  `rowindex`,
  `int64_col`,
  `bool_col`,
  `int64_col` > `int64_col` AS `int_gt_int`,
  `int64_col` > 1 AS `int_gt_1`,
  `int64_col` > CAST(`bool_col` AS INT64) AS `int_gt_bool`,
  CAST(`bool_col` AS INT64) > `int64_col` AS `bool_gt_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`