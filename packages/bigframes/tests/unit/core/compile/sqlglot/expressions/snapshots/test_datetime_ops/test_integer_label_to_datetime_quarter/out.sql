WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(DATETIME(
      CASE
        WHEN (
          MOD(
            `rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1,
            4
          ) + 1
        ) * 3 = 12
        THEN CAST(FLOOR(
          IEEE_DIVIDE(
            `rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1,
            4
          )
        ) AS INT64) + 1
        ELSE CAST(FLOOR(
          IEEE_DIVIDE(
            `rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1,
            4
          )
        ) AS INT64)
      END,
      CASE
        WHEN (
          MOD(
            `rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1,
            4
          ) + 1
        ) * 3 = 12
        THEN 1
        ELSE (
          MOD(
            `rowindex` * 1 + EXTRACT(YEAR FROM `timestamp_col`) * 4 + EXTRACT(QUARTER FROM `timestamp_col`) - 1,
            4
          ) + 1
        ) * 3 + 1
      END,
      1,
      0,
      0,
      0
    ) - INTERVAL 1 DAY AS TIMESTAMP) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `non_fixed_freq`
FROM `bfcte_1`