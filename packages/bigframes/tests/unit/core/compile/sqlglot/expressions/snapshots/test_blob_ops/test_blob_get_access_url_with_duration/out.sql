SELECT
  OBJ.GET_ACCESS_URL(`string_col`, 'READ', INTERVAL 3600 MICROSECOND) AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
