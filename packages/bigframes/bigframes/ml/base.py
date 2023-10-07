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

"""
Wraps primitives for machine learning with BQML

This library is an evolving attempt to
- implement BigQuery DataFrames API for BQML
- follow as close as possible the API design of SKLearn
    https://arxiv.org/pdf/1309.0238.pdf
"""

import abc
from typing import cast, Optional, TypeVar, Union

from bigframes.ml import core
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.base


class BaseEstimator(third_party.bigframes_vendored.sklearn.base.BaseEstimator, abc.ABC):
    """
    A BigQuery DataFrames machine learning component following the SKLearn API
    design Ref: https://bit.ly/3NyhKjN

    The estimator is the fundamental abstraction for all learning components. This includes learning
    algorithms, and also some preprocessing routines.

    This base class provides shared methods for inspecting parameters, and for building a consistent
    string representation of the component. By convention, the __init__ of all descendents will be
    assumed to be the list of hyperparameters.

    All descendents of this class should implement:
        def __init__(self, hyperparameter_1=default_1, hyperparameter_2=default_2, hyperparameter3, ...):
            '''Set hyperparameters'''
            self.hyperparameter_1 = hyperparameter_1
            self.hyperparameter_2 = hyperparameter_2
            self.hyperparameter3 = hyperparameter3
            ...
    Note: the object variable names must be exactly the same with parameter names. In order to utilize __repr__.

    fit(X, y) method is optional.

    The types of decendents of this class should be:

    1) Predictors
        These extend the interface with a .predict(self, x_test) method which predicts the target values
        according to the parameters that were calculated in .fit()

            def predict(self, x_test: Union[DataFrame, Series]) -> Union[DataFrame, Series]:
                '''Predict the target values according to the parameters that were calculated in .fit'''
                ...

    2) Transformers
        These extend the interface with .transform(self, x) and .fit_transform(x_train) methods, which
        apply data processing steps such as scaling that must be fitted to training data

            def transform(self, x: Union[DataFrame, Series]) -> Union[DataFrame, Series]:
                '''Transform the data according to the parameters that were calculated in .fit()'''
                ...

            def fit_transform(self, x_train: Union[DataFrame, Series], y_train: Union[DataFrame, Series]):
                '''Perform both fit() and transform()'''
                ...
    """

    def __repr__(self):
        """Print the estimator's constructor with all non-default parameter values"""

        # Estimator pretty printer adapted from Sklearn's, which is in turn an adaption of
        # the inbuilt pretty-printer in CPython
        import third_party.bigframes_vendored.cpython._pprint as adapted_pprint

        prettyprinter = adapted_pprint._EstimatorPrettyPrinter(
            compact=True, indent=1, indent_at_name=True, n_max_elements_to_show=30
        )

        return prettyprinter.pformat(self)


class Predictor(BaseEstimator):
    """A BigQuery DataFrames ML Model base class that can be used to predict outputs."""

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None

    @abc.abstractmethod
    def predict(self, X):
        pass

    _T = TypeVar("_T", bound="Predictor")

    def register(self: _T, vertex_ai_model_id: Optional[str] = None) -> _T:
        """Register the model to Vertex AI.

        After register, go to Google Cloud Console (https://console.cloud.google.com/vertex-ai/models)
        to manage the model registries.
        Refer to https://cloud.google.com/vertex-ai/docs/model-registry/introduction for more options.

        Args:
            vertex_ai_model_id (Optional[str], default None):
                optional string id as model id in Vertex. If not set, will by default to 'bigframes_{bq_model_id}'.
                Vertex Ai model id will be truncated to 63 characters due to its limitation.

        Returns:
            BigQuery DataFrames Model after register.
        """
        if not self._bqml_model:
            # TODO(garrettwu): find a more elegant way to do this.
            try:
                self._bqml_model = self._create_bqml_model()  # type: ignore
            except AttributeError:
                raise RuntimeError("A model must be trained before register.")
        self._bqml_model = cast(core.BqmlModel, self._bqml_model)

        self._bqml_model.register(vertex_ai_model_id)
        return self


class TrainablePredictor(Predictor):
    """A BigQuery DataFrames ML Model base class that can be used to fit and predict outputs.

    Also the predictor can be attached to a pipeline with transformers."""

    @abc.abstractmethod
    def _fit(self, X, y, transforms=None):
        pass

    @abc.abstractmethod
    def score(self, X, y):
        pass

    # TODO(b/291812029): move to Predictor after implement in LLM and imported models
    @abc.abstractmethod
    def to_gbq(self, model_name, replace):
        pass


class SupervisedTrainablePredictor(TrainablePredictor):
    """A BigQuery DataFrames ML Supervised Model base class that can be used to fit and predict outputs.

    Need to provide both X and y in supervised tasks."""

    _T = TypeVar("_T", bound="SupervisedTrainablePredictor")

    def fit(
        self: _T,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> _T:
        return self._fit(X, y)


class UnsupervisedTrainablePredictor(TrainablePredictor):
    """A BigQuery DataFrames ML Unsupervised Model base class that can be used to fit and predict outputs.

    Only need to provide both X (y is optional and ignored) in unsupervised tasks."""

    _T = TypeVar("_T", bound="UnsupervisedTrainablePredictor")

    def fit(
        self: _T,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Optional[Union[bpd.DataFrame, bpd.Series]] = None,
    ) -> _T:
        return self._fit(X, y)


class Transformer(BaseEstimator):
    """A BigQuery DataFrames Transformer base class that transforms data.

    Also the transformers can be attached to a pipeline with a predictor."""

    @abc.abstractmethod
    def fit(self, X, y):
        pass

    @abc.abstractmethod
    def transform(self, X):
        pass

    def fit_transform(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Optional[Union[bpd.DataFrame, bpd.Series]] = None,
    ) -> bpd.DataFrame:
        return self.fit(X, y).transform(X)


class LabelTransformer(BaseEstimator):
    """A BigQuery DataFrames Label Transformer base class that transforms data.

    Also the transformers can be attached to a pipeline with a predictor."""

    @abc.abstractmethod
    def fit(self, y):
        pass

    @abc.abstractmethod
    def transform(self, y):
        pass

    def fit_transform(
        self,
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        return self.fit(y).transform(y)
