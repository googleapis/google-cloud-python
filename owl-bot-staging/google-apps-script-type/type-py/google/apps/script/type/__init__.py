# -*- coding: utf-8 -*-
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
#
from google.apps.script.type import gapic_version as package_version

__version__ = package_version.__version__



from .types.addon_widget_set import AddOnWidgetSet
from .types.extension_point import HomepageExtensionPoint
from .types.extension_point import MenuItemExtensionPoint
from .types.extension_point import UniversalActionExtensionPoint
from .types.script_manifest import CommonAddOnManifest
from .types.script_manifest import HttpOptions
from .types.script_manifest import LayoutProperties
from .types.script_manifest import HttpAuthorizationHeader

__all__ = (
'AddOnWidgetSet',
'CommonAddOnManifest',
'HomepageExtensionPoint',
'HttpAuthorizationHeader',
'HttpOptions',
'LayoutProperties',
'MenuItemExtensionPoint',
'UniversalActionExtensionPoint',
)
