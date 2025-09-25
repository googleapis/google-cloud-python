WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    COUNT(1) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `size`
FROM `bfcte_1`