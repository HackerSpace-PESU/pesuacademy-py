# pesuacademy-py

![PyPI](https://img.shields.io/pypi/v/pesuacademy?label=pypi%20package)
![GitHub Release](https://img.shields.io/github/v/release/HackerSpace-PESU/pesuacademy-py)
![GitHub Tag](https://img.shields.io/github/v/tag/HackerSpace-PESU/pesuacademy-py)
![PyPI - Status](https://img.shields.io/pypi/status/pesuacademy)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pesuacademy)

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/HackerSpace-PESU/pesuacademy-py)
![GitHub last commit](https://img.shields.io/github/last-commit/HackerSpace-PESU/pesuacademy-py)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/HackerSpace-PESU/pesuacademy-py/latest)

![black.yml](https://github.com/HackerSpace-PESU/pesuacademy-py/actions/workflows/black.yml/badge.svg)
![python-package-pip.yml](https://github.com/HackerSpace-PESU/pesuacademy-py/actions/workflows/python-package-pip.yml/badge.svg)
![python-publish.yml](https://github.com/HackerSpace-PESU/pesuacademy-py/actions/workflows/python-publish.yml/badge.svg)
![build-docs.yml](https://github.com/HackerSpace-PESU/pesuacademy-py/actions/workflows/build-docs.yml/badge.svg)

Python wrapper and APIs for the PESU Academy website.

The wrapper provides **read-only** access to all the pages and information accessible on the PESU Academy website.
Without authentication, the wrapper will only be able to fetch details from the `Know Your Class and Section` page.

> :warning: **Warning:** This is not an official API and is not endorsed by PES University. Use at your own risk.

## Installation

### Installing from `pip`

```bash
pip install pesuacademy
```

### Installing from source

```bash
git clone https://github.com/HackerSpace-PESU/pesuacademy-py
cd pesuacademy-py
python setup.py install
```

## Usage

```python
from pesuacademy import PESUAcademy

p = PESUAcademy("PRN_or_SRN", "password")
# p = PESUAcademy() # Without authentication: can only fetch details from the `Know Your Class and Section` page
profile = p.profile()
courses = p.courses(semester=2)
attendance = p.attendance()
```