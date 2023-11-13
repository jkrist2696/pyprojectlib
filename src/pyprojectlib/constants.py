"""
Written by Jason Krist
"""

from os import path
import sys
from .helper import config_log


log = config_log  # pylint: disable=R0903

NAME = "pyprojectlib"

PYPI = "https://pypi.org/project"
GITHUB = "https://github.com"

SRC_DIR = "src"
DOCS_DIR = "docs"
TEST_DIR = "test"
USERS_DIR = ".users"
VERSIONS_DIR = ".versions"
PROJECTS_DIR = ".projects"

REQFILE = "requirements.txt"
LICFILE = "LICENSE.txt"
READFILE = "README.md"
DESC_REGEX = r"(?s)# Description(.*?)#"

PYEXE = sys.executable
ENVPATH = path.dirname(PYEXE)
PIPEXE = path.join(ENVPATH, "Scripts", "pip3")
TWINEEXE = path.join(ENVPATH, "Scripts", "twine")

TOMLSTR_START = """[project]
license = { text = "GPL-3.0-only" }
readme = "README.md"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
]

"""

IGNORELIST = [
    ".versions/",
    ".users/",
    ".git/",
    ".mypy_cache/",
    ".vscode/",
    "build/",
    "dist/",
    "docs/conf.txt",  # "src/proj/__pycache__
    "test/__pycache__",
    "test/.mypy_cache/",
    "test/docs",
    "test/examples",
    "test/cleandoc_log.txt",
]
