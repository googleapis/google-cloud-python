WITH `bfcte_0` AS (
  SELECT
    `datetime_col`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(FLOOR(
      IEEE_DIVIDE(
        UNIX_MICROS(CAST(`datetime_col` AS TIMESTAMP)) - UNIX_MICROS(CAST(`timestamp_col` AS TIMESTAMP)),
        86400000000
      )
    ) AS INT64) AS `bfcol_2`,
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
    END AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `fixed_freq`,
  `bfcol_3` AS `non_fixed_freq_weekly`
FROM `bfcte_1`