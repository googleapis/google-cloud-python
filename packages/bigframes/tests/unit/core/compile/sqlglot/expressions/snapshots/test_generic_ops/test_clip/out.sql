SELECT
  GREATEST(LEAST(`rowindex`, `int64_too`), `int64_col`) AS `result_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`