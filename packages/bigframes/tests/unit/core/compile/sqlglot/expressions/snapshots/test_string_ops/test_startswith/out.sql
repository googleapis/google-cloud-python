SELECT
  STARTS_WITH(`string_col`, 'ab') AS `single`,
  STARTS_WITH(`string_col`, 'ab') OR STARTS_WITH(`string_col`, 'cd') AS `double`,
  FALSE AS `empty`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`