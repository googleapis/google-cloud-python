SELECT
  CAST(FLOOR(
    IEEE_DIVIDE(
      UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) - UNIX_MICROS(CAST(`timestamp_col` AS TIMESTAMP)),
      86400000000
    )
  ) AS INT64) AS `fixed_freq`,
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
  END AS `non_fixed_freq_weekly`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`