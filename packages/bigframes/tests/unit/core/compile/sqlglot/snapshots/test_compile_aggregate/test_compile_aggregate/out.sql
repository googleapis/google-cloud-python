WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `int64_too` AS `bfcol_2`,
    `bool_col` AS `bfcol_3`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_3`,
    COALESCE(SUM(`bfcol_2`), 0) AS `bfcol_6`
  FROM `bfcte_1`
  WHERE
    NOT `bfcol_3` IS NULL
  GROUP BY
    `bfcol_3`
)
SELECT
  `bfcol_3` AS `bool_col`,
  `bfcol_6` AS `int64_too`
FROM `bfcte_2`
ORDER BY
  `bfcol_3` ASC NULLS LAST