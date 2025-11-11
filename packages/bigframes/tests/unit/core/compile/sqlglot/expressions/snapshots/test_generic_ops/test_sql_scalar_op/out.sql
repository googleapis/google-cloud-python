WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `bytes_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(`bool_col` AS INT64) + BYTE_LENGTH(`bytes_col`) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `bool_col`
FROM `bfcte_1`