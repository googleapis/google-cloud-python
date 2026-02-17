SELECT
  CASE
    WHEN `int64_col` > 0 AND `int64_col` <= 1
    THEN 0
    WHEN `int64_col` > 1 AND `int64_col` <= 2
    THEN 1
  END AS `interval_bins_labels`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`