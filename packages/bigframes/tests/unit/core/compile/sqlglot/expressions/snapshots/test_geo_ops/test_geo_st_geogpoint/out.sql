WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `rowindex_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ST_GEOGPOINT(`rowindex`, `rowindex_2`) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `rowindex`
FROM `bfcte_1`