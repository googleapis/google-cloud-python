WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_3` STRING, `bfcol_4` INT64, `bfcol_5` INT64>>[STRUCT('C_ACCTBAL', 0, 0)])
), `bfcte_1` AS (
  SELECT
    `O_CUSTKEY`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_1`
), `bfcte_2` AS (
  SELECT
    `C_PHONE`,
    `C_ACCTBAL`,
    `C_ACCTBAL` AS `bfcol_9`,
    SUBSTRING(`C_PHONE`, 1, 2) AS `bfcol_10`,
    `C_ACCTBAL` AS `bfcol_19`,
    COALESCE(
      COALESCE(SUBSTRING(`C_PHONE`, 1, 2) IN ('13', '31', '23', '29', '30', '18', '17'), FALSE),
      FALSE
    ) AS `bfcol_20`,
    `C_ACCTBAL` AS `bfcol_35`,
    `C_ACCTBAL` > 0.0 AS `bfcol_36`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0`
  WHERE
    COALESCE(
      COALESCE(SUBSTRING(`C_PHONE`, 1, 2) IN ('13', '31', '23', '29', '30', '18', '17'), FALSE),
      FALSE
    )
    AND `C_ACCTBAL` > 0.0
), `bfcte_3` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_32`,
    `C_ACCTBAL` AS `bfcol_33`,
    SUBSTRING(`C_PHONE`, 1, 2) AS `bfcol_34`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0`
  WHERE
    COALESCE(
      COALESCE(SUBSTRING(`C_PHONE`, 1, 2) IN ('13', '31', '23', '29', '30', '18', '17'), FALSE),
      FALSE
    )
), `bfcte_4` AS (
  SELECT
    `O_CUSTKEY`
  FROM `bfcte_1`
  GROUP BY
    `O_CUSTKEY`
), `bfcte_5` AS (
  SELECT
    AVG(`bfcol_35`) AS `bfcol_40`
  FROM `bfcte_2`
), `bfcte_6` AS (
  SELECT
    `O_CUSTKEY` AS `bfcol_0`
  FROM `bfcte_4`
), `bfcte_7` AS (
  SELECT
    `bfcol_40`,
    0 AS `bfcol_41`
  FROM `bfcte_5`
), `bfcte_8` AS (
  SELECT
    `bfcol_3`,
    `bfcol_4`,
    `bfcol_5`,
    `bfcol_40`,
    `bfcol_41`,
    CASE WHEN `bfcol_5` = 0 THEN `bfcol_40` END AS `bfcol_42`,
    IF(`bfcol_41` = 0, CASE WHEN `bfcol_5` = 0 THEN `bfcol_40` END, NULL) AS `bfcol_47`
  FROM `bfcte_0`
  CROSS JOIN `bfcte_7`
), `bfcte_9` AS (
  SELECT
    `bfcol_3`,
    `bfcol_4`,
    ANY_VALUE(`bfcol_47`) AS `bfcol_51`
  FROM `bfcte_8`
  GROUP BY
    `bfcol_3`,
    `bfcol_4`
), `bfcte_10` AS (
  SELECT
    `bfcol_51` AS `bfcol_52`
  FROM `bfcte_9`
), `bfcte_11` AS (
  SELECT
    `bfcol_32` AS `bfcol_61`,
    `bfcol_33` AS `bfcol_62`,
    `bfcol_34` AS `bfcol_63`
  FROM `bfcte_3`
  CROSS JOIN `bfcte_10`
  WHERE
    `bfcol_33` > `bfcol_52`
), `bfcte_12` AS (
  SELECT
    *,
    `bfcol_61` IN ((
        SELECT
          *
        FROM `bfcte_6`
    )) AS `bfcol_64`
  FROM `bfcte_11`
), `bfcte_13` AS (
  SELECT
    `bfcol_61`,
    `bfcol_62`,
    `bfcol_63`,
    `bfcol_64`,
    NOT (
      `bfcol_64`
    ) AS `bfcol_65`
  FROM `bfcte_12`
  WHERE
    NOT (
      `bfcol_64`
    )
), `bfcte_14` AS (
  SELECT
    `bfcol_63`,
    COUNT(`bfcol_61`) AS `bfcol_73`,
    COALESCE(SUM(`bfcol_62`), 0) AS `bfcol_74`
  FROM `bfcte_13`
  WHERE
    NOT `bfcol_63` IS NULL
  GROUP BY
    `bfcol_63`
)
SELECT
  `bfcol_63` AS `CNTRYCODE`,
  `bfcol_73` AS `NUMCUST`,
  `bfcol_74` AS `TOTACCTBAL`
FROM `bfcte_14`
ORDER BY
  `bfcol_63` ASC NULLS LAST