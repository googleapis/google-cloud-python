// Copyright 2020 Google LLC.
//
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file or at
// https://developers.google.com/open-source/licenses/bsd

package main

import (
	"context"
	"errors"
	"math/rand"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strings"
	"sync"

	"github.com/orijtech/otils"
)

func main() {
	testApps := otils.NonEmptyStrings(strings.Split(os.Getenv("DJANGO_TEST_APPS"), " ")...)
	if len(testApps) == 0 {
		panic("No DJANGO_TEST_APPS passed in")
	}

	rand.Shuffle(len(testApps), func(i, j int) {
		testApps[i], testApps[j] = testApps[j], testApps[i]
	})

	// Otherwise, we'll parallelize the builds.
	nProcs := runtime.GOMAXPROCS(0)
	println("nProcs", nProcs)

	shutdownCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Gracefully shutdown on Ctrl+C.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt)
	go func() {
		<-sigCh
		cancel()
	}()

	var wg sync.WaitGroup
	defer wg.Wait()

	// The number of Django apps to run per goroutine.
	nAppsPerG := 4
	if len(testApps) <= nAppsPerG {
		nAppsPerG = 1
	} else {
		nAppsPerG = len(testApps) / (nAppsPerG * nProcs)
	}
	println("apps per G: ", nAppsPerG)

	if nAppsPerG == 0 {
		nAppsPerG = 2
	}

	sema := make(chan bool, nProcs)
	// Now run the tests in parallel.
	for i := 0; i < len(testApps); i += nAppsPerG {
		apps := testApps[i : i+nAppsPerG]
		wg.Add(1)
		sema <- true

		go func(wg *sync.WaitGroup, apps []string) {
			defer func() {
				<-sema
				wg.Done()
			}()

			if len(apps) == 0 {
				return
			}
			if err := runTests(shutdownCtx, apps, "django_test_suite.sh"); err != nil {
				panic(err)
			}
		}(&wg, apps)
	}
}

func runTests(ctx context.Context, djangoApps []string, testSuiteScriptPath string) error {
	if len(djangoApps) == 0 {
		return errors.New("Expected at least one app")
	}

	cmd := exec.CommandContext(ctx, "bash", testSuiteScriptPath)
	cmd.Env = append(os.Environ(), `DJANGO_TEST_APPS=`+strings.Join(djangoApps, " ")+``)
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	return cmd.Run()
}
