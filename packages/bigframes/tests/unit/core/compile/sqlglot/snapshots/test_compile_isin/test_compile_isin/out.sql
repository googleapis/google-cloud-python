WITH `bfcte_2` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `int64_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_0` AS (
  SELECT
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `int64_too`
  FROM `bfcte_0`
  GROUP BY
    `int64_too`
), `bfcte_3` AS (
  SELECT
    `bfcte_2`.*,
    EXISTS(
      SELECT
        1
      FROM (
        SELECT
          `int64_too` AS `bfcol_4`
        FROM `bfcte_1`
      ) AS `bft_0`
      WHERE
        COALESCE(`bfcte_2`.`bfcol_3`, 0) = COALESCE(`bft_0`.`bfcol_4`, 0)
        AND COALESCE(`bfcte_2`.`bfcol_3`, 1) = COALESCE(`bft_0`.`bfcol_4`, 1)
    ) AS `bfcol_5`
  FROM `bfcte_2`
)
SELECT
  `bfcol_2` AS `rowindex`,
  `bfcol_5` AS `int64_col`
FROM `bfcte_3`