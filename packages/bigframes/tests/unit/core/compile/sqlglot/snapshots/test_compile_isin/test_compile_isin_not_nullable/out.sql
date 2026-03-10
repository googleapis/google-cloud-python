WITH `bfcte_0` AS (
  SELECT
    `rowindex_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_3`,
    `rowindex_2` AS `bfcol_4`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    `rowindex_2`
  FROM `bfcte_0`
  GROUP BY
    `rowindex_2`
), `bfcte_3` AS (
  SELECT
    `rowindex_2` AS `bfcol_0`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    `bfcol_4` IN ((
        SELECT
          *
        FROM `bfcte_3`
    )) AS `bfcol_5`
  FROM `bfcte_1`
)
SELECT
  `bfcol_3` AS `rowindex`,
  `bfcol_5` AS `rowindex_2`
FROM `bfcte_4`