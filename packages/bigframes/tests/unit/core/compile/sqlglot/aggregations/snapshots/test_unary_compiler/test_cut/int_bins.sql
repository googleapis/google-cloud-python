SELECT
  CASE
    WHEN `int64_col` <= MIN(`int64_col`) OVER () + (
      1 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
    )
    THEN STRUCT(
      (
        MIN(`int64_col`) OVER () + (
          0 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
        )
      ) - (
        (
          MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER ()
        ) * 0.001
      ) AS `left_exclusive`,
      MIN(`int64_col`) OVER () + (
        1 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
      ) + 0 AS `right_inclusive`
    )
    WHEN `int64_col` <= MIN(`int64_col`) OVER () + (
      2 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
    )
    THEN STRUCT(
      (
        MIN(`int64_col`) OVER () + (
          1 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
        )
      ) - 0 AS `left_exclusive`,
      MIN(`int64_col`) OVER () + (
        2 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
      ) + 0 AS `right_inclusive`
    )
    WHEN `int64_col` IS NOT NULL
    THEN STRUCT(
      (
        MIN(`int64_col`) OVER () + (
          2 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
        )
      ) - 0 AS `left_exclusive`,
      MIN(`int64_col`) OVER () + (
        3 * IEEE_DIVIDE(MAX(`int64_col`) OVER () - MIN(`int64_col`) OVER (), 3)
      ) + 0 AS `right_inclusive`
    )
  END AS `int_bins`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`