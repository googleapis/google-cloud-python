WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    STARTS_WITH(`string_col`, 'ab') AS `bfcol_1`,
    STARTS_WITH(`string_col`, 'ab') OR STARTS_WITH(`string_col`, 'cd') AS `bfcol_2`,
    FALSE AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `single`,
  `bfcol_2` AS `double`,
  `bfcol_3` AS `empty`
FROM `bfcte_1`