SELECT
  `rowindex`,
  `timestamp_col`,
  `int64_col`,
  CAST(IF(
    IEEE_DIVIDE(86400000000, `int64_col`) > 0,
    FLOOR(IEEE_DIVIDE(86400000000, `int64_col`)),
    CEIL(IEEE_DIVIDE(86400000000, `int64_col`))
  ) AS INT64) AS `timedelta_div_numeric`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`