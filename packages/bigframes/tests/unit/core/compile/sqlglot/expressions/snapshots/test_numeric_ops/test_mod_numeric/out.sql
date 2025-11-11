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
      WHEN `int64_col` = CAST(0 AS INT64)
      THEN CAST(0 AS INT64) * `int64_col`
      WHEN `int64_col` < CAST(0 AS INT64)
      AND (
        MOD(`int64_col`, `int64_col`)
      ) > CAST(0 AS INT64)
      THEN `int64_col` + (
        MOD(`int64_col`, `int64_col`)
      )
      WHEN `int64_col` > CAST(0 AS INT64)
      AND (
        MOD(`int64_col`, `int64_col`)
      ) < CAST(0 AS INT64)
      THEN `int64_col` + (
        MOD(`int64_col`, `int64_col`)
      )
      ELSE MOD(`int64_col`, `int64_col`)
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
      WHEN -(
        `bfcol_7`
      ) = CAST(0 AS INT64)
      THEN CAST(0 AS INT64) * `bfcol_7`
      WHEN -(
        `bfcol_7`
      ) < CAST(0 AS INT64)
      AND (
        MOD(`bfcol_7`, -(
          `bfcol_7`
        ))
      ) > CAST(0 AS INT64)
      THEN -(
        `bfcol_7`
      ) + (
        MOD(`bfcol_7`, -(
          `bfcol_7`
        ))
      )
      WHEN -(
        `bfcol_7`
      ) > CAST(0 AS INT64)
      AND (
        MOD(`bfcol_7`, -(
          `bfcol_7`
        ))
      ) < CAST(0 AS INT64)
      THEN -(
        `bfcol_7`
      ) + (
        MOD(`bfcol_7`, -(
          `bfcol_7`
        ))
      )
      ELSE MOD(`bfcol_7`, -(
        `bfcol_7`
      ))
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
      WHEN 1 = CAST(0 AS INT64)
      THEN CAST(0 AS INT64) * `bfcol_15`
      WHEN 1 < CAST(0 AS INT64) AND (
        MOD(`bfcol_15`, 1)
      ) > CAST(0 AS INT64)
      THEN 1 + (
        MOD(`bfcol_15`, 1)
      )
      WHEN 1 > CAST(0 AS INT64) AND (
        MOD(`bfcol_15`, 1)
      ) < CAST(0 AS INT64)
      THEN 1 + (
        MOD(`bfcol_15`, 1)
      )
      ELSE MOD(`bfcol_15`, 1)
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
      WHEN 0 = CAST(0 AS INT64)
      THEN CAST(0 AS INT64) * `bfcol_25`
      WHEN 0 < CAST(0 AS INT64) AND (
        MOD(`bfcol_25`, 0)
      ) > CAST(0 AS INT64)
      THEN 0 + (
        MOD(`bfcol_25`, 0)
      )
      WHEN 0 > CAST(0 AS INT64) AND (
        MOD(`bfcol_25`, 0)
      ) < CAST(0 AS INT64)
      THEN 0 + (
        MOD(`bfcol_25`, 0)
      )
      ELSE MOD(`bfcol_25`, 0)
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
      WHEN CAST(`bfcol_38` AS BIGNUMERIC) = CAST(0 AS INT64)
      THEN CAST('NaN' AS FLOAT64) * CAST(`bfcol_38` AS BIGNUMERIC)
      WHEN CAST(`bfcol_38` AS BIGNUMERIC) < CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_38` AS BIGNUMERIC), CAST(`bfcol_38` AS BIGNUMERIC))
      ) > CAST(0 AS INT64)
      THEN CAST(`bfcol_38` AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_38` AS BIGNUMERIC), CAST(`bfcol_38` AS BIGNUMERIC))
      )
      WHEN CAST(`bfcol_38` AS BIGNUMERIC) > CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_38` AS BIGNUMERIC), CAST(`bfcol_38` AS BIGNUMERIC))
      ) < CAST(0 AS INT64)
      THEN CAST(`bfcol_38` AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_38` AS BIGNUMERIC), CAST(`bfcol_38` AS BIGNUMERIC))
      )
      ELSE MOD(CAST(`bfcol_38` AS BIGNUMERIC), CAST(`bfcol_38` AS BIGNUMERIC))
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
      WHEN CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC) = CAST(0 AS INT64)
      THEN CAST('NaN' AS FLOAT64) * CAST(`bfcol_52` AS BIGNUMERIC)
      WHEN CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC) < CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_52` AS BIGNUMERIC), CAST(-(
          `bfcol_52`
        ) AS BIGNUMERIC))
      ) > CAST(0 AS INT64)
      THEN CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_52` AS BIGNUMERIC), CAST(-(
          `bfcol_52`
        ) AS BIGNUMERIC))
      )
      WHEN CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC) > CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_52` AS BIGNUMERIC), CAST(-(
          `bfcol_52`
        ) AS BIGNUMERIC))
      ) < CAST(0 AS INT64)
      THEN CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_52` AS BIGNUMERIC), CAST(-(
          `bfcol_52`
        ) AS BIGNUMERIC))
      )
      ELSE MOD(CAST(`bfcol_52` AS BIGNUMERIC), CAST(-(
        `bfcol_52`
      ) AS BIGNUMERIC))
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
      WHEN CAST(1 AS BIGNUMERIC) = CAST(0 AS INT64)
      THEN CAST('NaN' AS FLOAT64) * CAST(`bfcol_68` AS BIGNUMERIC)
      WHEN CAST(1 AS BIGNUMERIC) < CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_68` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
      ) > CAST(0 AS INT64)
      THEN CAST(1 AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_68` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
      )
      WHEN CAST(1 AS BIGNUMERIC) > CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_68` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
      ) < CAST(0 AS INT64)
      THEN CAST(1 AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_68` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
      )
      ELSE MOD(CAST(`bfcol_68` AS BIGNUMERIC), CAST(1 AS BIGNUMERIC))
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
      WHEN CAST(0 AS BIGNUMERIC) = CAST(0 AS INT64)
      THEN CAST('NaN' AS FLOAT64) * CAST(`bfcol_86` AS BIGNUMERIC)
      WHEN CAST(0 AS BIGNUMERIC) < CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_86` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
      ) > CAST(0 AS INT64)
      THEN CAST(0 AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_86` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
      )
      WHEN CAST(0 AS BIGNUMERIC) > CAST(0 AS INT64)
      AND (
        MOD(CAST(`bfcol_86` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
      ) < CAST(0 AS INT64)
      THEN CAST(0 AS BIGNUMERIC) + (
        MOD(CAST(`bfcol_86` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
      )
      ELSE MOD(CAST(`bfcol_86` AS BIGNUMERIC), CAST(0 AS BIGNUMERIC))
    END AS `bfcol_114`
  FROM `bfcte_7`
)
SELECT
  `bfcol_104` AS `rowindex`,
  `bfcol_105` AS `int64_col`,
  `bfcol_106` AS `float64_col`,
  `bfcol_107` AS `int_mod_int`,
  `bfcol_108` AS `int_mod_int_neg`,
  `bfcol_109` AS `int_mod_1`,
  `bfcol_110` AS `int_mod_0`,
  `bfcol_111` AS `float_mod_float`,
  `bfcol_112` AS `float_mod_float_neg`,
  `bfcol_113` AS `float_mod_1`,
  `bfcol_114` AS `float_mod_0`
FROM `bfcte_8`