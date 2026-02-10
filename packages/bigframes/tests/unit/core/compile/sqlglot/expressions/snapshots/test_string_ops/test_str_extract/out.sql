SELECT
  IF(
    REGEXP_CONTAINS(`string_col`, '([a-z]*)'),
    REGEXP_REPLACE(`string_col`, CONCAT('.*?(', '([a-z]*)', ').*'), '\\1'),
    NULL
  ) AS `zero`,
  IF(
    REGEXP_CONTAINS(`string_col`, '([a-z]*)'),
    REGEXP_REPLACE(`string_col`, CONCAT('.*?', '([a-z]*)', '.*'), '\\1'),
    NULL
  ) AS `one`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`