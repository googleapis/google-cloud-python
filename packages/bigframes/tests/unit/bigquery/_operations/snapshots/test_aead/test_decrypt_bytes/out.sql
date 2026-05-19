SELECT
  `rowindex`,
  AEAD.DECRYPT_BYTES(`string_col`, `bytes_col`, `bytes_col`) AS `0`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
