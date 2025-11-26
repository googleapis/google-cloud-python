WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 0.001) AS INT64)) AS TIMESTAMP) AS `bfcol_2`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`float64_col` * 0.001) AS INT64)) AS TIMESTAMP) AS `bfcol_3`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 1000000) AS INT64)) AS TIMESTAMP) AS `bfcol_4`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 1000) AS INT64)) AS TIMESTAMP) AS `bfcol_5`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col`) AS INT64)) AS TIMESTAMP) AS `bfcol_6`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 0.001) AS INT64)) AS TIMESTAMP) AS `bfcol_7`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`,
  `bfcol_3` AS `float64_col`,
  `bfcol_4` AS `int64_col_s`,
  `bfcol_5` AS `int64_col_ms`,
  `bfcol_6` AS `int64_col_us`,
  `bfcol_7` AS `int64_col_ns`
FROM `bfcte_1`