SELECT
  `rowindex`,
  FLATTEN(`string_col`, depth => `string_col`) AS `0`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
