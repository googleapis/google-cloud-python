// Copyright 2020 Google LLC.
//
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file or at
// https://developers.google.com/open-source/licenses/bsd

package main

import (
	"context"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"math/rand"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	workerIndex, err := strconv.ParseInt(os.Getenv("DJANGO_WORKER_INDEX"), 10, 64)
	if err != nil {
		log.Fatalf("Failed to parse DJANGO_WORKER_INDEX as an integer: %v", err)
	}
	workerCount, err := strconv.ParseInt(os.Getenv("DJANGO_WORKER_COUNT"), 10, 64)
	if err != nil {
		log.Fatalf("Failed to parse DJANGO_WORKER_COUNT as an integer: %v", err)
	}
	if workerIndex >= workerCount {
		// Re-enable when we figure out how to deal with Cloud Spanner's very low quotas.
		fmt.Printf("workerIndex (%d) >= workerCount (%d)", workerIndex, workerCount)
		return
	}
	allAppsBlob, err := ioutil.ReadFile("django_test_apps.txt")
	if err != nil {
		panic(err)
	}
	allApps := strings.Split(string(allAppsBlob), "\n")
	appsPerWorker := int(math.Ceil(float64(len(allApps)) / float64(workerCount)))
	if err != nil {
		log.Fatalf("Failed to parse WORKER_COUNT: %v", err)
	}
	startIndex := int(workerIndex) * appsPerWorker
	endIndex := startIndex + appsPerWorker
	if endIndex >= len(allApps) {
		endIndex = len(allApps)
	}
	testApps := allApps[startIndex:endIndex]
	println("startIndex:", startIndex, "endIndex:", endIndex, "totalApps", len(testApps))
	if len(testApps) == 0 {
		panic("No DJANGO_TEST_APPS passed in")
	}

	// Seeding the random generator only using time.Now() as that's sufficient
	// just to add jitter and reduce resource exhaustion limits.
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	rng.Shuffle(len(testApps), func(i, j int) {
		testApps[i], testApps[j] = testApps[j], testApps[i]
	})

	// Otherwise, we'll parallelize the builds.
	nProcs := runtime.GOMAXPROCS(0)
	println("GOMAXPROCS:", nProcs)

	shutdownCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	exitCode := int32(0)
	var wg sync.WaitGroup
	defer func() {
		wg.Wait()
		os.Exit(int(exitCode))
	}()

	// Gracefully shutdown on Ctrl+C.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt)
	go func() {
		<-sigCh
		cancel()
		wg.Wait()
	}()

	// The number of Django apps to run per goroutine.
	nAppsPerG := 3
	if len(testApps) <= nAppsPerG {
		nAppsPerG = 1
	} else {
		nAppsPerG = len(testApps) / (nAppsPerG * nProcs)
	}
	println("apps per G: ", nAppsPerG)

	if nAppsPerG == 0 {
		nAppsPerG = 2
	}

	emulatorPortIds := int(0)
	useEmulator := os.Getenv("USE_SPANNER_EMULATOR") != ""
	genEmulatorHost := func() string {
		if !useEmulator {
			return ""
		}
		emulatorPortIds++
		return fmt.Sprintf("localhost:%d", 9010+emulatorPortIds)
	}

	sema := make(chan bool, nProcs)
	// Now run the tests in parallel.
	for i := 0; i < len(testApps); i += nAppsPerG {
		apps := testApps[i : i+nAppsPerG]
		if len(apps) == 0 {
			continue
		}

		select {
		case <-shutdownCtx.Done():
			// No more spawning goroutines, the test has been cancelled.
			return

		case sema <- true:
			// Proceed normally.
			wg.Add(1)
		}

		go func(wg *sync.WaitGroup, apps []string) {
			defer func() {
				if r := recover(); r != nil {
					// Recover to ensure that other tests can
					// proceed regardless of any goroutine panic.
					fmt.Printf("\033[31m%v\033[00m\n", r)
					atomic.StoreInt32(&exitCode, -1)
				}

				wg.Done()

				select {
				case <-sema:
				case <-shutdownCtx.Done():
				}
			}()

			var throttle time.Duration
			if !useEmulator {
				// Artificially add a wait time so as to ensure that we don't
				// violate Cloud Spanner's 5QPs averaged over 100 seconds.
				// Here our throttle will be in the range:
				//      [1, 6 * (100sec / 5QPs)] aka [1s, 120sec]
				// to try to introduce variability.
				throttle = (time.Millisecond * time.Duration(rng.Intn(937))) + (time.Second * time.Duration(1+rng.Intn(int(6*100/5.0))))
				fmt.Printf("Throttling by sleeping for %s\n", throttle)
			}

			select {
			case <-shutdownCtx.Done():
				println("Canceled so returning ASAP")
				return
			case <-time.After(throttle):
			}

			if err := runTests(shutdownCtx, apps, "django_test_suite.sh", genEmulatorHost); err != nil {
				panic(err)
			}
		}(&wg, apps)
	}
}

func runTests(ctx context.Context, djangoApps []string, testSuiteScriptPath string, genEmulatorHost func() string) error {
	if len(djangoApps) == 0 {
		return errors.New("Expected at least one app")
	}

	cmd := exec.CommandContext(ctx, "bash", testSuiteScriptPath)
	cmd.Env = append(os.Environ(), `DJANGO_TEST_APPS=`+strings.Join(djangoApps, " ")+``)
	if emulatorHost := genEmulatorHost(); emulatorHost != "" {
		cmd.Env = append(cmd.Env, "SPANNER_EMULATOR_HOST="+emulatorHost)
	}
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	return cmd.Run()
}
