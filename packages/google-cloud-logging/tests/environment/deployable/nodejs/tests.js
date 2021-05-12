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

/**
 * The following are test functions that can be triggered in each service.
 * envctl nodejs <env> trigger simplelog log_name=foo,log_text=bar
 */
var simplelog = function(logname = "my-log", logtext = "hello world" ) {
  const log = logging.log(logname);

  const text_entry = log.entry(logtext);

  log.write(text_entry).then(r => console.log(r));
}

module.exports={ 'simplelog': simplelog }

