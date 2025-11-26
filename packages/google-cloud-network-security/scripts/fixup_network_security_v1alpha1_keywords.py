#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import argparse
import os
import libcst as cst
import pathlib
import sys
from typing import (Any, Callable, Dict, List, Sequence, Tuple)


def partition(
    predicate: Callable[[Any], bool],
    iterator: Sequence[Any]
) -> Tuple[List[Any], List[Any]]:
    """A stable, out-of-place partition."""
    results = ([], [])

    for i in iterator:
        results[int(predicate(i))].append(i)

    # Returns trueList, falseList
    return results[1], results[0]


class network_securityCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'create_authorization_policy': ('parent', 'authorization_policy_id', 'authorization_policy', ),
        'create_authz_policy': ('parent', 'authz_policy_id', 'authz_policy', 'request_id', ),
        'create_backend_authentication_config': ('parent', 'backend_authentication_config_id', 'backend_authentication_config', ),
        'create_client_tls_policy': ('parent', 'client_tls_policy_id', 'client_tls_policy', ),
        'create_dns_threat_detector': ('parent', 'dns_threat_detector', 'dns_threat_detector_id', ),
        'create_firewall_endpoint': ('parent', 'firewall_endpoint_id', 'firewall_endpoint', 'request_id', ),
        'create_firewall_endpoint_association': ('parent', 'firewall_endpoint_association', 'firewall_endpoint_association_id', 'request_id', ),
        'create_gateway_security_policy': ('parent', 'gateway_security_policy_id', 'gateway_security_policy', ),
        'create_gateway_security_policy_rule': ('parent', 'gateway_security_policy_rule', 'gateway_security_policy_rule_id', ),
        'create_intercept_deployment': ('parent', 'intercept_deployment_id', 'intercept_deployment', 'request_id', ),
        'create_intercept_deployment_group': ('parent', 'intercept_deployment_group_id', 'intercept_deployment_group', 'request_id', ),
        'create_intercept_endpoint_group': ('parent', 'intercept_endpoint_group_id', 'intercept_endpoint_group', 'request_id', ),
        'create_intercept_endpoint_group_association': ('parent', 'intercept_endpoint_group_association', 'intercept_endpoint_group_association_id', 'request_id', ),
        'create_mirroring_deployment': ('parent', 'mirroring_deployment_id', 'mirroring_deployment', 'request_id', ),
        'create_mirroring_deployment_group': ('parent', 'mirroring_deployment_group_id', 'mirroring_deployment_group', 'request_id', ),
        'create_mirroring_endpoint_group': ('parent', 'mirroring_endpoint_group_id', 'mirroring_endpoint_group', 'request_id', ),
        'create_mirroring_endpoint_group_association': ('parent', 'mirroring_endpoint_group_association', 'mirroring_endpoint_group_association_id', 'request_id', ),
        'create_partner_sse_gateway': ('parent', 'partner_sse_gateway_id', 'partner_sse_gateway', 'request_id', ),
        'create_partner_sse_realm': ('parent', 'partner_sse_realm_id', 'partner_sse_realm', 'request_id', ),
        'create_sac_attachment': ('parent', 'sac_attachment_id', 'sac_attachment', 'request_id', ),
        'create_sac_realm': ('parent', 'sac_realm_id', 'sac_realm', 'request_id', ),
        'create_security_profile': ('parent', 'security_profile_id', 'security_profile', ),
        'create_security_profile_group': ('parent', 'security_profile_group_id', 'security_profile_group', ),
        'create_server_tls_policy': ('parent', 'server_tls_policy_id', 'server_tls_policy', ),
        'create_tls_inspection_policy': ('parent', 'tls_inspection_policy_id', 'tls_inspection_policy', ),
        'create_url_list': ('parent', 'url_list_id', 'url_list', ),
        'delete_authorization_policy': ('name', ),
        'delete_authz_policy': ('name', 'request_id', ),
        'delete_backend_authentication_config': ('name', 'etag', ),
        'delete_client_tls_policy': ('name', ),
        'delete_dns_threat_detector': ('name', ),
        'delete_firewall_endpoint': ('name', 'request_id', ),
        'delete_firewall_endpoint_association': ('name', 'request_id', ),
        'delete_gateway_security_policy': ('name', ),
        'delete_gateway_security_policy_rule': ('name', ),
        'delete_intercept_deployment': ('name', 'request_id', ),
        'delete_intercept_deployment_group': ('name', 'request_id', ),
        'delete_intercept_endpoint_group': ('name', 'request_id', ),
        'delete_intercept_endpoint_group_association': ('name', 'request_id', ),
        'delete_mirroring_deployment': ('name', 'request_id', ),
        'delete_mirroring_deployment_group': ('name', 'request_id', ),
        'delete_mirroring_endpoint_group': ('name', 'request_id', ),
        'delete_mirroring_endpoint_group_association': ('name', 'request_id', ),
        'delete_partner_sse_gateway': ('name', 'request_id', ),
        'delete_partner_sse_realm': ('name', 'request_id', ),
        'delete_sac_attachment': ('name', 'request_id', ),
        'delete_sac_realm': ('name', 'request_id', ),
        'delete_security_profile': ('name', 'etag', ),
        'delete_security_profile_group': ('name', 'etag', ),
        'delete_server_tls_policy': ('name', ),
        'delete_tls_inspection_policy': ('name', 'force', ),
        'delete_url_list': ('name', ),
        'get_authorization_policy': ('name', ),
        'get_authz_policy': ('name', ),
        'get_backend_authentication_config': ('name', ),
        'get_client_tls_policy': ('name', ),
        'get_dns_threat_detector': ('name', ),
        'get_firewall_endpoint': ('name', ),
        'get_firewall_endpoint_association': ('name', ),
        'get_gateway_security_policy': ('name', ),
        'get_gateway_security_policy_rule': ('name', ),
        'get_intercept_deployment': ('name', ),
        'get_intercept_deployment_group': ('name', ),
        'get_intercept_endpoint_group': ('name', ),
        'get_intercept_endpoint_group_association': ('name', ),
        'get_mirroring_deployment': ('name', ),
        'get_mirroring_deployment_group': ('name', ),
        'get_mirroring_endpoint_group': ('name', ),
        'get_mirroring_endpoint_group_association': ('name', ),
        'get_partner_sse_gateway': ('name', ),
        'get_partner_sse_realm': ('name', ),
        'get_sac_attachment': ('name', ),
        'get_sac_realm': ('name', ),
        'get_security_profile': ('name', ),
        'get_security_profile_group': ('name', ),
        'get_server_tls_policy': ('name', ),
        'get_sse_gateway_reference': ('name', ),
        'get_tls_inspection_policy': ('name', ),
        'get_url_list': ('name', ),
        'list_authorization_policies': ('parent', 'page_size', 'page_token', ),
        'list_authz_policies': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_backend_authentication_configs': ('parent', 'page_size', 'page_token', ),
        'list_client_tls_policies': ('parent', 'page_size', 'page_token', ),
        'list_dns_threat_detectors': ('parent', 'page_size', 'page_token', ),
        'list_firewall_endpoint_associations': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_firewall_endpoints': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_gateway_security_policies': ('parent', 'page_size', 'page_token', ),
        'list_gateway_security_policy_rules': ('parent', 'page_size', 'page_token', ),
        'list_intercept_deployment_groups': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_intercept_deployments': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_intercept_endpoint_group_associations': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_intercept_endpoint_groups': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_mirroring_deployment_groups': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_mirroring_deployments': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_mirroring_endpoint_group_associations': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_mirroring_endpoint_groups': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_partner_sse_gateways': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_partner_sse_realms': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_sac_attachments': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_sac_realms': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_security_profile_groups': ('parent', 'page_size', 'page_token', ),
        'list_security_profiles': ('parent', 'page_size', 'page_token', ),
        'list_server_tls_policies': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_sse_gateway_references': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_tls_inspection_policies': ('parent', 'page_size', 'page_token', ),
        'list_url_lists': ('parent', 'page_size', 'page_token', ),
        'update_authorization_policy': ('authorization_policy', 'update_mask', ),
        'update_authz_policy': ('update_mask', 'authz_policy', 'request_id', ),
        'update_backend_authentication_config': ('backend_authentication_config', 'update_mask', ),
        'update_client_tls_policy': ('client_tls_policy', 'update_mask', ),
        'update_dns_threat_detector': ('dns_threat_detector', 'update_mask', ),
        'update_firewall_endpoint': ('update_mask', 'firewall_endpoint', 'request_id', ),
        'update_firewall_endpoint_association': ('update_mask', 'firewall_endpoint_association', 'request_id', ),
        'update_gateway_security_policy': ('gateway_security_policy', 'update_mask', ),
        'update_gateway_security_policy_rule': ('gateway_security_policy_rule', 'update_mask', ),
        'update_intercept_deployment': ('intercept_deployment', 'update_mask', 'request_id', ),
        'update_intercept_deployment_group': ('intercept_deployment_group', 'update_mask', 'request_id', ),
        'update_intercept_endpoint_group': ('intercept_endpoint_group', 'update_mask', 'request_id', ),
        'update_intercept_endpoint_group_association': ('intercept_endpoint_group_association', 'update_mask', 'request_id', ),
        'update_mirroring_deployment': ('mirroring_deployment', 'update_mask', 'request_id', ),
        'update_mirroring_deployment_group': ('mirroring_deployment_group', 'update_mask', 'request_id', ),
        'update_mirroring_endpoint_group': ('mirroring_endpoint_group', 'update_mask', 'request_id', ),
        'update_mirroring_endpoint_group_association': ('mirroring_endpoint_group_association', 'update_mask', 'request_id', ),
        'update_partner_sse_gateway': ('partner_sse_gateway', 'update_mask', 'request_id', ),
        'update_security_profile': ('update_mask', 'security_profile', ),
        'update_security_profile_group': ('update_mask', 'security_profile_group', ),
        'update_server_tls_policy': ('server_tls_policy', 'update_mask', ),
        'update_tls_inspection_policy': ('tls_inspection_policy', 'update_mask', ),
        'update_url_list': ('url_list', 'update_mask', ),
    }

    def leave_Call(self, original: cst.Call, updated: cst.Call) -> cst.CSTNode:
        try:
            key = original.func.attr.value
            kword_params = self.METHOD_TO_PARAMS[key]
        except (AttributeError, KeyError):
            # Either not a method from the API or too convoluted to be sure.
            return updated

        # If the existing code is valid, keyword args come after positional args.
        # Therefore, all positional args must map to the first parameters.
        args, kwargs = partition(lambda a: not bool(a.keyword), updated.args)
        if any(k.keyword.value == "request" for k in kwargs):
            # We've already fixed this file, don't fix it again.
            return updated

        kwargs, ctrl_kwargs = partition(
            lambda a: a.keyword.value not in self.CTRL_PARAMS,
            kwargs
        )

        args, ctrl_args = args[:len(kword_params)], args[len(kword_params):]
        ctrl_kwargs.extend(cst.Arg(value=a.value, keyword=cst.Name(value=ctrl))
                           for a, ctrl in zip(ctrl_args, self.CTRL_PARAMS))

        request_arg = cst.Arg(
            value=cst.Dict([
                cst.DictElement(
                    cst.SimpleString("'{}'".format(name)),
cst.Element(value=arg.value)
                )
                # Note: the args + kwargs looks silly, but keep in mind that
                # the control parameters had to be stripped out, and that
                # those could have been passed positionally or by keyword.
                for name, arg in zip(kword_params, args + kwargs)]),
            keyword=cst.Name("request")
        )

        return updated.with_changes(
            args=[request_arg] + ctrl_kwargs
        )


def fix_files(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    *,
    transformer=network_securityCallTransformer(),
):
    """Duplicate the input dir to the output dir, fixing file method calls.

    Preconditions:
    * in_dir is a real directory
    * out_dir is a real, empty directory
    """
    pyfile_gen = (
        pathlib.Path(os.path.join(root, f))
        for root, _, files in os.walk(in_dir)
        for f in files if os.path.splitext(f)[1] == ".py"
    )

    for fpath in pyfile_gen:
        with open(fpath, 'r') as f:
            src = f.read()

        # Parse the code and insert method call fixes.
        tree = cst.parse_module(src)
        updated = tree.visit(transformer)

        # Create the path and directory structure for the new file.
        updated_path = out_dir.joinpath(fpath.relative_to(in_dir))
        updated_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the updated source file at the corresponding path.
        with open(updated_path, 'w') as f:
            f.write(updated.code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Fix up source that uses the network_security client library.

The existing sources are NOT overwritten but are copied to output_dir with changes made.

Note: This tool operates at a best-effort level at converting positional
      parameters in client method calls to keyword based parameters.
      Cases where it WILL FAIL include
      A) * or ** expansion in a method call.
      B) Calls via function or method alias (includes free function calls)
      C) Indirect or dispatched calls (e.g. the method is looked up dynamically)

      These all constitute false negatives. The tool will also detect false
      positives when an API method shares a name with another method.
""")
    parser.add_argument(
        '-d',
        '--input-directory',
        required=True,
        dest='input_dir',
        help='the input directory to walk for python files to fix up',
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        required=True,
        dest='output_dir',
        help='the directory to output files fixed via un-flattening',
    )
    args = parser.parse_args()
    input_dir = pathlib.Path(args.input_dir)
    output_dir = pathlib.Path(args.output_dir)
    if not input_dir.is_dir():
        print(
            f"input directory '{input_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if not output_dir.is_dir():
        print(
            f"output directory '{output_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if os.listdir(output_dir):
        print(
            f"output directory '{output_dir}' is not empty",
            file=sys.stderr,
        )
        sys.exit(-1)

    fix_files(input_dir, output_dir)
