WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`int64_col` * 0.001) AS INT64)) AS DATETIME) AS `bfcol_6`,
    SAFE_CAST(`string_col` AS DATETIME) AS `bfcol_7`,
    CAST(TIMESTAMP_MICROS(CAST(TRUNC(`float64_col` * 0.001) AS INT64)) AS DATETIME) AS `bfcol_8`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `int64_col`,
  `bfcol_7` AS `string_col`,
  `bfcol_8` AS `float64_col`
FROM `bfcte_1`