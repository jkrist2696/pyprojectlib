# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:18:08 2023

@author: jkris
"""

# SETUP PROCESS BELOW
# cleandoc -d ./../src/{NAME} -w
# python setup.py bdist_wheel sdist
# twine check dist/*
# pip3 install .
# twine upload dist/*

# NEW SETUP PROCESS
# pip3 wheel --no-deps -w dist .
# OR python -m build

from os import path
from typing import Union
from platform import python_version
from pprint import pprint
from requests import get
from setuptools import find_packages, setup
from pipreqs.pipreqs import get_all_imports, get_pkg_names, get_import_local  # type: ignore # pylint: disable=E0401


pykwargs: dict[str, Union[str, list, dict]] = {}

# Find Package Name
setupdir = path.split(path.realpath(__file__))[0]
pkgname = path.split(setupdir)[1]
pykwargs["name"] = pkgname
print(f"\npkgname: {pkgname}")

# USER PARAMETERS
pykwargs["description"] = (
    "Python package leveraging doq, black, pylint, mypy and sphinx"
    + " to automatically clean and document python code."
)
pykwargs["python_requires"] = ">=" + python_version()
pykwargs["install_requires"] = ["black>=23.3.0", "Sphinx>=6.2.1", "doq>=0.9.1", "m2r2"]
pykwargs["entry_points"] = {"console_scripts": [f"{pkgname}={pkgname}:cli_main"]}
pykwargs["packages"] = []  # ["pkg.assets"]
# pykwargs["package_data"] = ({f"{pkgname}": ["assets/*"]},)
# pykwargs["include_package_data"] = True

# Find Latest Version and Add 0.0.1
VERSION = "0.0.1"
pkgpage = get(f"https://pypi.org/project/{pkgname}/", timeout=10).text
if "page not found" not in pkgpage and "404" not in pkgpage:
    start_ind = pkgpage.find('<h1 class="package-header__name">') + 33
    latest_start = pkgpage[start_ind:]
    latest = latest_start[0 : latest_start.find("</h1>")]
    latest = latest.strip().split(" ")[1]
    print(f"previous version: {latest}")
    latest_split = latest.split(".")
    latest_split[2] = str(int(latest_split[2]) + 1)
    VERSION = ".".join(latest_split)
pykwargs["version"] = VERSION
print(f"current version: {pykwargs['version']}\n")

# RUN CLEANDOC HERE WITH CURRENT VERSION
if __name__ == "__main__":
    try:
        from cleandoc import cleandoc_all  # type: ignore

        cleandoc_all(path.join(setupdir, "src", pkgname), release=VERSION)
    except ImportError:
        print("\n!!!! SKIPPING CLEANDOC CHECK !!!!")

# User README as PyPI home page
with open("README.md", "r", encoding="utf-8") as readme:
    readme_text = readme.read()

# Get Module Dependencies and their Versions
imports = get_all_imports(f"./src/{pkgname}", encoding="utf-8")
pkgnames = get_pkg_names(imports)
pkgdicts_all = get_import_local(pkgnames, encoding="utf-8")
pkgdicts: list[dict] = []
for pkgdict_orig in pkgdicts_all:
    pkgdicts_names = [pkgdict["name"] for pkgdict in pkgdicts]
    if pkgdict_orig["name"] not in pkgdicts_names:
        pkgdicts.append(pkgdict_orig)
pkglist = [pkgdict["name"] + ">=" + pkgdict["version"] for pkgdict in pkgdicts]
pykwargs["install_requires"] = pykwargs["install_requires"] + pkglist

# Find all Packages and Sub-Packages
packages = find_packages(where="src")
pykwargs["packages"].extend(packages)

print("\npykwargs:")
pprint(pykwargs)
print("\n")

# Run Setup
setup(
    **pykwargs,
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Jason Krist",
    author_email="jkrist2696@gmail.com",
    url=f"https://github.com/jkrist2696/{pkgname}",
    license="GNU GPLv3",
    package_dir={f"{pkgname}": f"src/{pkgname}"},
)
