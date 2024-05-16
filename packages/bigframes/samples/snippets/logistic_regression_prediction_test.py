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

"""BigQuery DataFrames code samples for
https://cloud.google.com/bigquery/docs/logistic-regression-prediction.
"""


def test_logistic_regression_prediction(random_model_id: str) -> None:
    your_model_id = random_model_id

    # [START bigquery_dataframes_logistic_regression_prediction_examine]
    import bigframes.pandas as bpd

    df = bpd.read_gbq(
        "bigquery-public-data.ml_datasets.census_adult_income",
        columns=(
            "age",
            "workclass",
            "marital_status",
            "education_num",
            "occupation",
            "hours_per_week",
            "income_bracket",
            "functional_weight",
        ),
        max_results=100,
    )
    df.peek()
    # Output:
    # age      workclass       marital_status  education_num          occupation  hours_per_week income_bracket  functional_weight
    #  47      Local-gov   Married-civ-spouse             13      Prof-specialty              40           >50K             198660
    #  56        Private        Never-married              9        Adm-clerical              40          <=50K              85018
    #  40        Private   Married-civ-spouse             12        Tech-support              40           >50K             285787
    #  34   Self-emp-inc   Married-civ-spouse              9        Craft-repair              54           >50K             207668
    #  23        Private   Married-civ-spouse             10   Handlers-cleaners              40          <=50K              40060
    # [END bigquery_dataframes_logistic_regression_prediction_examine]

    # [START bigquery_dataframes_logistic_regression_prediction_prepare]
    import bigframes.pandas as bpd

    input_data = bpd.read_gbq(
        "bigquery-public-data.ml_datasets.census_adult_income",
        columns=(
            "age",
            "workclass",
            "marital_status",
            "education_num",
            "occupation",
            "hours_per_week",
            "income_bracket",
            "functional_weight",
        ),
    )
    input_data["dataframe"] = bpd.Series("training", index=input_data.index,).case_when(
        [
            (((input_data["functional_weight"] % 10) == 8), "evaluation"),
            (((input_data["functional_weight"] % 10) == 9), "prediction"),
        ]
    )
    del input_data["functional_weight"]
    # [END bigquery_dataframes_logistic_regression_prediction_prepare]

    # [START bigquery_dataframes_logistic_regression_prediction_create_model]
    import bigframes.ml.linear_model

    # input_data is defined in an earlier step.
    training_data = input_data[input_data["dataframe"] == "training"]
    X = training_data.drop(columns=["income_bracket", "dataframe"])
    y = training_data["income_bracket"]

    census_model = bigframes.ml.linear_model.LogisticRegression(
        # Balance the class labels in the training data by setting
        # class_weight="balanced".
        #
        # By default, the training data is unweighted. If the labels
        # in the training data are imbalanced, the model may learn to
        # predict the most popular class of labels more heavily. In
        # this case, most of the respondents in the dataset are in the
        # lower income bracket. This may lead to a model that predicts
        # the lower income bracket too heavily. Class weights balance
        # the class labels by calculating the weights for each class in
        # inverse proportion to the frequency of that class.
        class_weight="balanced",
        max_iterations=15,
    )
    census_model.fit(X, y)

    census_model.to_gbq(
        your_model_id,  # For example: "your-project.census.census_model"
        replace=True,
    )
    # [END bigquery_dataframes_logistic_regression_prediction_create_model]

    # [START bigquery_dataframes_logistic_regression_prediction_evaluate_model]
    # Select model you'll use for predictions. `read_gbq_model` loads model
    # data from BigQuery, but you could also use the `census_model` object
    # from previous steps.
    census_model = bpd.read_gbq_model(
        your_model_id,  # For example: "your-project.census.census_model"
    )

    # input_data is defined in an earlier step.
    evaluation_data = input_data[input_data["dataframe"] == "evaluation"]
    X = evaluation_data.drop(columns=["income_bracket", "dataframe"])
    y = evaluation_data["income_bracket"]

    # The score() method evaluates how the model performs compared to the
    # actual data. Output DataFrame matches that of ML.EVALUATE().
    score = census_model.score(X, y)
    score.peek()
    # Output:
    #    precision    recall  accuracy  f1_score  log_loss   roc_auc
    # 0   0.685764  0.536685   0.83819  0.602134  0.350417  0.882953
    # [END bigquery_dataframes_logistic_regression_prediction_evaluate_model]

    # [START bigquery_dataframes_logistic_regression_prediction_predict_income_bracket]
    # Select model you'll use for predictions. `read_gbq_model` loads model
    # data from BigQuery, but you could also use the `census_model` object
    # from previous steps.
    census_model = bpd.read_gbq_model(
        your_model_id,  # For example: "your-project.census.census_model"
    )

    # input_data is defined in an earlier step.
    prediction_data = input_data[input_data["dataframe"] == "prediction"]

    predictions = census_model.predict(prediction_data)
    predictions.peek()
    # Output:
    #           predicted_income_bracket                     predicted_income_bracket_probs  age workclass  ... occupation  hours_per_week income_bracket   dataframe
    # 18004                    <=50K  [{'label': ' >50K', 'prob': 0.0763305999358786...   75         ?  ...          ?               6          <=50K  prediction
    # 18886                    <=50K  [{'label': ' >50K', 'prob': 0.0448866871906495...   73         ?  ...          ?              22           >50K  prediction
    # 31024                    <=50K  [{'label': ' >50K', 'prob': 0.0362982319421936...   69         ?  ...          ?               1          <=50K  prediction
    # 31022                    <=50K  [{'label': ' >50K', 'prob': 0.0787836112058324...   75         ?  ...          ?               5          <=50K  prediction
    # 23295                    <=50K  [{'label': ' >50K', 'prob': 0.3385373037905673...   78         ?  ...          ?              32          <=50K  prediction
    # [END bigquery_dataframes_logistic_regression_prediction_predict_income_bracket]

    # TODO(tswast): Implement ML.EXPLAIN_PREDICT() and corresponding sample.
    # TODO(tswast): Implement ML.GLOBAL_EXPLAIN() and corresponding sample.
