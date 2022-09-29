module github.com/googleapis/env-tests-logging/deployable/go/main

go 1.15

require (
	cloud.google.com/go/compute v1.7.0
	cloud.google.com/go/kms v1.4.0 // indirect
	cloud.google.com/go/logging v1.4.0
	cloud.google.com/go/pubsub v1.3.1
	google.golang.org/grpc v1.48.0
)

replace cloud.google.com/go/logging => ./logging
