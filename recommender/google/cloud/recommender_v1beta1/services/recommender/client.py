# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.recommender_v1beta1.services.recommender import pagers
from google.cloud.recommender_v1beta1.types import recommendation
from google.cloud.recommender_v1beta1.types import recommender_service

from .transports.base import RecommenderTransport
from .transports.grpc import RecommenderGrpcTransport


class RecommenderMeta(type):
    """Metaclass for the Recommender client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[RecommenderTransport]]
    _transport_registry["grpc"] = RecommenderGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[RecommenderTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class Recommender(metaclass=RecommenderMeta):
    """Provides recommendations for cloud customers for various
    categories like performance optimization, cost savings,
    reliability, feature discovery, etc. These recommendations are
    generated automatically based on analysis of user resources,
    configuration and monitoring metrics.
    """

    def __init__(
        self,
        *,
        host: str = "recommender.googleapis.com",
        credentials: credentials.Credentials = None,
        transport: Union[str, RecommenderTransport] = None
    ) -> None:
        """Instantiate the recommender.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RecommenderTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
        """
        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, RecommenderTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(credentials=credentials, host=host)

    def list_recommendations(
        self,
        request: recommender_service.ListRecommendationsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = ()
    ) -> pagers.ListRecommendationsPager:
        r"""Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Args:
            request (:class:`~.recommender_service.ListRecommendationsRequest`):
                The request object. Request for the
                `ListRecommendations` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListRecommendationsPager:
                Response to the ``ListRecommendations`` method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = recommender_service.ListRecommendationsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_recommendations,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRecommendationsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_recommendation(
        self,
        request: recommender_service.GetRecommendationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = ()
    ) -> recommendation.Recommendation:
        r"""Gets the requested recommendation. Requires the
        recommender.*.get IAM permission for the specified recommender.

        Args:
            request (:class:`~.recommender_service.GetRecommendationRequest`):
                The request object. Request to the `GetRecommendation`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recommendation.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        request = recommender_service.GetRecommendationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_recommendation,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                )
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def mark_recommendation_claimed(
        self,
        request: recommender_service.MarkRecommendationClaimedRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = ()
    ) -> recommendation.Recommendation:
        r"""Mark the Recommendation State as Claimed. Users can use this
        method to indicate to the Recommender API that they are starting
        to apply the recommendation themselves. This stops the
        recommendation content from being updated.

        MarkRecommendationClaimed can be applied to recommendations in
        CLAIMED, SUCCEEDED, FAILED, or ACTIVE state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`~.recommender_service.MarkRecommendationClaimedRequest`):
                The request object. Request for the
                `MarkRecommendationClaimed` Method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recommendation.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        request = recommender_service.MarkRecommendationClaimedRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.mark_recommendation_claimed,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def mark_recommendation_succeeded(
        self,
        request: recommender_service.MarkRecommendationSucceededRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = ()
    ) -> recommendation.Recommendation:
        r"""Mark the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation was successful.
        This stops the recommendation content from being updated.

        MarkRecommendationSucceeded can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`~.recommender_service.MarkRecommendationSucceededRequest`):
                The request object. Request for the
                `MarkRecommendationSucceeded` Method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recommendation.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        request = recommender_service.MarkRecommendationSucceededRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.mark_recommendation_succeeded,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def mark_recommendation_failed(
        self,
        request: recommender_service.MarkRecommendationFailedRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = ()
    ) -> recommendation.Recommendation:
        r"""Mark the Recommendation State as Failed. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation failed. This
        stops the recommendation content from being updated.

        MarkRecommendationFailed can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (:class:`~.recommender_service.MarkRecommendationFailedRequest`):
                The request object. Request for the
                `MarkRecommendationFailed` Method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recommendation.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        request = recommender_service.MarkRecommendationFailedRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.mark_recommendation_failed,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-recommender").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("Recommender",)
