WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64>>[STRUCT(0)])
), `bfcte_1` AS (
  SELECT
    `L_QUANTITY`,
    `L_EXTENDEDPRICE`,
    `L_DISCOUNT`,
    `L_SHIPDATE`,
    `L_QUANTITY` AS `bfcol_5`,
    `L_EXTENDEDPRICE` AS `bfcol_6`,
    `L_DISCOUNT` AS `bfcol_7`,
    (
      `L_SHIPDATE` >= CAST('1994-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1995-01-01' AS DATE)
    ) AS `bfcol_8`,
    `L_QUANTITY` AS `bfcol_16`,
    `L_EXTENDEDPRICE` AS `bfcol_17`,
    `L_DISCOUNT` AS `bfcol_18`,
    (
      `L_DISCOUNT` >= 0.05
    ) AND (
      `L_DISCOUNT` <= 0.07
    ) AS `bfcol_19`,
    `L_EXTENDEDPRICE` AS `bfcol_27`,
    `L_DISCOUNT` AS `bfcol_28`,
    `L_QUANTITY` < 24 AS `bfcol_29`,
    `L_EXTENDEDPRICE` AS `bfcol_35`,
    `L_DISCOUNT` AS `bfcol_36`,
    `L_EXTENDEDPRICE` * `L_DISCOUNT` AS `bfcol_39`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
  WHERE
    (
      `L_SHIPDATE` >= CAST('1994-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1995-01-01' AS DATE)
    )
    AND (
      `L_DISCOUNT` >= 0.05
    )
    AND (
      `L_DISCOUNT` <= 0.07
    )
    AND `L_QUANTITY` < 24
), `bfcte_2` AS (
  SELECT
    COALESCE(SUM(`bfcol_39`), 0) AS `bfcol_41`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *
  FROM `bfcte_2`
)
SELECT
  CASE WHEN `bfcol_0` = 0 THEN `bfcol_41` END AS `REVENUE`
FROM `bfcte_3`
CROSS JOIN `bfcte_0`