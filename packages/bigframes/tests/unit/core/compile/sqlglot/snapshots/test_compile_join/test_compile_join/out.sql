WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_2`,
    `int64_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `int64_col` AS `bfcol_6`,
    `int64_too` AS `bfcol_7`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_0`
  LEFT JOIN `bfcte_1`
    ON COALESCE(`bfcol_2`, 0) = COALESCE(`bfcol_6`, 0)
    AND COALESCE(`bfcol_2`, 1) = COALESCE(`bfcol_6`, 1)
)
SELECT
  `bfcol_3` AS `int64_col`,
  `bfcol_7` AS `int64_too`
FROM `bfcte_2`