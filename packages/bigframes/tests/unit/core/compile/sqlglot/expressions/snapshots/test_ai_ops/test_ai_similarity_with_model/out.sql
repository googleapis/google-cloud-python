SELECT
  AI.SIMILARITY(content1 => `string_col`, content2 => `string_col`, model => 'embeddinggemma-300m') AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`