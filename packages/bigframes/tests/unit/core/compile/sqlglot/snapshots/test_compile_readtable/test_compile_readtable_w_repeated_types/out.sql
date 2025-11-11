WITH `bfcte_0` AS (
  SELECT
    `bool_list_col`,
    `date_list_col`,
    `date_time_list_col`,
    `float_list_col`,
    `int_list_col`,
    `numeric_list_col`,
    `rowindex`,
    `string_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
)
SELECT
  `rowindex`,
  `rowindex` AS `rowindex_1`,
  `int_list_col`,
  `bool_list_col`,
  `float_list_col`,
  `date_list_col`,
  `date_time_list_col`,
  `numeric_list_col`,
  `string_list_col`
FROM `bfcte_0`