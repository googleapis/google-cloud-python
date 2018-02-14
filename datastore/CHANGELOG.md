# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datastore/#history

## 1.5.0

- Revert "api_core: Make PageIterator.item_to_value public. (#4702)" (#4731)
- api_core: Make PageIterator.item_to_value public. (#4702)
- Datastore: Entity doc consistency (#4641)
- Datastore: id from #3832 pull request with unit test (#4640)
- Adds optional location_prefix kwarg in to_legacy_urlsafe (#4635)
- Closes #4278 Datastore: Transaction Options (#4357)
- Updating datastore HTTP wrapper. (#4388)
- Update datastore doctests to reflect change in cursor behavior. (#4382)
- Set next_page_token to none if there are no more result (#4349)
- cosmetic changes to address #4343 (#4376)
- Allow specifying read consistency (#4343)
- New Datastore auto-gen. (#4348)
- Making a `nox -s default` session for all packages. (#4324)
- Closes #4319 - shorten test names (#4321)
- Fixing "Fore" -> "For" typo in README docs. (#4317)
- Marking all remaining versions as "dev". (#4299)

## 1.4.0

### Interface changes / additions

- Allowing `dict` (as an `Entity`) for property values. (#3927)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-datastore/1.4.0/
