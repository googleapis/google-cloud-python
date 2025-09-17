WITH `bfcte_0` AS (
  SELECT
    `geography_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ST_BUFFER(`bfcol_0`, 1.0, 8.0, FALSE) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `geography_col`
FROM `bfcte_1`