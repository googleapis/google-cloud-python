SELECT
  TIMESTAMP_TRUNC(`timestamp_col`, MICROSECOND) AS `timestamp_col_us`,
  TIMESTAMP_TRUNC(`timestamp_col`, MILLISECOND) AS `timestamp_col_ms`,
  TIMESTAMP_TRUNC(`timestamp_col`, SECOND) AS `timestamp_col_s`,
  TIMESTAMP_TRUNC(`timestamp_col`, MINUTE) AS `timestamp_col_min`,
  TIMESTAMP_TRUNC(`timestamp_col`, HOUR) AS `timestamp_col_h`,
  TIMESTAMP_TRUNC(`timestamp_col`, DAY) AS `timestamp_col_D`,
  TIMESTAMP_TRUNC(`timestamp_col`, WEEK(MONDAY)) AS `timestamp_col_W`,
  TIMESTAMP_TRUNC(`timestamp_col`, MONTH) AS `timestamp_col_M`,
  TIMESTAMP_TRUNC(`timestamp_col`, QUARTER) AS `timestamp_col_Q`,
  TIMESTAMP_TRUNC(`timestamp_col`, YEAR) AS `timestamp_col_Y`,
  TIMESTAMP_TRUNC(`datetime_col`, MICROSECOND) AS `datetime_col_q`,
  TIMESTAMP_TRUNC(`datetime_col`, MICROSECOND) AS `datetime_col_us`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`