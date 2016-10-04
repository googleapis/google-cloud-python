import json
import os


env = dict(os.environ)
print(json.dumps(env, indent=2, sort_keys=True))
