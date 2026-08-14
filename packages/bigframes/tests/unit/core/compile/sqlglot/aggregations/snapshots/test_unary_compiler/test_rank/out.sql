SELECT
  RANK() OVER (ORDER BY `int64_col` DESC NULLS FIRST) AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`