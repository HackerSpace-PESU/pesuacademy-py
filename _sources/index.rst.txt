.. pesuacademy-py documentation master file, created by
   sphinx-quickstart on Fri Apr 19 17:35:18 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pesuacademy-py

PESU Academy API
=======================================

Python wrapper and APIs for the PESU Academy website.

The wrapper requires the user's credentials to authenticate and provide **read-only** access to all the pages and
information accessible on the PESU Academy website. Without the credentials, the wrapper will only be able to fetch 
details from the `Know Your Class and Section` page.

**Warning:** This is not an official API and is not endorsed by PESU. Use at your own risk.

Installation
+++++++++++++++++++++++++++++++++

Installing from pip
---------------------------------

.. code:: bash

   pip install pesuacademy


Installing from source
---------------------------------

.. code:: bash

   git clone https://github.com/HackerSpace-PESU/pesuacademy-py
   cd pesuacademy-py
   python setup.py install


Usage
+++++++++++++++++++++++++++++++++

.. code:: python

   from pesuacademy import PESUAcademy
   p = PESUAcademy("PRN_or_SRN", "password")
   profile = p.profile()
   courses = p.courses(semester=2)
   attendance = p.attendance()
