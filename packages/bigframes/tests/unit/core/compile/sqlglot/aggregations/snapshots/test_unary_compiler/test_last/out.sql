SELECT
  LAST_VALUE(`int64_col`) OVER (
    ORDER BY `int64_col` DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`