SELECT
  LPAD(`string_col`, GREATEST(LENGTH(`string_col`), 10), '-') AS `left`,
  RPAD(`string_col`, GREATEST(LENGTH(`string_col`), 10), '-') AS `right`,
  RPAD(
    LPAD(
      `string_col`,
      CAST(FLOOR(SAFE_DIVIDE(GREATEST(LENGTH(`string_col`), 10) - LENGTH(`string_col`), 2)) AS INT64) + LENGTH(`string_col`),
      '-'
    ),
    GREATEST(LENGTH(`string_col`), 10),
    '-'
  ) AS `both`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`