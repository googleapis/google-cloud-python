WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    NOT `int64_col` IS NULL AS `bfcol_4`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    IF(
      `int64_col` IS NULL,
      NULL,
      CAST(GREATEST(
        CEIL(PERCENT_RANK() OVER (PARTITION BY `bfcol_4` ORDER BY `int64_col` ASC) * 4) - 1,
        0
      ) AS INT64)
    ) AS `bfcol_5`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    IF(`bfcol_4`, `bfcol_5`, NULL) AS `bfcol_6`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    NOT `int64_col` IS NULL AS `bfcol_10`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    CASE
      WHEN PERCENT_RANK() OVER (PARTITION BY `bfcol_10` ORDER BY `int64_col` ASC) < 0
      THEN NULL
      WHEN PERCENT_RANK() OVER (PARTITION BY `bfcol_10` ORDER BY `int64_col` ASC) <= 0.25
      THEN 0
      WHEN PERCENT_RANK() OVER (PARTITION BY `bfcol_10` ORDER BY `int64_col` ASC) <= 0.5
      THEN 1
      WHEN PERCENT_RANK() OVER (PARTITION BY `bfcol_10` ORDER BY `int64_col` ASC) <= 0.75
      THEN 2
      WHEN PERCENT_RANK() OVER (PARTITION BY `bfcol_10` ORDER BY `int64_col` ASC) <= 1
      THEN 3
      ELSE NULL
    END AS `bfcol_11`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    *,
    IF(`bfcol_10`, `bfcol_11`, NULL) AS `bfcol_12`
  FROM `bfcte_5`
)
SELECT
  `rowindex`,
  `int64_col`,
  `bfcol_6` AS `qcut_w_int`,
  `bfcol_12` AS `qcut_w_list`
FROM `bfcte_6`