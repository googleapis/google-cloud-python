MERGE INTO `bigframes-dev`.`sqlglot_test`.`dest_table`
USING (
  SELECT
    *
  FROM `source_table`
)
ON FALSE
WHEN NOT MATCHED BY SOURCE THEN DELETE
WHEN NOT MATCHED THEN INSERT ROW