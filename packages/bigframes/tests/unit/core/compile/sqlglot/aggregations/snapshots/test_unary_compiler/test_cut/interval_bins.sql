SELECT
  CASE
    WHEN `int64_col` > 0 AND `int64_col` <= 1
    THEN STRUCT(0 AS `left_exclusive`, 1 AS `right_inclusive`)
    WHEN `int64_col` > 1 AND `int64_col` <= 2
    THEN STRUCT(1 AS `left_exclusive`, 2 AS `right_inclusive`)
  END AS `interval_bins`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`