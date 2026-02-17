SELECT
  INSTR(`string_col`, 'e', 1) - 1 AS `none_none`,
  INSTR(`string_col`, 'e', 3) - 1 AS `start_none`,
  INSTR(SUBSTRING(`string_col`, 1, 5), 'e') - 1 AS `none_end`,
  INSTR(SUBSTRING(`string_col`, 3, 3), 'e') - 1 AS `start_end`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`