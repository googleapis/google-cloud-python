WITH `bfcte_0` AS (
  SELECT
    *
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    COUNT(1) AS `bfcol_32`
  FROM `bfcte_0`
)
SELECT
  `bfcol_32` AS `size`
FROM `bfcte_1`