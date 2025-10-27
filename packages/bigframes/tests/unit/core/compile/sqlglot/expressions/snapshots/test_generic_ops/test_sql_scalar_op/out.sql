WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `bytes_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(`bfcol_0` AS INT64) + BYTE_LENGTH(`bfcol_1`) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `bool_col`
FROM `bfcte_1`