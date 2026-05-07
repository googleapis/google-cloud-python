SELECT
  AI.SIMILARITY(
    content1 => `string_col`,
    content2 => `string_col`,
    endpoint => 'text-embedding-005',
    connection_id => 'bigframes-dev.us.bigframes-default-connection'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`