CREATE MODEL `my_project.my_dataset.my_model`
OPTIONS(model_type = 'LINEAR_REG', input_label_cols = ['label'])
AS SELECT * FROM my_table
