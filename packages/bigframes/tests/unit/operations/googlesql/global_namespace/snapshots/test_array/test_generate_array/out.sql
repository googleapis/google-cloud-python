SELECT
  `rowindex`,
  GENERATE_ARRAY(`string_col`, `string_col`, `string_col`) AS `0`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
