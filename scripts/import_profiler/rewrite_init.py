import re
import os

INIT_PATH = "packages/google-cloud-compute/google/cloud/compute_v1/__init__.py"

def rewrite():
    with open(INIT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the __all__ tuple/list
    all_match = re.search(r'__all__\s*=\s*\((.*?)\)', content, re.DOTALL)
    if not all_match:
        print("Could not find __all__")
        return
        
    all_contents = all_match.group(0)

    # Find all from .foo import Bar
    import_pattern = re.compile(r'^from\s+(\.[a-zA-Z0-9_.]+)\s+import\s+(.*?)$', re.MULTILINE | re.DOTALL)
    
    imports = []
    # To handle parentheses in imports like:
    # from .foo import (
    #     Bar,
    #     Baz,
    # )
    
    lines = content.split('\n')
    new_lines = []
    
    in_import = False
    import_module = ""
    import_names_str = ""
    
    parsed_imports = [] # list of (module, [names])
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("from .") and " import " in line:
            parts = line.split(" import ")
            mod = parts[0].replace("from ", "").strip()
            names_part = parts[1].strip()
            if "(" in names_part and ")" not in names_part:
                # multi-line import
                import_names_str = names_part.replace("(", "")
                i += 1
                while ")" not in lines[i]:
                    import_names_str += lines[i]
                    i += 1
                import_names_str += lines[i].replace(")", "")
            else:
                import_names_str = names_part.replace("(", "").replace(")", "")
                
            names = [n.strip() for n in import_names_str.split(",") if n.strip()]
            parsed_imports.append((mod, names))
        i += 1
        
    # Build registries
    lazy_modules_items = set()
    lazy_imports_dict_items = []
    
    eager_imports_str = []
    for mod, names in parsed_imports:
        if mod.startswith("."):
            lazy_modules_items.add(f'    f"{{__name__}}{mod}",')
        else:
            lazy_modules_items.add(f'    "{mod}",')
            
        names_joined = ", ".join(names)
        if len(names_joined) > 60:
            names_joined = f"({names_joined})"
        eager_imports_str.append(f"    from {mod} import {names_joined}")
        
        for name in names:
            lazy_imports_dict_items.append(f'        "{name}": "{mod}",')
                
    # Build the new file contents
    header = []
    for line in lines:
        if line.startswith("from .") and " import " in line:
            break
        header.append(line)
        
    # Ensure sys and typing are imported
    header_str = "\n".join(header)
    if "import sys" not in header_str:
        header_str += "\nimport sys\n"
    if "import typing" not in header_str:
        header_str += "import typing\n"
    
    lazy_mod_str = "\n".join(sorted(lazy_modules_items))
    eager_imports_joined = "\n".join(eager_imports_str)
    lazy_imports_dict_str = "\n".join(lazy_imports_dict_items)
    
    new_content = f"""{header_str}
__lazy_modules__ = {{
{lazy_mod_str}
}}

if typing.TYPE_CHECKING or sys.version_info >= (3, 15):
{eager_imports_joined}
else:
    import importlib
    _LAZY_IMPORTS = {{
{lazy_imports_dict_str}
    }}

    def __getattr__(name):
        if name in _LAZY_IMPORTS:
            module = importlib.import_module(_LAZY_IMPORTS[name], package=__name__)
            attr = getattr(module, name)
            globals()[name] = attr
            return attr
        raise AttributeError(f"module {{__name__!r}} has no attribute {{name!r}}")

{all_contents}
"""

    with open(INIT_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Done rewriting __init__.py")

if __name__ == "__main__":
    rewrite()
