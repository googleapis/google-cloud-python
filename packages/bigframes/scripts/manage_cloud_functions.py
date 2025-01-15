# Copyright 2023 Google LLC
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

import argparse
import datetime as dt
import sys
import time

import google.api_core.exceptions
from google.cloud import functions_v2

GCF_REGIONS_ALL = [
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast2",
    "europe-north1",
    "europe-southwest1",
    "europe-west1",
    "europe-west2",
    "europe-west4",
    "europe-west8",
    "europe-west9",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-east5",
    "us-south1",
    "us-west1",
    "asia-east2",
    "asia-northeast3",
    "asia-southeast1",
    "asia-southeast2",
    "asia-south1",
    "asia-south2",
    "australia-southeast1",
    "australia-southeast2",
    "europe-central2",
    "europe-west2",
    "europe-west3",
    "europe-west6",
    "northamerica-northeast1",
    "northamerica-northeast2",
    "southamerica-east1",
    "southamerica-west1",
    "us-west2",
    "us-west3",
    "us-west4",
]

GCF_CLIENT = functions_v2.FunctionServiceClient()


def get_bigframes_functions(project, region):
    parent = f"projects/{project}/locations/{region}"
    functions = GCF_CLIENT.list_functions(
        functions_v2.ListFunctionsRequest(parent=parent)
    )
    # Filter bigframes created functions
    functions = [
        function
        for function in functions
        if function.name.startswith(
            f"projects/{project}/locations/{region}/functions/bigframes-"
        )
    ]

    return functions


def summarize_gcfs(args):
    """Summarize number of bigframes cloud functions in various regions."""

    region_counts = {}
    for region in args.regions:
        functions = get_bigframes_functions(args.project_id, region)
        functions_count = len(functions)

        # Exclude reporting regions with 0 bigframes GCFs
        if functions_count == 0:
            continue

        # Count how many GCFs are newer than a day
        recent = 0
        for f in functions:
            age = dt.datetime.now() - dt.datetime.fromtimestamp(
                f.update_time.timestamp()
            )
            if age.total_seconds() < args.recency_cutoff:
                recent += 1

        region_counts[region] = (functions_count, recent)

    for item in sorted(
        region_counts.items(), key=lambda item: item[1][0], reverse=True
    ):
        region = item[0]
        count, recent = item[1]
        print(
            "{}: Total={}, Recent={}, Older={}".format(
                region, count, recent, count - recent
            )
        )


def cleanup_gcfs(args):
    """Clean-up bigframes cloud functions in the given regions."""
    max_delete_per_region = args.number

    for region in args.regions:
        functions = get_bigframes_functions(args.project_id, region)
        count = 0
        for f in functions:
            age = dt.datetime.now() - dt.datetime.fromtimestamp(
                f.update_time.timestamp()
            )
            if age.total_seconds() >= args.recency_cutoff:
                try:
                    count += 1
                    GCF_CLIENT.delete_function(name=f.name)
                    print(
                        f"[{region}]: deleted [{count}] {f.name} last updated on {f.update_time}"
                    )
                    if count >= max_delete_per_region:
                        break
                    # Mostly there is a 60 mutations per minute quota, we want to use 10% of
                    # that for this clean-up, i.e. 6 mutations per minute. So wait for
                    # 60/6 = 10 seconds
                    time.sleep(10)
                except google.api_core.exceptions.NotFound:
                    # Most likely the function was deleted otherwise
                    pass
                except google.api_core.exceptions.ResourceExhausted:
                    # Stop deleting in this region for now
                    print(
                        f"Failed to delete function in region {region} due to quota exhaustion. Pausing for 2 minutes."
                    )
                    time.sleep(120)


def list_str(values):
    return [val for val in values.split(",") if val]


def get_project_from_environment():
    from google.cloud import bigquery

    return bigquery.Client().project


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manage cloud functions created to serve bigframes remote functions."
    )
    parser.add_argument(
        "-p",
        "--project-id",
        type=str,
        required=False,
        action="store",
        help="GCP project-id. If not provided, the project-id resolved by the"
        " BigQuery client from the user environment would be used.",
    )
    parser.add_argument(
        "-r",
        "--regions",
        type=list_str,
        required=False,
        default=GCF_REGIONS_ALL,
        action="store",
        help="Cloud functions region(s). If multiple regions, Specify comma separated (e.g. region1,region2)",
    )

    def hours_to_timedelta(hrs):
        return dt.timedelta(hours=int(hrs)).total_seconds()

    parser.add_argument(
        "-c",
        "--recency-cutoff",
        type=hours_to_timedelta,
        required=False,
        default=hours_to_timedelta("24"),
        action="store",
        help="Number of hours, cloud functions older than which should be considered stale (worthy of cleanup).",
    )

    subparsers = parser.add_subparsers(title="subcommands", required=True)
    parser_summary = subparsers.add_parser(
        "summary",
        help="BigFrames cloud functions summary.",
        description="Show the bigframes cloud functions summary.",
    )
    parser_summary.set_defaults(func=summarize_gcfs)
    parser_cleanup = subparsers.add_parser(
        "cleanup",
        help="BigFrames cloud functions clean up.",
        description="Delete the stale bigframes cloud functions.",
    )
    parser_cleanup.add_argument(
        "-n",
        "--number",
        type=int,
        required=False,
        default=100,
        action="store",
        help="Number of stale (more than a day old) cloud functions to clean up.",
    )
    parser_cleanup.set_defaults(func=cleanup_gcfs)

    args = parser.parse_args(sys.argv[1:])
    if args.project_id is None:
        args.project_id = get_project_from_environment()
        if args.project_id is None:
            raise ValueError(
                "Could not resolve a project. Plese set it via --project-id option."
            )
    args.func(args)
