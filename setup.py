import setuptools

VERSION = "0.0.1"

DESCRIPTION = "Python wrapper and APIs for the PESU Academy website"

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setuptools.setup(
    name="pesuacademy",
    version=VERSION,
    author="Aditeya Baral",
    author_email="aditeya.baral@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HackerSpace-PESU/pesuacademy-py",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "requests-html",
        "beautifulsoup4",
        "lxml_html_clean"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    keywords=["pesu", "pesu academy", "api", "wrapper", "python"]
)
