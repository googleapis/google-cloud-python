WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ENDS_WITH(`bfcol_0`, 'ab') AS `bfcol_1`,
    ENDS_WITH(`bfcol_0`, 'ab') OR ENDS_WITH(`bfcol_0`, 'cd') AS `bfcol_2`,
    FALSE AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `single`,
  `bfcol_2` AS `double`,
  `bfcol_3` AS `empty`
FROM `bfcte_1`