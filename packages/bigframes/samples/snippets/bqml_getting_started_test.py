# Copyright 2023 Google LLC
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


def test_bqml_getting_started(random_model_id: str) -> None:
    your_model_id = random_model_id  # for example: bqml_tutorial.sample_model

    # [START bigquery_dataframes_bqml_getting_started_tutorial]
    from bigframes.ml.linear_model import LogisticRegression
    import bigframes.pandas as bpd

    # Start by selecting the data you'll use for training. `read_gbq` accepts
    # either a SQL query or a table ID. Since this example selects from multiple
    # tables via a wildcard, use SQL to define this data. Watch issue
    # https://github.com/googleapis/python-bigquery-dataframes/issues/169
    # for updates to `read_gbq` to support wildcard tables.

    df = bpd.read_gbq_table(
        "bigquery-public-data.google_analytics_sample.ga_sessions_*",
        filters=[
            ("_table_suffix", ">=", "20160801"),
            ("_table_suffix", "<=", "20170630"),
        ],
    )

    # Extract the total number of transactions within
    # the Google Analytics session.
    #
    # Because the totals column is a STRUCT data type, call
    # Series.struct.field("transactions") to extract the transactions field.
    # See the reference documentation below:
    # https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.structs.StructAccessor#bigframes_operations_structs_StructAccessor_field
    transactions = df["totals"].struct.field("transactions")

    # The "label" values represent the outcome of the model's
    # prediction. In this case, the model predicts if there are any
    # ecommerce transactions within the Google Analytics session.
    # If the number of transactions is NULL, the value in the label
    # column is set to 0. Otherwise, it is set to 1.
    label = transactions.notnull().map({True: 1, False: 0}).rename("label")

    # Extract the operating system of the visitor's device.
    operating_system = df["device"].struct.field("operatingSystem")
    operating_system = operating_system.fillna("")

    # Extract whether the visitor's device is a mobile device.
    is_mobile = df["device"].struct.field("isMobile")

    # Extract the country from which the sessions originated, based on the IP address.
    country = df["geoNetwork"].struct.field("country").fillna("")

    # Extract the total number of page views within the session.
    pageviews = df["totals"].struct.field("pageviews").fillna(0)

    # Combine all the feature columns into a single DataFrame
    # to use as training data.
    features = bpd.DataFrame(
        {
            "os": operating_system,
            "is_mobile": is_mobile,
            "country": country,
            "pageviews": pageviews,
        }
    )

    # Logistic Regression model splits data into two classes, giving the
    # a confidence score that the data is in one of the classes.
    model = LogisticRegression()
    model.fit(features, label)

    # The model.fit() call above created a temporary model.
    # Use the to_gbq() method to write to a permanent location.
    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.sample_model",
        replace=True,
    )
    # [END bigquery_dataframes_bqml_getting_started_tutorial]

    # [START bigquery_dataframes_bqml_getting_started_tutorial_evaluate]
    import bigframes.pandas as bpd

    # Select model you'll use for evaluating. `read_gbq_model` loads model data from a
    # BigQuery, but you could also use the `model` object from the previous steps.
    model = bpd.read_gbq_model(
        your_model_id,  # For example: "bqml_tutorial.sample_model",
    )

    # The filters parameter limits the number of tables scanned by the query.
    # The date range scanned is July 1, 2017 to August 1, 2017. This is the
    # data you're using to evaluate the predictive performance of the model.
    # It was collected in the month immediately following the time period
    # spanned by the training data.
    df = bpd.read_gbq_table(
        "bigquery-public-data.google_analytics_sample.ga_sessions_*",
        filters=[
            ("_table_suffix", ">=", "20170701"),
            ("_table_suffix", "<=", "20170801"),
        ],
    )

    transactions = df["totals"].struct.field("transactions")
    label = transactions.notnull().map({True: 1, False: 0}).rename("label")
    operating_system = df["device"].struct.field("operatingSystem")
    operating_system = operating_system.fillna("")
    is_mobile = df["device"].struct.field("isMobile")
    country = df["geoNetwork"].struct.field("country").fillna("")
    pageviews = df["totals"].struct.field("pageviews").fillna(0)
    features = bpd.DataFrame(
        {
            "os": operating_system,
            "is_mobile": is_mobile,
            "country": country,
            "pageviews": pageviews,
        }
    )

    # Some models include a convenient .score(X, y) method for evaluation with a preset accuracy metric:

    # Because you performed a logistic regression, the results include the following columns:

    # - precision — A metric for classification models. Precision identifies the frequency with
    # which a model was correct when predicting the positive class.

    # - recall — A metric for classification models that answers the following question:
    # Out of all the possible positive labels, how many did the model correctly identify?

    # - accuracy — Accuracy is the fraction of predictions that a classification model got right.

    # - f1_score — A measure of the accuracy of the model. The f1 score is the harmonic average of
    # the precision and recall. An f1 score's best value is 1. The worst value is 0.

    # - log_loss — The loss function used in a logistic regression. This is the measure of how far the
    # model's predictions are from the correct labels.

    # - roc_auc — The area under the ROC curve. This is the probability that a classifier is more confident that
    # a randomly chosen positive example
    # is actually positive than that a randomly chosen negative example is positive. For more information,
    # see ['Classification']('https://developers.google.com/machine-learning/crash-course/classification/video-lecture')
    # in the Machine Learning Crash Course.

    model.score(features, label)
    #    precision    recall  accuracy  f1_score  log_loss   roc_auc
    # 0   0.412621  0.079143  0.985074  0.132812  0.049764  0.974285
    # [1 rows x 6 columns]
    # [END bigquery_dataframes_bqml_getting_started_tutorial_evaluate]

    # [START bigquery_dataframes_bqml_getting_started_tutorial_predict_by_country]
    import bigframes.pandas as bpd

    # Select model you'll use for predicting.
    # `read_gbq_model` loads model data from
    # BigQuery, but you could also use the `model`
    # object from the previous steps.
    model = bpd.read_gbq_model(
        your_model_id,  # For example: "bqml_tutorial.sample_model",
    )

    # The filters parameter limits the number of tables scanned by the query.
    # The date range scanned is July 1, 2017 to August 1, 2017. This is the
    # data you're using to make the prediction.
    # It was collected in the month immediately following the time period
    # spanned by the training data.
    df = bpd.read_gbq_table(
        "bigquery-public-data.google_analytics_sample.ga_sessions_*",
        filters=[
            ("_table_suffix", ">=", "20170701"),
            ("_table_suffix", "<=", "20170801"),
        ],
    )

    operating_system = df["device"].struct.field("operatingSystem")
    operating_system = operating_system.fillna("")
    is_mobile = df["device"].struct.field("isMobile")
    country = df["geoNetwork"].struct.field("country").fillna("")
    pageviews = df["totals"].struct.field("pageviews").fillna(0)
    features = bpd.DataFrame(
        {
            "os": operating_system,
            "is_mobile": is_mobile,
            "country": country,
            "pageviews": pageviews,
        }
    )
    # Use Logistic Regression predict method to predict results
    # using your model.
    # Find more information here in
    # [BigFrames](https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.linear_model.LogisticRegression#bigframes_ml_linear_model_LogisticRegression_predict)

    predictions = model.predict(features)

    # Call groupby method to group predicted_label by country.
    # Call sum method to get the total_predicted_label by country.
    total_predicted_purchases = predictions.groupby(["country"])[
        ["predicted_label"]
    ].sum()

    # Call the sort_values method with the parameter
    # ascending = False to get the highest values.
    # Call head method to limit to the 10 highest values.
    total_predicted_purchases.sort_values(ascending=False).head(10)

    # country
    # United States    220
    # Taiwan             8
    # Canada             7
    # India              2
    # Japan              2
    # Turkey             2
    # Australia          1
    # Brazil             1
    # Germany            1
    # Guyana             1
    # Name: predicted_label, dtype: Int64

    # [END bigquery_dataframes_bqml_getting_started_tutorial_predict_by_country]

    # [START bigquery_dataframes_bqml_getting_started_tutorial_predict_by_visitor]

    import bigframes.pandas as bpd

    # Select model you'll use for predicting.
    # `read_gbq_model` loads model data from
    # BigQuery, but you could also use the `model`
    # object from the previous steps.
    model = bpd.read_gbq_model(
        your_model_id,  # For example: "bqml_tutorial.sample_model",
    )

    # The filters parameter limits the number of tables scanned by the query.
    # The date range scanned is July 1, 2017 to August 1, 2017. This is the
    # data you're using to make the prediction.
    # It was collected in the month immediately following the time period
    # spanned by the training data.
    df = bpd.read_gbq_table(
        "bigquery-public-data.google_analytics_sample.ga_sessions_*",
        filters=[
            ("_table_suffix", ">=", "20170701"),
            ("_table_suffix", "<=", "20170801"),
        ],
    )

    operating_system = df["device"].struct.field("operatingSystem")
    operating_system = operating_system.fillna("")
    is_mobile = df["device"].struct.field("isMobile")
    country = df["geoNetwork"].struct.field("country").fillna("")
    pageviews = df["totals"].struct.field("pageviews").fillna(0)
    full_visitor_id = df["fullVisitorId"]

    features = bpd.DataFrame(
        {
            "os": operating_system,
            "is_mobile": is_mobile,
            "country": country,
            "pageviews": pageviews,
            "fullVisitorId": full_visitor_id,
        }
    )

    predictions = model.predict(features)

    # Call groupby method to group predicted_label by visitor.
    # Call sum method to get the total_predicted_label by visitor.
    total_predicted_purchases = predictions.groupby(["fullVisitorId"])[
        ["predicted_label"]
    ].sum()

    # Call the sort_values method with the parameter
    # ascending = False to get the highest values.
    # Call head method to limit to the 10 highest values.
    total_predicted_purchases.sort_values(ascending=False).head(10)

    # fullVisitorId
    # 9417857471295131045    4
    # 0376394056092189113    2
    # 0456807427403774085    2
    # 057693500927581077     2
    # 112288330928895942     2
    # 1280993661204347450    2
    # 2105122376016897629    2
    # 2158257269735455737    2
    # 2969418676126258798    2
    # 489038402765684003     2
    # Name: predicted_label, dtype: Int64


# [END bigquery_dataframes_bqml_getting_started_tutorial_predict_by_visitor]
