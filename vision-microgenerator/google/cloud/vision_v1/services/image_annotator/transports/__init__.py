# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Type

from .base import ImageAnnotatorTransport
from .grpc import ImageAnnotatorGrpcTransport


# Compile a registry of transports.
_transport_registry = OrderedDict()  # type: Dict[str, Type[ImageAnnotatorTransport]]
_transport_registry["grpc"] = ImageAnnotatorGrpcTransport


__all__ = ("ImageAnnotatorTransport", "ImageAnnotatorGrpcTransport")
