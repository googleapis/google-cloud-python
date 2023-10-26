"""Base classes for all estimators."""

# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
# License: BSD 3 clause
# Original location: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/base.py

from __future__ import annotations

import inspect
from typing import Any, Dict, List

from bigframes import constants


class BaseEstimator:
    """Base class for all estimators.

    .. note::
        All estimators should specify all the parameters that can be set
        at the class level in their ``__init__`` as explicit keyword
        arguments (no ``*args`` or ``**kwargs``).
    """

    @classmethod
    def _get_param_names(cls: type[BaseEstimator]) -> List[str]:
        """Get parameter names for the estimator"""
        # fetch the constructor or the original constructor before
        # deprecation wrapping if any
        init = getattr(cls.__init__, "deprecated_original", cls.__init__)
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        # introspect the constructor arguments to find the model parameters
        # to represent
        init_signature = inspect.signature(init)
        # Consider the constructor parameters excluding 'self'
        parameters = [
            p
            for p in init_signature.parameters.values()
            if p.name != "self" and p.kind != p.VAR_KEYWORD
        ]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError(
                    "Estimators should always "
                    "specify their parameters in the signature"
                    " of their __init__ (no varargs)."
                    " %s with constructor %s doesn't "
                    " follow this convention." % (cls, init_signature)
                )
        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """Get parameters for this estimator.

        Args:
            deep (bool, default True):
                Default ``True``. If True, will return the parameters for this
                estimator and contained subobjects that are estimators.

        Returns:
            Dictionary: A dictionary of parameter names mapped to their values.
        """
        out: Dict = dict()
        for key in self._get_param_names():
            value = getattr(self, key)
            if deep and hasattr(value, "get_params") and not isinstance(value, type):
                deep_items = value.get_params().items()
                out.update((key + "__" + k, val) for k, val in deep_items)
            out[key] = value
        return out


class ClassifierMixin:
    """Mixin class for all classifiers."""

    _estimator_type = "classifier"

    def score(self, X, y):
        """Return the mean accuracy on the given test data and labels.

        In multi-label classification, this is the subset accuracy
        which is a harsh metric since you require for each sample that
        each label set be correctly predicted.

        .. note::

            Output matches that of the BigQuery ML.EVALUTE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#classification_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). Test samples.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples,) or (n_samples, n_outputs). True
                labels for `X`.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame of the evaluation result.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class RegressorMixin:
    """Mixin class for all regression estimators."""

    _estimator_type = "regressor"

    def score(self, X, y):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUTE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#regression_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Test samples. For
                some estimators this may be a precomputed kernel matrix or a
                list of generic objects instead with shape
                ``(n_samples, n_samples_fitted)``, where ``n_samples_fitted``
                is the number of samples used in the fitting for the estimator.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_outputs). True
                values for `X`.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame of the evaluation result.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class TransformerMixin:
    """Mixin class for all transformers."""

    def fit_transform(self, X, y=None):
        """Fit to data, then transform it.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features).
                Input samples.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_outputs). Default None.
                Target values (None for unsupervised transformations).

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_features_new)
                Transformed DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class MetaEstimatorMixin:
    _required_parameters = ["estimator"]
    """Mixin class for all meta estimators in scikit-learn."""
