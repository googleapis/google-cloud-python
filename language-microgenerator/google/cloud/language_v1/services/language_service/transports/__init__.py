# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Type

from .base import LanguageServiceTransport
from .grpc import LanguageServiceGrpcTransport


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[LanguageServiceTransport]]
_transport_registry["grpc"] = LanguageServiceGrpcTransport


__all__ = ("LanguageServiceTransport", "LanguageServiceGrpcTransport")
