SELECT
  CASE
    WHEN `int64_col` < MIN(`int64_col`) OVER () + (
      1 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
    )
    THEN 'a'
    WHEN `int64_col` < MIN(`int64_col`) OVER () + (
      2 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
    )
    THEN 'b'
    WHEN (
      `int64_col`
    ) IS NOT NULL
    THEN 'c'
  END AS `int_bins_labels`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`