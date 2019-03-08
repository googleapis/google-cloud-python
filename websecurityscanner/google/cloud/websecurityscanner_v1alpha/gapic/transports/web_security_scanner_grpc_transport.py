# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers

from google.cloud.websecurityscanner_v1alpha.proto import web_security_scanner_pb2_grpc


class WebSecurityScannerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.websecurityscanner.v1alpha WebSecurityScanner API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        channel=None,
        credentials=None,
        address="websecurityscanner.googleapis.com:443",
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "web_security_scanner_stub": web_security_scanner_pb2_grpc.WebSecurityScannerStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="websecurityscanner.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_scan_config(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.create_scan_config`.

        Creates a new ScanConfig.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].CreateScanConfig

    @property
    def delete_scan_config(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.delete_scan_config`.

        Deletes an existing ScanConfig and its child resources.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].DeleteScanConfig

    @property
    def get_scan_config(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.get_scan_config`.

        Gets a ScanConfig.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].GetScanConfig

    @property
    def list_scan_configs(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.list_scan_configs`.

        Lists ScanConfigs under a given project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].ListScanConfigs

    @property
    def update_scan_config(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.update_scan_config`.

        Updates a ScanConfig. This method support partial update of a ScanConfig.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].UpdateScanConfig

    @property
    def start_scan_run(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.start_scan_run`.

        Start a ScanRun according to the given ScanConfig.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].StartScanRun

    @property
    def get_scan_run(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.get_scan_run`.

        Gets a ScanRun.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].GetScanRun

    @property
    def list_scan_runs(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.list_scan_runs`.

        Lists ScanRuns under a given ScanConfig, in descending order of ScanRun
        stop time.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].ListScanRuns

    @property
    def stop_scan_run(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.stop_scan_run`.

        Stops a ScanRun. The stopped ScanRun is returned.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].StopScanRun

    @property
    def list_crawled_urls(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.list_crawled_urls`.

        List CrawledUrls under a given ScanRun.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].ListCrawledUrls

    @property
    def get_finding(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.get_finding`.

        Gets a Finding.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].GetFinding

    @property
    def list_findings(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.list_findings`.

        List Findings under a given ScanRun.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].ListFindings

    @property
    def list_finding_type_stats(self):
        """Return the gRPC stub for :meth:`WebSecurityScannerClient.list_finding_type_stats`.

        List all FindingTypeStats under a given ScanRun.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["web_security_scanner_stub"].ListFindingTypeStats
