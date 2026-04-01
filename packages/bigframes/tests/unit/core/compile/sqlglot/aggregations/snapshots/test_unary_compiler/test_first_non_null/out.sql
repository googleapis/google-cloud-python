SELECT
  FIRST_VALUE(`int64_col` IGNORE NULLS) OVER (
    ORDER BY `int64_col` ASC NULLS LAST
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`