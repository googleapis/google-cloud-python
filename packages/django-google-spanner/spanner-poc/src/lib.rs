//! # Spanner Native PyO3 Extension — GIL-Releasing gRPC Client
//!
//! ## GIL Release Mechanism Explained
//!
//! Under Python's default Global Interpreter Lock (GIL), only one thread can execute
//! Python bytecode at a time. When multiple threads perform high-throughput Cloud Spanner
//! operations, they frequently contend for the GIL during Python-level Protobuf serialization
//! and deserialization. This serializes the CPU execution time and limits overall throughput
//! to a hard ceiling of ~1000 QPS, regardless of available CPU cores or network channels.
//!
//! This Rust native extension addresses the bottleneck by moving the gRPC dispatch, network
//! transport, and Protobuf serialization and deserialization out of CPython entirely.
//!
//! By calling `py.allow_threads(|| { ... })`, we temporarily release the GIL during the entire
//! network round-trip. This allows other Python threads to acquire the GIL and dispatch
//! parallel requests concurrently. The multi-threaded Tokio runtime executes the async gRPC
//! requests in Rust, multiplexing concurrent requests over a single shared HTTP/2 transport
//! channel. When the network call completes, the GIL is reacquired to convert the returned
//! Rust-deserialized `ResultSet` values back to native Python objects.

use once_cell::sync::Lazy;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use tokio::runtime::Runtime;
use tonic::transport::{Channel, ClientTlsConfig};

// Include the generated code from tonic-build (build.rs output)
pub mod google {
    pub mod spanner {
        pub mod v1 {
            tonic::include_proto!("google.spanner.v1");
        }
    }
    pub mod rpc {
        tonic::include_proto!("google.rpc");
    }
    pub mod api {
        tonic::include_proto!("google.api");
    }
}

use google::spanner::v1::spanner_client::SpannerClient;
use google::spanner::v1::{ExecuteSqlRequest, ResultSet};

/// Shared multi-threaded Tokio runtime used to drive the async tonic gRPC client.
/// Configured with a pool of 4 dedicated threads to manage concurrent I/O.
static RUNTIME: Lazy<Runtime> = Lazy::new(|| {
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .build()
        .expect("Failed to initialize multi-threaded Tokio runtime")
});

/// Static shared connection channels pointing to the Spanner production endpoint.
/// We establish 4 distinct TCP/TLS connections to maximize concurrent I/O multiplexing.
static CHANNELS: Lazy<Vec<Channel>> = Lazy::new(|| {
    let endpoint = "https://spanner.googleapis.com:443";
    let mut tls_config = ClientTlsConfig::new().domain_name("spanner.googleapis.com");

    // Load system CA certificates to trust corporate proxy certs on Linux VMs
    let ca_paths = [
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/etc/ssl/ca-bundle.pem",
        "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",
    ];

    let mut cert_loaded = false;
    for path in &ca_paths {
        if let Ok(cert_bytes) = std::fs::read(path) {
            let cert = tonic::transport::Certificate::from_pem(cert_bytes);
            tls_config = tls_config.ca_certificate(cert);
            cert_loaded = true;
            break; // Successfully loaded the system bundle!
        }
    }

    if !cert_loaded {
        // Fallback: use enabled roots (webpki roots) if native files are not found (e.g. on Mac)
        tls_config = tls_config.with_enabled_roots();
    }

    let mut channels = Vec::new();
    RUNTIME.block_on(async {
        for _ in 0..4 {
            let ep = tonic::transport::Endpoint::from_static(endpoint)
                .tls_config(tls_config.clone())
                .expect("Failed to build TLS configuration endpoint");
            let channel = ep.connect()
                .await
                .expect("Failed to establish connection to spanner.googleapis.com");
            channels.push(channel);
        }
    });
    channels
});

/// Tonic gRPC interceptor to inject standard authentication and routing headers on every call.
#[derive(Clone)]
struct AuthInterceptor {
    token: String,
    session_name: String,
}

impl tonic::service::Interceptor for AuthInterceptor {
    fn call(&mut self, mut request: tonic::Request<()>) -> Result<tonic::Request<()>, tonic::Status> {
        // 1. Inject OAuth Bearer token header
        let bearer_token = format!("Bearer {}", self.token);
        let meta_value = tonic::metadata::MetadataValue::try_from(bearer_token)
            .map_err(|_| tonic::Status::invalid_argument("Invalid OAuth token string"))?;
        request.metadata_mut().insert("authorization", meta_value);

        // 2. Inject google-cloud-resource-prefix header for optimal regional routing
        // session_name format: projects/<PROJECT>/instances/<INSTANCE>/databases/<DATABASE>/sessions/<SESSION_ID>
        if let Some(idx) = self.session_name.find("/sessions/") {
            let db_prefix = &self.session_name[..idx];
            if let Ok(prefix_value) = tonic::metadata::MetadataValue::try_from(db_prefix) {
                request.metadata_mut().insert("google-cloud-resource-prefix", prefix_value);
            }
        } else if let Ok(prefix_value) = tonic::metadata::MetadataValue::try_from(&self.session_name) {
            request.metadata_mut().insert("google-cloud-resource-prefix", prefix_value);
        }

        Ok(request)
    }
}

/// Recursive helper to safely translate prost_types::Value structures into native Python objects.
fn proto_value_to_python(py: Python<'_>, value: &prost_types::Value) -> PyObject {
    use prost_types::value::Kind;
    match &value.kind {
        Some(Kind::NullValue(_)) => py.None(),
        Some(Kind::NumberValue(n)) => n.into_py(py),
        Some(Kind::StringValue(s)) => s.into_py(py),
        Some(Kind::BoolValue(b)) => b.into_py(py),
        Some(Kind::StructValue(s)) => {
            let dict = pyo3::types::PyDict::new_bound(py);
            for (k, v) in &s.fields {
                let py_val = proto_value_to_python(py, v);
                let _ = dict.set_item(k, py_val);
            }
            dict.to_object(py)
        }
        Some(Kind::ListValue(l)) => {
            let list = pyo3::types::PyList::empty_bound(py);
            for v in &l.values {
                let py_val = proto_value_to_python(py, v);
                let _ = list.append(py_val);
            }
            list.to_object(py)
        }
        None => py.None(),
    }
}

use std::sync::atomic::{AtomicUsize, Ordering};
static REQUEST_COUNTER: AtomicUsize = AtomicUsize::new(0);

/// Executes an SQL query natively in Rust, releasing the Python GIL during gRPC wait and serialization.
///
/// # Arguments
/// * `py` - CPython engine reference.
/// * `session_name` - Fully qualified Spanner session string.
/// * `sql` - The SQL query to run.
/// * `token` - Valid authorization token string.
/// * `use_multi_channel` - If true, load-balances across 4 distinct connections.
#[pyfunction]
fn execute_sql_native(
    py: Python<'_>,
    session_name: String,
    sql: String,
    token: String,
    use_multi_channel: bool,
) -> PyResult<PyObject> {
    // Clone string arguments to owned types before entering allow_threads.
    // Once GIL is released, Rust cannot touch Python-allocated memory/pointers.
    let session_clone = session_name.clone();
    let sql_clone = sql.clone();
    let token_clone = token.clone();

    let result: Result<ResultSet, tonic::Status> = py.allow_threads(|| {
        // Select the appropriate connection channel based on the flag
        let channel = if use_multi_channel {
            let idx = REQUEST_COUNTER.fetch_add(1, Ordering::Relaxed) % CHANNELS.len();
            CHANNELS[idx].clone()
        } else {
            CHANNELS[0].clone()
        };

        // Build a thread-local single-threaded runtime for zero lock contention
        let rt = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .map_err(|_| tonic::Status::internal("Failed to build thread-local runtime"))?;

        rt.block_on(async move {
            let interceptor = AuthInterceptor {
                token: token_clone,
                session_name: session_clone.clone(),
            };
            let mut client = SpannerClient::with_interceptor(channel, interceptor);

            let request = ExecuteSqlRequest {
                session: session_clone,
                sql: sql_clone,
                ..Default::default()
            };

            let response = client.execute_sql(request).await?;
            Ok(response.into_inner())
        })
    });

    // Re-acquire the GIL here. Convert the returned ResultSet to native Python Lists.
    match result {
        Ok(result_set) => {
            let rows_list = pyo3::types::PyList::empty_bound(py);
            for row in result_set.rows {
                let row_values = pyo3::types::PyList::empty_bound(py);
                for val in row.values {
                    let py_val = proto_value_to_python(py, &val);
                    row_values.append(py_val)?;
                }
                rows_list.append(row_values)?;
            }
            Ok(rows_list.to_object(py))
        }
        Err(status) => Err(PyRuntimeError::new_err(format!(
            "gRPC Spanner execution failed: (status: {:?}) {}",
            status.code(),
            status.message()
        ))),
    }
}

/// Registers the PyO3 extension module functions.
#[pymodule]
fn spanner_poc(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(execute_sql_native, m)?)?;
    Ok(())
}
