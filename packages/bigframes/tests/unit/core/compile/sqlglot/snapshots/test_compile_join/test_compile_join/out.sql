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
    `int64_col` AS `bfcol_4`,
    `int64_too` AS `bfcol_5`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_3` AS (
  SELECT
    `bfcol_4` AS `bfcol_6`,
    `bfcol_5` AS `bfcol_7`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *
  FROM `bfcte_2`
  LEFT JOIN `bfcte_3`
    ON COALESCE(`bfcol_2`, 0) = COALESCE(`bfcol_6`, 0)
    AND COALESCE(`bfcol_2`, 1) = COALESCE(`bfcol_6`, 1)
)
SELECT
  `bfcol_3` AS `int64_col`,
  `bfcol_7` AS `int64_too`
FROM `bfcte_4`