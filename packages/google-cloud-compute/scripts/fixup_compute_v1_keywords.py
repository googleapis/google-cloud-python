#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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


class computeCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'abandon_instances': ('instance_group_manager', 'instance_group_managers_abandon_instances_request_resource', 'project', 'zone', 'request_id', ),
        'add_access_config': ('access_config_resource', 'instance', 'network_interface', 'project', 'zone', 'request_id', ),
        'add_association': ('firewall_policy', 'firewall_policy_association_resource', 'replace_existing_association', 'request_id', ),
        'add_health_check': ('project', 'region', 'target_pool', 'target_pools_add_health_check_request_resource', 'request_id', ),
        'add_instance': ('project', 'region', 'target_pool', 'target_pools_add_instance_request_resource', 'request_id', ),
        'add_instances': ('instance_group', 'instance_groups_add_instances_request_resource', 'project', 'zone', 'request_id', ),
        'add_nodes': ('node_group', 'node_groups_add_nodes_request_resource', 'project', 'zone', 'request_id', ),
        'add_peering': ('network', 'networks_add_peering_request_resource', 'project', 'request_id', ),
        'add_resource_policies': ('disk', 'disks_add_resource_policies_request_resource', 'project', 'zone', 'request_id', ),
        'add_rule': ('firewall_policy', 'firewall_policy_rule_resource', 'request_id', ),
        'add_signed_url_key': ('backend_bucket', 'project', 'signed_url_key_resource', 'request_id', ),
        'aggregated_list': ('project', 'filter', 'include_all_scopes', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'apply_updates_to_instances': ('instance_group_manager', 'instance_group_managers_apply_updates_request_resource', 'project', 'zone', ),
        'attach_disk': ('attached_disk_resource', 'instance', 'project', 'zone', 'force_attach', 'request_id', ),
        'attach_network_endpoints': ('global_network_endpoint_groups_attach_endpoints_request_resource', 'network_endpoint_group', 'project', 'request_id', ),
        'bulk_insert': ('bulk_insert_instance_resource_resource', 'project', 'zone', 'request_id', ),
        'clone_rules': ('firewall_policy', 'request_id', 'source_firewall_policy', ),
        'create_instances': ('instance_group_manager', 'instance_group_managers_create_instances_request_resource', 'project', 'zone', 'request_id', ),
        'create_snapshot': ('disk', 'project', 'snapshot_resource', 'zone', 'guest_flush', 'request_id', ),
        'delete': ('address', 'project', 'region', 'request_id', ),
        'delete_access_config': ('access_config', 'instance', 'network_interface', 'project', 'zone', 'request_id', ),
        'delete_instances': ('instance_group_manager', 'instance_group_managers_delete_instances_request_resource', 'project', 'zone', 'request_id', ),
        'delete_nodes': ('node_group', 'node_groups_delete_nodes_request_resource', 'project', 'zone', 'request_id', ),
        'delete_per_instance_configs': ('instance_group_manager', 'instance_group_managers_delete_per_instance_configs_req_resource', 'project', 'zone', ),
        'delete_signed_url_key': ('backend_bucket', 'key_name', 'project', 'request_id', ),
        'deprecate': ('deprecation_status_resource', 'image', 'project', 'request_id', ),
        'detach_disk': ('device_name', 'instance', 'project', 'zone', 'request_id', ),
        'detach_network_endpoints': ('global_network_endpoint_groups_detach_endpoints_request_resource', 'network_endpoint_group', 'project', 'request_id', ),
        'disable_xpn_host': ('project', 'request_id', ),
        'disable_xpn_resource': ('project', 'projects_disable_xpn_resource_request_resource', 'request_id', ),
        'enable_xpn_host': ('project', 'request_id', ),
        'enable_xpn_resource': ('project', 'projects_enable_xpn_resource_request_resource', 'request_id', ),
        'expand_ip_cidr_range': ('project', 'region', 'subnetwork', 'subnetworks_expand_ip_cidr_range_request_resource', 'request_id', ),
        'get': ('accelerator_type', 'project', 'zone', ),
        'get_association': ('firewall_policy', 'name', ),
        'get_diagnostics': ('interconnect', 'project', ),
        'get_effective_firewalls': ('instance', 'network_interface', 'project', 'zone', ),
        'get_from_family': ('family', 'project', ),
        'get_guest_attributes': ('instance', 'project', 'zone', 'query_path', 'variable_key', ),
        'get_health': ('backend_service', 'project', 'resource_group_reference_resource', ),
        'get_iam_policy': ('project', 'resource', 'zone', 'options_requested_policy_version', ),
        'get_nat_mapping_info': ('project', 'region', 'router', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'get_router_status': ('project', 'region', 'router', ),
        'get_rule': ('firewall_policy', 'priority', ),
        'get_screenshot': ('instance', 'project', 'zone', ),
        'get_serial_port_output': ('instance', 'project', 'zone', 'port', 'start', ),
        'get_shielded_instance_identity': ('instance', 'project', 'zone', ),
        'get_status': ('project', 'region', 'vpn_gateway', ),
        'get_xpn_host': ('project', ),
        'get_xpn_resources': ('project', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'insert': ('address_resource', 'project', 'region', 'request_id', ),
        'invalidate_cache': ('cache_invalidation_rule_resource', 'project', 'url_map', 'request_id', ),
        'list': ('project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_associations': ('target_resource', ),
        'list_available_features': ('project', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_errors': ('instance_group_manager', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_instances': ('instance_group', 'instance_groups_list_instances_request_resource', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_managed_instances': ('instance_group_manager', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_network_endpoints': ('network_endpoint_group', 'project', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_nodes': ('node_group', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_peering_routes': ('network', 'project', 'direction', 'filter', 'max_results', 'order_by', 'page_token', 'peering_name', 'region', 'return_partial_success', ),
        'list_per_instance_configs': ('instance_group_manager', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_preconfigured_expression_sets': ('project', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_referrers': ('instance', 'project', 'zone', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_usable': ('project', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'list_xpn_hosts': ('project', 'projects_list_xpn_hosts_request_resource', 'filter', 'max_results', 'order_by', 'page_token', 'return_partial_success', ),
        'move': ('firewall_policy', 'parent_id', 'request_id', ),
        'move_disk': ('disk_move_request_resource', 'project', 'request_id', ),
        'move_instance': ('instance_move_request_resource', 'project', 'request_id', ),
        'patch': ('autoscaler_resource', 'project', 'zone', 'autoscaler', 'request_id', ),
        'patch_per_instance_configs': ('instance_group_manager', 'instance_group_managers_patch_per_instance_configs_req_resource', 'project', 'zone', 'request_id', ),
        'patch_rule': ('firewall_policy', 'firewall_policy_rule_resource', 'priority', 'request_id', ),
        'preview': ('project', 'region', 'router', 'router_resource', ),
        'recreate_instances': ('instance_group_manager', 'instance_group_managers_recreate_instances_request_resource', 'project', 'zone', 'request_id', ),
        'remove_association': ('firewall_policy', 'name', 'request_id', ),
        'remove_health_check': ('project', 'region', 'target_pool', 'target_pools_remove_health_check_request_resource', 'request_id', ),
        'remove_instance': ('project', 'region', 'target_pool', 'target_pools_remove_instance_request_resource', 'request_id', ),
        'remove_instances': ('instance_group', 'instance_groups_remove_instances_request_resource', 'project', 'zone', 'request_id', ),
        'remove_peering': ('network', 'networks_remove_peering_request_resource', 'project', 'request_id', ),
        'remove_resource_policies': ('disk', 'disks_remove_resource_policies_request_resource', 'project', 'zone', 'request_id', ),
        'remove_rule': ('firewall_policy', 'priority', 'request_id', ),
        'reset': ('instance', 'project', 'zone', 'request_id', ),
        'resize': ('disk', 'disks_resize_request_resource', 'project', 'zone', 'request_id', ),
        'resume': ('instance', 'project', 'zone', 'request_id', ),
        'send_diagnostic_interrupt': ('instance', 'project', 'zone', ),
        'set_backend_service': ('project', 'target_ssl_proxies_set_backend_service_request_resource', 'target_ssl_proxy', 'request_id', ),
        'set_backup': ('project', 'region', 'target_pool', 'target_reference_resource', 'failover_ratio', 'request_id', ),
        'set_certificate_map': ('project', 'target_https_proxies_set_certificate_map_request_resource', 'target_https_proxy', 'request_id', ),
        'set_common_instance_metadata': ('metadata_resource', 'project', 'request_id', ),
        'set_default_network_tier': ('project', 'projects_set_default_network_tier_request_resource', 'request_id', ),
        'set_deletion_protection': ('project', 'resource', 'zone', 'deletion_protection', 'request_id', ),
        'set_disk_auto_delete': ('auto_delete', 'device_name', 'instance', 'project', 'zone', 'request_id', ),
        'set_edge_security_policy': ('backend_bucket', 'project', 'security_policy_reference_resource', 'request_id', ),
        'set_iam_policy': ('project', 'resource', 'zone', 'zone_set_policy_request_resource', ),
        'set_instance_template': ('instance_group_manager', 'instance_group_managers_set_instance_template_request_resource', 'project', 'zone', 'request_id', ),
        'set_labels': ('project', 'resource', 'zone', 'zone_set_labels_request_resource', 'request_id', ),
        'set_machine_resources': ('instance', 'instances_set_machine_resources_request_resource', 'project', 'zone', 'request_id', ),
        'set_machine_type': ('instance', 'instances_set_machine_type_request_resource', 'project', 'zone', 'request_id', ),
        'set_metadata': ('instance', 'metadata_resource', 'project', 'zone', 'request_id', ),
        'set_min_cpu_platform': ('instance', 'instances_set_min_cpu_platform_request_resource', 'project', 'zone', 'request_id', ),
        'set_named_ports': ('instance_group', 'instance_groups_set_named_ports_request_resource', 'project', 'zone', 'request_id', ),
        'set_node_template': ('node_group', 'node_groups_set_node_template_request_resource', 'project', 'zone', 'request_id', ),
        'set_private_ip_google_access': ('project', 'region', 'subnetwork', 'subnetworks_set_private_ip_google_access_request_resource', 'request_id', ),
        'set_proxy_header': ('project', 'target_ssl_proxies_set_proxy_header_request_resource', 'target_ssl_proxy', 'request_id', ),
        'set_quic_override': ('project', 'target_https_proxies_set_quic_override_request_resource', 'target_https_proxy', 'request_id', ),
        'set_scheduling': ('instance', 'project', 'scheduling_resource', 'zone', 'request_id', ),
        'set_security_policy': ('backend_service', 'project', 'security_policy_reference_resource', 'request_id', ),
        'set_service_account': ('instance', 'instances_set_service_account_request_resource', 'project', 'zone', 'request_id', ),
        'set_shielded_instance_integrity_policy': ('instance', 'project', 'shielded_instance_integrity_policy_resource', 'zone', 'request_id', ),
        'set_ssl_certificates': ('project', 'region', 'region_target_https_proxies_set_ssl_certificates_request_resource', 'target_https_proxy', 'request_id', ),
        'set_ssl_policy': ('project', 'ssl_policy_reference_resource', 'target_https_proxy', 'request_id', ),
        'set_tags': ('instance', 'project', 'tags_resource', 'zone', 'request_id', ),
        'set_target': ('forwarding_rule', 'project', 'region', 'target_reference_resource', 'request_id', ),
        'set_target_pools': ('instance_group_manager', 'instance_group_managers_set_target_pools_request_resource', 'project', 'zone', 'request_id', ),
        'set_url_map': ('project', 'region', 'target_http_proxy', 'url_map_reference_resource', 'request_id', ),
        'set_usage_export_bucket': ('project', 'usage_export_location_resource', 'request_id', ),
        'simulate_maintenance_event': ('instance', 'project', 'zone', ),
        'start': ('instance', 'project', 'zone', 'request_id', ),
        'start_with_encryption_key': ('instance', 'instances_start_with_encryption_key_request_resource', 'project', 'zone', 'request_id', ),
        'stop': ('instance', 'project', 'zone', 'request_id', ),
        'suspend': ('instance', 'project', 'zone', 'request_id', ),
        'switch_to_custom_mode': ('network', 'project', 'request_id', ),
        'test_iam_permissions': ('project', 'resource', 'test_permissions_request_resource', 'zone', ),
        'update': ('autoscaler_resource', 'project', 'zone', 'autoscaler', 'request_id', ),
        'update_access_config': ('access_config_resource', 'instance', 'network_interface', 'project', 'zone', 'request_id', ),
        'update_display_device': ('display_device_resource', 'instance', 'project', 'zone', 'request_id', ),
        'update_network_interface': ('instance', 'network_interface', 'network_interface_resource', 'project', 'zone', 'request_id', ),
        'update_peering': ('network', 'networks_update_peering_request_resource', 'project', 'request_id', ),
        'update_per_instance_configs': ('instance_group_manager', 'instance_group_managers_update_per_instance_configs_req_resource', 'project', 'zone', 'request_id', ),
        'update_shielded_instance_config': ('instance', 'project', 'shielded_instance_config_resource', 'zone', 'request_id', ),
        'validate': ('project', 'region', 'region_url_maps_validate_request_resource', 'url_map', ),
        'wait': ('operation', 'project', ),
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
    transformer=computeCallTransformer(),
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
        description="""Fix up source that uses the compute client library.

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
