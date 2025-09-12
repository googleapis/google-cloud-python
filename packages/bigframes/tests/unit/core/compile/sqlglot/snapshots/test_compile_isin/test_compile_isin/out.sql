WITH `bfcte_1` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    `bfcol_1` AS `bfcol_2`,
    `bfcol_0` AS `bfcol_3`
  FROM `bfcte_1`
), `bfcte_0` AS (
  SELECT
    `int64_too` AS `bfcol_4`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    `bfcte_2`.*,
    EXISTS(
      SELECT
        1
      FROM (
        SELECT
          `bfcol_4`
        FROM `bfcte_0`
        GROUP BY
          `bfcol_4`
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