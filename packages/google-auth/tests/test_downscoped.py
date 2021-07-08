# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from google.auth import downscoped


EXPRESSION = (
    "resource.name.startsWith('projects/_/buckets/example-bucket/objects/customer-a')"
)
TITLE = "customer-a-objects"
DESCRIPTION = (
    "Condition to make permissions available for objects starting with customer-a"
)
AVAILABLE_RESOURCE = "//storage.googleapis.com/projects/_/buckets/example-bucket"
AVAILABLE_PERMISSIONS = ["inRole:roles/storage.objectViewer"]

OTHER_EXPRESSION = (
    "resource.name.startsWith('projects/_/buckets/example-bucket/objects/customer-b')"
)
OTHER_TITLE = "customer-b-objects"
OTHER_DESCRIPTION = (
    "Condition to make permissions available for objects starting with customer-b"
)
OTHER_AVAILABLE_RESOURCE = "//storage.googleapis.com/projects/_/buckets/other-bucket"
OTHER_AVAILABLE_PERMISSIONS = ["inRole:roles/storage.objectCreator"]


def make_availability_condition(expression, title=None, description=None):
    return downscoped.AvailabilityCondition(expression, title, description)


def make_access_boundary_rule(
    available_resource, available_permissions, availability_condition=None
):
    return downscoped.AccessBoundaryRule(
        available_resource, available_permissions, availability_condition
    )


def make_credential_access_boundary(rules):
    return downscoped.CredentialAccessBoundary(rules)


class TestAvailabilityCondition(object):
    def test_constructor(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )

        assert availability_condition.expression == EXPRESSION
        assert availability_condition.title == TITLE
        assert availability_condition.description == DESCRIPTION

    def test_constructor_required_params_only(self):
        availability_condition = make_availability_condition(EXPRESSION)

        assert availability_condition.expression == EXPRESSION
        assert availability_condition.title is None
        assert availability_condition.description is None

    def test_setters(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        availability_condition.expression = OTHER_EXPRESSION
        availability_condition.title = OTHER_TITLE
        availability_condition.description = OTHER_DESCRIPTION

        assert availability_condition.expression == OTHER_EXPRESSION
        assert availability_condition.title == OTHER_TITLE
        assert availability_condition.description == OTHER_DESCRIPTION

    def test_invalid_expression_type(self):
        with pytest.raises(TypeError) as excinfo:
            make_availability_condition([EXPRESSION], TITLE, DESCRIPTION)

        assert excinfo.match("The provided expression is not a string.")

    def test_invalid_title_type(self):
        with pytest.raises(TypeError) as excinfo:
            make_availability_condition(EXPRESSION, False, DESCRIPTION)

        assert excinfo.match("The provided title is not a string or None.")

    def test_invalid_description_type(self):
        with pytest.raises(TypeError) as excinfo:
            make_availability_condition(EXPRESSION, TITLE, False)

        assert excinfo.match("The provided description is not a string or None.")

    def test_to_json_required_params_only(self):
        availability_condition = make_availability_condition(EXPRESSION)

        assert availability_condition.to_json() == {"expression": EXPRESSION}

    def test_to_json_(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )

        assert availability_condition.to_json() == {
            "expression": EXPRESSION,
            "title": TITLE,
            "description": DESCRIPTION,
        }


class TestAccessBoundaryRule(object):
    def test_constructor(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )

        assert access_boundary_rule.available_resource == AVAILABLE_RESOURCE
        assert access_boundary_rule.available_permissions == tuple(
            AVAILABLE_PERMISSIONS
        )
        assert access_boundary_rule.availability_condition == availability_condition

    def test_constructor_required_params_only(self):
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS
        )

        assert access_boundary_rule.available_resource == AVAILABLE_RESOURCE
        assert access_boundary_rule.available_permissions == tuple(
            AVAILABLE_PERMISSIONS
        )
        assert access_boundary_rule.availability_condition is None

    def test_setters(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        other_availability_condition = make_availability_condition(
            OTHER_EXPRESSION, OTHER_TITLE, OTHER_DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        access_boundary_rule.available_resource = OTHER_AVAILABLE_RESOURCE
        access_boundary_rule.available_permissions = OTHER_AVAILABLE_PERMISSIONS
        access_boundary_rule.availability_condition = other_availability_condition

        assert access_boundary_rule.available_resource == OTHER_AVAILABLE_RESOURCE
        assert access_boundary_rule.available_permissions == tuple(
            OTHER_AVAILABLE_PERMISSIONS
        )
        assert (
            access_boundary_rule.availability_condition == other_availability_condition
        )

    def test_invalid_available_resource_type(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        with pytest.raises(TypeError) as excinfo:
            make_access_boundary_rule(
                None, AVAILABLE_PERMISSIONS, availability_condition
            )

        assert excinfo.match("The provided available_resource is not a string.")

    def test_invalid_available_permissions_type(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        with pytest.raises(TypeError) as excinfo:
            make_access_boundary_rule(
                AVAILABLE_RESOURCE, [0, 1, 2], availability_condition
            )

        assert excinfo.match(
            "Provided available_permissions are not a list of strings."
        )

    def test_invalid_available_permissions_value(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        with pytest.raises(ValueError) as excinfo:
            make_access_boundary_rule(
                AVAILABLE_RESOURCE,
                ["roles/storage.objectViewer"],
                availability_condition,
            )

        assert excinfo.match("available_permissions must be prefixed with 'inRole:'.")

    def test_invalid_availability_condition_type(self):
        with pytest.raises(TypeError) as excinfo:
            make_access_boundary_rule(
                AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, {"foo": "bar"}
            )

        assert excinfo.match(
            "The provided availability_condition is not a 'google.auth.downscoped.AvailabilityCondition' or None."
        )

    def test_to_json(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )

        assert access_boundary_rule.to_json() == {
            "availablePermissions": AVAILABLE_PERMISSIONS,
            "availableResource": AVAILABLE_RESOURCE,
            "availabilityCondition": {
                "expression": EXPRESSION,
                "title": TITLE,
                "description": DESCRIPTION,
            },
        }

    def test_to_json_required_params_only(self):
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS
        )

        assert access_boundary_rule.to_json() == {
            "availablePermissions": AVAILABLE_PERMISSIONS,
            "availableResource": AVAILABLE_RESOURCE,
        }


class TestCredentialAccessBoundary(object):
    def test_constructor(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule]
        credential_access_boundary = make_credential_access_boundary(rules)

        assert credential_access_boundary.rules == tuple(rules)

    def test_setters(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule]
        other_availability_condition = make_availability_condition(
            OTHER_EXPRESSION, OTHER_TITLE, OTHER_DESCRIPTION
        )
        other_access_boundary_rule = make_access_boundary_rule(
            OTHER_AVAILABLE_RESOURCE,
            OTHER_AVAILABLE_PERMISSIONS,
            other_availability_condition,
        )
        other_rules = [other_access_boundary_rule]
        credential_access_boundary = make_credential_access_boundary(rules)
        credential_access_boundary.rules = other_rules

        assert credential_access_boundary.rules == tuple(other_rules)

    def test_add_rule(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule] * 9
        credential_access_boundary = make_credential_access_boundary(rules)

        # Add one more rule. This should not raise an error.
        additional_access_boundary_rule = make_access_boundary_rule(
            OTHER_AVAILABLE_RESOURCE, OTHER_AVAILABLE_PERMISSIONS
        )
        credential_access_boundary.add_rule(additional_access_boundary_rule)

        assert len(credential_access_boundary.rules) == 10
        assert credential_access_boundary.rules[9] == additional_access_boundary_rule

    def test_add_rule_invalid_value(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule] * 10
        credential_access_boundary = make_credential_access_boundary(rules)

        # Add one more rule to exceed maximum allowed rules.
        with pytest.raises(ValueError) as excinfo:
            credential_access_boundary.add_rule(access_boundary_rule)

        assert excinfo.match(
            "Credential access boundary rules can have a maximum of 10 rules."
        )
        assert len(credential_access_boundary.rules) == 10

    def test_add_rule_invalid_type(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule]
        credential_access_boundary = make_credential_access_boundary(rules)

        # Add an invalid rule to exceed maximum allowed rules.
        with pytest.raises(TypeError) as excinfo:
            credential_access_boundary.add_rule("invalid")

        assert excinfo.match(
            "The provided rule does not contain a valid 'google.auth.downscoped.AccessBoundaryRule'."
        )
        assert len(credential_access_boundary.rules) == 1
        assert credential_access_boundary.rules[0] == access_boundary_rule

    def test_invalid_rules_type(self):
        with pytest.raises(TypeError) as excinfo:
            make_credential_access_boundary(["invalid"])

        assert excinfo.match(
            "List of rules provided do not contain a valid 'google.auth.downscoped.AccessBoundaryRule'."
        )

    def test_invalid_rules_value(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        too_many_rules = [access_boundary_rule] * 11
        with pytest.raises(ValueError) as excinfo:
            make_credential_access_boundary(too_many_rules)

        assert excinfo.match(
            "Credential access boundary rules can have a maximum of 10 rules."
        )

    def test_to_json(self):
        availability_condition = make_availability_condition(
            EXPRESSION, TITLE, DESCRIPTION
        )
        access_boundary_rule = make_access_boundary_rule(
            AVAILABLE_RESOURCE, AVAILABLE_PERMISSIONS, availability_condition
        )
        rules = [access_boundary_rule]
        credential_access_boundary = make_credential_access_boundary(rules)

        assert credential_access_boundary.to_json() == {
            "accessBoundary": {
                "accessBoundaryRules": [
                    {
                        "availablePermissions": AVAILABLE_PERMISSIONS,
                        "availableResource": AVAILABLE_RESOURCE,
                        "availabilityCondition": {
                            "expression": EXPRESSION,
                            "title": TITLE,
                            "description": DESCRIPTION,
                        },
                    }
                ]
            }
        }
