SELECT
  [COALESCE(`bool_col`, FALSE)] AS `bool_col`,
  [COALESCE(`int64_col`, 0)] AS `int64_col`,
  [COALESCE(`string_col`, ''), COALESCE(`string_col`, '')] AS `strs_col`,
  [
    COALESCE(`int64_col`, 0),
    CAST(COALESCE(`bool_col`, FALSE) AS INT64),
    COALESCE(`float64_col`, 0.0)
  ] AS `numeric_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`