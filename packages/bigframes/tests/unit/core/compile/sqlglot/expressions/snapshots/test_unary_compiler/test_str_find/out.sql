WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    INSTR(`bfcol_0`, 'e', 1) - 1 AS `bfcol_1`,
    INSTR(`bfcol_0`, 'e', 3) - 1 AS `bfcol_2`,
    INSTR(SUBSTRING(`bfcol_0`, 1, 5), 'e') - 1 AS `bfcol_3`,
    INSTR(SUBSTRING(`bfcol_0`, 3, 3), 'e') - 1 AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `none_none`,
  `bfcol_2` AS `start_none`,
  `bfcol_3` AS `none_end`,
  `bfcol_4` AS `start_end`
FROM `bfcte_1`