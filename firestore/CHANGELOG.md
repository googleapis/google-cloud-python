# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-firestore/#history

## 0.29.0

- Firestore: System test fix, changed ALREADY_EXISTS and MISSING_ENTITY to DOCUMENT_EXISTS and MISSING_DOCUMENT and updated wording (#4803)
- Revert "Do not use easily-misread glyphs in Firestore auto-IDs." (#4589)
- Do not use easily-misread glyphs in Firestore auto-IDs. (#4107)
- firestore: cross-language tests (#4359)
- Firestore: Import column lengths pass 79 (#4464)
- Making a `nox -s default` session for all packages. (#4324)
- Closes #4319 - shorten test names (#4321)
- Fixing "Fore" -> "For" typo in README docs. (#4317)
- Marking all remaining versions as "dev". (#4299)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-firestore/0.28.0/
