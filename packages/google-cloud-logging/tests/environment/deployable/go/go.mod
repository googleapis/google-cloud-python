module github.com/googleapis/env-tests-logging/deployable/go/main

go 1.15

require (
	cloud.google.com/go v0.78.0
	cloud.google.com/go/logging v1.3.0
)

replace cloud.google.com/go => ./google-cloud-go/.
replace cloud.google.com/go/logging => ./google-cloud-go/logging