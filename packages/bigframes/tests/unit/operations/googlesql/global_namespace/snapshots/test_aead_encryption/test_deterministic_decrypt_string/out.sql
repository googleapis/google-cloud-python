SELECT
  `rowindex`,
  DETERMINISTIC_DECRYPT_STRING(`bytes_col`, `bytes_col`, `string_col`) AS `0`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
