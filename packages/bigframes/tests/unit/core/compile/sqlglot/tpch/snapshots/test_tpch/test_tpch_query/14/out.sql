WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_5` STRING, `bfcol_6` INT64, `bfcol_7` INT64>>[STRUCT('TEMP', 0, 0)])
), `bfcte_1` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_10` STRING, `bfcol_11` INT64, `bfcol_12` INT64>>[STRUCT('TEMP', 0, 0)])
), `bfcte_2` AS (
  SELECT
    `L_PARTKEY` AS `bfcol_0`,
    `L_EXTENDEDPRICE` AS `bfcol_1`,
    `L_DISCOUNT` AS `bfcol_2`,
    `L_SHIPDATE` AS `bfcol_3`
  FROM `bigframes-dev`.`tpch`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_3` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_4`
  FROM `bigframes-dev`.`tpch`.`PART` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_4` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_8`,
    `P_TYPE` AS `bfcol_9`
  FROM `bigframes-dev`.`tpch`.`PART` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_5` AS (
  SELECT
    `bfcol_4`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_3`,
    `bfcol_1` AS `bfcol_20`,
    `bfcol_2` AS `bfcol_21`,
    (
      `bfcol_3` >= CAST('1995-09-01' AS DATE)
    )
    AND (
      `bfcol_3` < CAST('1995-10-01' AS DATE)
    ) AS `bfcol_22`,
    `bfcol_1` AS `bfcol_39`,
    `bfcol_2` AS `bfcol_40`,
    `bfcol_1` AS `bfcol_45`,
    1 - `bfcol_2` AS `bfcol_46`,
    `bfcol_1` * (
      1 - `bfcol_2`
    ) AS `bfcol_51`
  FROM `bfcte_3`
  INNER JOIN `bfcte_2`
    ON `bfcol_4` = `bfcol_0`
  WHERE
    (
      `bfcol_3` >= CAST('1995-09-01' AS DATE)
    )
    AND (
      `bfcol_3` < CAST('1995-10-01' AS DATE)
    )
), `bfcte_6` AS (
  SELECT
    `bfcol_8`,
    `bfcol_9`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_3`,
    `bfcol_9` AS `bfcol_23`,
    `bfcol_1` AS `bfcol_24`,
    `bfcol_2` AS `bfcol_25`,
    (
      `bfcol_3` >= CAST('1995-09-01' AS DATE)
    )
    AND (
      `bfcol_3` < CAST('1995-10-01' AS DATE)
    ) AS `bfcol_26`,
    (
      `bfcol_1` * (
        1 - `bfcol_2`
      )
    ) * CAST(REGEXP_CONTAINS(`bfcol_9`, 'PROMO') AS INT64) AS `bfcol_41`
  FROM `bfcte_4`
  INNER JOIN `bfcte_2`
    ON `bfcol_8` = `bfcol_0`
  WHERE
    (
      `bfcol_3` >= CAST('1995-09-01' AS DATE)
    )
    AND (
      `bfcol_3` < CAST('1995-10-01' AS DATE)
    )
), `bfcte_7` AS (
  SELECT
    COALESCE(SUM(`bfcol_51`), 0) AS `bfcol_54`
  FROM `bfcte_5`
), `bfcte_8` AS (
  SELECT
    COALESCE(SUM(`bfcol_41`), 0) AS `bfcol_47`
  FROM `bfcte_6`
), `bfcte_9` AS (
  SELECT
    `bfcol_54`,
    0 AS `bfcol_59`
  FROM `bfcte_7`
), `bfcte_10` AS (
  SELECT
    `bfcol_47`,
    0 AS `bfcol_50`
  FROM `bfcte_8`
), `bfcte_11` AS (
  SELECT
    `bfcol_5`,
    `bfcol_6`,
    `bfcol_7`,
    `bfcol_54`,
    `bfcol_59`,
    CASE WHEN `bfcol_7` = 0 THEN `bfcol_54` END AS `bfcol_64`,
    IF(`bfcol_59` = 0, CASE WHEN `bfcol_7` = 0 THEN `bfcol_54` END, NULL) AS `bfcol_72`
  FROM `bfcte_0`
  CROSS JOIN `bfcte_9`
), `bfcte_12` AS (
  SELECT
    `bfcol_10`,
    `bfcol_11`,
    `bfcol_12`,
    `bfcol_47`,
    `bfcol_50`,
    CASE WHEN `bfcol_12` = 0 THEN `bfcol_47` END AS `bfcol_53`,
    IF(`bfcol_50` = 0, CASE WHEN `bfcol_12` = 0 THEN `bfcol_47` END, NULL) AS `bfcol_60`
  FROM `bfcte_1`
  CROSS JOIN `bfcte_10`
), `bfcte_13` AS (
  SELECT
    `bfcol_5`,
    `bfcol_6`,
    ANY_VALUE(`bfcol_72`) AS `bfcol_79`
  FROM `bfcte_11`
  GROUP BY
    `bfcol_5`,
    `bfcol_6`
), `bfcte_14` AS (
  SELECT
    `bfcol_10`,
    `bfcol_11`,
    ANY_VALUE(`bfcol_60`) AS `bfcol_65`
  FROM `bfcte_12`
  GROUP BY
    `bfcol_10`,
    `bfcol_11`
), `bfcte_15` AS (
  SELECT
    `bfcol_5` AS `bfcol_80`,
    `bfcol_79` AS `bfcol_81`
  FROM `bfcte_13`
), `bfcte_16` AS (
  SELECT
    `bfcol_10` AS `bfcol_77`,
    100.0 * `bfcol_65` AS `bfcol_78`
  FROM `bfcte_14`
)
SELECT
  ROUND(IEEE_DIVIDE(`bfcol_78`, `bfcol_81`), 2) AS `PROMO_REVENUE`
FROM `bfcte_16`
FULL OUTER JOIN `bfcte_15`
  ON `bfcol_77` = `bfcol_80`
ORDER BY
  COALESCE(`bfcol_77`, `bfcol_80`) ASC NULLS LAST