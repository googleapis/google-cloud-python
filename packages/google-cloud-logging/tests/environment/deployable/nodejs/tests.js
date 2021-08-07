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

const {Logging} = require('@google-cloud/logging');
const logging = new Logging();
const defaultRequest = {
  method: 'POST',
  httpVersion: 'HTTP/1.1',
  url: 'https://google.com',
  headers: {'x-cloud-trace-context': '1/1;o=1'},
  rawHeaders: ['X-Cloud-Trace-Context'],
  statusCode: 200,
}

/**
 * The following are test functions that can be triggered in each service.
 * envctl nodejs <env> trigger simplelog log_name=foo,log_text=bar
 */
var simplelog = function(logname = "my-log", logtext = "hello world" ) {
  const log = logging.log(logname);

  const text_entry = log.entry(logtext);

  log.write(text_entry).then(r => console.log(r));
}

/**
 * envctl nodejs <env> trigger requestlog log_name=foo,log_text=bar
 */
var requestlog = function(logname = 'my-log', logtext = 'hello world', request) {
  if (!request) request = defaultRequest;
  const log = logging.log(logname);
  const entry = log.entry({httpRequest: request}, logtext);
  log.write(entry).then(r => console.log(r));
}

/**
 * envctl nodejs <env> trigger stdoutlog log_name=foo,log_text=bar
 */
var stdoutlog = function(logname = 'my-log', logtext = 'hello world', request) {
  if (!request) request = defaultRequest;
  logging.setProjectId().then( res => {
    logging.setDetectedResource().then( res => {
      const log = logging.logSync(logname);
      const meta = {
        // Fields all agents lift:
        severity: 'WARNING',
        httpRequest: request,
        labels: {foo: 'bar'},
        // Fields not lifted by all agents, e.g. GCF:
        insertId: '42',
        timestamp: new Date(2021,1,1,1,1,1,1),
        resource: {
          type: 'global',
          labels: {
            region: 'my-backyard',
            zone: 'twilight',
          }
        },
        // Note: explicit trace declarations override httpRequest header context
        trace: 'projects/my-projectid/traces/0679686673a',
        spanId: '000000000000004a',
        traceSampled: false,
      }
      const entry = log.entry(meta, logtext);
      log.write(entry);
    });
  });
}

module.exports={
  'simplelog': simplelog,
  'stdoutlog': stdoutlog,
  'requestlog': requestlog,
}

