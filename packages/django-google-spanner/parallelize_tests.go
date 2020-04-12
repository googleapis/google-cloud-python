// Copyright 2020 Google LLC.
//
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file or at
// https://developers.google.com/open-source/licenses/bsd

package main

import (
	"context"
	"crypto/sha256"
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

	"cloud.google.com/go/compute/metadata"
	instance "cloud.google.com/go/spanner/admin/instance/apiv1"
	instancepb "google.golang.org/genproto/googleapis/spanner/admin/instance/v1"
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
	startIndex := int(workerIndex) * appsPerWorker
	if startIndex >= len(allApps) {
		startIndex = int(workerIndex)
	}
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

	// Create a unique instance for this worker to circumvent quota limits; to upto 56 seconds.
	createInstanceThrottle := time.Millisecond * time.Duration(417+rng.Intn(54937))
	fmt.Printf("createInstance: throttling by sleeping for %s\n", createInstanceThrottle)
	time.Sleep(createInstanceThrottle)
	instanceName, deleteInstance, err := createInstance()
	if err != nil {
		panic(err)
	}
	defer deleteInstance()
	fmt.Printf("Spanner instance: %q\n", instanceName)

	shutdownCtx, cancel := context.WithCancel(context.Background())
	defer cancel()

	exitCode := int32(0)
	var wg sync.WaitGroup
	defer func() {
		wg.Wait()
		cancel()
		deleteInstance()
		os.Exit(int(exitCode))
	}()

	// Gracefully shutdown on Ctrl+C.
	sigCh := make(chan os.Signal)
	signal.Notify(sigCh, os.Interrupt)
	go func() {
		<-sigCh
		cancel()
		wg.Wait()
		deleteInstance()
	}()

	nProcs := runtime.GOMAXPROCS(0)
	println("GOMAXPROCS:", nProcs)

	// The number of Django apps to run per goroutine.
	nAppsPerG := 3

	if len(testApps) <= nProcs || len(testApps) <= nAppsPerG {
		// We can evenly spread each app per P.
		nAppsPerG = 1
	} else {
		nAppsPerG = len(testApps) / (nAppsPerG * nProcs)
	}
	if nAppsPerG == 0 {
		nAppsPerG = 2
	}

	println("apps per G: ", nAppsPerG)

	emulatorPortIds := int(0)
	envUseEmulator := os.Getenv("USE_SPANNER_EMULATOR")
	useEmulator := envUseEmulator != "0" && envUseEmulator != ""
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

			if err := runTests(shutdownCtx, instanceName, apps, "django_test_suite.sh", genEmulatorHost); err != nil {
				panic(err)
			}
		}(&wg, apps)

		// Add as much jitter as possible.
		<-time.After(871 * time.Millisecond)
	}
}

func runTests(ctx context.Context, instanceName string, djangoApps []string, testSuiteScriptPath string, genEmulatorHost func() string) error {
	if len(djangoApps) == 0 {
		return errors.New("Expected at least one app")
	}

	cmd := exec.CommandContext(ctx, "bash", testSuiteScriptPath)
	cmd.Env = append(os.Environ(), `DJANGO_TEST_APPS=`+strings.Join(djangoApps, " ")+``)
	cmd.Env = append(cmd.Env, "SPANNER_TEST_INSTANCE="+instanceName)
	if emulatorHost := genEmulatorHost(); emulatorHost != "" {
		cmd.Env = append(cmd.Env, "SPANNER_EMULATOR_HOST="+emulatorHost)
	}
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	return cmd.Run()
}

func createInstance() (name string, done func(), xerr error) {
	ctx := context.Background()
	client, err := instance.NewInstanceAdminClient(ctx)
	if err != nil {
		xerr = err
		return
	}

	h := sha256.New()
	fmt.Fprintf(h, "%s", time.Now())
	hs := fmt.Sprintf("%x", h.Sum(nil))
	displayName := fmt.Sprintf("django-%s", hs[:12])

	projectID := strings.TrimSpace(os.Getenv("PROJECT_ID"))
	if projectID == "" {
		xerr = errors.New(`"PROJECT_ID" must be set in your environment`)
		return
	}
	projectPrefix := "projects/" + projectID
	instanceName := projectPrefix + "/instances/" + displayName
	instanceConfig := projectPrefix + "/instanceConfigs/regional-" + findRegion()
	req := &instancepb.CreateInstanceRequest{
		Parent:     projectPrefix,
		InstanceId: displayName,
		Instance: &instancepb.Instance{
			Name:        instanceName,
			DisplayName: displayName,
			NodeCount:   1,
			Config:      instanceConfig,
		},
	}

	op, err := client.CreateInstance(ctx, req)
	if err != nil {
		xerr = err
		return
	}

	res, err := op.Wait(context.Background())
	if err != nil {
		xerr = err
		return
	}
	// Double check that the instance was actually
	// created as we wanted and that its state is READY!
	retrieved, err := client.GetInstance(ctx, &instancepb.GetInstanceRequest{
		Name: res.Name,
	})
	if err != nil {
		xerr = err
		return
	}
	if g, w := retrieved.GetState(), instancepb.Instance_READY; g != w {
		xerr = fmt.Errorf("invalid state of instance:: got %s, want %s", g, w)
	}

	// The short name of reference for the Spanner instance, and not its InstanceName.
	name = retrieved.DisplayName
	deletionName := retrieved.Name
	var doneOnce sync.Once
	done = func() {
		doneOnce.Do(func() {
			if err := client.DeleteInstance(ctx, &instancepb.DeleteInstanceRequest{Name: deletionName}); err == nil {
				fmt.Printf("Deleted instance: %q\n", name)
			} else {
				fmt.Printf("Failed to delete instance: %q ==> %v\n", name, err)
			}
		})
	}
	return
}

func findRegion() string {
	zone := "us-central1-b"
	if metadata.OnGCE() {
		foundZone, err := metadata.Zone()
		if err == nil {
			zone = foundZone
		}
	}
	// There is no metadata API to retrieve the region from the zone,
	// so we have to improvise and trim off the last '-' e.g.
	// with a zone of "us-central1-b", the region will be "us-central".
	return zone[:strings.LastIndex(zone, "-")]
}
