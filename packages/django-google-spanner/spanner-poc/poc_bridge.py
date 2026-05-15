import threading
import google.auth
import google.auth.transport.requests
from google.cloud import spanner

# Import the compiled Rust extension module
try:
    import spanner_poc
except ImportError:
    # In case the module hasn't been compiled or loaded yet during planning
    spanner_poc = None


class NativeSpannerDatabase:
    """Bridges the official google-cloud-spanner Python library with our compiled

    Rust gRPC extension, delegating the core database calls while retaining standard
    session pool and authentication mechanisms.
    """

    def __init__(self, project: str, instance_id: str, database_id: str):
        # Initialize standard Python Spanner Client
        self._client = spanner.Client(project=project)
        self._instance = self._client.instance(instance_id)
        self._database = self._instance.database(database_id)

        # Load default application credentials with Spanner scope
        scopes = ["https://www.googleapis.com/auth/spanner.data"]
        self._credentials, _ = google.auth.default(scopes=scopes)
        self._token_lock = threading.Lock()
        self._auth_request = google.auth.transport.requests.Request()

    def _get_fresh_token(self) -> str:
        """Retrieves a fresh OAuth2 access token.

        Protects the refresh logic with a threading lock to prevent multi-threaded
        race conditions during high-concurrency execution.
        """
        with self._token_lock:
            # refresh() is cheap and a no-op if the token is still valid
            self._credentials.refresh(self._auth_request)
            return self._credentials.token

    def _get_session_name(self) -> str:
        """POC Session Hack: checks out a session from the Python pool, extracts

        its session name, and immediately returns it to the pool.
        In production, session pool management would be fully implemented in Rust.
        """
        # We use the snapshot context manager to borrow a session, copy its name,
        # and immediately release it back to the pool by exiting the context.
        with self._database.snapshot() as snapshot:
            session_name = snapshot._session.name
        return session_name

    def execute_sql_native(self, sql: str) -> list:
        """Executes SQL natively using the Rust/PyO3 extension, releasing the GIL."""
        if spanner_poc is None:
            raise RuntimeError(
                "Rust extension 'spanner_poc' is not compiled or installed. "
                "Please run maturin develop --release."
            )

        session_name = self._get_session_name()
        token = self._get_fresh_token()

        # Call native Rust function which releases the GIL during the transport phase
        return spanner_poc.execute_sql_native(session_name, sql, token)

    def execute_sql_python(self, sql: str) -> list:
        """Baseline execution path using the standard Python Spanner library."""
        with self._database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql)
            # Convert to a Python list of lists to match the output format of the Rust extension
            return [list(row) for row in results]
