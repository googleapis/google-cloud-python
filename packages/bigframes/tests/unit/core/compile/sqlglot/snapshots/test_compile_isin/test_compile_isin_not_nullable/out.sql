WITH `bfcte_2` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `rowindex_2` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_0` AS (
  SELECT
    `rowindex_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `rowindex_2`
  FROM `bfcte_0`
  GROUP BY
    `rowindex_2`
), `bfcte_3` AS (
  SELECT
    `bfcte_2`.*,
    `bfcte_2`.`bfcol_3` IN ((
        SELECT
          `rowindex_2` AS `bfcol_4`
        FROM `bfcte_1`
    )) AS `bfcol_5`
  FROM `bfcte_2`
)
SELECT
  `bfcol_2` AS `rowindex`,
  `bfcol_5` AS `rowindex_2`
FROM `bfcte_3`