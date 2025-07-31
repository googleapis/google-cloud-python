WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_0` IN (1, 2, 3) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int64_col`
FROM `bfcte_1`