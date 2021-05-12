module github.com/googleapis/env-tests-logging/deployable/go/main

go 1.15

require (
	cloud.google.com/go v0.81.0
	cloud.google.com/go/logging v1.4.0
	cloud.google.com/go/pubsub v1.3.1
	google.golang.org/grpc v1.37.0
)

replace cloud.google.com/go/logging => ./logging
