WITH `bfcte_0` AS (
  SELECT
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    `rowindex` AS `bfcol_3`,
    `int64_col` AS `bfcol_4`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    `int64_too`
  FROM `bfcte_0`
  GROUP BY
    `int64_too`
), `bfcte_3` AS (
  SELECT
    `int64_too` AS `bfcol_0`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    STRUCT(COALESCE(`bfcol_4`, 0) AS `bfpart1`, COALESCE(`bfcol_4`, 1) AS `bfpart2`) IN (
      (
        SELECT
          STRUCT(COALESCE(`bfcol_0`, 0) AS `bfpart1`, COALESCE(`bfcol_0`, 1) AS `bfpart2`)
        FROM `bfcte_3`
      )
    ) AS `bfcol_5`
  FROM `bfcte_1`
)
SELECT
  `bfcol_3` AS `rowindex`,
  `bfcol_5` AS `int64_col`
FROM `bfcte_4`