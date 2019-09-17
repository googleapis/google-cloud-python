# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Type

from .base import ProductSearchTransport
from .grpc import ProductSearchGrpcTransport


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[ProductSearchTransport]]
_transport_registry["grpc"] = ProductSearchGrpcTransport


__all__ = ("ProductSearchTransport", "ProductSearchGrpcTransport")
