# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def test_linear_regression(random_model_id: str) -> None:
    your_model_id = random_model_id
    # [START bigquery_dataframes_bqml_linear_regression]
    from bigframes.ml.linear_model import LinearRegression
    import bigframes.pandas as bpd

    # Load data from BigQuery
    bq_df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # Drop rows with nulls to get training data
    training_data = bq_df.dropna(subset=["body_mass_g"])

    # Specify your feature (or input) columns and the label (or output) column:
    feature_columns = training_data.drop(columns=["body_mass_g"])
    label_columns = training_data[["body_mass_g"]]

    # Create the linear model
    model = LinearRegression()
    model.fit(feature_columns, label_columns)
    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.penguins_model"
        replace=True,
    )
    # [END bigquery_dataframes_bqml_linear_regression]
    # [START bigquery_dataframes_bqml_linear_evaluate]
    import bigframes.pandas as bpd

    # Select the model you will be evaluating. `read_gbq_model` loads model data from
    # BigQuery, but you could also use the `model` object from the previous steps.
    model = bpd.read_gbq_model(
        your_model_id,  # For example: "bqml_tutorial.penguins_model"
    )

    # Score the model with input data defined in an earlier step to compare
    # model predictions on feature_columns to true labels in label_columns.
    score = model.score(feature_columns, label_columns)
    # Expected output results:
    # index  mean_absolute_error  mean_squared_error  mean_squared_log_error  median_absolute_error  r2_score  explained_variance
    #   0        227.012237         81838.159892            0.00507                173.080816        0.872377    0.872377
    #   1 rows x 6 columns
    # [END bigquery_dataframes_bqml_linear_evaluate]
    # [START bigquery_dataframes_bqml_linear_predict]
    # Select the model you'll use for predictions. `read_gbq_model` loads
    # model data from BigQuery, but you could also use the `model` object
    # object from previous steps.
    model = bpd.read_gbq_model(
        your_model_id,
        # For example: "bqml_tutorial.penguins_model",
    )

    # Load data from BigQuery
    bq_df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # Use 'contains' function to filter by island containing the string
    # "Biscoe".
    biscoe_data = bq_df.loc[bq_df["island"].str.contains("Biscoe")]

    result = model.predict(biscoe_data)

    # Expected output results:
    #     predicted_body_mass_g  	      species	                island	 culmen_length_mm  culmen_depth_mm   body_mass_g 	flipper_length_mm	sex
    # 23	  4681.782896	   Gentoo penguin (Pygoscelis papua)	Biscoe	      <NA>	            <NA>	        <NA>	          <NA>	        <NA>
    # 332	  4740.7907	       Gentoo penguin (Pygoscelis papua)	Biscoe	      46.2	            14.4	        214.0	          4650.0	    <NA>
    # 160	  4731.310452	   Gentoo penguin (Pygoscelis papua)	Biscoe	      44.5	            14.3	        216.0	          4100.0	    <NA>
    # [END bigquery_dataframes_bqml_linear_predict]
    # [START bigquery_dataframes_bqml_linear_predict_explain]
    # Use 'predict_explain' function to understand why the model is generating these prediction results.
    # 'predict_explain'is an extended version of the 'predict' function that not only outputs prediction results, but also outputs additional columns to explain the prediction results.
    # Using the trained model and utilizing data specific to Biscoe Island, explain the predictions of the top 3 features
    explained = model.predict_explain(biscoe_data, top_k_features=3)

    # Expected results:
    #   predicted_body_mass_g               top_feature_attributions	        baseline_prediction_value	prediction_value	approximation_error	              species	            island	culmen_length_mm	culmen_depth_mm	flipper_length_mm	body_mass_g	    sex
    # 0	 5413.510134	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          5413.510134	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    45.2	              16.4	        223.0	           5950.0	    MALE
    # 1	 4768.351092            [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          4768.351092	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.5	              14.5	        213.0	           4400.0	   FEMALE
    # 2	 3235.896372	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          3235.896372	            0.0	        Adelie Penguin (Pygoscelis adeliae)	Biscoe	    37.7	              16.0          183.0	           3075.0	   FEMALE
    # 3	 5349.603734	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          5349.603734	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.4	              15.6	        221.0	           5000.0	    MALE
    # 4	 4637.165037	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          4637.165037	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.1	              13.2	        211.0	           4500.0	   FEMALE
    # [END bigquery_dataframes_bqml_linear_predict_explain]
    # [START bigquery_dataframes_bqml_linear_global_explain]
    # To use the `global_explain()` function, the model must be recreated with `enable_global_explain` set to `True`.
    model = LinearRegression(enable_global_explain=True)

    # The model must the be fitted before it can be saved to BigQuery and then explained.
    training_data = bq_df.dropna(subset=["body_mass_g"])
    X = training_data.drop(columns=["body_mass_g"])
    y = training_data[["body_mass_g"]]
    model.fit(X, y)
    model.to_gbq("bqml_tutorial.penguins_model", replace=True)

    # Explain the model
    explain_model = model.global_explain()

    # Expected results:
    #                       attribution
    # feature
    # island	            5737.315921
    # species	            4073.280549
    # sex	                622.070896
    # flipper_length_mm	    193.612051
    # culmen_depth_mm	    117.084944
    # culmen_length_mm	    94.366793
    # [END bigquery_dataframes_bqml_linear_global_explain]
    assert explain_model is not None
    assert feature_columns is not None
    assert label_columns is not None
    assert model is not None
    assert score is not None
    assert result is not None
    assert explained is not None
