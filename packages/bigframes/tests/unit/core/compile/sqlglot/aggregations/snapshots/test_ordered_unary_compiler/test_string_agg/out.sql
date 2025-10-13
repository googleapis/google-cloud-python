WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    COALESCE(STRING_AGG(`bfcol_0`, ','
    ORDER BY
      `bfcol_0` IS NULL ASC,
      `bfcol_0` ASC), '') AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_col`
FROM `bfcte_1`