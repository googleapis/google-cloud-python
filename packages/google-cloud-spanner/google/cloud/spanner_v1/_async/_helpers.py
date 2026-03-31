import asyncio
import inspect
import time

from google.api_core.exceptions import Aborted


async def _delay_until_retry(exc, deadline, attempts, default_retry_delay=None):
    from google.cloud.spanner_v1._helpers import _get_retry_delay

    cause = exc.errors[0] if hasattr(exc, "errors") and exc.errors else exc
    now = time.time()
    if now >= deadline:
        raise exc

    delay = _get_retry_delay(cause, attempts, default_retry_delay)
    if now + delay > deadline:
        raise exc

    await asyncio.sleep(delay)


async def _retry_on_aborted_exception(func, deadline, default_retry_delay=None):
    attempts = 0
    while True:
        try:
            attempts += 1
            return await func()
        except Aborted as exc:
            await _delay_until_retry(
                exc,
                deadline=deadline,
                attempts=attempts,
                default_retry_delay=default_retry_delay,
            )
            continue


async def _retry(
    func,
    retry_count=5,
    delay=2,
    allowed_exceptions=None,
    before_next_retry=None,
):
    retries = 0
    while True:
        try:
            res = func()
            if asyncio.iscoroutine(res) or inspect.isawaitable(res):
                return await res
            return res
        except Exception as e:
            if allowed_exceptions is not None:
                if type(e) not in allowed_exceptions:
                    raise e
                _check_err = allowed_exceptions.get(type(e))
                if callable(_check_err) and not _check_err(e):
                    raise e
            if retries >= retry_count:
                raise e
            if before_next_retry:
                res = before_next_retry(retries, delay)
                if asyncio.iscoroutine(res) or inspect.isawaitable(res):
                    await res
            await asyncio.sleep(delay)
            retries += 1


def _create_experimental_host_transport(
    transport_factory,
    experimental_host,
    use_plain_text,
    ca_certificate,
    client_certificate,
    client_key,
    interceptors=None,
):
    """Creates an experimental host transport for Spanner in async mode.

    Args:
        transport_factory (type): The transport class to instantiate (e.g.
            `SpannerGrpcAsyncIOTransport`).
        experimental_host (str): The endpoint for the experimental host.
        use_plain_text (bool): Whether to use a plain text (insecure) connection.
        ca_certificate (str): Path to the CA certificate file for TLS.
        client_certificate (str): Path to the client certificate file for mTLS.
        client_key (str): Path to the client key file for mTLS.
        interceptors (list): Optional list of interceptors to add to the channel.

    Returns:
        object: An instance of the transport class created by `transport_factory`.

    Raises:
        ValueError: If TLS/mTLS configuration is invalid.
    """
    from google.auth.credentials import AnonymousCredentials
    import grpc.aio

    channel = None
    if use_plain_text:
        channel = grpc.aio.insecure_channel(
            target=experimental_host, interceptors=interceptors
        )
    elif ca_certificate:
        with open(ca_certificate, "rb") as f:
            ca_cert = f.read()
        if client_certificate and client_key:
            with open(client_certificate, "rb") as f:
                client_cert = f.read()
            with open(client_key, "rb") as f:
                private_key = f.read()
            ssl_creds = grpc.ssl_channel_credentials(
                root_certificates=ca_cert,
                private_key=private_key,
                certificate_chain=client_cert,
            )
        elif client_certificate or client_key:
            raise ValueError(
                "Both client_certificate and client_key must be provided for mTLS connection"
            )
        else:
            ssl_creds = grpc.ssl_channel_credentials(root_certificates=ca_cert)
        channel = grpc.aio.secure_channel(
            experimental_host, ssl_creds, interceptors=interceptors
        )
    else:
        raise ValueError(
            "TLS/mTLS connection requires ca_certificate to be set for experimental_host"
        )
    return transport_factory(channel=channel, credentials=AnonymousCredentials())
