"""
Written by Jason Krist
"""

from os import path
import sys
from cleandoc import cleandoc_all  # type: ignore # pylint: disable=E0401,C0413

testdir = path.dirname(path.realpath(__file__))
appendpath = path.join(testdir, "../src")
sys.path.insert(0, appendpath)

from pyprojectlib.pyuser import User  # type: ignore # pylint: disable=E0401,C0413
import pyprojectlib as ppl  # type: ignore # pylint: disable=E0401,C0413,E0611


def package():
    """function for packaging modules"""
    pkgpath = path.realpath(path.join(testdir, "../"))
    srcpath = path.join(pkgpath, "src", path.basename(pkgpath))
    # Run Cleandoc
    cleandoc_all(srcpath)
    # Package this project
    user = User(name="Jason Krist", email="jkrist2696@gmail.com", gituser="jkrist2696")
    ppl.Log.package_project(pkgpath, user, install=True, upload=True)


if __name__ == "__main__":
    package()
