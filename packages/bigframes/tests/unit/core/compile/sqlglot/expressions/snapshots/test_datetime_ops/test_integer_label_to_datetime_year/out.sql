SELECT
  CAST(TIMESTAMP(DATETIME(`rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) + 1, 1, 1, 0, 0, 0)) - INTERVAL 1 DAY AS TIMESTAMP) AS `non_fixed_freq_yearly`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`