SELECT
  ENDS_WITH(`string_col`, 'ab') AS `single`,
  ENDS_WITH(`string_col`, 'ab') OR ENDS_WITH(`string_col`, 'cd') AS `double`,
  FALSE AS `empty`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`