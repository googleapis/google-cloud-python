SELECT
  CAST(MOD(EXTRACT(DAYOFWEEK FROM `timestamp_col`) + 5, 7) AS INT64) + 1 AS `timestamp_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`