SELECT
  MIN(`int64_col`) OVER () AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`