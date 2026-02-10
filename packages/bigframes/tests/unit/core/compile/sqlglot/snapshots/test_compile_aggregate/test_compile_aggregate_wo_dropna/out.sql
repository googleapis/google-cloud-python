WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_too`,
    `int64_too` AS `bfcol_2`,
    `bool_col` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    `bfcol_3`,
    COALESCE(SUM(`bfcol_2`), 0) AS `bfcol_6`
  FROM `bfcte_0`
  GROUP BY
    `bfcol_3`
)
SELECT
  `bfcol_3` AS `bool_col`,
  `bfcol_6` AS `int64_too`
FROM `bfcte_1`
ORDER BY
  `bfcol_3` ASC NULLS LAST