/*
/* Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package envtest.deployable;

import com.google.cloud.functions.BackgroundFunction;
import com.google.cloud.functions.Context;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.logging.Level;
import java.util.logging.Logger;

import java.util.Map;
import java.util.HashMap;
import java.nio.charset.StandardCharsets;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class CloudFunctionTrigger implements BackgroundFunction<PubSubMessage> {

  @Override
  public void accept(PubSubMessage message, Context context) {
    String fnName = new String(Base64.getDecoder().decode(message.data.getBytes(StandardCharsets.UTF_8)), StandardCharsets.UTF_8);
    Map<String, String> args = message.attributes;
    if (args == null){
        args =  new HashMap<String, String>();
    }
    triggerSnippet(fnName, args);
    return;
  }

  public static void triggerSnippet(String fnName, Map<String,String> args) {
    try {
      Snippets obj = new Snippets();
      Class<?> c = obj.getClass();
      Method found = c.getDeclaredMethod(fnName, new Class[] {Map.class});
      found.invoke(obj, args);
    } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
      e.printStackTrace();
    }
  }
}

class PubSubMessage {
  public String data;
  public Map<String, String> attributes;
  public String messageId;
  public String publishTime;
}
