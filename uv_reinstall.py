import os
import re
from pathlib import Path

def patch_noxfiles():
    updated = 0
    # Walk through all packages in the monorepo
    for path in Path("packages").rglob("noxfile.py"):
        content = path.read_text(encoding="utf-8")

        # Skip files that don't implement the session or don't use the legacy flag
        if "def core_deps_from_source" not in content or '"--ignore-installed"' not in content:
            continue

        # Regex captures the exact whitespace/indentation before the target loop
        pattern = re.compile(
            r'^([ \t]*)for dep in core_dependencies_from_source:\n[ \t]*session\.install\(dep, "--no-deps", "--ignore-installed"\)',
            re.MULTILINE
        )

        def replacer(match):
            indent = match.group(1)
            # Inject the backend-aware variable and apply it to the loop
            return (
                f'{indent}# Natively adapt the overwrite flag based on the active resolver\n'
                f'{indent}force_overwrite_flag = "--reinstall" if os.environ.get("NOX_DEFAULT_VENV_BACKEND") == "uv" else "--ignore-installed"\n'
                f'{indent}for dep in core_dependencies_from_source:\n'
                f'{indent}    session.install(dep, "--no-deps", force_overwrite_flag)'
            )

        new_content, count = pattern.subn(replacer, content)

        if count > 0:
            path.write_text(new_content, encoding="utf-8")
            print(f"✅ Patched: {path}")
            updated += 1

    print(f"\nSuccess: Safely patched {updated} noxfiles.")

if __name__ == "__main__":
    patch_noxfiles()