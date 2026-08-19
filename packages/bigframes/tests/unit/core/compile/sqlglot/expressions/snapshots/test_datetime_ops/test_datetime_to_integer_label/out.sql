SELECT
  CAST(FLOOR(
    IEEE_DIVIDE(
      UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) - UNIX_MICROS(CAST(`timestamp_col` AS TIMESTAMP)),
      86400000000
    )
  ) AS INT64) AS `fixed_freq`,
  CAST(FLOOR(IEEE_DIVIDE(UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) - 0, 86400000000)) AS INT64) AS `origin_epoch`,
  CAST(FLOOR(
    IEEE_DIVIDE(
      UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) - UNIX_MICROS(CAST(CAST(`timestamp_col` AS DATE) AS TIMESTAMP)),
      86400000000
    )
  ) AS INT64) AS `origin_start_day`,
  CASE
    WHEN UNIX_MICROS(
      CAST(TIMESTAMP_TRUNC(`datetime_col`, WEEK(MONDAY)) + INTERVAL 6 DAY AS TIMESTAMP)
    ) = UNIX_MICROS(
      CAST(TIMESTAMP_TRUNC(`timestamp_col`, WEEK(MONDAY)) + INTERVAL 6 DAY AS TIMESTAMP)
    )
    THEN 0
    ELSE CAST(FLOOR(
      IEEE_DIVIDE(
        UNIX_MICROS(
          CAST(TIMESTAMP_TRUNC(`datetime_col`, WEEK(MONDAY)) + INTERVAL 6 DAY AS TIMESTAMP)
        ) - UNIX_MICROS(
          CAST(TIMESTAMP_TRUNC(`timestamp_col`, WEEK(MONDAY)) + INTERVAL 6 DAY AS TIMESTAMP)
        ) - 1,
        604800000000
      )
    ) AS INT64) + 1
  END AS `non_fixed_freq_weekly`,
  CASE
    WHEN (
      EXTRACT(YEAR FROM `datetime_col`) * 12 + EXTRACT(MONTH FROM `datetime_col`) - 1
    ) = (
      EXTRACT(YEAR FROM `timestamp_col`) * 12 + EXTRACT(MONTH FROM `timestamp_col`) - 1
    )
    THEN 0
    ELSE CAST(FLOOR(
      IEEE_DIVIDE(
        (
          EXTRACT(YEAR FROM `datetime_col`) * 12 + EXTRACT(MONTH FROM `datetime_col`) - 1
        ) - (
          EXTRACT(YEAR FROM `timestamp_col`) * 12 + EXTRACT(MONTH FROM `timestamp_col`) - 1
        ) - 1,
        1
      )
    ) AS INT64) + 1
  END AS `non_fixed_freq_monthly`,
  CASE
    WHEN (
      EXTRACT(YEAR FROM `datetime_col`) * 4 + EXTRACT(QUARTER FROM `datetime_col`) - 1
    ) = (
      EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1
    )
    THEN 0
    ELSE CAST(FLOOR(
      IEEE_DIVIDE(
        (
          EXTRACT(YEAR FROM `datetime_col`) * 4 + EXTRACT(QUARTER FROM `datetime_col`) - 1
        ) - (
          EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1
        ) - 1,
        1
      )
    ) AS INT64) + 1
  END AS `non_fixed_freq_quarterly`,
  CASE
    WHEN EXTRACT(YEAR FROM `datetime_col`) = EXTRACT(YEAR FROM `timestamp_col`)
    THEN 0
    ELSE CAST(FLOOR(
      IEEE_DIVIDE(EXTRACT(YEAR FROM `datetime_col`) - EXTRACT(YEAR FROM `timestamp_col`) - 1, 1)
    ) AS INT64) + 1
  END AS `non_fixed_freq_yearly`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`