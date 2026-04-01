SELECT
  COALESCE(CAST(`int64_col` AS STRING), '$NULL_SENTINEL$') = COALESCE(CAST(CAST(`bool_col` AS INT64) AS STRING), '$NULL_SENTINEL$') AS `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`