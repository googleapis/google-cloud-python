WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN SUBSTRING(`bfcol_0`, 1, 1) = '-'
      THEN CONCAT('-', LPAD(SUBSTRING(`bfcol_0`, 1), 9, '0'))
      ELSE LPAD(`bfcol_0`, 10, '0')
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_col`
FROM `bfcte_1`