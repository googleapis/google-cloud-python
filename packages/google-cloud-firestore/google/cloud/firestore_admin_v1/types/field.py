# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.cloud.firestore_admin_v1.types import index


__protobuf__ = proto.module(package="google.firestore.admin.v1", manifest={"Field",},)


class Field(proto.Message):
    r"""Represents a single field in the database.
    Fields are grouped by their "Collection Group", which represent
    all collections in the database with the same id.

    Attributes:
        name (str):
            A field name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_path}``

            A field path may be a simple field name, e.g. ``address`` or
            a path to fields within map_value , e.g. ``address.city``,
            or a special field path. The only valid special field is
            ``*``, which represents any field.

            Field paths may be quoted using
            ``(backtick). The only character that needs to be escaped within a quoted field path is the backtick character itself, escaped using a backslash. Special characters in field paths that must be quoted include:``\ \*\ ``,``.\ :literal:`, ``` (backtick),`\ [``,``]`,
            as well as any ascii symbolic characters.

            Examples: (Note: Comments here are written in markdown
            syntax, so there is an additional layer of backticks to
            represent a code block)
            ``\``\ address.city\`\ ``represents a field named``\ address.city\ ``, not the map key``\ city\ ``in the field``\ address\ ``.``\ \`\ *\`\ ``represents a field named``*\ \`,
            not any field.

            A special ``Field`` contains the default indexing settings
            for all fields. This field's resource name is:
            ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``
            Indexes defined on this ``Field`` will be applied to all
            fields which do not have their own ``Field`` index
            configuration.
        index_config (google.cloud.firestore_admin_v1.types.Field.IndexConfig):
            The index configuration for this field. If unset, field
            indexing will revert to the configuration defined by the
            ``ancestor_field``. To explicitly remove all indexes for
            this field, specify an index config with an empty list of
            indexes.
    """

    class IndexConfig(proto.Message):
        r"""The index configuration for this field.
        Attributes:
            indexes (Sequence[google.cloud.firestore_admin_v1.types.Index]):
                The indexes supported for this field.
            uses_ancestor_config (bool):
                Output only. When true, the ``Field``'s index configuration
                is set from the configuration specified by the
                ``ancestor_field``. When false, the ``Field``'s index
                configuration is defined explicitly.
            ancestor_field (str):
                Output only. Specifies the resource name of the ``Field``
                from which this field's index configuration is set (when
                ``uses_ancestor_config`` is true), or from which it *would*
                be set if this field had no index configuration (when
                ``uses_ancestor_config`` is false).
            reverting (bool):
                Output only When true, the ``Field``'s index configuration
                is in the process of being reverted. Once complete, the
                index config will transition to the same state as the field
                specified by ``ancestor_field``, at which point
                ``uses_ancestor_config`` will be ``true`` and ``reverting``
                will be ``false``.
        """

        indexes = proto.RepeatedField(proto.MESSAGE, number=1, message=index.Index,)
        uses_ancestor_config = proto.Field(proto.BOOL, number=2,)
        ancestor_field = proto.Field(proto.STRING, number=3,)
        reverting = proto.Field(proto.BOOL, number=4,)

    name = proto.Field(proto.STRING, number=1,)
    index_config = proto.Field(proto.MESSAGE, number=2, message=IndexConfig,)


__all__ = tuple(sorted(__protobuf__.manifest))
