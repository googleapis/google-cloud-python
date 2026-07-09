import os
import glob
import re

def get_module_name(golden_dir):
    setup_py = os.path.join(golden_dir, "setup.py")
    if not os.path.exists(setup_py):
        return "google"
    
    with open(setup_py, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(r"'(google/[^']+)/gapic_version.py'", content)
    if match:
        return match.group(1).replace("/", ".")
    
    match = re.search(r"\"(google/[^\"]+)/gapic_version.py\"", content)
    if match:
        return match.group(1).replace("/", ".")
        
    return "google"

def patch_noxfile(golden_dir):
    path = os.path.join(golden_dir, "noxfile.py")
    if not os.path.exists(path):
        return False
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False
        
    module_name = get_module_name(golden_dir)

    idx = content.find("@nox.session(python=\"3.15\")\ndef import_profile(session):")
    if idx != -1:
        content = content[:idx].strip() + "\n"
    else:
        idx = content.find("@nox.session\ndef import_profile")
        if idx != -1:
            content = content[:idx].strip() + "\n"

    if "nox.options.sessions =" in content and "\"import_profile\"" not in content:
        content = re.sub(
            r'(\n\s*"docs",\n)(\s*\])',
            r'\1    "import_profile",\n\2',
            content
        )
    
    session_text = f"""
@nox.session(python="3.15")
def import_profile(session):
    \"\"\"Ensure import times remain below defined thresholds.\"\"\"
    profiler_script = (
        CURRENT_DIRECTORY.parent.parent / "scripts" / "import_profiler" / "profiler.py"
    )
    if not profiler_script.exists():
        session.skip("The import profiler script was not found.")

    session.install(".")
    session.run(
        "python",
        str(profiler_script),
        "--package",
        "{module_name}",
        "--fail-threshold",
        "5000",
        "--iterations",
        "10",
        *session.posargs,
    )
"""
    
    content += "\n" + session_text
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

count = 0
for golden_dir in glob.glob('packages/gapic-generator/tests/integration/goldens/*'):
    if os.path.isdir(golden_dir):
        if patch_noxfile(golden_dir):
            count += 1

print(f"Patched {count} goldens.")
