const {Logging} = require('@google-cloud/logging');
const logging = new Logging();

/**
 * Background Cloud Function to be triggered by Pub/Sub.
 * This function is exported by index.js, and executed when
 * the trigger topic receives a message.
 *
 * @param {object} message The Pub/Sub message.
 * @param {object} context The event metadata.
 */
exports.pubsubFunction = (message, context) => {
  const msg = message.data
      ? Buffer.from(message.data, 'base64').toString()
      : console.log("no log function was invoked");

  console.log('attributes if any: ');
  console.log(message.attributes);

  // TODO later (nicolezhu):
  // write fns in separate file and do var funcFo0 = function(){}... modules.exports={ func: funcFoo}
  // var methods = require()... methods['funcString']()
  switch (msg) {
    case 'simplelog':
      if (message.attributes) {
        simplelog(message.attributes['log_name'], message.attributes['log_text']);
      } else {
        simplelog();
      }
      break;
    default:
      console.log(`Invalid log function was invoked.`);
  }
};

/**
 * envctl nodejs <env> trigger simplelog log_name=foo,log_text=bar
 */
function simplelog(logname = "my-log", logtext = "hello world" ) {
  const log = logging.log(logname);

  const text_entry = log.entry(logtext);

  log.write(text_entry).then(r => console.log(r));
}
