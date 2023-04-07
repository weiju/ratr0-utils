# ratr0-utils - Utility collection for the RATR0 Engine

## Description

This is a collection of utilities to convert common multimedia
formats into formats that can be used within the RATR0 game
engine.
It also aims for providing data conversion tools that target
retro platforms and that are open and documented without
intentionally keeping secrets from its users.

Detailed documentation available at

https://weiju.github.io/ratr0-utils/

## Build distribution

Note: While developing, there seems to be a confusion how
setuptools or wheel is treating hyphens, so the project name
is using underscore

python3 setup.py sdist bdist_wheel

## Uploading to pypi

twine upload -r pypi dist/ratr0_utils-<version>*

## Known pitfalls

Image conversion can fail when the PNG is not in indexed format.
Modern image editors often save PNG in 24bit format, so make sure
that the PNG is in the format you need
