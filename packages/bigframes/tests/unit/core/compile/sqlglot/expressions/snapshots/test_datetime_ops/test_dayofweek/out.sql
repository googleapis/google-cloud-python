SELECT
  CAST(MOD(EXTRACT(DAYOFWEEK FROM `datetime_col`) + 5, 7) AS INT64) AS `datetime_col`,
  CAST(MOD(EXTRACT(DAYOFWEEK FROM `timestamp_col`) + 5, 7) AS INT64) AS `timestamp_col`,
  CAST(MOD(EXTRACT(DAYOFWEEK FROM `date_col`) + 5, 7) AS INT64) AS `date_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`