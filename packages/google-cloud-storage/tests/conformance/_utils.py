import os
import socket
import subprocess
import time
import traceback
from typing import Optional, Tuple

import requests

DEFAULT_TESTBENCH_IMAGE = (
    "gcr.io/cloud-devrel-public-resources/storage-testbench:latest"
)


def get_container_docker_network() -> Optional[str]:
    """Return a shared user-defined Docker network (e.g. 'cloudbuild') when
    running inside a container attached to one, or None on a regular host.
    """
    if not os.path.exists("/.dockerenv"):
        return None
    hostname = socket.gethostname()
    try:
        result = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}",
                hostname,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode == 0:
            networks = [
                net
                for net in result.stdout.strip().split()
                if net and net not in ("bridge", "host", "none")
            ]
            if "cloudbuild" in networks:
                return "cloudbuild"
            if networks:
                return networks[0]
        # Fallback if container hostname was overridden from container ID.
        cb_check = subprocess.run(
            ["docker", "network", "inspect", "cloudbuild"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            check=False,
        )
        if cb_check.returncode == 0:
            return "cloudbuild"
    except (OSError, subprocess.SubprocessError):
        return None
    return None


def stop_testbench(container_name: str) -> None:
    """Force-remove a running storage-testbench container, ignoring errors."""
    subprocess.run(
        ["docker", "rm", "-f", container_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def start_testbench(
    container_name: str,
    host_http_port: int,
    host_grpc_port: Optional[int] = None,
    image: str = DEFAULT_TESTBENCH_IMAGE,
    ready_timeout: float = 30.0,
) -> Tuple[str, Optional[str]]:
    """Pull and start storage-testbench, returning (http_endpoint, grpc_endpoint).

    When running inside a container on a Docker network (such as Cloud Build's
    'cloudbuild' network), attaches the testbench to that same network and
    returns container-DNS endpoints; otherwise publishes host ports on localhost.
    """
    subprocess.run(["docker", "pull", image], check=True)
    stop_testbench(container_name)

    network = get_container_docker_network()
    if network:
        cmd = [
            "docker",
            "run",
            "--rm",
            "-d",
            "--name",
            container_name,
            "--network",
            network,
            image,
        ]
        http_endpoint = f"http://{container_name}:9000"
        grpc_endpoint = (
            f"{container_name}:{host_grpc_port}" if host_grpc_port is not None else None
        )
    else:
        cmd = [
            "docker",
            "run",
            "--rm",
            "-d",
            "--name",
            container_name,
            "-p",
            f"{host_http_port}:9000",
        ]
        if host_grpc_port is not None:
            cmd.extend(["-p", f"{host_grpc_port}:{host_grpc_port}"])
        cmd.append(image)
        http_endpoint = f"http://localhost:{host_http_port}"
        grpc_endpoint = (
            f"localhost:{host_grpc_port}" if host_grpc_port is not None else None
        )

    subprocess.run(cmd, check=True)

    deadline = time.time() + ready_timeout
    last_err = None
    while time.time() < deadline:
        try:
            requests.get(f"{http_endpoint}/", timeout=2)
            return http_endpoint, grpc_endpoint
        except requests.exceptions.RequestException as exc:
            last_err = exc
            time.sleep(0.5)

    stop_testbench(container_name)
    raise RuntimeError(
        f"storage-testbench ({container_name}) did not become ready at "
        f"{http_endpoint} within {ready_timeout}s: {last_err}"
    )


def start_grpc_server(grpc_endpoint, http_endpoint):
    """Starts the testbench gRPC server if it's not already running.

    this essentially makes -

    `curl -s --retry 5 --retry-max-time 40 "http://localhost:9000/start_grpc?port=8888"`
    """
    start_time = time.time()
    max_time = 40
    retries = 5
    port = grpc_endpoint.split(":")[-1]
    url = f"{http_endpoint}/start_grpc?port={port}"

    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            print("Failed to create grpc server", traceback.format_exc())
            raise

        elapsed_time = time.time() - start_time
        if elapsed_time >= max_time:
            raise RuntimeError("Failed to start gRPC server within the time limit.")

        # backoff
        time.sleep(1)
