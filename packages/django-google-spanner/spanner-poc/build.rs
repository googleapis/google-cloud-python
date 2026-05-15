fn main() -> Result<(), Box<dyn std::error::Error>> {
    // We compile the gRPC Spanner client protos.
    // Transitive dependencies are resolved from /tmp/googleapis and spanner-poc/proto.
    let proto_files = &[
        "proto/google/spanner/v1/spanner.proto",
        "proto/google/spanner/v1/transaction.proto",
        "proto/google/spanner/v1/result_set.proto",
    ];

    let include_dirs = &[
        "proto",
        "/tmp/googleapis",
    ];

    println!("cargo:rerun-if-changed=proto");
    println!("cargo:rerun-if-changed=build.rs");

    tonic_build::configure()
        .build_server(false) // Only generate client code
        .compile(proto_files, include_dirs)?;

    Ok(())
}
