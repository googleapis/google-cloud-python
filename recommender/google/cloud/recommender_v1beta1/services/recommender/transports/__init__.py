# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Type

from .base import RecommenderTransport
from .grpc import RecommenderGrpcTransport


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[RecommenderTransport]]
_transport_registry["grpc"] = RecommenderGrpcTransport


__all__ = ("RecommenderTransport", "RecommenderGrpcTransport")
