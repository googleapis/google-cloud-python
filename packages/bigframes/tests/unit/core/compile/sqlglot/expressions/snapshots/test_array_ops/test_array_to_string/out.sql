SELECT
  ARRAY_TO_STRING(`string_list_col`, '.') AS `string_list_col`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`