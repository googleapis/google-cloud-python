# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import atexit
import http.server
import json
import socketserver
import threading
from typing import Dict, List


def execute_node_expansion(params, request):
    return {"error": "Node expansion not yet implemented"}


def convert_graph_data(query_results: Dict[str, Dict[str, str]]):
    """
    Converts graph data to the form expected by the visualization framework.

    Receives graph data as a dictionary, produced by converting the underlying
    DataFrame representing the query results into JSON, then into a
    python dictionary. Converts it into a form expected by the visualization
    framework.

    Args:
        query_results:
            A dictionary with one key/value pair per column. For each column:
            - The key is the name of the column (str)
            - The value is another dictionary with one key/value pair per row.
              Row each row:
              - The key is a string that specifies the integer index of the row
                (e.g. '0', '1', '2')
              - The value is a JSON string containing the result of the query
                for the current row/column. (Note: We only support graph
                visualization for columns of type JSON).
    """
    # Delay spanner imports until this function is called to avoid making
    # spanner-graph-notebook (and its dependencies) hard requirements for bigquery
    # magics users, who don't need graph visualization.
    #
    # Note that these imports do not need to be in a try/except, as this function
    # does not even get called unless spanner_graphs has already been confirmed
    # to exist upstream.
    from google.cloud.spanner_v1.types import StructType, Type, TypeCode
    from spanner_graphs.conversion import get_nodes_edges

    try:
        fields: List[StructType.Field] = []
        data = {}
        tabular_data = {}
        for key, value in query_results.items():
            column_name = None
            column_value = None
            if not isinstance(key, str):
                raise ValueError(f"Expected outer key to be str, got {type(key)}")
            if not isinstance(value, dict):
                raise ValueError(f"Expected outer value to be dict, got {type(value)}")
            column_name = key
            column_value = value

            fields.append(
                StructType.Field(name=column_name, type=Type(code=TypeCode.JSON))
            )
            data[column_name] = []
            tabular_data[column_name] = []
            for value_key, value_value in column_value.items():
                try:
                    row_json = json.loads(value_value)
                    data[column_name].append(row_json)
                    tabular_data[column_name].append(row_json)
                except (ValueError, TypeError):
                    # Non-JSON columns cannot be visualized, but we still want them
                    # in the tabular view.
                    tabular_data[column_name].append(str(value_value))

        nodes, edges = get_nodes_edges(data, fields, schema_json=None)

        # Convert nodes and edges to json objects.
        # (Unfortunately, the code coverage tooling does not allow this
        #  to be expressed as list comprehension).
        nodes_json = []
        for node in nodes:
            nodes_json.append(node.to_json())
        edges_json = []
        for edge in edges:
            edges_json.append(edge.to_json())

        return {
            "response": {
                # These fields populate the graph result view.
                "nodes": nodes_json,
                "edges": edges_json,
                # This populates the visualizer's schema view, but not yet implemented on the
                # BigQuery side.
                "schema": None,
                # This field is used to populate the visualizer's tabular view.
                "query_result": tabular_data,
            }
        }
    except Exception as e:
        return {"error": getattr(e, "message", str(e))}


class GraphServer:
    """
    Http server invoked by Javascript to obtain the query results for visualization.

    The server is invoked by Javascript, generated as part of
    spanner_graphs.graph_visualization.generate_visualization_html().

    This server is used only in Jupyter; in colab, google.colab.output.register_callback()
    is used instead.
    """

    host = "http://localhost"
    endpoints = {
        "get_ping": "/get_ping",
        "post_ping": "/post_ping",
        "post_node_expansion": "/post_node_expansion",
        "post_query": "/post_query",
    }

    def __init__(self):
        self.port = None
        self.url = None
        self._server = None

    def build_route(self, endpoint):
        """
        Returns a url for connecting to the given endpoint.
        Supported values include:
          - "get_ping": sends a GET request to ping the server.
          - "post_ping": sends a POST request to ping the server.
          - "post_query": sends a POST request to obtain query results.
        """
        return f"{self.url}{endpoint}"

    def _start_server(self):
        class ThreadedTCPServer(socketserver.TCPServer):
            # Allow socket reuse to avoid "Address already in use" errors
            allow_reuse_address = True
            # Daemon threads automatically terminate when the main program exits
            daemon_threads = True

        with ThreadedTCPServer(("", self.port), GraphServerHandler) as httpd:
            self._server = httpd
            self._server.serve_forever()

    def init(self):
        """
        Starts the HTTP server. The server runs forever, until stop_server() is called.
        """
        import portpicker

        self.port = portpicker.pick_unused_port()
        self.url = f"{GraphServer.host}:{self.port}"

        server_thread = threading.Thread(target=self._start_server)
        server_thread.start()
        return server_thread

    def stop_server(self):
        """
        Starts the HTTP server, if it is currently running.
        """
        if self._server:
            self._server.shutdown()
            print("BigQuery-magics graph server shutting down...")
            self._server = None


global graph_server
graph_server = GraphServer()


class GraphServerHandler(http.server.SimpleHTTPRequestHandler):
    """
    Handles HTTP requests send to the graph server.
    """

    def log_message(self, format, *args):
        pass

    def do_json_response(self, data):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_message_response(self, message):
        self.do_json_response({"message": message})

    def do_data_response(self, data):
        self.do_json_response(data)

    def parse_post_data(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        return json.loads(post_data)

    def handle_get_ping(self):
        self.do_message_response("pong")

    def handle_post_ping(self):
        data = self.parse_post_data()
        self.do_data_response({"your_request": data})

    def handle_post_query(self):
        data = self.parse_post_data()
        response = convert_graph_data(query_results=json.loads(data["params"]))
        self.do_data_response(response)

    def handle_post_node_expansion(self):
        """Handle POST requests for node expansion.

        Expects a JSON payload with:
        - params: A JSON string containing connection parameters (project, instance, database, graph)
        - request: A dictionary with node details (uid, node_labels, node_properties, direction, edge_label)
        """
        data = self.parse_post_data()

        # Execute node expansion with:
        # - params_str: JSON string with connection parameters (project, instance, database, graph)
        # - request: Dict with node details (uid, node_labels, node_properties, direction, edge_label)
        self.do_data_response(
            execute_node_expansion(
                params=data.get("params"), request=data.get("request")
            )
        )

    def do_GET(self):
        assert self.path == GraphServer.endpoints["get_ping"]
        self.handle_get_ping()

    def do_POST(self):
        if self.path == GraphServer.endpoints["post_ping"]:
            self.handle_post_ping()
        elif self.path == GraphServer.endpoints["post_node_expansion"]:
            self.handle_post_node_expansion()
        else:
            assert self.path == GraphServer.endpoints["post_query"]
            self.handle_post_query()


atexit.register(graph_server.stop_server)
