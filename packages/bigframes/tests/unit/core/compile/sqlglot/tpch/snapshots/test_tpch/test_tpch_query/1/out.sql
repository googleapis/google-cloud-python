WITH `bfcte_0` AS (
  SELECT
    `L_QUANTITY`,
    `L_EXTENDEDPRICE`,
    `L_DISCOUNT`,
    `L_TAX`,
    `L_RETURNFLAG`,
    `L_LINESTATUS`,
    `L_SHIPDATE`,
    `L_QUANTITY` AS `bfcol_7`,
    `L_EXTENDEDPRICE` AS `bfcol_8`,
    `L_DISCOUNT` AS `bfcol_9`,
    `L_TAX` AS `bfcol_10`,
    `L_RETURNFLAG` AS `bfcol_11`,
    `L_LINESTATUS` AS `bfcol_12`,
    `L_SHIPDATE` <= CAST('1998-09-02' AS DATE) AS `bfcol_13`,
    `L_QUANTITY` AS `bfcol_27`,
    `L_EXTENDEDPRICE` AS `bfcol_28`,
    `L_DISCOUNT` AS `bfcol_29`,
    `L_TAX` AS `bfcol_30`,
    `L_RETURNFLAG` AS `bfcol_31`,
    `L_LINESTATUS` AS `bfcol_32`,
    `L_EXTENDEDPRICE` * (
      1.0 - `L_DISCOUNT`
    ) AS `bfcol_33`,
    `L_QUANTITY` AS `bfcol_41`,
    `L_EXTENDEDPRICE` AS `bfcol_42`,
    `L_DISCOUNT` AS `bfcol_43`,
    `L_RETURNFLAG` AS `bfcol_44`,
    `L_LINESTATUS` AS `bfcol_45`,
    `L_EXTENDEDPRICE` * (
      1.0 - `L_DISCOUNT`
    ) AS `bfcol_46`,
    (
      `L_EXTENDEDPRICE` * (
        1.0 - `L_DISCOUNT`
      )
    ) * (
      1.0 + `L_TAX`
    ) AS `bfcol_47`
  FROM `bigframes-dev`.`tpch`.`LINEITEM` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
  WHERE
    `L_SHIPDATE` <= CAST('1998-09-02' AS DATE)
), `bfcte_1` AS (
  SELECT
    `bfcol_44`,
    `bfcol_45`,
    COALESCE(SUM(`bfcol_41`), 0) AS `bfcol_55`,
    COALESCE(SUM(`bfcol_42`), 0) AS `bfcol_56`,
    COALESCE(SUM(`bfcol_46`), 0) AS `bfcol_57`,
    COALESCE(SUM(`bfcol_47`), 0) AS `bfcol_58`,
    AVG(`bfcol_41`) AS `bfcol_59`,
    AVG(`bfcol_42`) AS `bfcol_60`,
    AVG(`bfcol_43`) AS `bfcol_61`,
    COUNT(`bfcol_41`) AS `bfcol_62`
  FROM `bfcte_0`
  GROUP BY
    `bfcol_44`,
    `bfcol_45`
)
SELECT
  `bfcol_44` AS `L_RETURNFLAG`,
  `bfcol_45` AS `L_LINESTATUS`,
  `bfcol_55` AS `SUM_QTY`,
  `bfcol_56` AS `SUM_BASE_PRICE`,
  `bfcol_57` AS `SUM_DISC_PRICE`,
  `bfcol_58` AS `SUM_CHARGE`,
  `bfcol_59` AS `AVG_QTY`,
  `bfcol_60` AS `AVG_PRICE`,
  `bfcol_61` AS `AVG_DISC`,
  `bfcol_62` AS `COUNT_ORDER`
FROM `bfcte_1`
ORDER BY
  `bfcol_44` ASC NULLS LAST,
  `bfcol_45` ASC NULLS LAST