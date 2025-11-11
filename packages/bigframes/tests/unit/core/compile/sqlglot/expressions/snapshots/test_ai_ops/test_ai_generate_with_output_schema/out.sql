WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.GENERATE(
      prompt => (`string_col`, ' is the same as ', `string_col`),
      connection_id => 'bigframes-dev.us.bigframes-default-connection',
      endpoint => 'gemini-2.5-flash',
      request_type => 'SHARED',
      output_schema => 'x INT64, y FLOAT64'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`