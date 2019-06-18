import re

with open("setup.py") as f:
    content = f.read()

VERSION_REGEX = re.compile(r"""version\s*=\s*["'](.+)["']""")
print(VERSION_REGEX.search(content).group(1))