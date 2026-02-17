SELECT
  FORMAT_DATE('%Y-%m-%d', `date_col`) AS `date_col`,
  FORMAT_DATETIME('%Y-%m-%d', `datetime_col`) AS `datetime_col`,
  FORMAT_TIME('%Y-%m-%d', `time_col`) AS `time_col`,
  FORMAT_TIMESTAMP('%Y-%m-%d', `timestamp_col`) AS `timestamp_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`