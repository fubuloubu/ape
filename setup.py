#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (  # type: ignore
    setup,
    find_packages,
)

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0,<7.0",  # Core testing package
        "pytest-xdist",  # multi-process runner
        "pytest-coverage",  # Coverage analyzer plugin
    ],
    "fuzz": [  # `fuzz` GitHub Action job uses this
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
    ],
    "lint": [
        "black>=20.8b1,<21.0",  # auto-formatter and linter
        "mypy>=0.800,<1.0",  # Static type analyzer
    ],
    "doc": [
        "Sphinx>=3.4.3,<4",  # Documentation generator
        "sphinx_rtd_theme>=0.1.9,<1",  # Readthedocs.org theme
        "towncrier>=19.2.0, <20",  # Generate release notes
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "wheel",  # Packaging tool
        "twine",  # Package upload tool
    ],
    "dev": [
        "commitizen",  # Manage commits and publishing releases
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["fuzz"]
    + extras_require["lint"]
    + extras_require["doc"]
    + extras_require["release"]
    + extras_require["dev"]
)

# NOTE: This comes after the previous so we don't have double dependencies
extras_require["fuzz"] = extras_require["test"] + extras_require["fuzz"]

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="eth-ape",
    # *IMPORTANT*: Don't manually change the version here. Use `cz bump`
    version="0.1.0-alpha.1",
    description="Ape Ethereum Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ApeWorX Ltd.",
    author_email="admin@apeworx.io",
    url="https://github.com/ApeWorX/ape",
    include_package_data=True,
    install_requires=[
        "click>=7.1.2",
        "eth-account>=0.5.4,<0.6.0",
        "pyyaml>=0.2.5",
    ],
    entry_points={
        "console_scripts": ["ape=ape._cli.__init__:cli"],
    },
    python_requires=">=3.6,<4",
    extras_require=extras_require,
    py_modules=["ape"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_accounts": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)