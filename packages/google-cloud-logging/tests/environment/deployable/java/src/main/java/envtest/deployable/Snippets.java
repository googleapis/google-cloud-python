// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package envtest.deployable;
import java.util.Map;
import java.util.Collections;

import com.google.cloud.MonitoredResource;
import com.google.cloud.logging.LogEntry;
import com.google.cloud.logging.Logging;
import com.google.cloud.logging.LoggingOptions;
import com.google.cloud.logging.Payload.StringPayload;
import com.google.cloud.logging.Severity;
import com.google.logging.type.LogSeverity;

public class Snippets {

    public void simplelog(Map<String,String> args){
        System.out.println("Called Simplelog!");
        // pull out arguments
        String logText = args.getOrDefault("log_text", "simplelog");
        String logName = args.getOrDefault("log_name", "test");
        String severityString = args.getOrDefault("severity", "DEFAULT");

        // Instantiates a client
        Logging logging = LoggingOptions.getDefaultInstance().getService();
        LogEntry entry =
            LogEntry.newBuilder(StringPayload.of(logText))
                .setSeverity(Severity.ERROR)
                .setLogName(logName)
                .setResource(MonitoredResource.newBuilder("global").build())
                .build();

         //Writes the log entry asynchronously
        logging.write(Collections.singleton(entry));
    }
}
