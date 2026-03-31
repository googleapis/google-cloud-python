SELECT
  `rowindex`,
  `timestamp_col`,
  `date_col`,
  TIMESTAMP_ADD(CAST(`date_col` AS DATETIME), INTERVAL 86400000000 MICROSECOND) AS `date_add_timedelta`,
  TIMESTAMP_ADD(`timestamp_col`, INTERVAL 86400000000 MICROSECOND) AS `timestamp_add_timedelta`,
  TIMESTAMP_ADD(CAST(`date_col` AS DATETIME), INTERVAL 86400000000 MICROSECOND) AS `timedelta_add_date`,
  TIMESTAMP_ADD(`timestamp_col`, INTERVAL 86400000000 MICROSECOND) AS `timedelta_add_timestamp`,
  172800000000 AS `timedelta_add_timedelta`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`