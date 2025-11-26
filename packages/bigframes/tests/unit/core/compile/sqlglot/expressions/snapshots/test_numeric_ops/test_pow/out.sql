WITH `bfcte_0` AS (
  SELECT
    `float64_col`,
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `int64_col` AS `bfcol_7`,
    `float64_col` AS `bfcol_8`,
    CASE
      WHEN `int64_col` <> 0 AND `int64_col` * LN(ABS(`int64_col`)) > 43.66827237527655
      THEN NULL
      ELSE CAST(POWER(CAST(`int64_col` AS NUMERIC), `int64_col`) AS INT64)
    END AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    CASE
      WHEN `bfcol_8` = CAST(0 AS INT64)
      THEN 1
      WHEN `bfcol_7` = 1
      THEN 1
      WHEN `bfcol_7` = CAST(0 AS INT64) AND `bfcol_8` < CAST(0 AS INT64)
      THEN CAST('Infinity' AS FLOAT64)
      WHEN ABS(`bfcol_7`) = CAST('Infinity' AS FLOAT64)
      THEN POWER(
        `bfcol_7`,
        CASE
          WHEN ABS(`bfcol_8`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_8`)
          ELSE `bfcol_8`
        END
      )
      WHEN ABS(`bfcol_8`) > 9007199254740992
      THEN POWER(
        `bfcol_7`,
        CASE
          WHEN ABS(`bfcol_8`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_8`)
          ELSE `bfcol_8`
        END
      )
      WHEN `bfcol_7` < CAST(0 AS INT64) AND NOT CAST(`bfcol_8` AS INT64) = `bfcol_8`
      THEN CAST('NaN' AS FLOAT64)
      WHEN `bfcol_7` <> CAST(0 AS INT64) AND `bfcol_8` * LN(ABS(`bfcol_7`)) > 709.78
      THEN CAST('Infinity' AS FLOAT64) * CASE
        WHEN `bfcol_7` < CAST(0 AS INT64) AND MOD(CAST(`bfcol_8` AS INT64), 2) = 1
        THEN -1
        ELSE 1
      END
      ELSE POWER(
        `bfcol_7`,
        CASE
          WHEN ABS(`bfcol_8`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_8`)
          ELSE `bfcol_8`
        END
      )
    END AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    CASE
      WHEN `bfcol_15` = CAST(0 AS INT64)
      THEN 1
      WHEN `bfcol_16` = 1
      THEN 1
      WHEN `bfcol_16` = CAST(0 AS INT64) AND `bfcol_15` < CAST(0 AS INT64)
      THEN CAST('Infinity' AS FLOAT64)
      WHEN ABS(`bfcol_16`) = CAST('Infinity' AS FLOAT64)
      THEN POWER(
        `bfcol_16`,
        CASE
          WHEN ABS(`bfcol_15`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_15`)
          ELSE `bfcol_15`
        END
      )
      WHEN ABS(`bfcol_15`) > 9007199254740992
      THEN POWER(
        `bfcol_16`,
        CASE
          WHEN ABS(`bfcol_15`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_15`)
          ELSE `bfcol_15`
        END
      )
      WHEN `bfcol_16` < CAST(0 AS INT64) AND NOT CAST(`bfcol_15` AS INT64) = `bfcol_15`
      THEN CAST('NaN' AS FLOAT64)
      WHEN `bfcol_16` <> CAST(0 AS INT64) AND `bfcol_15` * LN(ABS(`bfcol_16`)) > 709.78
      THEN CAST('Infinity' AS FLOAT64) * CASE
        WHEN `bfcol_16` < CAST(0 AS INT64) AND MOD(CAST(`bfcol_15` AS INT64), 2) = 1
        THEN -1
        ELSE 1
      END
      ELSE POWER(
        `bfcol_16`,
        CASE
          WHEN ABS(`bfcol_15`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_15`)
          ELSE `bfcol_15`
        END
      )
    END AS `bfcol_29`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    `bfcol_24` AS `bfcol_36`,
    `bfcol_25` AS `bfcol_37`,
    `bfcol_26` AS `bfcol_38`,
    `bfcol_27` AS `bfcol_39`,
    `bfcol_28` AS `bfcol_40`,
    `bfcol_29` AS `bfcol_41`,
    CASE
      WHEN `bfcol_26` = CAST(0 AS INT64)
      THEN 1
      WHEN `bfcol_26` = 1
      THEN 1
      WHEN `bfcol_26` = CAST(0 AS INT64) AND `bfcol_26` < CAST(0 AS INT64)
      THEN CAST('Infinity' AS FLOAT64)
      WHEN ABS(`bfcol_26`) = CAST('Infinity' AS FLOAT64)
      THEN POWER(
        `bfcol_26`,
        CASE
          WHEN ABS(`bfcol_26`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_26`)
          ELSE `bfcol_26`
        END
      )
      WHEN ABS(`bfcol_26`) > 9007199254740992
      THEN POWER(
        `bfcol_26`,
        CASE
          WHEN ABS(`bfcol_26`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_26`)
          ELSE `bfcol_26`
        END
      )
      WHEN `bfcol_26` < CAST(0 AS INT64) AND NOT CAST(`bfcol_26` AS INT64) = `bfcol_26`
      THEN CAST('NaN' AS FLOAT64)
      WHEN `bfcol_26` <> CAST(0 AS INT64) AND `bfcol_26` * LN(ABS(`bfcol_26`)) > 709.78
      THEN CAST('Infinity' AS FLOAT64) * CASE
        WHEN `bfcol_26` < CAST(0 AS INT64) AND MOD(CAST(`bfcol_26` AS INT64), 2) = 1
        THEN -1
        ELSE 1
      END
      ELSE POWER(
        `bfcol_26`,
        CASE
          WHEN ABS(`bfcol_26`) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(`bfcol_26`)
          ELSE `bfcol_26`
        END
      )
    END AS `bfcol_42`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    `bfcol_36` AS `bfcol_50`,
    `bfcol_37` AS `bfcol_51`,
    `bfcol_38` AS `bfcol_52`,
    `bfcol_39` AS `bfcol_53`,
    `bfcol_40` AS `bfcol_54`,
    `bfcol_41` AS `bfcol_55`,
    `bfcol_42` AS `bfcol_56`,
    CASE
      WHEN `bfcol_37` <> 0 AND 0 * LN(ABS(`bfcol_37`)) > 43.66827237527655
      THEN NULL
      ELSE CAST(POWER(CAST(`bfcol_37` AS NUMERIC), 0) AS INT64)
    END AS `bfcol_57`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    *,
    `bfcol_50` AS `bfcol_66`,
    `bfcol_51` AS `bfcol_67`,
    `bfcol_52` AS `bfcol_68`,
    `bfcol_53` AS `bfcol_69`,
    `bfcol_54` AS `bfcol_70`,
    `bfcol_55` AS `bfcol_71`,
    `bfcol_56` AS `bfcol_72`,
    `bfcol_57` AS `bfcol_73`,
    CASE
      WHEN 0 = CAST(0 AS INT64)
      THEN 1
      WHEN `bfcol_52` = 1
      THEN 1
      WHEN `bfcol_52` = CAST(0 AS INT64) AND 0 < CAST(0 AS INT64)
      THEN CAST('Infinity' AS FLOAT64)
      WHEN ABS(`bfcol_52`) = CAST('Infinity' AS FLOAT64)
      THEN POWER(
        `bfcol_52`,
        CASE
          WHEN ABS(0) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
          ELSE 0
        END
      )
      WHEN ABS(0) > 9007199254740992
      THEN POWER(
        `bfcol_52`,
        CASE
          WHEN ABS(0) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
          ELSE 0
        END
      )
      WHEN `bfcol_52` < CAST(0 AS INT64) AND NOT CAST(0 AS INT64) = 0
      THEN CAST('NaN' AS FLOAT64)
      WHEN `bfcol_52` <> CAST(0 AS INT64) AND 0 * LN(ABS(`bfcol_52`)) > 709.78
      THEN CAST('Infinity' AS FLOAT64) * CASE
        WHEN `bfcol_52` < CAST(0 AS INT64) AND MOD(CAST(0 AS INT64), 2) = 1
        THEN -1
        ELSE 1
      END
      ELSE POWER(
        `bfcol_52`,
        CASE
          WHEN ABS(0) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(0)
          ELSE 0
        END
      )
    END AS `bfcol_74`
  FROM `bfcte_5`
), `bfcte_7` AS (
  SELECT
    *,
    `bfcol_66` AS `bfcol_84`,
    `bfcol_67` AS `bfcol_85`,
    `bfcol_68` AS `bfcol_86`,
    `bfcol_69` AS `bfcol_87`,
    `bfcol_70` AS `bfcol_88`,
    `bfcol_71` AS `bfcol_89`,
    `bfcol_72` AS `bfcol_90`,
    `bfcol_73` AS `bfcol_91`,
    `bfcol_74` AS `bfcol_92`,
    CASE
      WHEN `bfcol_67` <> 0 AND 1 * LN(ABS(`bfcol_67`)) > 43.66827237527655
      THEN NULL
      ELSE CAST(POWER(CAST(`bfcol_67` AS NUMERIC), 1) AS INT64)
    END AS `bfcol_93`
  FROM `bfcte_6`
), `bfcte_8` AS (
  SELECT
    *,
    `bfcol_84` AS `bfcol_104`,
    `bfcol_85` AS `bfcol_105`,
    `bfcol_86` AS `bfcol_106`,
    `bfcol_87` AS `bfcol_107`,
    `bfcol_88` AS `bfcol_108`,
    `bfcol_89` AS `bfcol_109`,
    `bfcol_90` AS `bfcol_110`,
    `bfcol_91` AS `bfcol_111`,
    `bfcol_92` AS `bfcol_112`,
    `bfcol_93` AS `bfcol_113`,
    CASE
      WHEN 1 = CAST(0 AS INT64)
      THEN 1
      WHEN `bfcol_86` = 1
      THEN 1
      WHEN `bfcol_86` = CAST(0 AS INT64) AND 1 < CAST(0 AS INT64)
      THEN CAST('Infinity' AS FLOAT64)
      WHEN ABS(`bfcol_86`) = CAST('Infinity' AS FLOAT64)
      THEN POWER(
        `bfcol_86`,
        CASE
          WHEN ABS(1) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
          ELSE 1
        END
      )
      WHEN ABS(1) > 9007199254740992
      THEN POWER(
        `bfcol_86`,
        CASE
          WHEN ABS(1) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
          ELSE 1
        END
      )
      WHEN `bfcol_86` < CAST(0 AS INT64) AND NOT CAST(1 AS INT64) = 1
      THEN CAST('NaN' AS FLOAT64)
      WHEN `bfcol_86` <> CAST(0 AS INT64) AND 1 * LN(ABS(`bfcol_86`)) > 709.78
      THEN CAST('Infinity' AS FLOAT64) * CASE
        WHEN `bfcol_86` < CAST(0 AS INT64) AND MOD(CAST(1 AS INT64), 2) = 1
        THEN -1
        ELSE 1
      END
      ELSE POWER(
        `bfcol_86`,
        CASE
          WHEN ABS(1) > 9007199254740992
          THEN CAST('Infinity' AS FLOAT64) * SIGN(1)
          ELSE 1
        END
      )
    END AS `bfcol_114`
  FROM `bfcte_7`
)
SELECT
  `bfcol_104` AS `rowindex`,
  `bfcol_105` AS `int64_col`,
  `bfcol_106` AS `float64_col`,
  `bfcol_107` AS `int_pow_int`,
  `bfcol_108` AS `int_pow_float`,
  `bfcol_109` AS `float_pow_int`,
  `bfcol_110` AS `float_pow_float`,
  `bfcol_111` AS `int_pow_0`,
  `bfcol_112` AS `float_pow_0`,
  `bfcol_113` AS `int_pow_1`,
  `bfcol_114` AS `float_pow_1`
FROM `bfcte_8`