SELECT
  CAST(`bool_col` AS INT64) + BYTE_LENGTH(`bytes_col`) AS `bool_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`