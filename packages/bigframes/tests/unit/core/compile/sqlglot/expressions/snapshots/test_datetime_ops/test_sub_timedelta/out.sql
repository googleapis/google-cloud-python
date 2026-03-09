SELECT
  `rowindex`,
  `timestamp_col`,
  `duration_col`,
  `date_col`,
  TIMESTAMP_SUB(CAST(`date_col` AS DATETIME), INTERVAL `duration_col` MICROSECOND) AS `date_sub_timedelta`,
  TIMESTAMP_SUB(`timestamp_col`, INTERVAL `duration_col` MICROSECOND) AS `timestamp_sub_timedelta`,
  TIMESTAMP_DIFF(CAST(`date_col` AS DATETIME), CAST(`date_col` AS DATETIME), MICROSECOND) AS `timestamp_sub_date`,
  TIMESTAMP_DIFF(`timestamp_col`, `timestamp_col`, MICROSECOND) AS `date_sub_timestamp`,
  `duration_col` - `duration_col` AS `timedelta_sub_timedelta`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`