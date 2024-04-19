# PESU Academy API

Python wrapper and APIs for the PESU Academy website.

The wrapper requires the user's credentials to authenticate and provide **read-only** access to all the pages and
information accessible on the PESU Academy website. Without the credentials, the wrapper will only be able to fetch 
details from the `Know Your Class and Section` page.

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
profile = p.profile()
courses = p.courses(semester=2)
attendance = p.attendance()
```