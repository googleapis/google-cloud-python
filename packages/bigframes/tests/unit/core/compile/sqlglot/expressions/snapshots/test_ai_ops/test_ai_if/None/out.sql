SELECT
  AI.IF(prompt => (`string_col`, ' is the same as ', `string_col`)) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`