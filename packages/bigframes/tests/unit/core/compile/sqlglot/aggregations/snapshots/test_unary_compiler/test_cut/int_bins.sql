WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
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
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int_bins`
FROM `bfcte_1`